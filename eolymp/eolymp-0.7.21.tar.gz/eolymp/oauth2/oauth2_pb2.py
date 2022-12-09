# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eolymp/oauth2/oauth2.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from eolymp.annotations import ratelimit_pb2 as eolymp_dot_annotations_dot_ratelimit__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1a\x65olymp/oauth2/oauth2.proto\x12\reolymp.oauth2\x1a\"eolymp/annotations/ratelimit.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xd5\x02\n\nTokenInput\x12\x37\n\ngrant_type\x18\x01 \x01(\x0e\x32#.eolymp.oauth2.TokenInput.GrantType\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x10\n\x08password\x18\x03 \x01(\t\x12\x11\n\tclient_id\x18\x04 \x01(\t\x12\x15\n\rclient_secret\x18\x05 \x01(\t\x12\x0c\n\x04\x63ode\x18\x06 \x01(\t\x12\x15\n\rcode_verifier\x18\x07 \x01(\t\x12\r\n\x05scope\x18\x08 \x01(\t\x12\x15\n\rrefresh_token\x18\t \x01(\t\x12\x14\n\x0credirect_uri\x18\n \x01(\t\"_\n\tGrantType\x12\x08\n\x04NONE\x10\x00\x12\x0c\n\x08PASSWORD\x10\x01\x12\x16\n\x12\x41UTHORIZATION_CODE\x10\x02\x12\x11\n\rREFRESH_TOKEN\x10\x03\x12\x0f\n\x0bGOOGLE_CODE\x10\x04\"\x83\x01\n\x0bTokenOutput\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x01 \x01(\t\x12\x12\n\ntoken_type\x18\x02 \x01(\t\x12\x12\n\nexpires_in\x18\x03 \x01(\r\x12\x15\n\rrefresh_token\x18\x04 \x01(\t\x12\r\n\x05scope\x18\x05 \x01(\t\x12\x10\n\x08id_token\x18\x64 \x01(\t\"\xa5\x01\n\x0e\x41uthorizeInput\x12\x11\n\tclient_id\x18\x01 \x01(\t\x12\x16\n\x0e\x63ode_challenge\x18\x02 \x01(\t\x12\x1d\n\x15\x63ode_challenge_method\x18\x03 \x01(\t\x12\x14\n\x0credirect_uri\x18\x04 \x01(\t\x12\x15\n\rresponse_type\x18\x05 \x01(\t\x12\r\n\x05scope\x18\x06 \x01(\t\x12\r\n\x05state\x18\x07 \x01(\t\"\'\n\x0f\x41uthorizeOutput\x12\x14\n\x0credirect_uri\x18\x01 \x01(\t\",\n\rCallbackInput\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\x12\r\n\x05state\x18\x02 \x01(\t\"&\n\x0e\x43\x61llbackOutput\x12\x14\n\x0credirect_uri\x18\x01 \x01(\t\"\x0f\n\rUserInfoInput\"\xe8\x01\n\x0eUserInfoOutput\x12\x0e\n\x06issuer\x18\x01 \x01(\t\x12\x0f\n\x07subject\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x12\n\ngiven_name\x18\x04 \x01(\t\x12\x13\n\x0b\x66\x61mily_name\x18\x05 \x01(\t\x12\x13\n\x0bmiddle_name\x18\x06 \x01(\t\x12\x10\n\x08nickname\x18\x07 \x01(\t\x12\x0f\n\x07picture\x18\x08 \x01(\t\x12\r\n\x05\x65mail\x18\t \x01(\t\x12\x16\n\x0e\x65mail_verified\x18\n \x01(\x08\x12\x0e\n\x06locale\x18\x0b \x01(\t\x12\x0f\n\x07profile\x18\x0c \x01(\t\" \n\x0fIntrospectInput\x12\r\n\x05token\x18\x01 \x01(\t\"\xf8\x01\n\x10IntrospectOutput\x12\x0e\n\x06\x61\x63tive\x18\x01 \x01(\x08\x12\r\n\x05scope\x18\x02 \x01(\t\x12*\n\x06\x65xpire\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0f\n\x07subject\x18\x04 \x01(\t\x12\x10\n\x08\x61udience\x18\x05 \x01(\t\x12\x0e\n\x06issuer\x18\x06 \x01(\t\x12\x0c\n\x04name\x18\x64 \x01(\t\x12\x10\n\x08nickname\x18\x65 \x01(\t\x12\x0f\n\x07picture\x18\x66 \x01(\t\x12\r\n\x05\x65mail\x18g \x01(\t\x12\x16\n\x0e\x65mail_verified\x18h \x01(\x08\x12\x0e\n\x06locale\x18i \x01(\t\"\xa4\x01\n\rAuthCodeInput\x12\x11\n\tclient_id\x18\x01 \x01(\t\x12\x16\n\x0e\x63ode_challenge\x18\x02 \x01(\t\x12\x1d\n\x15\x63ode_challenge_method\x18\x03 \x01(\t\x12\x14\n\x0credirect_uri\x18\x04 \x01(\t\x12\x15\n\rresponse_type\x18\x05 \x01(\t\x12\r\n\x05scope\x18\x06 \x01(\t\x12\r\n\x05state\x18\x07 \x01(\t\"B\n\x0e\x41uthCodeOutput\x12\x1a\n\x12\x61uthorization_code\x18\x01 \x01(\t\x12\x14\n\x0credirect_uri\x18\x02 \x01(\t\"\x1c\n\x0bRevokeInput\x12\r\n\x05token\x18\x01 \x01(\t\"\x0e\n\x0cRevokeOutput2\xfe\x04\n\x06OAuth2\x12P\n\x05Token\x12\x19.eolymp.oauth2.TokenInput\x1a\x1a.eolymp.oauth2.TokenOutput\"\x10\xea\xe2\n\x0c\xf5\xe2\n\x00\x00\xf0\x41\xf8\xe2\n\xac\x02\x12Y\n\x08UserInfo\x12\x1c.eolymp.oauth2.UserInfoInput\x1a\x1d.eolymp.oauth2.UserInfoOutput\"\x10\xea\xe2\n\x0c\xf5\xe2\n\x00\x00\xf0\x41\xf8\xe2\n\xac\x02\x12^\n\nIntrospect\x12\x1e.eolymp.oauth2.IntrospectInput\x1a\x1f.eolymp.oauth2.IntrospectOutput\"\x0f\xea\xe2\n\x0b\xf5\xe2\n\x00\x00 A\xf8\xe2\n2\x12S\n\x06Revoke\x12\x1a.eolymp.oauth2.RevokeInput\x1a\x1b.eolymp.oauth2.RevokeOutput\"\x10\xea\xe2\n\x0c\xf5\xe2\n\x00\x00\xf0\x41\xf8\xe2\n\xac\x02\x12Y\n\x08\x41uthCode\x12\x1c.eolymp.oauth2.AuthCodeInput\x1a\x1d.eolymp.oauth2.AuthCodeOutput\"\x10\xea\xe2\n\x0c\xf5\xe2\n\x00\x00\xf0\x41\xf8\xe2\n\xac\x02\x12\\\n\tAuthorize\x12\x1d.eolymp.oauth2.AuthorizeInput\x1a\x1e.eolymp.oauth2.AuthorizeOutput\"\x10\xea\xe2\n\x0c\xf5\xe2\n\x00\x00\xf0\x41\xf8\xe2\n\xac\x02\x12Y\n\x08\x43\x61llback\x12\x1c.eolymp.oauth2.CallbackInput\x1a\x1d.eolymp.oauth2.CallbackOutput\"\x10\xea\xe2\n\x0c\xf5\xe2\n\x00\x00\xf0\x41\xf8\xe2\n\xac\x02\x42/Z-github.com/eolymp/go-sdk/eolymp/oauth2;oauth2b\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'eolymp.oauth2.oauth2_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z-github.com/eolymp/go-sdk/eolymp/oauth2;oauth2'
  _OAUTH2.methods_by_name['Token']._options = None
  _OAUTH2.methods_by_name['Token']._serialized_options = b'\352\342\n\014\365\342\n\000\000\360A\370\342\n\254\002'
  _OAUTH2.methods_by_name['UserInfo']._options = None
  _OAUTH2.methods_by_name['UserInfo']._serialized_options = b'\352\342\n\014\365\342\n\000\000\360A\370\342\n\254\002'
  _OAUTH2.methods_by_name['Introspect']._options = None
  _OAUTH2.methods_by_name['Introspect']._serialized_options = b'\352\342\n\013\365\342\n\000\000 A\370\342\n2'
  _OAUTH2.methods_by_name['Revoke']._options = None
  _OAUTH2.methods_by_name['Revoke']._serialized_options = b'\352\342\n\014\365\342\n\000\000\360A\370\342\n\254\002'
  _OAUTH2.methods_by_name['AuthCode']._options = None
  _OAUTH2.methods_by_name['AuthCode']._serialized_options = b'\352\342\n\014\365\342\n\000\000\360A\370\342\n\254\002'
  _OAUTH2.methods_by_name['Authorize']._options = None
  _OAUTH2.methods_by_name['Authorize']._serialized_options = b'\352\342\n\014\365\342\n\000\000\360A\370\342\n\254\002'
  _OAUTH2.methods_by_name['Callback']._options = None
  _OAUTH2.methods_by_name['Callback']._serialized_options = b'\352\342\n\014\365\342\n\000\000\360A\370\342\n\254\002'
  _TOKENINPUT._serialized_start=115
  _TOKENINPUT._serialized_end=456
  _TOKENINPUT_GRANTTYPE._serialized_start=361
  _TOKENINPUT_GRANTTYPE._serialized_end=456
  _TOKENOUTPUT._serialized_start=459
  _TOKENOUTPUT._serialized_end=590
  _AUTHORIZEINPUT._serialized_start=593
  _AUTHORIZEINPUT._serialized_end=758
  _AUTHORIZEOUTPUT._serialized_start=760
  _AUTHORIZEOUTPUT._serialized_end=799
  _CALLBACKINPUT._serialized_start=801
  _CALLBACKINPUT._serialized_end=845
  _CALLBACKOUTPUT._serialized_start=847
  _CALLBACKOUTPUT._serialized_end=885
  _USERINFOINPUT._serialized_start=887
  _USERINFOINPUT._serialized_end=902
  _USERINFOOUTPUT._serialized_start=905
  _USERINFOOUTPUT._serialized_end=1137
  _INTROSPECTINPUT._serialized_start=1139
  _INTROSPECTINPUT._serialized_end=1171
  _INTROSPECTOUTPUT._serialized_start=1174
  _INTROSPECTOUTPUT._serialized_end=1422
  _AUTHCODEINPUT._serialized_start=1425
  _AUTHCODEINPUT._serialized_end=1589
  _AUTHCODEOUTPUT._serialized_start=1591
  _AUTHCODEOUTPUT._serialized_end=1657
  _REVOKEINPUT._serialized_start=1659
  _REVOKEINPUT._serialized_end=1687
  _REVOKEOUTPUT._serialized_start=1689
  _REVOKEOUTPUT._serialized_end=1703
  _OAUTH2._serialized_start=1706
  _OAUTH2._serialized_end=2344
# @@protoc_insertion_point(module_scope)
