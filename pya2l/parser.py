"""
@project: pya2l
@file: parser.py
@author: Guillaume Sottas
@date: 20.03.2018
"""
import ctypes
import logging
import os
import struct
import sys
import sysconfig
import typing
import platform

from google.protobuf.message import Message

from pya2l.protobuf.API_pb2 import *
from pya2l.protobuf.API_pb2_grpc import *
from pya2l.protobuf.A2L_pb2 import *

protocol_size_margin = 256


class A2lError(Exception):
    """raised when the backend reports an error while converting a document."""


def chunk_generator(_data: bytes, _chunk_size: int):
    """
    Generates chunks of the given size from the input data.
    :param _data: The data to be chunked.
    :param _chunk_size: Size of each chunk.
    :yield: Chunks of the specified size.
    """
    for i in range(0, len(_data), _chunk_size):
        yield _data[i : i + _chunk_size]


def get_architecture() -> str:
    # the shared object is loaded in the process of the interpreter, which means that the architecture of the
    # interpreter is the relevant one. on Windows, platform.machine() reports the architecture of the machine instead,
    # which differs from the one of the interpreter when the latter runs under emulation, as an x86-64 interpreter
    # does on an ARM64 machine. the platform the interpreter was built for is therefore used on that operating system.
    windows_architecture = {'win32': '386', 'win-amd64': 'amd64', 'win-arm32': 'arm', 'win-arm64': 'arm64'}
    build_platform = sysconfig.get_platform()
    if build_platform in windows_architecture:
        return windows_architecture[build_platform]
    machine = platform.machine().lower()
    if machine in ('x86_64', 'amd64'):
        if struct.calcsize('P') == 4:
            return '386'
        elif struct.calcsize('P') == 8:
            return 'amd64'
        else:
            raise RuntimeError('Unsupported architecture')
    elif machine in ('aarch64', 'arm64'):
        # 'aarch64' is reported on Linux, 'arm64' on macOS and Windows
        return 'arm64'
    elif machine.startswith('arm'):
        return 'arm'
    else:
        raise RuntimeError('Unsupported architecture')


