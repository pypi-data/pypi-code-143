import threading
import time
from typing import List, Dict

from sqlalchemy import Column, String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base

from openmodule.config import settings
from openmodule.connection_status import ConnectionStatus
from openmodule.core import core
from openmodule.models.base import OpenModuleModel
from openmodule.models.kv_store import KVSetRequest, KVSetRequestKV, KVSetResponseKV, \
    KVSyncRequest, KVSetResponse, KVSyncResponse, ServerSyncResponse, ServerSyncResponseKV
from openmodule.models.rpc import ServerRPCRequest
from openmodule.rpc import RPCServer, RPCClient
from openmodule.utils.kv_store import KVStore, KVEntry, KVStoreWithChangedNotification
from openmodule_test.core import OpenModuleCoreTestMixin
from openmodule_test.database import SQLiteTestMixin
from openmodule_test.rpc import RPCServerTestMixin, MockRPCClient

Base = declarative_base()


class ExampleKVEntry(KVEntry, Base):
    __tablename__ = "example_kv_entry"

    value_1 = Column(String, nullable=True)
    value_2 = Column(String, nullable=False)

    @classmethod
    def parse_value(cls, value) -> dict:
        return {"value_1": value.get("value_1"), "value_2": value.get("value_2")}

    def comparison_value(self) -> str:
        return self.value_1 + "|" + self.value_2

    def __eq__(self, other):
        return isinstance(other, ExampleKVEntry) and self.key == other.key and self.value_1 == other.value_1 \
               and self.value_2 == other.value_2 and self.e_tag == other.e_tag

    def __repr__(self):
        return f"ExampleKVEntry(key={self.key}, value_1={self.value_1}, value_2={self.value_2}, e_tag={self.e_tag})"


class ExampleKVStore(KVStore):
    database_table = ExampleKVEntry


