import struct
import typing

from pya2l.protobuf.A2L_pb2 import AxisPtsType
from .compu_method import CompuMethod, compu_method_factory
from .module import Module
from .record_layout import RecordLayout
from .referencer import Referencer
from .helpers import *


class AxisPts(Referencer):
    def __init__(self, module: Module, axis_pts: AxisPtsType):
        super().__init__(module)
        self._axis_pts = axis_pts

    @property
    def name(self) -> str:
        return self._axis_pts.Name.Value

    @property
    def address(self) -> int:
        return self._axis_pts.Address.Value

    @property
    def conversion(self) -> CompuMethod:
        conversion = self._axis_pts.Conversion.Value
        for compu_method in self._module.a2l_module.COMPU_METHOD:
            if compu_method.Name.Value == conversion:
                return compu_method_factory(self._module, compu_method)
        raise ValueError(f'COMPU_METHOD {conversion} not found in MODULE {self._module.name}')

    def get_raw_values(self, data: bytearray) -> typing.Tuple[typing.Any, ...]:
        """
        Returns the raw values for this AXIS_PTS from the provided protocol data.

        :param data: the protocol data
        :return: the raw values for this AXIS_PTS
        """
        return struct.unpack(self.unpack_format, data)

    @property
    def protocol_data_size(self) -> int:
        """
        Returns the XCP data size in bytes of this AXIS_PTS.

        :return: the XCP data size of this AXIS_PTS
        """
        return get_byte_size_from_unpack_format(self.unpack_format)

    def get_physical_values(self, data: typing.Tuple[typing.Any, ...]) -> typing.Tuple[typing.Any, ...]:
        data = [d for i, d in enumerate(data) if
                self.record_layout.get_meta_data_indexes(self.max_axis_points)[i] == 'n']
        return tuple(self.conversion.convert_to_physical_from_internal(d) for d in data)

    @property
    def record_layout(self) -> RecordLayout:
        deposit_name = self._axis_pts.DepositR.Value
        for record_layout in self._module.a2l_module.RECORD_LAYOUT:
            if record_layout.Name.Value == deposit_name:
                return RecordLayout(self._module, record_layout)
        raise ValueError(f'RECORD_LAYOUT {deposit_name} not found in MODULE {self._module.name}')

    @property
    def unpack_format(self) -> str:
        return self.record_layout.get_unpack_format(data_size=self.max_axis_points)

    @property
    def max_axis_points(self) -> int:
        return self._axis_pts.MaxAxisPoints.Value
