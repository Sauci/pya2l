import math
import typing
from typing import Any

from pya2l.protobuf.A2L_pb2 import CompuMethodType, CompuTabType, CompuVTabType
from .module import Module


def sin(x):
    return math.sin(x)


def cos(x):
    return math.cos(x)


def tan(x):
    return math.tan(x)


def arcsin(x):
    return math.asin(x)


def arccos(x):
    return math.acos(x)


def arctan(x):
    return math.atan(x)


def sinh(x):
    return math.sinh(x)


def cosh(x):
    return math.cosh(x)


def tanh(x):
    return math.tanh(x)


def exp(x):
    return math.exp(x)


def ln(x):
    return math.log(x, math.e)


def log(x):
    print(x)
    return math.log(x, 10)


def sqrt(x):
    return math.sqrt(x)


class CompuMethod(object):
    def __init__(self, module: Module, compu_method: CompuMethodType):
        self._compu_method = compu_method
        self._module = module

    @property
    def a2l_compu_method(self) -> CompuMethodType:
        return self._compu_method

    @property
    def unit(self) -> str:
        return self.a2l_compu_method.Unit.Value

    @property
    def format(self) -> str:
        return self.a2l_compu_method.Format.Value

    def convert_to_physical_from_internal(self, value: Any) -> typing.Any:
        raise NotImplementedError


class CompuMethodTabIntp(CompuMethod):

    @property
    def compu_tab(self) -> CompuTabType:
        compu_tab_ref = self.a2l_compu_method.COMPU_TAB_REF.ConversionTable.Value
        for compu_tab in self._module.a2l_module.COMPU_TAB:
            if compu_tab.Name.Value == compu_tab_ref:
                return compu_tab
        raise ValueError(f'COMPU_TAB <{compu_tab_ref}> not found in MODULE <{self._module.name}>')

    def convert_to_physical_from_internal(self, value: Any) -> typing.Any:
        internal_vector = [e.InVal.Value for e in self.compu_tab.InValOutVal]
        physical_vector = [e.OutVal.Value for e in self.compu_tab.InValOutVal]

        for i in range(len(internal_vector) - 1):
            p0_internal = internal_vector[i]
            p1_internal = internal_vector[i + 1]
            p0_physical = physical_vector[i]
            p1_physical = physical_vector[i + 1]
            dy_internal = p1_internal - p0_internal
            dy_physical = p1_physical - p0_physical
            if p0_internal <= value <= p1_internal:
                return (value - p0_internal) / dy_internal * dy_physical + p0_physical
        if value < internal_vector[0]:
            return physical_vector[0]
        else:
            return physical_vector[-1]


class CompuMethodTabNoIntp(CompuMethod):
    pass


class CompuMethodTabVerb(CompuMethod):

    @property
    def compu_vtab(self) -> CompuVTabType:
        compu_tab_ref = self.a2l_compu_method.COMPU_TAB_REF.ConversionTable.Value
        for compu_vtab in self._module.a2l_module.COMPU_VTAB:
            if compu_vtab.Name.Value == compu_tab_ref:
                return compu_vtab
        raise ValueError(f'COMPU_VTAB <{compu_tab_ref}> not found in MODULE <{self._module.name}>')

    def convert_to_physical_from_internal(self, value: Any) -> typing.Any:
        for in_val_out_val in self.compu_vtab.InValOutVal:
            if in_val_out_val.InVal.Value == value:
                return in_val_out_val.OutVal.Value
        raise IndexError(f'value {value} exceeds COMPU_VTAB {self.compu_vtab.Name.Value} range')


class CompuMethodRatFunc(CompuMethod):

    def convert_to_physical_from_internal(self, value: Any) -> typing.Any:
        coeffs = self.a2l_compu_method.COEFFS
        i = value
        a = coeffs.A.Value
        b = coeffs.B.Value
        c = coeffs.C.Value
        d = coeffs.D.Value
        e = coeffs.E.Value
        f = coeffs.F.Value
        # see https://www.wolframalpha.com/input?i=solve%28i+%3D+%28a+*+p+*+p+%2B+b+*+p+%2B+c%29+%2F+%28d+*+p+*+p+%2B+e+*+p+%2B+f%29%2C+p%29
        try:
            result = -math.sqrt(pow(b - e * i, 2) - 4 * (a - d * i) * (c - f * i) - b + e * i) / (2 * (a - d * i))
        except ZeroDivisionError:
            result = (f * i - c) / (b - e * i)
        return result  # (f'{self.format}f' % result).strip()


class CompuMethodForm(CompuMethod):

    def convert_to_physical_from_internal(self, value: Any) -> typing.Any:
        formula = self.a2l_compu_method.FORMULA.FX.Value
        try:
            for i, v in enumerate(value):
                formula = formula.replace(f'X{i + 1}', str(v))
        except TypeError:
            if 'X1' in formula:
                formula = formula.replace('X1', str(value))
            elif 'X' in formula:
                formula = formula.replace('X', str(value))
        result = eval(formula.replace('^', '**').replace('XOR', '^'))
        return result


def compu_method_factory(module: Module, compu_method: CompuMethodType) -> CompuMethod:
    return dict(TAB_INTP=CompuMethodTabIntp,
                TAB_NOINTP=CompuMethodTabNoIntp,
                TAB_VERB=CompuMethodTabVerb,
                RAT_FUNC=CompuMethodRatFunc,
                FORM=CompuMethodForm)[compu_method.ConversionType](module, compu_method)