class DatabaseTest(SQLiteTestMixin):
    alembic_path = "../tests/test_kv_store_database"
    database_name = "kvstore"

    def setUp(self) -> None:
        super().setUp()
        self.kv_store = ExampleKVStore(self.database, lambda: None)

    def test_kvs_set(self):
        request = KVSetRequest(service=settings.NAME, kvs=[
            KVSetRequestKV(key="test", value='{"value_1": "test", "value_2": "test2"}', e_tag=1)])
        response = self.kv_store._kvs_set(request, None)
        self.assertListEqual(response.kvs, [KVSetResponseKV(key="test", status="ok")])
        with self.database() as session:
            kvs = session.query(ExampleKVEntry).all()
            self.assertEqual(len(kvs), 1)
            self.assertEqual(kvs[0], ExampleKVEntry(key="test", e_tag=1, value_1="test", value_2="test2"))

    def test_kvs_set_override(self):
        with self.database() as session:
            session.add(ExampleKVEntry(key="test", value_1="test", value_2="test2", e_tag=1))
            session.commit()
        request = KVSetRequest(kvs=[
            KVSetRequestKV(key="test", value='{"value_1": "123", "value_2": "234"}', e_tag=2, previous_e_tag=1)
        ], service=settings.NAME)
        response = self.kv_store._kvs_set(request, None)
        self.assertListEqual(response.kvs, [KVSetResponseKV(key="test", status="ok")])
        with self.database() as session:
            db_kvs = session.query(ExampleKVEntry).all()
            self.assertEqual(len(db_kvs), 1)
            self.assertEqual(db_kvs[0], ExampleKVEntry(key="test", value_1="123", value_2="234", e_tag=2))

    def test_kvs_set_override_mismatch(self):
        with self.database() as session:
            session.add(ExampleKVEntry(key="test", value_1="test", value_2="test2", e_tag=1))
            session.commit()
        request = KVSetRequest(kvs=[
            KVSetRequestKV(key="test", value='{"value_1": "123", "value_2": "234"}', e_tag=2, previous_e_tag=3)
        ], service=settings.NAME)
        response = self.kv_store._kvs_set(request, None)
        self.assertListEqual(response.kvs, [KVSetResponseKV(key="test", status="error", error="e_tag_mismatch")])
        with self.database() as session:
            db_kvs = session.query(ExampleKVEntry).all()
            self.assertEqual(len(db_kvs), 1)
            self.assertEqual(db_kvs[0], ExampleKVEntry(key="test", value_1="test", value_2="test2", e_tag=1))

    def test_kvs_set_multiple(self):
        with self.database() as session:
            session.add(ExampleKVEntry(key="test", value_1="test", value_2="test2", e_tag=1))
            session.add(ExampleKVEntry(key="test1", value_1="abc", value_2="def", e_tag=2))
            session.add(ExampleKVEntry(key="test2", value_1="222", value_2="333", e_tag=3))
            session.add(ExampleKVEntry(key="test3", value_1="111", value_2="000", e_tag=8))
            session.commit()
        request = KVSetRequest(kvs=[
            KVSetRequestKV(key="test", value='{"value_2": "123"}', e_tag=4, previous_e_tag=1),  # ok
            KVSetRequestKV(key="test_new", value='{"value_2": "123", "value_1": "456"}', e_tag=5),  # ok
            KVSetRequestKV(key="test1", value='{"value_1": "ghi", "value_2": "jkl"}', e_tag=6, previous_e_tag=2),  # ok
            KVSetRequestKV(key="test2", value='{"value_1": "ghi", "value_2": "jkl"}',
                           e_tag=7, previous_e_tag=4),  # e_tag mismatch
            KVSetRequestKV(key="test3", value='{"value_1": "ghi", "value_2": "jkl"}',
                           e_tag=9, previous_e_tag=None),  # e_tag mismatch
        ], service=settings.NAME)
        response = self.kv_store._kvs_set(request, None)
        self.assertCountEqual(response.kvs, [
            KVSetResponseKV(key="test", status="ok"),
            KVSetResponseKV(key="test_new", status="ok"),
            KVSetResponseKV(key="test1", status="ok"),
            KVSetResponseKV(key="test2", status="error", error="e_tag_mismatch"),
            KVSetResponseKV(key="test3", status="error", error="e_tag_mismatch")
        ])
        with self.database() as session:
            db_kvs = session.query(ExampleKVEntry).all()
            self.assertEqual(len(db_kvs), 5)
            self.assertIn(ExampleKVEntry(key="test", value_1=None, value_2="123", e_tag=4), db_kvs)
            self.assertIn(ExampleKVEntry(key="test_new", value_1="456", value_2="123", e_tag=5), db_kvs)
            self.assertIn(ExampleKVEntry(key="test1", value_1="ghi", value_2="jkl", e_tag=6), db_kvs)
            self.assertIn(ExampleKVEntry(key="test2", value_1="222", value_2="333", e_tag=3), db_kvs)
            self.assertIn(ExampleKVEntry(key="test3", value_1="111", value_2="000", e_tag=8), db_kvs)

    def test_sync(self):
        with self.database() as session:
            session.add(ExampleKVEntry(key="test", value_1="test", value_2="test2", e_tag=1))  # no change
            session.add(ExampleKVEntry(key="test1", value_1="abc", value_2="def", e_tag=2))  # changed e_tag 5
            session.add(ExampleKVEntry(key="test2", value_1="222", value_2="333", e_tag=3))  # no change
            session.add(ExampleKVEntry(key="test3", value_1="123", value_2="456", e_tag=4))  # addition
            session.commit()

        request = KVSyncRequest(service=settings.NAME, kvs={
            "test": 1,  # no change
            "test1": 5,  # changed e_tag 2
            "test2": 3,  # no change
            "test4": 6  # missing
        })
        response = self.kv_store._kvs_sync(request, None)
        self.assertDictEqual(response.additions, {"test3": 4})
        self.assertDictEqual(response.changes, {"test1": 2})
        self.assertDictEqual(response.missing, {"test4": 6})

    def test_delete_kv(self):
        with self.database() as session:
            session.add(ExampleKVEntry(key="test", value_1="test", value_2="test2", e_tag=1))  # deleting
            session.add(ExampleKVEntry(key="test1", value_1="abc", value_2="def", e_tag=2))  # no change
            session.add(ExampleKVEntry(key="test2", value_1="222", value_2="333", e_tag=3))  # no change
            session.commit()
        request = KVSetRequest(service=settings.NAME, kvs=[
            KVSetRequestKV(key="test", value='null', e_tag=4, previous_e_tag=1)])
        response = self.kv_store._kvs_set(request, None)
        self.assertCountEqual(response.kvs, [KVSetResponseKV(key="test", status="ok")])
        with self.database() as session:
            db_kvs = session.query(ExampleKVEntry).all()
            self.assertEqual(len(db_kvs), 2)
            self.assertIn(ExampleKVEntry(key="test1", value_1="abc", value_2="def", e_tag=2), db_kvs)
            self.assertIn(ExampleKVEntry(key="test2", value_1="222", value_2="333", e_tag=3), db_kvs)

    def test_wrong_data(self):
        request = KVSetRequest(service=settings.NAME, kvs=[])
        response = self.kv_store._kvs_set(request, None)
        self.assertCountEqual(response.kvs, [])
        request = KVSetRequest(service=settings.NAME, kvs=[
            KVSetRequestKV(key="test", value='{"value_2": "123"}', e_tag=4),  # ok
            KVSetRequestKV(key="test1", value='["wrong"]', e_tag=6),  # wrong type
        ])
        response = self.kv_store._kvs_set(request, None)
        self.assertCountEqual(response.kvs, [
            KVSetResponseKV(key="test", status="ok"),
            KVSetResponseKV(key="test1", status="error", error="parse_error")
        ])
        request = KVSetRequest(service=settings.NAME, kvs=[
            KVSetRequestKV(key="test2", value='{"value_2": "123"}', e_tag=4),  # ok
            KVSetRequestKV(key="test3", value='{"value_1": "123"}', e_tag=6),  # value_2 cannot be null
        ])
        with self.assertRaises(SQLAlchemyError) as e:
            response = self.kv_store._kvs_set(request, None)

    def test_add_debug_entries(self):
        self.kv_store.debug_entries = {"test": {"value_1": "test_changed", "value_2": "test_changed2"},
                                       "test2": {"value_1": "test2_changed", "value_2": "test2_changed2"}}

        request = KVSetRequest(service=settings.NAME, kvs=[
            KVSetRequestKV(key="test", value='{"value_1": "test", "value_2": "test2"}', e_tag=1)])
        response = self.kv_store._kvs_set(request, None)

        self.kv_store._add_debug_entries()
        with self.database as db:
            res = db.query(ExampleKVEntry).all()
            self.assertEqual(2, len(res))
            self.assertCountEqual([("test", "test_changed"), ("test2", "test2_changed")],
                                  [(x.key, x.value_1) for x in res])


