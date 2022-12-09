# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eolymp/helpdesk/helpdesk.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from eolymp.annotations import http_pb2 as eolymp_dot_annotations_dot_http__pb2
from eolymp.annotations import ratelimit_pb2 as eolymp_dot_annotations_dot_ratelimit__pb2
from eolymp.annotations import scope_pb2 as eolymp_dot_annotations_dot_scope__pb2
from eolymp.helpdesk import document_pb2 as eolymp_dot_helpdesk_dot_document__pb2
from eolymp.wellknown import expression_pb2 as eolymp_dot_wellknown_dot_expression__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1e\x65olymp/helpdesk/helpdesk.proto\x12\x0f\x65olymp.helpdesk\x1a\x1d\x65olymp/annotations/http.proto\x1a\"eolymp/annotations/ratelimit.proto\x1a\x1e\x65olymp/annotations/scope.proto\x1a\x1e\x65olymp/helpdesk/document.proto\x1a!eolymp/wellknown/expression.proto\",\n\x15\x44\x65scribeDocumentInput\x12\x13\n\x0b\x64ocument_id\x18\x01 \x01(\t\"E\n\x16\x44\x65scribeDocumentOutput\x12+\n\x08\x64ocument\x18\x01 \x01(\x0b\x32\x19.eolymp.helpdesk.Document\"\x99\x02\n\x12ListDocumentsInput\x12\x0e\n\x06offset\x18\n \x01(\x05\x12\x0c\n\x04size\x18\x0b \x01(\x05\x12;\n\x07\x66ilters\x18( \x01(\x0b\x32*.eolymp.helpdesk.ListDocumentsInput.Filter\x1a\xa7\x01\n\x06\x46ilter\x12\r\n\x05query\x18\x01 \x01(\t\x12*\n\x02id\x18\x02 \x03(\x0b\x32\x1e.eolymp.wellknown.ExpressionID\x12\x30\n\x04path\x18\x03 \x03(\x0b\x32\".eolymp.wellknown.ExpressionString\x12\x30\n\x06locale\x18\x04 \x03(\x0b\x32 .eolymp.wellknown.ExpressionEnum\"N\n\x13ListDocumentsOutput\x12\r\n\x05total\x18\x01 \x01(\x05\x12(\n\x05items\x18\x02 \x03(\x0b\x32\x19.eolymp.helpdesk.Document\"B\n\x13\x43reateDocumentInput\x12+\n\x08\x64ocument\x18\x01 \x01(\x0b\x32\x19.eolymp.helpdesk.Document\"+\n\x14\x43reateDocumentOutput\x12\x13\n\x0b\x64ocument_id\x18\x01 \x01(\t\"W\n\x13UpdateDocumentInput\x12\x13\n\x0b\x64ocument_id\x18\x01 \x01(\t\x12+\n\x08\x64ocument\x18\x02 \x01(\x0b\x32\x19.eolymp.helpdesk.Document\"\x16\n\x14UpdateDocumentOutput\"*\n\x13\x44\x65leteDocumentInput\x12\x13\n\x0b\x64ocument_id\x18\x01 \x01(\t\"\x16\n\x14\x44\x65leteDocumentOutput\"<\n\x11\x44\x65scribePathInput\x12\x0c\n\x04path\x18\x01 \x01(\t\x12\x19\n\x11preferred_locales\x18\x02 \x03(\t\"A\n\x12\x44\x65scribePathOutput\x12+\n\x08\x64ocument\x18\x01 \x01(\x0b\x32\x19.eolymp.helpdesk.Document\"\xfe\x01\n\x0eListPathsInput\x12\x19\n\x11preferred_locales\x18\x01 \x03(\t\x12\x0e\n\x06offset\x18\n \x01(\x05\x12\x0c\n\x04size\x18\x0b \x01(\x05\x12\x37\n\x07\x66ilters\x18( \x01(\x0b\x32&.eolymp.helpdesk.ListPathsInput.Filter\x1az\n\x06\x46ilter\x12\r\n\x05query\x18\x01 \x01(\t\x12\x30\n\x04path\x18\x02 \x03(\x0b\x32\".eolymp.wellknown.ExpressionString\x12/\n\x05label\x18\x03 \x03(\x0b\x32 .eolymp.wellknown.ExpressionEnum\"J\n\x0fListPathsOutput\x12\r\n\x05total\x18\x01 \x01(\x05\x12(\n\x05items\x18\x02 \x03(\x0b\x32\x19.eolymp.helpdesk.Document\";\n\x10ListParentsInput\x12\x0c\n\x04path\x18\x01 \x01(\t\x12\x19\n\x11preferred_locales\x18\x02 \x03(\t\"L\n\x11ListParentsOutput\x12\r\n\x05total\x18\x01 \x01(\x05\x12(\n\x05items\x18\x02 \x03(\x0b\x32\x19.eolymp.helpdesk.Document2\xfa\n\n\x08Helpdesk\x12\xbc\x01\n\x10\x44\x65scribeDocument\x12&.eolymp.helpdesk.DescribeDocumentInput\x1a\'.eolymp.helpdesk.DescribeDocumentOutput\"W\x82\xe3\n\x1a\x8a\xe3\n\x16helpdesk:document:read\xea\xe2\n\x0c\xf5\xe2\n\x00\x00\xa0\x41\xf8\xe2\n\xf4\x03\x82\xd3\xe4\x93\x02#\x12!/helpdesk/documents/{document_id}\x12\xa4\x01\n\rListDocuments\x12#.eolymp.helpdesk.ListDocumentsInput\x1a$.eolymp.helpdesk.ListDocumentsOutput\"H\x82\xe3\n\x1a\x8a\xe3\n\x16helpdesk:document:read\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\xa0\x41\xf8\xe2\nd\x82\xd3\xe4\x93\x02\x15\x12\x13/helpdesk/documents\x12\xa8\x01\n\x0e\x43reateDocument\x12$.eolymp.helpdesk.CreateDocumentInput\x1a%.eolymp.helpdesk.CreateDocumentOutput\"I\x82\xe3\n\x1b\x8a\xe3\n\x17helpdesk:document:write\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\xa0@\xf8\xe2\n2\x82\xd3\xe4\x93\x02\x15\"\x13/helpdesk/documents\x12\xb6\x01\n\x0eUpdateDocument\x12$.eolymp.helpdesk.UpdateDocumentInput\x1a%.eolymp.helpdesk.UpdateDocumentOutput\"W\x82\xe3\n\x1b\x8a\xe3\n\x17helpdesk:document:write\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\xa0@\xf8\xe2\n2\x82\xd3\xe4\x93\x02#\x1a!/helpdesk/documents/{document_id}\x12\xb6\x01\n\x0e\x44\x65leteDocument\x12$.eolymp.helpdesk.DeleteDocumentInput\x1a%.eolymp.helpdesk.DeleteDocumentOutput\"W\x82\xe3\n\x1b\x8a\xe3\n\x17helpdesk:document:write\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\xa0@\xf8\xe2\n2\x82\xd3\xe4\x93\x02#*!/helpdesk/documents/{document_id}\x12\xa5\x01\n\x0c\x44\x65scribePath\x12\".eolymp.helpdesk.DescribePathInput\x1a#.eolymp.helpdesk.DescribePathOutput\"L\x82\xe3\n\x1a\x8a\xe3\n\x16helpdesk:document:read\xea\xe2\n\x0c\xf5\xe2\n\x00\x00\xa0\x41\xf8\xe2\n\xf4\x03\x82\xd3\xe4\x93\x02\x18\x12\x16/helpdesk/paths/{path}\x12\x95\x01\n\tListPaths\x12\x1f.eolymp.helpdesk.ListPathsInput\x1a .eolymp.helpdesk.ListPathsOutput\"E\x82\xe3\n\x1a\x8a\xe3\n\x16helpdesk:document:read\xea\xe2\n\x0c\xf5\xe2\n\x00\x00\xa0\x41\xf8\xe2\n\xf4\x03\x82\xd3\xe4\x93\x02\x11\x12\x0f/helpdesk/paths\x12\xaa\x01\n\x0bListParents\x12!.eolymp.helpdesk.ListParentsInput\x1a\".eolymp.helpdesk.ListParentsOutput\"T\x82\xe3\n\x1a\x8a\xe3\n\x16helpdesk:document:read\xea\xe2\n\x0c\xf5\xe2\n\x00\x00\xa0\x41\xf8\xe2\n\xf4\x03\x82\xd3\xe4\x93\x02 \x12\x1e/helpdesk/paths/{path}/parentsB3Z1github.com/eolymp/go-sdk/eolymp/helpdesk;helpdeskb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'eolymp.helpdesk.helpdesk_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z1github.com/eolymp/go-sdk/eolymp/helpdesk;helpdesk'
  _HELPDESK.methods_by_name['DescribeDocument']._options = None
  _HELPDESK.methods_by_name['DescribeDocument']._serialized_options = b'\202\343\n\032\212\343\n\026helpdesk:document:read\352\342\n\014\365\342\n\000\000\240A\370\342\n\364\003\202\323\344\223\002#\022!/helpdesk/documents/{document_id}'
  _HELPDESK.methods_by_name['ListDocuments']._options = None
  _HELPDESK.methods_by_name['ListDocuments']._serialized_options = b'\202\343\n\032\212\343\n\026helpdesk:document:read\352\342\n\013\365\342\n\000\000\240A\370\342\nd\202\323\344\223\002\025\022\023/helpdesk/documents'
  _HELPDESK.methods_by_name['CreateDocument']._options = None
  _HELPDESK.methods_by_name['CreateDocument']._serialized_options = b'\202\343\n\033\212\343\n\027helpdesk:document:write\352\342\n\013\365\342\n\000\000\240@\370\342\n2\202\323\344\223\002\025\"\023/helpdesk/documents'
  _HELPDESK.methods_by_name['UpdateDocument']._options = None
  _HELPDESK.methods_by_name['UpdateDocument']._serialized_options = b'\202\343\n\033\212\343\n\027helpdesk:document:write\352\342\n\013\365\342\n\000\000\240@\370\342\n2\202\323\344\223\002#\032!/helpdesk/documents/{document_id}'
  _HELPDESK.methods_by_name['DeleteDocument']._options = None
  _HELPDESK.methods_by_name['DeleteDocument']._serialized_options = b'\202\343\n\033\212\343\n\027helpdesk:document:write\352\342\n\013\365\342\n\000\000\240@\370\342\n2\202\323\344\223\002#*!/helpdesk/documents/{document_id}'
  _HELPDESK.methods_by_name['DescribePath']._options = None
  _HELPDESK.methods_by_name['DescribePath']._serialized_options = b'\202\343\n\032\212\343\n\026helpdesk:document:read\352\342\n\014\365\342\n\000\000\240A\370\342\n\364\003\202\323\344\223\002\030\022\026/helpdesk/paths/{path}'
  _HELPDESK.methods_by_name['ListPaths']._options = None
  _HELPDESK.methods_by_name['ListPaths']._serialized_options = b'\202\343\n\032\212\343\n\026helpdesk:document:read\352\342\n\014\365\342\n\000\000\240A\370\342\n\364\003\202\323\344\223\002\021\022\017/helpdesk/paths'
  _HELPDESK.methods_by_name['ListParents']._options = None
  _HELPDESK.methods_by_name['ListParents']._serialized_options = b'\202\343\n\032\212\343\n\026helpdesk:document:read\352\342\n\014\365\342\n\000\000\240A\370\342\n\364\003\202\323\344\223\002 \022\036/helpdesk/paths/{path}/parents'
  _DESCRIBEDOCUMENTINPUT._serialized_start=217
  _DESCRIBEDOCUMENTINPUT._serialized_end=261
  _DESCRIBEDOCUMENTOUTPUT._serialized_start=263
  _DESCRIBEDOCUMENTOUTPUT._serialized_end=332
  _LISTDOCUMENTSINPUT._serialized_start=335
  _LISTDOCUMENTSINPUT._serialized_end=616
  _LISTDOCUMENTSINPUT_FILTER._serialized_start=449
  _LISTDOCUMENTSINPUT_FILTER._serialized_end=616
  _LISTDOCUMENTSOUTPUT._serialized_start=618
  _LISTDOCUMENTSOUTPUT._serialized_end=696
  _CREATEDOCUMENTINPUT._serialized_start=698
  _CREATEDOCUMENTINPUT._serialized_end=764
  _CREATEDOCUMENTOUTPUT._serialized_start=766
  _CREATEDOCUMENTOUTPUT._serialized_end=809
  _UPDATEDOCUMENTINPUT._serialized_start=811
  _UPDATEDOCUMENTINPUT._serialized_end=898
  _UPDATEDOCUMENTOUTPUT._serialized_start=900
  _UPDATEDOCUMENTOUTPUT._serialized_end=922
  _DELETEDOCUMENTINPUT._serialized_start=924
  _DELETEDOCUMENTINPUT._serialized_end=966
  _DELETEDOCUMENTOUTPUT._serialized_start=968
  _DELETEDOCUMENTOUTPUT._serialized_end=990
  _DESCRIBEPATHINPUT._serialized_start=992
  _DESCRIBEPATHINPUT._serialized_end=1052
  _DESCRIBEPATHOUTPUT._serialized_start=1054
  _DESCRIBEPATHOUTPUT._serialized_end=1119
  _LISTPATHSINPUT._serialized_start=1122
  _LISTPATHSINPUT._serialized_end=1376
  _LISTPATHSINPUT_FILTER._serialized_start=1254
  _LISTPATHSINPUT_FILTER._serialized_end=1376
  _LISTPATHSOUTPUT._serialized_start=1378
  _LISTPATHSOUTPUT._serialized_end=1452
  _LISTPARENTSINPUT._serialized_start=1454
  _LISTPARENTSINPUT._serialized_end=1513
  _LISTPARENTSOUTPUT._serialized_start=1515
  _LISTPARENTSOUTPUT._serialized_end=1591
  _HELPDESK._serialized_start=1594
  _HELPDESK._serialized_end=2996
# @@protoc_insertion_point(module_scope)
