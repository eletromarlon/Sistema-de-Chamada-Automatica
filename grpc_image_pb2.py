# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: grpc_image.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10grpc_image.proto\x12\rimage_service\"\"\n\x0cImageRequest\x12\x12\n\nimage_data\x18\x01 \x01(\x0c\"5\n\x11ImageConfirmation\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t2Z\n\x0cImageService\x12J\n\tSendImage\x12\x1b.image_service.ImageRequest\x1a .image_service.ImageConfirmationb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'grpc_image_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_IMAGEREQUEST']._serialized_start=35
  _globals['_IMAGEREQUEST']._serialized_end=69
  _globals['_IMAGECONFIRMATION']._serialized_start=71
  _globals['_IMAGECONFIRMATION']._serialized_end=124
  _globals['_IMAGESERVICE']._serialized_start=126
  _globals['_IMAGESERVICE']._serialized_end=216
# @@protoc_insertion_point(module_scope)