class ExampleNotifyKVStore(KVStoreWithChangedNotification):
    database_table = ExampleKVEntry
    changed = []

    def _get_comparison_values(self, updated_kv_entries: List[KVEntry]):
        return {kv.key: kv.comparison_value() for kv in updated_kv_entries}

    def _send_changed_notification(self, success_keys: List[str], old_values: Dict[str, str]):
        self.changed = self._find_changed_kvs(success_keys, old_values)


class DatabaseNotifyTest(SQLiteTestMixin):
    alembic_path = "../tests/test_kv_store_database"
    database_name = "kvstore"

    def setUp(self) -> None:
        super().setUp()
        self.kv_store = ExampleNotifyKVStore(self.database, lambda: None)

    def test_find_changed_kvs(self):
        with self.database() as session:
            session.add(ExampleKVEntry(key="1", value_1="test", value_2="test2", e_tag=1))
            session.add(ExampleKVEntry(key="2", value_1="test", value_2="test2", e_tag=2))
            session.add(ExampleKVEntry(key="3", value_1="test", value_2="test2", e_tag=3))
            session.add(ExampleKVEntry(key="4", value_1="test", value_2="test2", e_tag=4))
            session.commit()
        # 0: deleted, 1: changed, 2: changed to same, 3: added, 4: no success
        changed = self.kv_store._find_changed_kvs(success_keys=["0", "1", "2", "3"],
                                                  old_values={"0": "c|test2", "1": "c|test2", "2": "test|test2",
                                                              "4": "test|test2"})
        self.assertCountEqual(["0", "1", "3"], changed)

    def test_set_with_changed(self):
        with self.database() as session:
            session.add(ExampleKVEntry(key="1", value_1="test", value_2="test2", e_tag=1))
            session.add(ExampleKVEntry(key="2", value_1="test", value_2="test2", e_tag=2))
            session.add(ExampleKVEntry(key="3", value_1="test", value_2="test2", e_tag=3))
            session.add(ExampleKVEntry(key="4", value_1="test", value_2="test2", e_tag=4))
            session.commit()
        self.kv_store._kvs_set(KVSetRequest(service="test",
                                            kvs=[KVSetRequestKV(key="1", value='{"value_1":"test","value_2":"test2"}',
                                                                e_tag=5, previous_e_tag=1),
                                                 KVSetRequestKV(key="2", value='{"value_1":"c","value_2":"test2"}',
                                                                e_tag=6, previous_e_tag=2),
                                                 KVSetRequestKV(key="4", value='null', previous_e_tag=4),
                                                 KVSetRequestKV(key="5", value='{"value_1":"test","value_2":"t2"}')]),
                               None)
        self.assertEqual(self.kv_store.changed, ['2', '4', '5'])


