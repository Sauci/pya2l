"""
@project: pya2l
@file: parser.py
@author: Guillaume Sottas
@date: 20.03.2018
"""
import ctypes
import os
import typing

import google.protobuf.message
from google.protobuf.json_format import MessageToJson

from protobuf.API_pb2 import *
from protobuf.API_pb2_grpc import *


class A2lParser(object):
    def __init__(self, string, include_dir=tuple()):
        if os.name == 'nt':
            shared_object = 'a2l_grpc_windows_amd64.dll'
        elif os.name == 'posix':
            shared_object = 'a2l_grpc_linux_amd64.so'
        else:
            raise Exception(f'unsupported operating system {os.name}')
        self._dll = ctypes.cdll.LoadLibrary(
            os.path.join(os.path.dirname(__file__), 'a2l_grpc', shared_object))
        options = [('grpc.max_receive_message_length', 100 * 1024 * 1024),
                   ('grpc.max_send_message_length', 100 * 1024 * 1024)]
        channel = grpc.insecure_channel('localhost:3333', options=options)
        client = A2LStub(channel)
        if self._dll.Create(3333):
            raise Exception(1)
        setattr(google.protobuf.message.Message, 'properties',
                property(lambda e: [str(f) for f in e.DESCRIPTOR.fields_by_name]))
        setattr(google.protobuf.message.Message, 'is_none',
                property(lambda e: not e.Present if 'Present' in e.properties else len(e.ListFields()) == 0))
        setattr(google.protobuf.message.Message, 'json',
                lambda e,
                       indent=True,
                       sort_keys=False,
                       include_default_value_fields=True: MessageToJson(e,
                                                                        indent=indent,
                                                                        sort_keys=sort_keys,
                                                                        including_default_value_fields=include_default_value_fields,
                                                                        preserving_proto_field_name=True))
        self.ast = client.GetTree(GetTreeRequest(a2l=string))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._dll.Close():
            raise Exception(1)

    @staticmethod
    def get_if_data_by_name_and_index(node, name: str, index: typing.Union[int, None] = None):
        if 'IF_DATA' in node.properties:
            for if_data_node in node.IF_DATA:
                if if_data_node.Name.Value == name:
                    if index is not None:
                        return getattr(if_data_node.Blob[index], if_data_node.Blob[index].WhichOneof('oneof'))
                    else:
                        return [getattr(if_data_node.Blob[index], if_data_node.Blob[index].WhichOneof('oneof')) for index in range(len(if_data_node.Blob))]
        return None

    def dump(self, indent=4, line_ending='\n', indent_char=' '):
        if self.ast and hasattr(self.ast, 'project'):
            result = list()
            for indentation_level, string in self.ast.project.dump():
                result.append(((indent_char * indent) * indentation_level) + string)
            return line_ending.join(result)
        else:
            return ''
