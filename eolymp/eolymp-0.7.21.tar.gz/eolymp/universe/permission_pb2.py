# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eolymp/universe/permission.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n eolymp/universe/permission.proto\x12\x0f\x65olymp.universe\"\x99\x01\n\nPermission\x12\n\n\x02id\x18\x01 \x01(\t\x12.\n\x04role\x18\x02 \x01(\x0e\x32 .eolymp.universe.Permission.Role\x12\x0f\n\x07user_id\x18\x03 \x01(\t\">\n\x04Role\x12\x08\n\x04NONE\x10\x00\x12\t\n\x05OWNER\x10\x01\x12\t\n\x05\x41\x44MIN\x10\x02\x12\n\n\x06VIEWER\x10\x03\x12\n\n\x06\x43USTOM\x10\x04\x42\x33Z1github.com/eolymp/go-sdk/eolymp/universe;universeb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'eolymp.universe.permission_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z1github.com/eolymp/go-sdk/eolymp/universe;universe'
  _PERMISSION._serialized_start=54
  _PERMISSION._serialized_end=207
  _PERMISSION_ROLE._serialized_start=145
  _PERMISSION_ROLE._serialized_end=207
# @@protoc_insertion_point(module_scope)
