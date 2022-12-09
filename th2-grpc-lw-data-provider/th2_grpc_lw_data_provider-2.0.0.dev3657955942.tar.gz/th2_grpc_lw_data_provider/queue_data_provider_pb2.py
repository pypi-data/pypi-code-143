# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: th2_grpc_lw_data_provider/queue_data_provider.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from th2_grpc_lw_data_provider import lw_data_provider_pb2 as th2__grpc__lw__data__provider_dot_lw__data__provider__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n3th2_grpc_lw_data_provider/queue_data_provider.proto\x12\x14th2.data_provider.lw\x1a\x1egoogle/protobuf/duration.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x30th2_grpc_lw_data_provider/lw_data_provider.proto\"\xe6\x03\n\x1fMessageGroupsQueueSearchRequest\x12\x33\n\x0fstart_timestamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x31\n\rend_timestamp\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12W\n\rmessage_group\x18\x07 \x03(\x0b\x32@.th2.data_provider.lw.MessageGroupsQueueSearchRequest.BookGroups\x12\x30\n\rsync_interval\x18\x04 \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x16\n\x0e\x65xternal_queue\x18\x05 \x01(\t\x12\x12\n\nkeep_alive\x18\x06 \x01(\x08\x12\x19\n\x11send_raw_directly\x18\x08 \x01(\x08\x1a\x82\x01\n\nBookGroups\x12-\n\x07\x62ook_id\x18\x01 \x01(\x0b\x32\x1c.th2.data_provider.lw.BookId\x12\x45\n\x05group\x18\x02 \x03(\x0b\x32\x36.th2.data_provider.lw.MessageGroupsSearchRequest.GroupJ\x04\x08\x03\x10\x04\"\xf1\x01\n\x16MessageLoadedStatistic\x12\x44\n\x04stat\x18\x01 \x03(\x0b\x32\x36.th2.data_provider.lw.MessageLoadedStatistic.GroupStat\x1a\x90\x01\n\tGroupStat\x12-\n\x07\x62ook_id\x18\x03 \x01(\x0b\x32\x1c.th2.data_provider.lw.BookId\x12\x45\n\x05group\x18\x01 \x01(\x0b\x32\x36.th2.data_provider.lw.MessageGroupsSearchRequest.Group\x12\r\n\x05\x63ount\x18\x02 \x01(\x04\"\x9d\x03\n\x17\x45ventQueueSearchRequest\x12\x33\n\x0fstart_timestamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x31\n\rend_timestamp\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12N\n\x0c\x65vent_scopes\x18\x07 \x03(\x0b\x32\x38.th2.data_provider.lw.EventQueueSearchRequest.BookScopes\x12\x30\n\rsync_interval\x18\x04 \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x16\n\x0e\x65xternal_queue\x18\x05 \x01(\t\x12\x12\n\nkeep_alive\x18\x06 \x01(\x08\x1al\n\nBookScopes\x12-\n\x07\x62ook_id\x18\x01 \x01(\x0b\x32\x1c.th2.data_provider.lw.BookId\x12/\n\x05scope\x18\x02 \x03(\x0b\x32 .th2.data_provider.lw.EventScope\"\xd6\x01\n\x14\x45ventLoadedStatistic\x12\x42\n\x04stat\x18\x01 \x03(\x0b\x32\x34.th2.data_provider.lw.EventLoadedStatistic.ScopeStat\x1az\n\tScopeStat\x12-\n\x07\x62ook_id\x18\x03 \x01(\x0b\x32\x1c.th2.data_provider.lw.BookId\x12/\n\x05scope\x18\x01 \x01(\x0b\x32 .th2.data_provider.lw.EventScope\x12\r\n\x05\x63ount\x18\x02 \x01(\x04\x32\xfa\x01\n\x11QueueDataProvider\x12z\n\x13SearchMessageGroups\x12\x35.th2.data_provider.lw.MessageGroupsQueueSearchRequest\x1a,.th2.data_provider.lw.MessageLoadedStatistic\x12i\n\x0cSearchEvents\x12-.th2.data_provider.lw.EventQueueSearchRequest\x1a*.th2.data_provider.lw.EventLoadedStatisticB)\n%com.exactpro.th2.dataprovider.lw.grpcP\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'th2_grpc_lw_data_provider.queue_data_provider_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n%com.exactpro.th2.dataprovider.lw.grpcP\001'
  _MESSAGEGROUPSQUEUESEARCHREQUEST._serialized_start=193
  _MESSAGEGROUPSQUEUESEARCHREQUEST._serialized_end=679
  _MESSAGEGROUPSQUEUESEARCHREQUEST_BOOKGROUPS._serialized_start=543
  _MESSAGEGROUPSQUEUESEARCHREQUEST_BOOKGROUPS._serialized_end=673
  _MESSAGELOADEDSTATISTIC._serialized_start=682
  _MESSAGELOADEDSTATISTIC._serialized_end=923
  _MESSAGELOADEDSTATISTIC_GROUPSTAT._serialized_start=779
  _MESSAGELOADEDSTATISTIC_GROUPSTAT._serialized_end=923
  _EVENTQUEUESEARCHREQUEST._serialized_start=926
  _EVENTQUEUESEARCHREQUEST._serialized_end=1339
  _EVENTQUEUESEARCHREQUEST_BOOKSCOPES._serialized_start=1231
  _EVENTQUEUESEARCHREQUEST_BOOKSCOPES._serialized_end=1339
  _EVENTLOADEDSTATISTIC._serialized_start=1342
  _EVENTLOADEDSTATISTIC._serialized_end=1556
  _EVENTLOADEDSTATISTIC_SCOPESTAT._serialized_start=1434
  _EVENTLOADEDSTATISTIC_SCOPESTAT._serialized_end=1556
  _QUEUEDATAPROVIDER._serialized_start=1559
  _QUEUEDATAPROVIDER._serialized_end=1809
# @@protoc_insertion_point(module_scope)
