# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eolymp/community/attribute.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from eolymp.annotations import resource_pb2 as eolymp_dot_annotations_dot_resource__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n eolymp/community/attribute.proto\x12\x10\x65olymp.community\x1a!eolymp/annotations/resource.proto\"\xa1\x04\n\tAttribute\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x0c\n\x03\x65rn\x18\x8fN \x01(\t\x12<\n\x0b\x64\x65scription\x18\n \x03(\x0b\x32\'.eolymp.community.Attribute.Description\x12.\n\x04type\x18\x14 \x01(\x0e\x32 .eolymp.community.Attribute.Type\x12\r\n\x05index\x18\x15 \x01(\r\x12\x10\n\x08required\x18\x1f \x01(\x08\x12\x0e\n\x06hidden\x18  \x01(\x08\x12\x0e\n\x06regexp\x18\x64 \x01(\t\x12\x0b\n\x03min\x18\x65 \x01(\x05\x12\x0b\n\x03max\x18\x66 \x01(\x05\x12\x0f\n\x07\x63hoices\x18g \x03(\t\x12\x0f\n\x07\x63ountry\x18h \x01(\t\x1a\\\n\x0b\x44\x65scription\x12\x0f\n\x07\x64\x65\x66\x61ult\x18\x01 \x01(\x08\x12\x0e\n\x06locale\x18\x02 \x01(\t\x12\r\n\x05label\x18\x03 \x01(\t\x12\x0c\n\x04help\x18\x04 \x01(\t\x12\x0f\n\x07\x63hoices\x18\x05 \x03(\t\"}\n\x04Type\x12\x0b\n\x07UNKNOWN\x10\x00\x12\n\n\x06STRING\x10\x01\x12\x08\n\x04TEXT\x10\x02\x12\n\n\x06NUMBER\x10\x03\x12\n\n\x06\x43HOICE\x10\x04\x12\x08\n\x04\x44\x41TE\x10\x05\x12\t\n\x05\x45MAIL\x10\x06\x12\x0c\n\x08\x43HECKBOX\x10\x07\x12\x0b\n\x07\x43OUNTRY\x10\x08\x12\n\n\x06REGION\x10\t:1\xb2\xe3\n-\xba\xe3\n\tattribute\xc2\xe3\n\x15\x65olymp.universe.Space\xca\xe3\n\x03keyB5Z3github.com/eolymp/go-sdk/eolymp/community;communityb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'eolymp.community.attribute_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z3github.com/eolymp/go-sdk/eolymp/community;community'
  _ATTRIBUTE._options = None
  _ATTRIBUTE._serialized_options = b'\262\343\n-\272\343\n\tattribute\302\343\n\025eolymp.universe.Space\312\343\n\003key'
  _ATTRIBUTE._serialized_start=90
  _ATTRIBUTE._serialized_end=635
  _ATTRIBUTE_DESCRIPTION._serialized_start=365
  _ATTRIBUTE_DESCRIPTION._serialized_end=457
  _ATTRIBUTE_TYPE._serialized_start=459
  _ATTRIBUTE_TYPE._serialized_end=584
# @@protoc_insertion_point(module_scope)
