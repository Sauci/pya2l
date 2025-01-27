from pya2l.protobuf.A2L_pb2 import RecordLayoutType
from .helpers import *
from .referencer import Referencer
from .module import Module


class RecordLayout(Referencer):
    def __init__(self, module: Module, record_layout: RecordLayoutType):
        super().__init__(module)
        self._record_layout = record_layout

    @property
    def name(self):
        return self._record_layout.Name.Value

    def _process_internal_properties(self, data_size=1) -> (str, str):
        pack = self._module.unpack_format
        meta = ''
        for record_layout_property in ('NO_AXIS_PTS_X',
                                       'NO_AXIS_PTS_Y',
                                       'NO_AXIS_PTS_Z',):
            if not getattr(self._record_layout, record_layout_property).is_none:
                p = getattr(self._record_layout, record_layout_property).Position.Value
                t = getattr(self._record_layout, record_layout_property).DataType.Value
                pack = pack[:p] + get_unpack_format_from_a2l_datatype(t) + pack[p:]
                meta = meta[:p] + 'y' + meta[p:]

        for record_layout_property in ('FNC_VALUES',
                                       'AXIS_PTS_X',
                                       'AXIS_PTS_Y',
                                       'AXIS_PTS_Z'):
            if not getattr(self._record_layout, record_layout_property).is_none:
                p = getattr(self._record_layout, record_layout_property).Position.Value
                t = getattr(self._record_layout, record_layout_property).DataType.Value
                pack = pack[:p] + get_unpack_format_from_a2l_datatype(t) * data_size + pack[p:]
                meta = meta[:p] + 'n' * data_size + meta[p:]

        return pack, meta

    def get_meta_data_indexes(self, data_size=1) -> str:
        return self._process_internal_properties(data_size=data_size)[1]

    def get_unpack_format(self, data_size=1) -> str:
        return self._process_internal_properties(data_size=data_size)[0]