class A2lParser(object):
    def __init__(self, port=0, max_msg_size=4*1024*1024, logger: logging.Logger = None):
        self._logger = logger
        self.chunk_size = max_msg_size - protocol_size_margin
        self.warnings: typing.List[str] = []
        if os.name == 'nt':
            shared_object = f'a2l_grpc_windows_{get_architecture()}.dll'
        elif os.name == 'posix':
            if sys.platform == 'darwin':
                shared_object = f'a2l_grpc_darwin_{get_architecture()}.dylib'
            else:
                shared_object = f'a2l_grpc_linux_{get_architecture()}.so'
        else:
            raise Exception(f'unsupported operating system {os.name}')
        self._dll = ctypes.cdll.LoadLibrary(
            os.path.join(os.path.dirname(__file__), 'a2l_grpc', shared_object))
        if self._dll.Create(port, max_msg_size):
            raise Exception('server is already running')
        # with a port of 0 the operating system chooses a free one, which the backend reports; this is what lets
        # several processes run a parser each without agreeing on a port
        self.port = self._dll.GetPort()
        options = [('grpc.max_receive_message_length', max_msg_size),
                   ('grpc.max_send_message_length', max_msg_size)]
        channel = grpc.insecure_channel(f'127.0.0.1:{self.port}', options=options)
        self._client = A2LStub(channel)
        setattr(Message, 'properties', property(lambda e: [str(f) for f in e.DESCRIPTOR.fields_by_name]))
        setattr(Message, 'is_none',
                property(lambda e: not e.Present if 'Present' in e.properties else len(e.ListFields()) == 0))

    def _request_generator(self,
                           request: typing.Union[TreeFromA2LRequest, JSONFromTreeRequest, A2LFromTreeRequest, TreeFromJSONRequest],
                           data: bytes,
                           **kwargs) -> typing.Union[TreeFromA2LRequest, JSONFromTreeRequest, A2LFromTreeRequest, TreeFromJSONRequest]:
        if not hasattr(request, 'DESCRIPTOR'):
            raise TypeError(f"Invalid request type: {type(request)}. Expected a gRPC protobuf request class.")

        key = next(
            (name for name, field in request.DESCRIPTOR.fields_by_name.items() if field.type == field.TYPE_BYTES),
            None
        )
        if not key:
            raise ValueError(f"No `bytes` field found for request class {request.DESCRIPTOR.name}")
        for chunk in chunk_generator(data, self.chunk_size):
            kwargs[key] = chunk
            yield request(**kwargs)

    def _add_warnings(self, warnings: typing.Iterable[str]) -> None:
        for warning in warnings:
            self.warnings.append(warning)
            if self._logger:
                self._logger.warning(warning)

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

    def tree_from_a2l(self, a2l_data: bytes, enforce_version_check: bool = False) -> RootNodeType:
        """
        Converts an A2L into gRPC object.
        :param a2l_data: the A2L data to deserialize
        :param enforce_version_check: rejects keywords requiring a newer ASAP2 version than the one declared by the
            file with ASAP2_VERSION. When disabled, such keywords are reported in the warnings property
        :return: a gRPC object
        """
        if self._logger:
            self._logger.info('start parsing A2L')

        self.warnings = []
        response_tree_data = bytearray()
        for response in self._client.GetTreeFromA2L(
                self._request_generator(TreeFromA2LRequest, a2l_data, enforce_version_check=enforce_version_check)):
            if response.HasField('error'):
                raise A2lError(response.error)

            self._add_warnings(response.warnings)

            if response.serializedTreeChunk:
                response_tree_data.extend(response.serializedTreeChunk)
            elif not response.warnings:
                # the warnings come in responses of their own, ahead of the chunks of the tree
                if self._logger:
                    self._logger.warning("Received an empty or unexpected response chunk")

        tree = RootNodeType()
        tree.ParseFromString(bytes(response_tree_data))

        if self._logger:
            self._logger.info('finished parsing A2L')

        return tree

    def tree_from_json(self, json_data: bytes, allow_partial: bool = False) -> RootNodeType:
        """
        Converts a JSON-formatted A2L into gRPC object.
        :param json_data: the JSON to deserialize
        :param allow_partial: allows elements that have missing required fields to serialize without returning an error
        :return: a gRPC object
        """
        if self._logger:
            self._logger.info('start parsing JSON A2L')

        self.warnings = []
        response_tree_data = bytearray()

        for response in self._client.GetTreeFromJSON(self._request_generator(TreeFromJSONRequest, json_data, allow_partial=allow_partial)):
            if response.HasField('error'):
                raise A2lError(response.error)

            self._add_warnings(response.warnings)

            if response.serializedTreeChunk:
                response_tree_data.extend(response.serializedTreeChunk)

        tree = RootNodeType()
        tree.ParseFromString(bytes(response_tree_data))

        if self._logger:
            self._logger.info('finished parsing JSON A2L')

        return tree

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

        if self._logger:
            self._logger.info("start streaming conversion from tree to JSON")

        tree_bytes = tree.SerializeToString()

        json_data = bytearray()
        for response in self._client.GetJSONFromTree(self._request_generator(JSONFromTreeRequest, tree_bytes, indent=indent, allow_partial=allow_partial, emit_unpopulated=emit_unpopulated)):
            if response.HasField('error'):
                raise A2lError(response.error)

            if response.json:
                json_data.extend(response.json)

        if self._logger:
            self._logger.info("finished streaming conversion from tree to JSON")

        return bytes(json_data)

    def a2l_from_tree(self, tree: RootNodeType, sorted: bool = False, indent: int = None) -> bytes:
        """
        Converts a gRPC-formatted A2L into A2L.
        :param tree: the gRPC object to serialize
        :param sorted: sort the elements based on their unique identifier within the document
        :param indent: number of indentation spaces
        :return: a byte-encoded A2L
        """
        if self._logger:
            self._logger.info("start streaming conversion from tree to A2L")

        tree_bytes = tree.SerializeToString()

        a2l_data = bytearray()
        for response in self._client.GetA2LFromTree(self._request_generator(A2LFromTreeRequest, tree_bytes, sorted=sorted, indent=indent)):
            if response.HasField('error'):
                raise A2lError(response.error)
            if response.a2l:
                a2l_data.extend(response.a2l)

        if self._logger:
            self._logger.info("finished streaming conversion from tree to A2L")

        return bytes(a2l_data)
