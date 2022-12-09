"""Common functions and objects for the unesco_reader package."""

import requests
import io
from zipfile import ZipFile
import pandas as pd


def mapping_dict(df: pd.DataFrame, key_col: str = 'left') -> dict:
    """Create a mapping dictionary from a dataframe with 2 columns

    Args:
        df: dataframe with two columns, left and right
        key_col: column to use as keys in the dictionary. Choose from 'left' or 'right'. Default is 'left'

    Returns:
        A dictionary with the values from the left column as keys,
        and the values from the right column as values
    """

    if len(df.columns) != 2:
        raise ValueError('df can only contain 2 columns')
    if key_col not in ['left', 'right']:
        raise ValueError('Invalid key_col. Please choose from ["left", "right"]')

    if key_col == 'left':
        k, v = 0, 1
    else:
        k, v = 1, 0
    return (df
            .set_index(df.iloc[:, k])
            .iloc[:, v]
            .to_dict()
            )


def unzip_folder_from_web(url: str) -> ZipFile:
    """unzip a folder from a url.

    Args:
        url: url to unzip

    Returns:
        Zipfile: object containing unzipped folder
    """

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return ZipFile(io.BytesIO(response.content))
        else:
            raise ConnectionError(f"Could not read file from url: {url}")

    except ConnectionError:
        raise ConnectionError(f"Could not read file from url: {url}")


def unzip_folder_from_disk(path: str) -> ZipFile:
    """unzip a folder from disk.

    Args:
        path: local path to folder

    Returns:
        Zipfile: object containing unzipped folder
    """

    try:
        return ZipFile(path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find file: {path}")


def read_csv(folder: ZipFile, path: str) -> pd.DataFrame:
    """Read a CSV file from a ZipFile object.

    Args:
        folder: ZipFile object containing the CSV file
        path: path to the CVS in the zipped folder

    Returns:
        pd.DataFrame: dataframe containing the data from the CSV
    """

    if path not in folder.namelist():
        raise FileNotFoundError(f"Could not find file: {path}")

    return pd.read_csv(folder.open(path), low_memory=False)