class KVStoreRPCTestCase(SQLiteTestMixin, RPCServerTestMixin, OpenModuleCoreTestMixin):
    alembic_path = "../tests/test_kv_store_database"
    database_name = "kvstore"
    rpc_channels = ["kv_sync", "rpc-websocket"]

    def setUp(self):
        super().setUp()

        self.rpc_server = RPCServer(self.zmq_context())
        self.kv_store = ExampleKVStore(self.database, self.core.rpc_client, sync_timeout=2.0)
        self.kv_store.register_rpcs(self.rpc_server)
        self.rpc_server.run_as_thread()
        self.wait_for_rpc_server(self.rpc_server)

    def tearDown(self):
        self.rpc_server.shutdown()
        super().tearDown()

    def test_rpcs(self):
        with self.database() as session:
            session.add(ExampleKVEntry(key="test", value_1="test", value_2="test2", e_tag=1))
            session.add(ExampleKVEntry(key="test1", value_1="abc", value_2="def", e_tag=2))
            session.add(ExampleKVEntry(key="test2", value_1="222", value_2="333", e_tag=3))
            session.add(ExampleKVEntry(key="test3", value_1="222", value_2="333", e_tag=4))
            session.commit()
        set_request = KVSetRequest(service=settings.NAME, kvs=[
            KVSetRequestKV(key="test3", value='null', e_tag=5, previous_e_tag=4)])
        response = self.rpc(channel="kv_sync", type="set", request=set_request, response_type=KVSetResponse)
        self.assertCountEqual(response.kvs, [KVSetResponseKV(key="test3", status="ok")])
        sync_request = KVSyncRequest(service=settings.NAME, kvs={
            "test": 1,  # no change
            "test1": 6,  # changed e_tag 2
            "test3": 7,  # no change
        })
        response = self.rpc(channel="kv_sync", type="sync", request=sync_request, response_type=KVSyncResponse)
        self.assertDictEqual(response.additions, {"test2": 3})
        self.assertDictEqual(response.changes, {"test1": 2})
        self.assertDictEqual(response.missing, {"test3": 7})

    def test_filter(self):
        request = KVSetRequest(service="wrong", kvs=[
            KVSetRequestKV(key="test", value="test", e_tag=1, previous_e_tag=0)])
        with self.assertRaises(RPCClient.TimeoutError):
            self.rpc(channel="kv_sync", type="set", request=request, response_type=KVSetResponse, timeout=1)

    def test_start_sync(self):
        def start_sync(*_):
            sync_request = KVSyncRequest(service=settings.NAME, kvs={
                "test": 1,  # no change
                "test1": 5,  # changed e_tag 2
                "test2": 3,  # no change
                "test4": 6  # missing
            })
            sync_response = self.rpc(channel="kv_sync", type="sync", request=sync_request, response_type=KVSyncResponse)
            self.assertDictEqual(sync_response.additions, {"test3": 4})
            self.assertDictEqual(sync_response.changes, {"test1": 2})
            self.assertDictEqual(sync_response.missing, {"test4": 6})
            set_request = KVSetRequest(service=settings.NAME, kvs=[
                KVSetRequestKV(key="test3", value='null', e_tag=5, previous_e_tag=4),
                KVSetRequestKV(key="test4", value='{"value_1": "000", "value_2": "000"}', e_tag=6, previous_e_tag=None),
                KVSetRequestKV(key="test1", value='{"value_1": "789", "value_2": "101"}', e_tag=7, previous_e_tag=2),
            ])
            set_response = self.rpc(channel="kv_sync", type="set", request=set_request, response_type=KVSetResponse)
            self.assertCountEqual(set_response.kvs, [
                KVSetResponseKV(key="test3", status="ok"),
                KVSetResponseKV(key="test4", status="ok"),
                KVSetResponseKV(key="test1", status="ok"),
            ])
            return ServerSyncResponse(
                errors=[
                    ServerSyncResponseKV(key="test5", status="error", error="e_tag_mismatch")],
                successes=[
                    ServerSyncResponseKV(key="test1", status="ok"),
                    ServerSyncResponseKV(key="test3", status="ok"),
                    ServerSyncResponseKV(key="test4", status="ok"),
                ])

        with self.database() as session:
            session.add(ExampleKVEntry(key="test", value_1="test", value_2="test2", e_tag=1))  # no change
            session.add(ExampleKVEntry(key="test1", value_1="abc", value_2="def", e_tag=2))  # changed e_tag 5
            session.add(ExampleKVEntry(key="test2", value_1="222", value_2="333", e_tag=3))  # no change
            session.add(ExampleKVEntry(key="test3", value_1="123", value_2="456", e_tag=4))  # addition
            session.commit()

        self.kv_store.rpc_client = MockRPCClient(responses={("rpc-websocket", "server_rpc"): start_sync()})
        entry = self.kv_store.sync_with_server()
        response = self.kv_store.log_sync_rpc_response(entry)
        self.assertEqual(response, ServerSyncResponse(
            errors=[
                ServerSyncResponseKV(key="test5", status="error", error="e_tag_mismatch")],
            successes=[
                ServerSyncResponseKV(key="test1", status="ok"),
                ServerSyncResponseKV(key="test3", status="ok"),
                ServerSyncResponseKV(key="test4", status="ok"),
            ]))

    def test_sync_errors(self):
        def raise_error(*_):
            raise ValueError("test")

        def wrong_response(*_):
            return {}

        # status error
        self.rpc_server.register_handler("rpc-websocket", "server_rpc", ServerRPCRequest, ServerSyncResponse,
                                         raise_error, register_schema=False)
        entry = self.kv_store.sync_with_server()
        response = self.kv_store.log_sync_rpc_response(entry)
        self.assertIsNone(response)

        # validation error
        del self.rpc_server.handlers[("rpc-websocket", "server_rpc")]
        self.rpc_server.register_handler("rpc-websocket", "server_rpc", ServerRPCRequest, OpenModuleModel,
                                         wrong_response, register_schema=False)
        entry = self.kv_store.sync_with_server()
        response = self.kv_store.log_sync_rpc_response(entry)
        self.assertIsNone(response)

        # timeout
        del self.rpc_server.handlers[("rpc-websocket", "server_rpc")]
        entry = self.kv_store.sync_with_server()
        response = self.kv_store.log_sync_rpc_response(entry)
        self.assertIsNone(response)

    def test_debug_entries_on_error(self):
        def raise_error(*_):
            raise ValueError("test")

        core().connection_listener._set(ConnectionStatus.online)
        self.kv_store.debug_entries = {"test": {"value_1": "test_changed", "value_2": "test_changed2"},
                                       "test2": {"value_1": "test2_changed", "value_2": "test2_changed2"}}
        self.rpc_server.register_handler("rpc-websocket", "server_rpc", ServerRPCRequest, ServerSyncResponse,
                                         raise_error, register_schema=False)
        self.kv_store.run_as_thread()
        time.sleep(2)
        self.kv_store.shutdown()

        # check if debug entries are in db
        with self.kv_store.db as db:
            self.assertEqual(2, db.query(self.kv_store.database_table).count())


