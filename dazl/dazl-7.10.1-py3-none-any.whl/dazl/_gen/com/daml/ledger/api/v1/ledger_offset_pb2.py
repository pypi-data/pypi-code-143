# Copyright (c) 2017-2022 Digital Asset (Switzerland) GmbH and/or its affiliates. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# fmt: off
# isort: skip_file
# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: com/daml/ledger/api/v1/ledger_offset.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*com/daml/ledger/api/v1/ledger_offset.proto\x12\x16\x63om.daml.ledger.api.v1\"\xbc\x01\n\x0cLedgerOffset\x12\x1c\n\x08\x61\x62solute\x18\x01 \x01(\tH\x00R\x08\x61\x62solute\x12Q\n\x08\x62oundary\x18\x02 \x01(\x0e\x32\x33.com.daml.ledger.api.v1.LedgerOffset.LedgerBoundaryH\x00R\x08\x62oundary\"2\n\x0eLedgerBoundary\x12\x10\n\x0cLEDGER_BEGIN\x10\x00\x12\x0e\n\nLEDGER_END\x10\x01\x42\x07\n\x05valueB\x90\x01\n\x16\x63om.daml.ledger.api.v1B\x16LedgerOffsetOuterClassZEgithub.com/digital-asset/dazl-client/v7/go/api/com/daml/ledger/api/v1\xaa\x02\x16\x43om.Daml.Ledger.Api.V1b\x06proto3')



_LEDGEROFFSET = DESCRIPTOR.message_types_by_name['LedgerOffset']
_LEDGEROFFSET_LEDGERBOUNDARY = _LEDGEROFFSET.enum_types_by_name['LedgerBoundary']
LedgerOffset = _reflection.GeneratedProtocolMessageType('LedgerOffset', (_message.Message,), {
  'DESCRIPTOR' : _LEDGEROFFSET,
  '__module__' : 'com.daml.ledger.api.v1.ledger_offset_pb2'
  # @@protoc_insertion_point(class_scope:com.daml.ledger.api.v1.LedgerOffset)
  })
_sym_db.RegisterMessage(LedgerOffset)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\026com.daml.ledger.api.v1B\026LedgerOffsetOuterClassZEgithub.com/digital-asset/dazl-client/v7/go/api/com/daml/ledger/api/v1\252\002\026Com.Daml.Ledger.Api.V1'
  _LEDGEROFFSET._serialized_start=71
  _LEDGEROFFSET._serialized_end=259
  _LEDGEROFFSET_LEDGERBOUNDARY._serialized_start=200
  _LEDGEROFFSET_LEDGERBOUNDARY._serialized_end=250
# @@protoc_insertion_point(module_scope)
