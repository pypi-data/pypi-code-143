# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eolymp/cognito/access_key.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1f\x65olymp/cognito/access_key.proto\x12\x0e\x65olymp.cognito\x1a\x1fgoogle/protobuf/timestamp.proto\"\x94\x01\n\tAccessKey\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\r\n\x05scope\x18\x03 \x01(\t\x12.\n\ncreated_at\x18\n \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\nexpires_at\x18\x0b \x01(\x0b\x32\x1a.google.protobuf.TimestampB1Z/github.com/eolymp/go-sdk/eolymp/cognito;cognitob\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'eolymp.cognito.access_key_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z/github.com/eolymp/go-sdk/eolymp/cognito;cognito'
  _ACCESSKEY._serialized_start=85
  _ACCESSKEY._serialized_end=233
# @@protoc_insertion_point(module_scope)
