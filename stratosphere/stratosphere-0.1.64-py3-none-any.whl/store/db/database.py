import getpass
import logging
import re
import uuid
from typing import Callable, Iterator, List, Union

import pandas as pd
from sqlalchemy import MetaData, Table, create_engine, sql
from sqlalchemy.engine import make_url
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.orm import Query, sessionmaker
from stratosphere import config
from stratosphere.store.db.models import Base
from stratosphere.utils.enums import IfExists
from stratosphere.utils.progress import progress
from ulid import monotonic as ulid


class Database:
    """
    This class is the entry point for all things SQLAlchemy, and it represents the link
    to the database for experiments and runs. It uses the SQAlchemy 1.4 API interface.
    """

    def __init__(self, url: str = config.db.default_url, echo=False, lazy=False, ask_password=False):
        """It creates a new database interface.

        Args:
            url (str, optional): Database URL, passed to SQLAlchemy. Defaults to config.db.default_url.
            echo (bool, optional): If True, log the SQL commands. Defaults to False.
            lazy (bool, optional): If True, don't initialize the object (useful to handle serialization).
            Defaults to False.
        """

        if lazy:
            # We activate this flag in the __reduce__, called upon pickling.
            # This behaviour allows to use sqlite in memory, since only one sqlite instance
            # gets created and reused for all experiments, runs, created or loaded via unpickling.
            # Further, it let us not run into pickling errors, which do happen with SQLAlchemy objects.
            return

        self.echo = echo
        self.url = make_url(url)
        if ask_password:
            self.url = self.url.set(password=getpass.getpass(prompt="Password: "))

        # Set up database connector, without establishing any connection yet
        # https://docs.sqlalchemy.org/en/13/core/pooling.html#disconnect-handling-pessimistic
        self.engine = create_engine(self.url, echo=echo, pool_pre_ping=True)

        # Session factory
        self.session = sessionmaker(self.engine)

        # create tables if missing
        Base.metadata.create_all(self.engine)

    def __reduce__(self):
        """
        We return a tuple of class_name to call,
        and optional parameters to pass when re-creating
        """
        return self.__class__, (self.url, self.echo, True)

    def info(self):
        """Log some stats about the database."""
        logging.info(f"Database: {self.url.render_as_string(hide_password=True)}")

    def delete(self):
        """Delete all tables defined in the schema module"""
        with self.session() as session:
            for table in Base.metadata.sorted_tables:
                session.query(table).delete()
            session.commit()

    def pandas_to_sql(self, df: pd.DataFrame, name: str, if_exists: IfExists, dtype: dict = None):
        """Insert a Pandas dataframe as a new database table.

        Args:
            df (pd.DataFrame): Dataframe to insert.
            name (str): Name of the database table to create.
            if_exists (IfExists): Either "replace" or "fail".
        """

        if len(df) == 0:
            # nothing to do
            return

        with self.session() as session:
            if config.tqdm.enable:
                dfs = chunker(df, config.db.query_write_chunk_size)
                funcs = []
                for idx, df_chunk in enumerate(dfs):

                    def process_chunk():
                        df_chunk.to_sql(
                            name, session.bind, if_exists=if_exists if idx == 0 else "append", index=False, dtype=dtype
                        )
                        return len(df_chunk), None

                    funcs.append(process_chunk)

                tqdm_chunk(funcs, len(df))
            else:
                df.to_sql(f"experiment.{name}", session.bind, if_exists=if_exists, index=False, dtype=dtype)

    def drop_table(self, name: str):
        """Drop database table if it exists.

        Args:
            name (str): Name of the table to drop.
        """
        with self.session() as session:
            try:
                Table(name, MetaData(bind=session.bind), autoload_with=session.bind).drop()
            except NoSuchTableError:
                pass
            session.commit()

    def vacuum(self):
        """Vacuum the database. This operation makes the database
        more compact and performant.
        """
        with self.session() as session:
            if self.url.drivername not in ["sqlite"]:
                # sqlite wants a transaction to VACUUM,
                # postgresql doesn't. With a COMMIT,
                # we terminate the transaction, and
                # we can then execute the VACUUM command.
                session.execute("COMMIT")

            session.execute("VACUUM")

        logging.info("VACUUM executed.")

    def pandas(
        self,
        query: Union[str, Query, sql.expression.text],
        verbose=False,
        use_tqdm=True,
        tqdm_total=None,
    ) -> pd.DataFrame:
        """Query database and return result as Pandas dataframe.

        Args:
            query (Union[str, Query, sql.expression.text]): Query to execute.
            verbose (bool, optional): If True, log the SQL query. Defaults to False.
            use_tqdm (bool, optional): If True, use tqdm progress bar. Defaults to True.
            tqdm_total (_type_, optional): Provide the expected number of rows retrieved.
            If missing, we'll first count them, and then retrieve them, resulting in two
            distinct queries. Defaults to None.

        Returns:
            pd.DataFrame: Resulting rows.
        """

        with self.session() as session:
            df = pandas_query(
                query,
                session,
                verbose=verbose,
                use_tqdm=use_tqdm,
                tqdm_total=tqdm_total,
            )

            # handle UUID type conversions. If the DB handled natively UUID columns,
            # SQLAlchemy is already handling it transparently. If it doesn't, we need
            # to detect it, and apply the conversion.
            if len(df) > 0:
                if "id_run" in df and not isinstance(df["id_run"].iloc[0], uuid.UUID):
                    df["id_run"] = df["id_run"].apply(uuid.UUID)

                if "id_experiment" in df and not isinstance(df["id_experiment"].iloc[0], uuid.UUID):
                    df["id_experiment"] = df["id_experiment"].apply(uuid.UUID)

            return df


