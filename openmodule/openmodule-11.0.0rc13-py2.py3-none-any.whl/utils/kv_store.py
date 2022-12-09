import json
import logging
import threading
import time
from typing import Type, Optional, List, Union, Tuple, Dict, Any

from sqlalchemy import Column, String, Integer

from openmodule.config import settings
from openmodule.connection_status import ConnectionStatus
from openmodule.core import core
from openmodule.database.database import Database
from openmodule.models.kv_store import ServerSyncResponse, KVSetRequest, KVSyncRequest, KVSyncResponse, KVSetResponse, \
    KVSetRequestKV, KVSetResponseKV
from openmodule.models.rpc import ServerRPCRequest
from openmodule.rpc import RPCServer, RPCClient
from openmodule.threading import get_thread_wrapper
from openmodule.utils.db_helper import delete_query


class KVEntry:
    """
    Inherit from this class and add columns that should be parsed from the value coming from the server
        and implement the parse_value method.
    """

    key = Column(String, nullable=False, index=True, unique=True)
    e_tag = Column(Integer, nullable=False, primary_key=True, index=True)

    @classmethod
    def parse_value(cls, value) -> dict:  # pragma: no cover
        """Parses the value from the server into a dict of {column-name: value}"""
        raise NotImplementedError

    def comparison_value(self) -> str:
        """
        return some hash or other string. Changed messages are only sent if this value changed for a key
        if you don't want changed messages, use for efficiency:
        """
        return self.key


