import struct
import typing

from pya2l.protobuf.A2L_pb2 import CharacteristicType
from .axis_descr import AxisDescr, axis_descr_factory
from .compu_method import CompuMethod, compu_method_factory
from .record_layout import *
from .referencer import Referencer
from .helpers import *


class Characteristic(Referencer):
    def __init__(self, module: Module, name: str):
        super().__init__(module)
        self._name = name
        self._characteristic = None

    @property
    def _a2l_characteristic(self) -> CharacteristicType:
        if self._characteristic is None:
            self._characteristic = self.get_ast_characteristic_from_module(self._module, self._name)
        return self._characteristic

    @staticmethod
    def get_ast_characteristic_from_module(module: Module, name: str) -> CharacteristicType:
        """
        Returns the CHARACTERISTIC with the specified name, in the scope of the specified module.

        :param module: the module to get the CHARACTERISTIC from
        :param name: the name of the CHARACTERISTIC to retrieve
        :return: the CHARACTERISTIC with the specified name, in the scope of the specified module
        """
        for characteristic in module.a2l_module.CHARACTERISTIC:
            if characteristic.Name.Value == name:
                return characteristic
        raise ValueError(f'CHARACTERISTIC {name} not found in MODULE {module.name}')

    @property
    def name(self) -> str:
        """
        Returns the name of this CHARACTERISTIC.

        :return: the name of this CHARACTERISTIC
        """
        return self._a2l_characteristic.Name.Value

    @property
    def address(self) -> int:
        """
        Returns the address of this CHARACTERISTIC.

        :return: the address of this CHARACTERISTIC
        """
        return self._a2l_characteristic.Address.Value

    @property
    def conversion(self) -> CompuMethod:
        """
        Returns the COMPU_METHOD of this CHARACTERISTIC.

        :return: the COMPU_METHOD of this CHARACTERISTIC
        """
        conversion = self._a2l_characteristic.Conversion.Value
        for compu_method in self._module.a2l_module.COMPU_METHOD:
            if compu_method.Name.Value == conversion:
                return compu_method_factory(self._module, compu_method)
        raise ValueError(f'COMPU_METHOD {conversion} not found in MODULE {self._module.name}')

    @property
    def record_layout(self) -> RecordLayout:
        """
        Returns the RECORD_LAYOUT of this CHARACTERISTIC.

        :return: the RECORD_LAYOUT of this CHARACTERISTIC
        """
        deposit_name = self._a2l_characteristic.Deposit.Value
        for record_layout in self._module.a2l_module.RECORD_LAYOUT:
            if record_layout.Name.Value == deposit_name:
                return RecordLayout(self._module, record_layout)
        raise ValueError(f'RECORD_LAYOUT {deposit_name} not found in MODULE {self._module.name}')

    @property
    def data_size(self) -> int:
        """
        Returns the XCP data size in bytes of this CHARACTERISTIC. This value does not include elements such as
        NO_AXIS_PTS_X/Y/Z, but only the actual data size.

        :return: the XCP data size of this CHARACTERISTIC
        """
        raise NotImplementedError

    @property
    def protocol_data_size(self) -> int:
        """
        Returns the XCP data size in bytes of this CHARACTERISTIC. This value includes elements such as NO_AXIS_PTS_X/Y/
        Z.

        :return: the XCP data size of this CHARACTERISTIC
        """
        return get_byte_size_from_unpack_format(self.unpack_format)

    @property
    def unpack_format(self) -> str:
        """
        Returns the XCP data unpacking format in the format of struct.unpack() method's parameter.

        :return: the XCP data packing format
        """
        return self.record_layout.get_unpack_format(self.data_size)

    def get_raw_values(self, data: bytearray) -> typing.Tuple[typing.Any, ...]:
        """
        Returns the raw values for this CHARACTERISTIC from the provided protocol data.

        :param data: the protocol data
        :return: the raw values for this CHARACTERISTIC
        """
        return struct.unpack(self.unpack_format, data)

    def get_physical_values(self, data: typing.Tuple[typing.Any, ...]) -> typing.Tuple[typing.Any, ...]:
        data = [d for i, d in enumerate(data) if self.record_layout.get_meta_data_indexes(self.data_size)[i] == 'n']
        return tuple(self.conversion.convert_to_physical_from_internal(d) for d in data)


class CharacteristicValue(Characteristic):

    @property
    def data_size(self) -> int:
        return 1


class CharacteristicCurve(Characteristic):

    @property
    def x_axis_descr(self) -> AxisDescr:
        return axis_descr_factory(self._module, self._a2l_characteristic.AXIS_DESCR[0])

    @property
    def data_size(self) -> int:
        return self.x_axis_descr.xcp_data_size


class CharacteristicMap(Characteristic):

    @property
    def x_axis_descr(self) -> AxisDescr:
        return axis_descr_factory(self._module, self._a2l_characteristic.AXIS_DESCR[0])

    @property
    def y_axis_descr(self) -> AxisDescr:
        return axis_descr_factory(self._module, self._a2l_characteristic.AXIS_DESCR[1])

    @property
    def data_size(self) -> int:
        return self.x_axis_descr.xcp_data_size * self.y_axis_descr.xcp_data_size


class CharacteristicCuboid(Characteristic):
    pass


class CharacteristicValBlk(Characteristic):

    @property
    def data_size(self) -> int:
        if not self._a2l_characteristic.MATRIX_DIM.is_none:
            return (self._a2l_characteristic.MATRIX_DIM.XDim.Value *
                    self._a2l_characteristic.MATRIX_DIM.YDim.Value *
                    self._a2l_characteristic.MATRIX_DIM.ZDim.Value)
        elif not self._a2l_characteristic.NUMBER.is_none:
            return self._a2l_characteristic.NUMBER.Number
        else:
            raise NotImplementedError


class CharacteristicAscii(Characteristic):
    pass


def characteristic_factory(module: Module, name: str) -> Characteristic:
    characteristic = Characteristic.get_ast_characteristic_from_module(module, name)
    return dict(VALUE=CharacteristicValue,
                CURVE=CharacteristicCurve,
                MAP=CharacteristicMap,
                CUBOID=CharacteristicCuboid,
                VAL_BLK=CharacteristicValBlk,
                ASCII=CharacteristicAscii)[characteristic.Type](module, name)
