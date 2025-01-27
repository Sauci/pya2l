import typing

from pya2l.protobuf.A2L_pb2 import AxisDescrType
from .axis_pts import AxisPts
from .compu_method import CompuMethod, compu_method_factory
from .module import Module
from .referencer import Referencer


class AxisDescr(Referencer):
    def __init__(self, module: Module, axis_descr: AxisDescrType):
        super().__init__(module)
        self._axis_descr = axis_descr

    @property
    def axis_pts(self) -> AxisPts:
        axis_pts_ref = self._axis_descr.AXIS_PTS_REF.AxisPoints.Value
        for axis_pts in self._module.a2l_module.AXIS_PTS:
            if axis_pts.Name.Value == axis_pts_ref:
                return AxisPts(self._module, axis_pts)
        raise ValueError(f'AXIS_PTS <{axis_pts_ref}> not found in MODULE <{self._module.name}>')

    @property
    def conversion(self) -> typing.Union[CompuMethod, None]:
        conversion = self._axis_descr.Conversion.Value
        if conversion == 'NO_COMPU_METHOD':
            return None
        for compu_method in self._module.a2l_module.COMPU_METHOD:
            if compu_method.Name.Value == conversion:
                return compu_method_factory(self._module, compu_method)
        raise ValueError(f'COMPU_METHOD <{conversion}> not found in MODULE <{self._module.name}>')

    @property
    def xcp_data_size(self) -> int:
        """
        Returns the XCP data size in bytes of this AXIS_DESCR. This property is typically used to determine the number
        of data elements parameter of the XCP DOWNLOAD/UPLOAD CTOs.

        :return: the XCP data size of this AXIS_DESCR
        """
        raise NotImplementedError


class AxisDescrStd(AxisDescr):

    @property
    def xcp_data_size(self) -> int:
        return self._axis_descr.MaxAxisPoints.Value


class AxisDescrFix(AxisDescr):

    @property
    def xcp_data_size(self) -> int:
        if not self._axis_descr.FIX_AXIS_PAR.is_none:
            return self._axis_descr.FIX_AXIS_PAR.Numberapo.Value
        elif not self._axis_descr.FIX_AXIS_PAR_DIST.is_none:
            return self._axis_descr.FIX_AXIS_PAR_DIST.Numberapo.Value
        elif not self._axis_descr.FIX_AXIS_PAR_LIST.is_none:
            return len(self._axis_descr.FIX_AXIS_PAR_LIST.AxisPtsValue)
        raise ValueError(f'AXIS_DESCR malformed')


class AxisDescrCom(AxisDescrStd):

    @property
    def xcp_data_size(self) -> int:
        return self.axis_pts.max_axis_points


class AxisDescrRes(AxisDescr):

    @property
    def xcp_data_size(self) -> int:
        return self.axis_pts.max_axis_points


class AxisDescrCurve(AxisDescr):
    pass


def axis_descr_factory(module: Module, axis_descr: AxisDescrType) -> AxisDescr:
    return dict(STD_AXIS=AxisDescrStd,
                FIX_AXIS=AxisDescrFix,
                COM_AXIS=AxisDescrCom,
                RES_AXIS=AxisDescrRes,
                CURVE_AXIS=AxisDescrCurve)[axis_descr.Attribute](module, axis_descr)
