# Copyright (c) 2017-2022 Digital Asset (Switzerland) GmbH and/or its affiliates. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# fmt: off
# isort: skip_file
# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: com/daml/ledger/api/v1/version_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import experimental_features_pb2 as com_dot_daml_dot_ledger_dot_api_dot_v1_dot_experimental__features__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n,com/daml/ledger/api/v1/version_service.proto\x12\x16\x63om.daml.ledger.api.v1\x1a\x32\x63om/daml/ledger/api/v1/experimental_features.proto\"9\n\x1aGetLedgerApiVersionRequest\x12\x1b\n\tledger_id\x18\x01 \x01(\tR\x08ledgerId\"\x7f\n\x1bGetLedgerApiVersionResponse\x12\x18\n\x07version\x18\x01 \x01(\tR\x07version\x12\x46\n\x08\x66\x65\x61tures\x18\x02 \x01(\x0b\x32*.com.daml.ledger.api.v1.FeaturesDescriptorR\x08\x66\x65\x61tures\"\xbe\x01\n\x12\x46\x65\x61turesDescriptor\x12V\n\x0fuser_management\x18\x02 \x01(\x0b\x32-.com.daml.ledger.api.v1.UserManagementFeatureR\x0euserManagement\x12P\n\x0c\x65xperimental\x18\x01 \x01(\x0b\x32,.com.daml.ledger.api.v1.ExperimentalFeaturesR\x0c\x65xperimental\"\x93\x01\n\x15UserManagementFeature\x12\x1c\n\tsupported\x18\x01 \x01(\x08R\tsupported\x12-\n\x13max_rights_per_user\x18\x02 \x01(\x05R\x10maxRightsPerUser\x12-\n\x13max_users_page_size\x18\x03 \x01(\x05R\x10maxUsersPageSize2\x90\x01\n\x0eVersionService\x12~\n\x13GetLedgerApiVersion\x12\x32.com.daml.ledger.api.v1.GetLedgerApiVersionRequest\x1a\x33.com.daml.ledger.api.v1.GetLedgerApiVersionResponseB\x92\x01\n\x16\x63om.daml.ledger.api.v1B\x18VersionServiceOuterClassZEgithub.com/digital-asset/dazl-client/v7/go/api/com/daml/ledger/api/v1\xaa\x02\x16\x43om.Daml.Ledger.Api.V1b\x06proto3')



_GETLEDGERAPIVERSIONREQUEST = DESCRIPTOR.message_types_by_name['GetLedgerApiVersionRequest']
_GETLEDGERAPIVERSIONRESPONSE = DESCRIPTOR.message_types_by_name['GetLedgerApiVersionResponse']
_FEATURESDESCRIPTOR = DESCRIPTOR.message_types_by_name['FeaturesDescriptor']
_USERMANAGEMENTFEATURE = DESCRIPTOR.message_types_by_name['UserManagementFeature']
GetLedgerApiVersionRequest = _reflection.GeneratedProtocolMessageType('GetLedgerApiVersionRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETLEDGERAPIVERSIONREQUEST,
  '__module__' : 'com.daml.ledger.api.v1.version_service_pb2'
  # @@protoc_insertion_point(class_scope:com.daml.ledger.api.v1.GetLedgerApiVersionRequest)
  })
_sym_db.RegisterMessage(GetLedgerApiVersionRequest)

GetLedgerApiVersionResponse = _reflection.GeneratedProtocolMessageType('GetLedgerApiVersionResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETLEDGERAPIVERSIONRESPONSE,
  '__module__' : 'com.daml.ledger.api.v1.version_service_pb2'
  # @@protoc_insertion_point(class_scope:com.daml.ledger.api.v1.GetLedgerApiVersionResponse)
  })
_sym_db.RegisterMessage(GetLedgerApiVersionResponse)

FeaturesDescriptor = _reflection.GeneratedProtocolMessageType('FeaturesDescriptor', (_message.Message,), {
  'DESCRIPTOR' : _FEATURESDESCRIPTOR,
  '__module__' : 'com.daml.ledger.api.v1.version_service_pb2'
  # @@protoc_insertion_point(class_scope:com.daml.ledger.api.v1.FeaturesDescriptor)
  })
_sym_db.RegisterMessage(FeaturesDescriptor)

UserManagementFeature = _reflection.GeneratedProtocolMessageType('UserManagementFeature', (_message.Message,), {
  'DESCRIPTOR' : _USERMANAGEMENTFEATURE,
  '__module__' : 'com.daml.ledger.api.v1.version_service_pb2'
  # @@protoc_insertion_point(class_scope:com.daml.ledger.api.v1.UserManagementFeature)
  })
_sym_db.RegisterMessage(UserManagementFeature)

_VERSIONSERVICE = DESCRIPTOR.services_by_name['VersionService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\026com.daml.ledger.api.v1B\030VersionServiceOuterClassZEgithub.com/digital-asset/dazl-client/v7/go/api/com/daml/ledger/api/v1\252\002\026Com.Daml.Ledger.Api.V1'
  _GETLEDGERAPIVERSIONREQUEST._serialized_start=124
  _GETLEDGERAPIVERSIONREQUEST._serialized_end=181
  _GETLEDGERAPIVERSIONRESPONSE._serialized_start=183
  _GETLEDGERAPIVERSIONRESPONSE._serialized_end=310
  _FEATURESDESCRIPTOR._serialized_start=313
  _FEATURESDESCRIPTOR._serialized_end=503
  _USERMANAGEMENTFEATURE._serialized_start=506
  _USERMANAGEMENTFEATURE._serialized_end=653
  _VERSIONSERVICE._serialized_start=656
  _VERSIONSERVICE._serialized_end=800
# @@protoc_insertion_point(module_scope)
