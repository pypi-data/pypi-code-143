# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eolymp/atlas/template.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from eolymp.annotations import resource_pb2 as eolymp_dot_annotations_dot_resource__pb2
from eolymp.atlas import file_pb2 as eolymp_dot_atlas_dot_file__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1b\x65olymp/atlas/template.proto\x12\x0c\x65olymp.atlas\x1a!eolymp/annotations/resource.proto\x1a\x17\x65olymp/atlas/file.proto\"\x82\x02\n\x08Template\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x03\x65rn\x18\x8fN \x01(\t\x12\x12\n\nproblem_id\x18\x02 \x01(\t\x12\x0f\n\x07runtime\x18\x03 \x01(\t\x12\x0e\n\x06source\x18\n \x01(\t\x12\x0e\n\x06header\x18\x0b \x01(\t\x12\x0e\n\x06\x66ooter\x18\x0c \x01(\t\x12\x12\n\nsource_ern\x18\x14 \x01(\t\x12\x12\n\nheader_ern\x18\x15 \x01(\t\x12\x12\n\nfooter_ern\x18\x16 \x01(\t\x12!\n\x05\x66iles\x18\x1e \x03(\x0b\x32\x12.eolymp.atlas.File:(\xb2\xe3\n$\xba\xe3\n\x08template\xc2\xe3\n\x14\x65olymp.atlas.ProblemB-Z+github.com/eolymp/go-sdk/eolymp/atlas;atlasb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'eolymp.atlas.template_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z+github.com/eolymp/go-sdk/eolymp/atlas;atlas'
  _TEMPLATE._options = None
  _TEMPLATE._serialized_options = b'\262\343\n$\272\343\n\010template\302\343\n\024eolymp.atlas.Problem'
  _TEMPLATE._serialized_start=106
  _TEMPLATE._serialized_end=364
# @@protoc_insertion_point(module_scope)