def sanitize_table_name(name: str) -> str:
    return re.sub("[^0-9a-zA-Z]+", "_", str(name)).strip("_").lower()


def pandas_query(
    query: Union[str, Query, sql.expression.text],
    session,
    verbose=False,
    use_tqdm=True,
    tqdm_total=None,
) -> pd.DataFrame:
    """Evaluate an SQL query on the database and return the result
    as a Pandas dataframe.

    Args:
        query (Union[str, Query, sql.expression.text]): Query to execute.
        session: SQLAlchemy session to use.
        verbose (bool, optional): If True, log the SQL query. Defaults to False.
        use_tqdm (bool, optional): If True, use tqdm progress bar. Defaults to True.
        tqdm_total (_type_, optional): Provide the expected number of rows retrieved.
        If missing, we'll first count them, and then retrieve them, resulting in two
        distinct queries. Defaults to None.

    Returns:
        pd.DataFrame: Resulting rows. The column types are guessed by Pandas.
    """

    # Normalise query to sql.expression.text
    if type(query) == Query:
        query = query.statement
    elif type(query) == str:
        query = sql.expression.text(query)

    if verbose:
        logging.info(f"SQL: {query.compile(session.bind)}")

    if use_tqdm:
        if tqdm_total is None:
            # If hint on total not available, query the database for it
            tqdm_total = session.execute(f"SELECT COUNT(*) FROM ({query}) t").first()[0]

        df_chunks = pd.read_sql_query(query, session.bind, chunksize=config.db.query_read_chunk_size)

        funcs = [lambda: (len(df_chunk), df_chunk) for df_chunk in df_chunks]
        dfs = tqdm_chunk(funcs, tqdm_total)

        df = pd.concat(dfs, ignore_index=True)
    else:
        df = pd.read_sql_query(query, session.bind)

    return df.apply(pd.to_numeric, errors="ignore")


def next_ulid() -> str:
    """Return the next monotonic ULID (https://github.com/ulid/spec).

    Returns:
        str: New ULID in UUID format, ready to be used as Experiment or Run ID.
    """
    return uuid.UUID(bytes=ulid.new().bytes)  # str(uuid.UUID(bytes=ulid.new().bytes))


def chunker(seq: List, size) -> List[List]:
    """Given a list, return a list of lists, where each sub-list is up to a certain
    chunk size.

    Args:
        seq (List): List to partition.
        size (_type_): Chunk size.

    Returns:
        List[List]: List of chunks.
    """
    return (seq[pos : pos + size] for pos in range(0, len(seq), size))  # noqa


def tqdm_chunk(
    iterator: Iterator[Callable],
    total: int,
) -> List:
    """Renders a progress bar, working on chunks of work.

    Args:
        iterator (Iterator[Callable]): Iterator of functions to call, returning (size, ret). Size is
        used to update the progress bar, and ret is accumulated as one more element in the returned list.
        total (int): Total number of items to process, regardless of chunking.

    Returns:
        List: List of return values from callables.
    """

    pbar = progress(total=total)
    pbar.clear()

    rets = []
    for item in iterator:
        size, ret = item()
        pbar.update(size)

        rets.append(ret)

    pbar.close()

    return rets
