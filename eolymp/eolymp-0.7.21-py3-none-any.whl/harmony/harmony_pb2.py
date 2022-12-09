# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eolymp/harmony/harmony.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from eolymp.annotations import http_pb2 as eolymp_dot_annotations_dot_http__pb2
from eolymp.annotations import ratelimit_pb2 as eolymp_dot_annotations_dot_ratelimit__pb2
from eolymp.harmony import agreement_pb2 as eolymp_dot_harmony_dot_agreement__pb2
from eolymp.harmony import consent_pb2 as eolymp_dot_harmony_dot_consent__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1c\x65olymp/harmony/harmony.proto\x12\x0e\x65olymp.harmony\x1a\x1d\x65olymp/annotations/http.proto\x1a\"eolymp/annotations/ratelimit.proto\x1a\x1e\x65olymp/harmony/agreement.proto\x1a\x1c\x65olymp/harmony/consent.proto\"0\n\x13ListAgreementsInput\x12\x19\n\x11preferred_locales\x18\x01 \x03(\t\"@\n\x14ListAgreementsOutput\x12(\n\x05items\x18\x01 \x03(\x0b\x32\x19.eolymp.harmony.Agreement\"\'\n\x0fGetConsentInput\x12\x14\n\x0c\x61greement_id\x18\x01 \x01(\t\"<\n\x10GetConsentOutput\x12(\n\x07\x63onsent\x18\x01 \x01(\x0b\x32\x17.eolymp.harmony.Consent\"W\n\x0fSetConsentInput\x12\x14\n\x0c\x61greement_id\x18\x01 \x01(\t\x12.\n\x06status\x18\x02 \x01(\x0e\x32\x1e.eolymp.harmony.Consent.Status\"<\n\x10SetConsentOutput\x12(\n\x07\x63onsent\x18\x01 \x01(\x0b\x32\x17.eolymp.harmony.Consent\"Z\n\x13\x46ollowShortcutInput\x12\x13\n\x0bshortcut_id\x18\x01 \x01(\t\x12.\n\x06status\x18\x02 \x01(\x0e\x32\x1e.eolymp.harmony.Consent.Status\"\x16\n\x14\x46ollowShortcutOutput2\xd4\x04\n\x07Harmony\x12\x87\x01\n\x0eListAgreements\x12#.eolymp.harmony.ListAgreementsInput\x1a$.eolymp.harmony.ListAgreementsOutput\"*\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\xa0@\xf8\xe2\n\n\x82\xd3\xe4\x93\x02\x15\x12\x13/harmony/agreements\x12\x92\x01\n\nGetConsent\x12\x1f.eolymp.harmony.GetConsentInput\x1a .eolymp.harmony.GetConsentOutput\"A\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\xa0@\xf8\xe2\n\n\x82\xd3\xe4\x93\x02,\x12*/harmony/agreements/{agreement_id}/consent\x12\x92\x01\n\nSetConsent\x12\x1f.eolymp.harmony.SetConsentInput\x1a .eolymp.harmony.SetConsentOutput\"A\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\xa0@\xf8\xe2\n\n\x82\xd3\xe4\x93\x02,\x1a*/harmony/agreements/{agreement_id}/consent\x12\x94\x01\n\x0e\x46ollowShortcut\x12#.eolymp.harmony.FollowShortcutInput\x1a$.eolymp.harmony.FollowShortcutOutput\"7\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\xa0@\xf8\xe2\n\n\x82\xd3\xe4\x93\x02\"\" /harmony/shortcuts/{shortcut_id}B1Z/github.com/eolymp/go-sdk/eolymp/harmony;harmonyb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'eolymp.harmony.harmony_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z/github.com/eolymp/go-sdk/eolymp/harmony;harmony'
  _HARMONY.methods_by_name['ListAgreements']._options = None
  _HARMONY.methods_by_name['ListAgreements']._serialized_options = b'\352\342\n\013\365\342\n\000\000\240@\370\342\n\n\202\323\344\223\002\025\022\023/harmony/agreements'
  _HARMONY.methods_by_name['GetConsent']._options = None
  _HARMONY.methods_by_name['GetConsent']._serialized_options = b'\352\342\n\013\365\342\n\000\000\240@\370\342\n\n\202\323\344\223\002,\022*/harmony/agreements/{agreement_id}/consent'
  _HARMONY.methods_by_name['SetConsent']._options = None
  _HARMONY.methods_by_name['SetConsent']._serialized_options = b'\352\342\n\013\365\342\n\000\000\240@\370\342\n\n\202\323\344\223\002,\032*/harmony/agreements/{agreement_id}/consent'
  _HARMONY.methods_by_name['FollowShortcut']._options = None
  _HARMONY.methods_by_name['FollowShortcut']._serialized_options = b'\352\342\n\013\365\342\n\000\000\240@\370\342\n\n\202\323\344\223\002\"\" /harmony/shortcuts/{shortcut_id}'
  _LISTAGREEMENTSINPUT._serialized_start=177
  _LISTAGREEMENTSINPUT._serialized_end=225
  _LISTAGREEMENTSOUTPUT._serialized_start=227
  _LISTAGREEMENTSOUTPUT._serialized_end=291
  _GETCONSENTINPUT._serialized_start=293
  _GETCONSENTINPUT._serialized_end=332
  _GETCONSENTOUTPUT._serialized_start=334
  _GETCONSENTOUTPUT._serialized_end=394
  _SETCONSENTINPUT._serialized_start=396
  _SETCONSENTINPUT._serialized_end=483
  _SETCONSENTOUTPUT._serialized_start=485
  _SETCONSENTOUTPUT._serialized_end=545
  _FOLLOWSHORTCUTINPUT._serialized_start=547
  _FOLLOWSHORTCUTINPUT._serialized_end=637
  _FOLLOWSHORTCUTOUTPUT._serialized_start=639
  _FOLLOWSHORTCUTOUTPUT._serialized_end=661
  _HARMONY._serialized_start=664
  _HARMONY._serialized_end=1260
# @@protoc_insertion_point(module_scope)
