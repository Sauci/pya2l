from pya2l.protobuf.A2L_pb2 import ModuleType


class Module(object):
    def __init__(self, module: ModuleType):
        self._module = module

    @property
    def name(self) -> str:
        """
        Returns the name of this MODULE.

        :return: the name of this MODULE
        """
        return self.a2l_module.Name.Value

    @property
    def a2l_module(self) -> ModuleType:
        return self._module

    @property
    def endianness(self) -> str:
        """
        Returns the endianness of this MODULE.

        :return: the endianness of this MODULE
        """
        if not self._module.MOD_COMMON.is_none:
            if not self._module.MOD_COMMON.BYTE_ORDER.is_none:
                if self._module.MOD_COMMON.BYTE_ORDER.ByteOrder in ('MSB_FIRST', 'BIG_ENDIAN'):
                    result = 'big'
                else:
                    result = 'little'
            else:
                result = 'little'
        else:
            result = 'little'
        return result

    @property
    def unpack_format(self) -> str:
        """
        Returns the XCP data unpacking format in the format of struct.unpack() method's parameter.

        :return: the XCP data packing format
        """
        if self.endianness == 'big':
            return '>'
        else:
            return '<'