class KVStore:
    """
    Inherit this class to create a Key-Value store in the database.
    register_rpcs must be called on startup to register the RPCs
    sync_with_server must be called on startup and on reconnect (use ConnectionStatusListener) to sync the
        Key Value store with the server. The response can then be logged with log_sync_rpc_response.
    Implement any getter methods that you need. They must not change the data.

    database_table: Must be an inherited class of KVEntry.
    db: The database to use. If None, the core database is used.
    rpc_client: The RPC client to use. If None, the core RPC client is used.
    """
    database_table: Type[KVEntry]
    DEBUG_ENTRY_START = 2**62

    def __init__(self, db: Database = None, rpc_client: RPCClient = None, sync_timeout: float = 30.0,
                 debug_entries: Optional[Dict[str, Any]] = None):
        assert self.database_table != KVEntry, "You must set the database_table attribute to a subclass of KVEntry"
        self.log = logging.getLogger(self.__class__.__name__)
        self.db = db or core().database
        self.rpc_client = rpc_client or core().rpc_client
        self.sync_timeout = sync_timeout
        self.debug_entries = debug_entries or {}
        self.run_thread = None
        self.running = True
        self.sync_rpc_entry = None
        self.sync_wait = threading.Event()

    def sync_with_server(self) -> RPCClient.RPCEntry:
        """
        This method should be called on startup and on reconnect (use ConnectionStatusListener) to sync the
        Key Value store with the server.
        """
        self.log.debug("Sending sync request")
        return self.rpc_client.rpc_non_blocking("rpc-websocket", "server_rpc",
                                                ServerRPCRequest(rpc="kvs_sync", data={"resource": settings.RESOURCE,
                                                                                       "service": settings.NAME,
                                                                                       "timeout": self.sync_timeout-5}),
                                                timeout=self.sync_timeout)

    def log_sync_rpc_response(self, rpc_entry: RPCClient.RPCEntry) -> Optional[ServerSyncResponse]:
        """Waits for the RPC to finish and logs the response"""
        self.log.debug("Parsing sync response")
        try:
            sync_response = rpc_entry.result(ServerSyncResponse)
            self.log.info("Synced kvs with server with %s successes and %s errors",
                          len(sync_response.successes), len(sync_response.errors))
            if sync_response.errors:
                self.log.warning("Sync kvs errors: %s", sync_response.errors)
            return sync_response
        except RPCClient.TimeoutError:
            self.log.error("Timeout syncing kvs")
        except RPCClient.CancelError:
            self.log.error("Cancelled waiting for result of syncing kvs")
        except RPCClient.ValidationError as e:
            self.log.exception("Error parsing sync response")
        except (RPCClient.ServerHandlerError, RPCClient.ServerValidationError, RPCClient.ServerFilterError) as e:
            self.log.exception("Error on server side in sync")
        except Exception as e:
            self.log.exception("Unexpected exception in sync response")

    def register_rpcs(self, rpc_server: RPCServer) -> None:
        """
        Must be called on startup to register the RPCs
        RPCs are filtered by service name
        """
        rpc_server.register_handler("kv_sync", "set", KVSetRequest, KVSetResponse, self._kvs_set)
        rpc_server.register_handler("kv_sync", "sync", KVSyncRequest, KVSyncResponse, self._kvs_sync)
        rpc_server.add_filter(self._sync_rpc_filter, channel="kv_sync")

    @staticmethod
    def _sync_rpc_filter(request: Union[KVSetRequest, KVSyncRequest], **__) -> KVSetRequest:
        """RPCs for kv_sync are filtered by service name"""
        return request.service == settings.NAME

    @staticmethod
    def _kvs_set_find_mismatched(request: KVSetRequest, current_kvs: List[KVEntry]) -> List[KVEntry]:
        mismatched = []
        for kv in request.kvs:
            for current in current_kvs:
                if kv.key == current.key and kv.previous_e_tag == current.e_tag:
                    break
                if kv.key == current.key and kv.previous_e_tag is None:
                    mismatched.append(kv)
                    break
            else:
                if kv.previous_e_tag is not None:
                    mismatched.append(kv)
        return mismatched

    def _kvs_set_parse_kvs(self, kvs: List[KVSetRequestKV]) -> Tuple[List[KVEntry], List[KVSetResponseKV],
                                                                     List[KVSetResponseKV]]:
        successes = []
        to_set = []
        errors = []
        for kv in kvs:
            try:
                value = json.loads(kv.value)
                if value is None:
                    successes.append(KVSetResponseKV(key=kv.key, status="ok"))
                else:
                    to_set.append(self.database_table(key=kv.key, e_tag=kv.e_tag,
                                                      **self.database_table.parse_value(value)))
                    successes.append(KVSetResponseKV(key=kv.key, status="ok"))
            except Exception as e:
                self.log.exception("Error parsing value %s for key %s: %s", kv.value, kv.key, e)
                errors.append(KVSetResponseKV(key=kv.key, status="error", error="parse_error"))
        return to_set, successes, errors

    def _get_comparison_values(self, updated_kv_entries: List[KVEntry]):
        # only used in KVStoreWithChangedNotification
        pass

    def _send_changed_notification(self, success_keys: List[str], old_values: Dict[str, str]):
        # only used in KVStoreWithChangedNotification
        pass

    def _kvs_set(self, request: KVSetRequest, _) -> KVSetResponse:
        """
        This method is called by the server to set values in the database.
        It must never be called from the device.
        Database entries must only be created/edited/deleted by this method.
        Entries are never changed, only deleted and recreated with new values and e_tag.
        The e_tag of the current value of a key needs to match previous_e_tag in the request, otherwise the key is
            rejected.
        """
        if not request.kvs:
            return KVSetResponse()
        with self.db() as session:
            current_kvs = \
                session.query(self.database_table).filter(self.database_table.key.in_([kv.key for kv in request.kvs]))
            comparison_values = self._get_comparison_values(current_kvs)
            mismatched_kvs = self._kvs_set_find_mismatched(request, current_kvs)
            errors = [KVSetResponseKV(key=kv.key, status="error", error="e_tag_mismatch") for kv in mismatched_kvs]
            to_set, successes, new_errors = self._kvs_set_parse_kvs(
                [kv for kv in request.kvs if kv not in mismatched_kvs])
            errors.extend(new_errors)
            if errors:
                self.log.warning("Mismatched kvs: %s", errors)
                current_kvs = list(filter(lambda x: not any(error for error in errors if error.key == x.key),
                                          current_kvs))
            if current_kvs:
                delete_query(session, session.query(self.database_table).filter(
                    self.database_table.key.in_([kv.key for kv in current_kvs])))
            if to_set:
                session.add_all(to_set)
            try:
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

        if successes:
            self._send_changed_notification([s.key for s in successes], comparison_values)
        return KVSetResponse(kvs=errors + successes)

    def _kvs_sync(self, request: KVSyncRequest, _) -> KVSyncResponse:
        """
        missing_kvs: All keys that were in the request but are not in the database (key=key, e_tag=request.e_tag)
        changed_kvs: All keys that were in the request and are in the database but have a different e_tag
                     (key=key, e_tag=database.e_tag)
        additional_kvs: All keys that were not in the request but are in the database (key=key, e_tag=database.e_tag)
        """
        self.log.debug("Syncing kvs for %s", request.service)
        with self.db() as session:
            current_kvs = session.query(self.database_table).all()
            changed_kvs = {key: current.e_tag
                           for current in current_kvs for key, e_tag in request.kvs.items()
                           if current.key == key and current.e_tag != e_tag}
            missing_kvs = {key: e_tag for key, e_tag in request.kvs.items() if
                           not any(current for current in current_kvs if current.key == key)}
            additional_kvs = {current.key: current.e_tag for current in current_kvs
                              if not any(key for key, _ in request.kvs.items() if key == current.key)}
            return KVSyncResponse(additions=additional_kvs, changes=changed_kvs, missing=missing_kvs)

    def _remove_debug_entries(self):
        with self.db() as session:
            delete_query(session,
                         session.query(self.database_table).filter(self.database_table.e_tag >= self.DEBUG_ENTRY_START))
            # delete because we want to override with debug entries
            delete_query(session,
                         session.query(self.database_table).filter(self.database_table.key.in_(self.debug_entries)))

    def _add_debug_entries(self):
        self._remove_debug_entries()
        with self.db() as session:
            for i, (key, value) in enumerate(self.debug_entries.items()):
                session.add(self.database_table(e_tag=self.DEBUG_ENTRY_START + i, key=key,
                                                **self.database_table.parse_value(value)))

    def _try_sync(self):
        while self.running:
            start = time.time()
            if core().connection_listener.get() not in (ConnectionStatus.startup, ConnectionStatus.online):
                # cancel trying to sync if offline
                break
            self.sync_rpc_entry = self.sync_with_server()
            response = self.log_sync_rpc_response(self.sync_rpc_entry)
            if self.debug_entries:
                self._add_debug_entries()
            self.sync_rpc_entry = None
            if response is not None:
                # if sync was successful cancel retries
                break
            if self.running:
                self.sync_wait.wait(max(0.0, self.sync_timeout - (time.time() - start)))

    def _wait_for_change_to_online(self):
        while self.running:
            changed = core().connection_listener.changed(id(self))  # always true first time after startup
            if changed and core().connection_listener.get() in (ConnectionStatus.startup, ConnectionStatus.online) and \
                    core().connection_listener.previous in (ConnectionStatus.shutdown, ConnectionStatus.offline):
                return True
            time.sleep(1)
        return False

    def run(self):
        try:
            while self.running:
                if self._wait_for_change_to_online():
                    self._try_sync()
        except KeyboardInterrupt:
            self.log.warning("KeyboardInterrupt received, shutting down...")
        except:
            self.log.exception("Unexpected exception in Access Service run")

    def run_as_thread(self):
        self.run_thread = threading.Thread(target=get_thread_wrapper(self.run))
        self.run_thread.start()

    def shutdown(self, timeout=10):
        self.running = False
        self.sync_wait.set()
        if self.sync_rpc_entry:
            self.sync_rpc_entry.cancel()
        if self.run_thread:
            self.run_thread.join(timeout=timeout)


class KVStoreWithChangedNotification(KVStore):
    def _get_comparison_values(self, updated_kv_entries: List[KVEntry]):
        """
        make sure your db model has a meaningful `comparison_value` method
        """
        raise NotImplementedError

    def _find_changed_kvs(self, success_keys: List[str], old_values: Dict[str, str]):
        changed = []
        with self.db() as session:
            kvs = session.query(self.database_table).filter(self.database_table.key.in_(success_keys)).all()
            new_values = {kv.key: kv.comparison_value() for kv in kvs}
            for key in success_keys:
                if key not in old_values or key not in new_values or old_values[key] != new_values[key]:
                    changed.append(key)
        return changed

    def _send_changed_notification(self, success_keys: List[str], old_values: Dict[str, str]):
        """
        consider using self._find_changed_kvs when implementing this
        also make sure your db model has a meaningful `comparison_value` method
        """
        raise NotImplementedError

