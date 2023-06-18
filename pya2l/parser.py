"""
@project: pya2l
@file: parser.py
@author: Guillaume Sottas
@date: 20.03.2018
"""
import ctypes
import json
import logging
import os
import typing

import google.protobuf.message

from pya2l.protobuf.API_pb2 import *
from pya2l.protobuf.API_pb2_grpc import *
from pya2l.protobuf.A2L_pb2 import *


class A2lParser(object):
    def __init__(self, port=3333, logger: logging.Logger = None):
        self._logger = logger
        if os.name == 'nt':
            shared_object = 'a2l_grpc_windows_amd64.dll'
        elif os.name == 'posix':
            shared_object = 'a2l_grpc_linux_amd64.so'
        else:
            raise Exception(f'unsupported operating system {os.name}')
        self._dll = ctypes.cdll.LoadLibrary(
            os.path.join(os.path.dirname(__file__), 'a2l_grpc', shared_object))
        options = [('grpc.max_receive_message_length', 200 * 1024 * 1024),
                   ('grpc.max_send_message_length', 200 * 1024 * 1024)]
        channel = grpc.insecure_channel(f'localhost:{port}', options=options)
        self._client = A2LStub(channel)
        if self._dll.Create(port):
            raise Exception(1)
        setattr(google.protobuf.message.Message, 'properties',
                property(lambda e: [str(f) for f in e.DESCRIPTOR.fields_by_name]))
        setattr(google.protobuf.message.Message, 'is_none',
                property(lambda e: not e.Present if 'Present' in e.properties else len(e.ListFields()) == 0))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
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
                        return [getattr(if_data_node.Blob[index], if_data_node.Blob[index].WhichOneof('oneof')) for
                                index in range(len(if_data_node.Blob))]
        return None

    def tree_from_a2l(self, a2l_string: str) -> RootNodeType:
        if self._logger:
            self._logger.info('start parsing A2L')
        response = self._client.GetTreeFromA2L(A2LRequest(a2l=a2l_string))
        if self._logger:
            self._logger.info('finished parsing A2L')
        if response.error != '' and self._logger:
            self._logger.warning(response.error)
        return response.tree

    def tree_from_json(self, json_string: str) -> RootNodeType:
        if self._logger:
            self._logger.info('start parsing JSON A2L')
        response = self._client.GetTreeFromJSON(JSONRequest(json=json_string))
        if self._logger:
            self._logger.info('finished parsing JSON A2L')
        if response.error != '' and self._logger:
            self._logger.warning(response.error)
        return response.tree

    def json_from_tree(self, tree, indent : int = None) -> str:
        response = self._client.GetJSONFromTree(JSONFromTreeRequest(tree=tree, indent=indent))
        if response.error == '':
            return response.json
        else:
            if self._logger:
                self._logger.warning(response.error)

    # def dump(self, indent=4, line_ending='\n', indent_char=' '):
    #     if self.ast and hasattr(self.ast, 'project'):
    #         result = list()
    #         for indentation_level, string in self.ast.project.dump():
    #             result.append(((indent_char * indent) * indentation_level) + string)
    #         return line_ending.join(result)
    #     else:
    #         return ''
