"""
@project: pya2l
@file: parser.py
@author: Guillaume Sottas
@date: 20.03.2018
"""
import ctypes
import logging
import os
import sys
import typing

from google.protobuf.message import Message

from pya2l.protobuf.API_pb2 import *
from pya2l.protobuf.API_pb2_grpc import *
from pya2l.protobuf.A2L_pb2 import *


class A2lParser(object):
    def __init__(self, port=3333, logger: logging.Logger = None):
        self._logger = logger
        if os.name == 'nt':
            shared_object = 'a2l_grpc_windows_amd64.dll'
        elif os.name == 'posix':
            if sys.platform == 'darwin':
                shared_object = 'a2l_grpc_darwin_arm64.dylib'
            else:
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
            raise Exception('server is already running')
        setattr(Message, 'properties', property(lambda e: [str(f) for f in e.DESCRIPTOR.fields_by_name]))
        setattr(Message, 'is_none',
                property(lambda e: not e.Present if 'Present' in e.properties else len(e.ListFields()) == 0))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self._dll.Close():
            raise Exception('server is not running')

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

    def tree_from_a2l(self, a2l_data: bytes) -> RootNodeType:
        """
        Converts an A2L into gRPC object.
        :param a2l_data: the A2L data to deserialize
        :return: a gRPC object
        """
        if self._logger:
            self._logger.info('start parsing A2L')
        response = self._client.GetTreeFromA2L(TreeFromA2LRequest(a2l=a2l_data))
        if self._logger:
            self._logger.info('finished parsing A2L')
        if response.error != '' and self._logger:
            self._logger.warning(response.error)
        return response.tree

    def tree_from_json(self, json_data: bytes, allow_partial: bool = False) -> RootNodeType:
        """
        Converts a JSON-formatted A2L into gRPC object.
        :param json_data: the JSON to deserialize
        :param allow_partial: allows elements that have missing required fields to serialize without returning an error
        :return: a gRPC object
        """
        if self._logger:
            self._logger.info('start parsing JSON A2L')
        response = self._client.GetTreeFromJSON(TreeFromJSONRequest(json=json_data, allow_partial=allow_partial))
        if self._logger:
            self._logger.info('finished parsing JSON A2L')
        if response.error != '' and self._logger:
            self._logger.warning(response.error)
        return response.tree

    def json_from_tree(self,
                       tree: RootNodeType,
                       indent: int = None,
                       allow_partial: bool = False,
                       emit_unpopulated: bool = False) -> bytes:
        """
        Converts a gRPC-formatted A2L into JSON.
        :param tree: the gRPC object to serialize
        :param indent: number of indentation spaces
        :param allow_partial: allows elements that have missing required fields to serialize without returning an error
        :param emit_unpopulated: emits tree's unpopulated value(s) in the JSON output
        :return: a bytes-encoded JSON
        """
        response = self._client.GetJSONFromTree(JSONFromTreeRequest(tree=tree,
                                                                    indent=indent,
                                                                    allow_partial=allow_partial,
                                                                    emit_unpopulated=emit_unpopulated))
        if response.error != '' and self._logger:
            self._logger.warning(response.error)
        return response.json

    def a2l_from_tree(self, tree: RootNodeType, sorted: bool = False, indent: int = None) -> bytes:
        """
        Converts a gRPC-formatted A2L into A2L.
        :param tree: the gRPC object to serialize
        :param sorted: sort the elements based on their unique identifier within the document
        :param indent: number of indentation spaces
        :return: a byte-encoded A2L
        """
        response = self._client.GetA2LFromTree(A2LFromTreeRequest(tree=tree, sorted=sorted, indent=indent))
        if response.error != '' and self._logger:
            self._logger.warning(response.error)
        return response.a2l
