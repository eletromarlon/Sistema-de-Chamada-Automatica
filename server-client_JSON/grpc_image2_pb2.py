# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: grpc_image2.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11grpc_image2.proto\x12\nhelloworld\"*\n\x0cHelloRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x0c\"\x1a\n\nHelloReply\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\x32G\n\x07Greeter\x12<\n\x08SayHello\x12\x18.helloworld.HelloRequest\x1a\x16.helloworld.HelloReplyb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'grpc_image2_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_HELLOREQUEST']._serialized_start=33
  _globals['_HELLOREQUEST']._serialized_end=75
  _globals['_HELLOREPLY']._serialized_start=77
  _globals['_HELLOREPLY']._serialized_end=103
  _globals['_GREETER']._serialized_start=105
  _globals['_GREETER']._serialized_end=176
# @@protoc_insertion_point(module_scope)