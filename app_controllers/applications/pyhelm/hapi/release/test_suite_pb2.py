# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hapi/release/test_suite.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from hapi.release import test_run_pb2 as hapi_dot_release_dot_test__run__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='hapi/release/test_suite.proto',
  package='hapi.release',
  syntax='proto3',
  serialized_options=_b('Z\007release'),
  serialized_pb=_b('\n\x1dhapi/release/test_suite.proto\x12\x0chapi.release\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1bhapi/release/test_run.proto\"\x95\x01\n\tTestSuite\x12.\n\nstarted_at\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x30\n\x0c\x63ompleted_at\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12&\n\x07results\x18\x03 \x03(\x0b\x32\x15.hapi.release.TestRunB\tZ\x07releaseb\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,hapi_dot_release_dot_test__run__pb2.DESCRIPTOR,])




_TESTSUITE = _descriptor.Descriptor(
  name='TestSuite',
  full_name='hapi.release.TestSuite',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='started_at', full_name='hapi.release.TestSuite.started_at', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='completed_at', full_name='hapi.release.TestSuite.completed_at', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='results', full_name='hapi.release.TestSuite.results', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=110,
  serialized_end=259,
)

_TESTSUITE.fields_by_name['started_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_TESTSUITE.fields_by_name['completed_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_TESTSUITE.fields_by_name['results'].message_type = hapi_dot_release_dot_test__run__pb2._TESTRUN
DESCRIPTOR.message_types_by_name['TestSuite'] = _TESTSUITE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TestSuite = _reflection.GeneratedProtocolMessageType('TestSuite', (_message.Message,), {
  'DESCRIPTOR' : _TESTSUITE,
  '__module__' : 'hapi.release.test_suite_pb2'
  # @@protoc_insertion_point(class_scope:hapi.release.TestSuite)
  })
_sym_db.RegisterMessage(TestSuite)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