class KVStoreSyncTriggerTestCase(OpenModuleCoreTestMixin):
    def setUp(self) -> None:
        super().setUp()
        self.rpc_client = MockRPCClient(callbacks={("rpc-websocket", "server_rpc"): self.on_sync_request})
        core().rpc_client = self.rpc_client
        core().connection_listener._set(ConnectionStatus.startup)
        self.kv_store = ExampleKVStore(None, self.core.rpc_client, sync_timeout=0.5)  # no database needed
        self.fail = False
        self.errors = False
        self.timeout = 0.0
        self.sync_requested = threading.Event()
        self.sync_count = 0

    def tearDown(self):
        self.kv_store.shutdown()
        super().tearDown()

    def on_sync_request(self, request: ServerRPCRequest, _) -> ServerSyncResponse:
        """
        test sync request handler
        """
        self.sync_count += 1
        self.sync_requested.set()
        if self.fail:
            raise Exception()
        if self.timeout:
            time.sleep(self.timeout)
            raise TimeoutError()
        return ServerSyncResponse(successes=[],
                                  errors=[ServerSyncResponseKV(key="1", status="1")] if self.errors else [])

    def test_sync_success(self):
        self.kv_store.run_as_thread()

        self.assertTrue(self.sync_requested.wait(1))        # check sync on start
        self.assertEqual(1, self.sync_count)                # check that only one sync
        self.sync_requested.clear()
        self.assertFalse(self.sync_requested.wait(1))       # check no retry

        core().connection_listener._set(ConnectionStatus.shutdown)
        core().connection_listener._set(ConnectionStatus.startup)
        time.sleep(1)
        self.assertTrue(self.sync_requested.wait(1))        # check sync on going online
        self.sync_requested.clear()
        self.assertFalse(self.sync_requested.wait(1))       # check no second sync
        self.assertEqual(2, self.sync_count)                # check that only one sync additional sync

    def test_sync_fail(self):
        self.fail = True
        self.kv_store.run_as_thread()

        self.assertTrue(self.sync_requested.wait(1))        # check sync on start
        self.sync_requested.clear()
        self.assertTrue(self.sync_requested.wait(1))        # check retry because of errors

        self.fail = False
        self.errors = True                                  # errors should not lead to retry
        self.assertTrue(self.sync_requested.wait(1))        # check retry success
        time.sleep(1.0)
        self.sync_requested.clear()
        self.assertFalse(self.sync_requested.wait(1))       # check no retry

        self.timeout = 0.5
        self.sync_requested.clear()
        core().connection_listener._set(ConnectionStatus.shutdown)
        core().connection_listener._set(ConnectionStatus.startup)
        self.assertTrue(self.sync_requested.wait(1))        # check sync on going online

        self.sync_requested.clear()
        self.assertTrue(self.sync_requested.wait(1))        # check retry because of timeout

    def test_shutdown(self):
        self.timeout = 5
        self.kv_store.sync_timeout = 1000
        self.kv_store.run_as_thread()
        time.sleep(1)
        self.kv_store.shutdown(2)
        self.assertFalse(self.kv_store.run_thread.is_alive())
