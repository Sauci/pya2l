"""
@project: pya2l
@file: a2l_node.py
@author: Guillaume Sottas
@date: 05.04.2018
"""

from pya2l.parser.node import ASTNode, node_type
from pya2l.parser.a2l_type import *

enum_index_mode = Ident
enum_attribute = Ident
enum_type = Ident
enum_conversion_type = Ident
enum_prg_type = Ident
enum_memory_type = Ident
enum_mode = Ident
monotony_enum = Ident
enum_tag = Ident


class A2lNode(ASTNode):
    def __setattr__(self, key, value):
        if hasattr(self, key) and isinstance(getattr(self, key), String):
            value = String(value)
        return super(A2lNode, self).__setattr__(key, value)

    def dump(self, n=0):
        yield n, '/begin {node}'.format(node=self.node)
        for e in super(A2lNode, self).dump(n=n + 1):
            yield e
        yield n, '/end {node}'.format(node=self.node)


class A2lTagNode(A2lNode):
    def dump(self, n=0):
        yield n, '{node} {value}'.format(node=self.node, value=getattr(self, list(self.properties)[0]))


@node_type('a2l')
class A2lFile(A2lNode):
    __slots__ = 'asap2_version', 'a2ml_version', 'project'

    def __init__(self, args):
        self.asap2_version = None
        self.a2ml_version = None
        self.project = None
        super(A2lFile, self).__init__(*args)


@node_type('IF_DATA')
class IF_DATA(A2lNode):
    def __new__(cls, tag=None, value=None):
        cls.__slots__ = cls.__slots__ + tuple([tag])
        setattr(cls, tag, value)
        return super(IF_DATA, cls).__new__(cls)

    def __init__(self, tag=None, value=None):
        super(IF_DATA, self).__init__((tag, value))

    def dict(self):
        return dict((tag, getattr(self, tag).dict()) for tag in self.properties)

    def dump(self, n=0):
        for tag, value in ((t, getattr(self, t)) for t in self.properties):
            yield n, '/begin {node} {tag}'.format(node=self.node, tag=tag)
            for e in value.dump(n=n + 1):
                yield e
            yield n, '/end {node}'.format(node=self.node)


@node_type('A2ML')
class A2ML(A2lNode):
    def __new__(cls, a2ml):
        cls.__slots__ = tuple(['type_definition'] + list(b.tag for b in filter(lambda d: hasattr(d, 'tag'), a2ml)))
        setattr(cls, 'type_definition', list())
        for e in a2ml:
            if hasattr(e, 'tag'):
                setattr(cls, e.tag, e)
            # elif e not in getattr(cls, 'type_definition'):
            #     getattr(cls, 'type_definition').append(e)
        return super(A2ML, cls).__new__(cls)

    def __init__(self, a2ml):
        args = [('type_definition', d) for d in filter(lambda d: not hasattr(d, 'tag'), a2ml)]
        for block in filter(lambda d: hasattr(d, 'tag'), a2ml):
            args.append((block.tag, block))
        super(A2ML, self).__init__(*args)

    def dump(self, n=0):
        return (e for e in super(A2ML, self).dump(n=n))


@node_type('A2ML_VERSION')
class A2ML_VERSION(A2lNode):
    __slots__ = 'version_no', 'upgrade_no', 

    def __init__(self, version_no, upgrade_no, ):
        self.version_no = Int(version_no)
        self.upgrade_no = Int(upgrade_no)
        super(A2ML_VERSION, self).__init__()


@node_type('ADDR_EPK')
class ADDR_EPK(Long):
    def __new__(cls, address):
        return super(ADDR_EPK, cls).__new__(cls, address)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(ADDR_EPK, self).__str__())


@node_type('ALIGNMENT_BYTE')
class ALIGNMENT_BYTE(Int):
    def __new__(cls, alignment_border):
        return super(ALIGNMENT_BYTE, cls).__new__(cls, alignment_border)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(ALIGNMENT_BYTE, self).__str__())


@node_type('ALIGNMENT_FLOAT32_IEEE')
class ALIGNMENT_FLOAT32_IEEE(Int):
    def __new__(cls, alignment_border):
        return super(ALIGNMENT_FLOAT32_IEEE, cls).__new__(cls, alignment_border)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(ALIGNMENT_FLOAT32_IEEE, self).__str__())


@node_type('ALIGNMENT_FLOAT64_IEEE')
class ALIGNMENT_FLOAT64_IEEE(Int):
    def __new__(cls, alignment_border):
        return super(ALIGNMENT_FLOAT64_IEEE, cls).__new__(cls, alignment_border)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(ALIGNMENT_FLOAT64_IEEE, self).__str__())


@node_type('ALIGNMENT_LONG')
class ALIGNMENT_LONG(Int):
    def __new__(cls, alignment_border):
        return super(ALIGNMENT_LONG, cls).__new__(cls, alignment_border)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(ALIGNMENT_LONG, self).__str__())


@node_type('ALIGNMENT_WORD')
class ALIGNMENT_WORD(Int):
    def __new__(cls, alignment_border):
        return super(ALIGNMENT_WORD, cls).__new__(cls, alignment_border)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(ALIGNMENT_WORD, self).__str__())


@node_type('ANNOTATION')
class ANNOTATION(A2lNode):
    __slots__ = 'annotation_label', 'annotation_origin', 'annotation_text', 

    def __init__(self, args):
        self.annotation_label = None
        self.annotation_origin = None
        self.annotation_text = None
        super(ANNOTATION, self).__init__(*args)


@node_type('ANNOTATION_LABEL')
class ANNOTATION_LABEL(String):
    def __new__(cls, label):
        return super(ANNOTATION_LABEL, cls).__new__(cls, label)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(ANNOTATION_LABEL, self).__str__())


@node_type('ANNOTATION_ORIGIN')
class ANNOTATION_ORIGIN(String):
    def __new__(cls, origin):
        return super(ANNOTATION_ORIGIN, cls).__new__(cls, origin)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(ANNOTATION_ORIGIN, self).__str__())


@node_type('ANNOTATION_TEXT')
class ANNOTATION_TEXT(A2lNode):
    __slots__ = 'text', 

    def __init__(self, args):
        self.text = list()
        super(ANNOTATION_TEXT, self).__init__(*args)


@node_type('ARRAY_SIZE')
class ARRAY_SIZE(Int):
    def __new__(cls, number):
        return super(ARRAY_SIZE, cls).__new__(cls, number)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(ARRAY_SIZE, self).__str__())


@node_type('ASAP2_VERSION')
class ASAP2_VERSION(A2lNode):
    __slots__ = 'version_no', 'upgrade_no', 

    def __init__(self, version_no, upgrade_no, ):
        self.version_no = Int(version_no)
        self.upgrade_no = Int(upgrade_no)
        super(ASAP2_VERSION, self).__init__()


@node_type('AXIS_DESCR')
class AXIS_DESCR(A2lNode):
    __slots__ = 'attribute', 'input_quantity', 'conversion', 'max_axis_points', 'lower_limit', 'upper_limit', 'read_only', 'format', 'annotation', 'axis_pts_ref', 'max_grad', 'monotony', 'byte_order', 'extended_limits', 'fix_axis_par', 'fix_axis_par_dist', 'fix_axis_par_list', 'deposit', 'curve_axis_ref', 

    def __init__(self, attribute, input_quantity, conversion, max_axis_points, lower_limit, upper_limit, args):
        self.attribute = enum_attribute(attribute)
        self.input_quantity = Ident(input_quantity)
        self.conversion = Ident(conversion)
        self.max_axis_points = Int(max_axis_points)
        self.lower_limit = Float(lower_limit)
        self.upper_limit = Float(upper_limit)
        self.read_only = None
        self.format = None
        self.annotation = list()
        self.axis_pts_ref = None
        self.max_grad = None
        self.monotony = None
        self.byte_order = None
        self.extended_limits = None
        self.fix_axis_par = None
        self.fix_axis_par_dist = None
        self.fix_axis_par_list = None
        self.deposit = None
        self.curve_axis_ref = None
        super(AXIS_DESCR, self).__init__(*args)


@node_type('AXIS_PTS')
class AXIS_PTS(A2lNode):
    __slots__ = 'name', 'long_identifier', 'address', 'input_quantity', 'deposit', 'max_diff', 'conversion', 'max_axis_points', 'lower_limit', 'upper_limit', 'display_identifier', 'read_only', 'format', 'deposit', 'byte_order', 'function_list', 'ref_memory_segment', 'guard_rails', 'extended_limits', 'annotation', 'if_data', 'calibration_access', 'ecu_address_extension', 

    def __init__(self, name, long_identifier, address, input_quantity, deposit, max_diff, conversion, max_axis_points, lower_limit, upper_limit, args):
        self.name = Ident(name)
        self.long_identifier = String(long_identifier)
        self.address = Long(address)
        self.input_quantity = Ident(input_quantity)
        self.deposit = Ident(deposit)
        self.max_diff = Float(max_diff)
        self.conversion = Ident(conversion)
        self.max_axis_points = Int(max_axis_points)
        self.lower_limit = Float(lower_limit)
        self.upper_limit = Float(upper_limit)
        self.display_identifier = None
        self.read_only = None
        self.format = None
        self.deposit = None
        self.byte_order = None
        self.function_list = None
        self.ref_memory_segment = None
        self.guard_rails = None
        self.extended_limits = None
        self.annotation = list()
        self.if_data = dict()
        self.calibration_access = None
        self.ecu_address_extension = None
        super(AXIS_PTS, self).__init__(*args)


@node_type('AXIS_PTS_REF')
class AXIS_PTS_REF(Ident):
    def __new__(cls, axis_points):
        return super(AXIS_PTS_REF, cls).__new__(cls, axis_points)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(AXIS_PTS_REF, self).__str__())


@node_type('AXIS_PTS_X')
class AXIS_PTS_X(A2lNode):
    __slots__ = 'position', 'data_type', 'index_incr', 'addressing', 

    def __init__(self, position, data_type, index_incr, addressing, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        self.index_incr = IndexOrder(index_incr)
        self.addressing = AddrType(addressing)
        super(AXIS_PTS_X, self).__init__()


@node_type('AXIS_PTS_Y')
class AXIS_PTS_Y(A2lNode):
    __slots__ = 'position', 'data_type', 'index_incr', 'addressing', 

    def __init__(self, position, data_type, index_incr, addressing, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        self.index_incr = IndexOrder(index_incr)
        self.addressing = AddrType(addressing)
        super(AXIS_PTS_Y, self).__init__()


@node_type('AXIS_PTS_Z')
class AXIS_PTS_Z(A2lNode):
    __slots__ = 'position', 'data_type', 'index_incr', 'addressing', 

    def __init__(self, position, data_type, index_incr, addressing, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        self.index_incr = IndexOrder(index_incr)
        self.addressing = AddrType(addressing)
        super(AXIS_PTS_Z, self).__init__()


@node_type('AXIS_RESCALE_X')
class AXIS_RESCALE_X(A2lNode):
    __slots__ = 'position', 'data_type', 'max_number_of_rescale_pairs', 'index_incr', 'addressing', 

    def __init__(self, position, data_type, max_number_of_rescale_pairs, index_incr, addressing, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        self.max_number_of_rescale_pairs = Int(max_number_of_rescale_pairs)
        self.index_incr = IndexOrder(index_incr)
        self.addressing = AddrType(addressing)
        super(AXIS_RESCALE_X, self).__init__()


@node_type('AXIS_RESCALE_Y')
class AXIS_RESCALE_Y(A2lNode):
    __slots__ = 'position', 'data_type', 'max_number_of_rescale_pairs', 'index_incr', 'addressing', 

    def __init__(self, position, data_type, max_number_of_rescale_pairs, index_incr, addressing, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        self.max_number_of_rescale_pairs = Int(max_number_of_rescale_pairs)
        self.index_incr = IndexOrder(index_incr)
        self.addressing = AddrType(addressing)
        super(AXIS_RESCALE_Y, self).__init__()


@node_type('AXIS_RESCALE_Z')
class AXIS_RESCALE_Z(A2lNode):
    __slots__ = 'position', 'data_type', 'max_number_of_rescale_pairs', 'index_incr', 'addressing', 

    def __init__(self, position, data_type, max_number_of_rescale_pairs, index_incr, addressing, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        self.max_number_of_rescale_pairs = Int(max_number_of_rescale_pairs)
        self.index_incr = IndexOrder(index_incr)
        self.addressing = AddrType(addressing)
        super(AXIS_RESCALE_Z, self).__init__()


@node_type('BIT_MASK')
class BIT_MASK(Long):
    def __new__(cls, mask):
        return super(BIT_MASK, cls).__new__(cls, mask)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(BIT_MASK, self).__str__())


@node_type('BIT_OPERATION')
class BIT_OPERATION(A2lNode):
    __slots__ = 'left_shift', 'right_shift', 'sign_extend', 

    def __init__(self, args):
        self.left_shift = None
        self.right_shift = None
        self.sign_extend = None
        super(BIT_OPERATION, self).__init__(*args)


@node_type('BYTE_ORDER')
class BYTE_ORDER(ByteOrder):
    def __new__(cls, byte_order):
        return super(BYTE_ORDER, cls).__new__(cls, byte_order)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(BYTE_ORDER, self).__str__())


@node_type('CALIBRATION_ACCESS')
class CALIBRATION_ACCESS(enum_type):
    def __new__(cls, type):
        return super(CALIBRATION_ACCESS, cls).__new__(cls, type)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(CALIBRATION_ACCESS, self).__str__())


@node_type('CALIBRATION_HANDLE')
class CALIBRATION_HANDLE(A2lNode):
    __slots__ = 'handle', 

    def __init__(self, args):
        self.handle = list()
        super(CALIBRATION_HANDLE, self).__init__(*args)


@node_type('CALIBRATION_METHOD')
class CALIBRATION_METHOD(A2lNode):
    __slots__ = 'method', 'version', 'calibration_handle', 

    def __init__(self, method, version, args):
        self.method = String(method)
        self.version = Long(version)
        self.calibration_handle = list()
        super(CALIBRATION_METHOD, self).__init__(*args)


@node_type('CHARACTERISTIC')
class CHARACTERISTIC(A2lNode):
    __slots__ = 'name', 'long_identifier', 'type', 'address', 'deposit', 'max_diff', 'conversion', 'lower_limit', 'upper_limit', 'display_identifier', 'format', 'byte_order', 'bit_mask', 'function_list', 'number', 'extended_limits', 'read_only', 'guard_rails', 'map_list', 'max_refresh', 'dependent_characteristic', 'virtual_characteristic', 'ref_memory_segment', 'annotation', 'comparison_quantity', 'if_data', 'axis_descr', 'calibration_access', 'matrix_dim', 'ecu_address_extension', 

    def __init__(self, name, long_identifier, type, address, deposit, max_diff, conversion, lower_limit, upper_limit, args):
        self.name = Ident(name)
        self.long_identifier = String(long_identifier)
        self.type = enum_type(type)
        self.address = Long(address)
        self.deposit = Ident(deposit)
        self.max_diff = Float(max_diff)
        self.conversion = Ident(conversion)
        self.lower_limit = Float(lower_limit)
        self.upper_limit = Float(upper_limit)
        self.display_identifier = None
        self.format = None
        self.byte_order = None
        self.bit_mask = None
        self.function_list = None
        self.number = None
        self.extended_limits = None
        self.read_only = None
        self.guard_rails = None
        self.map_list = None
        self.max_refresh = None
        self.dependent_characteristic = None
        self.virtual_characteristic = None
        self.ref_memory_segment = None
        self.annotation = list()
        self.comparison_quantity = None
        self.if_data = dict()
        self.axis_descr = list()
        self.calibration_access = None
        self.matrix_dim = None
        self.ecu_address_extension = None
        super(CHARACTERISTIC, self).__init__(*args)


@node_type('COEFFS')
class COEFFS(A2lNode):
    __slots__ = 'a', 'b', 'c', 'd', 'e', 'f', 

    def __init__(self, a, b, c, d, e, f, ):
        self.a = Float(a)
        self.b = Float(b)
        self.c = Float(c)
        self.d = Float(d)
        self.e = Float(e)
        self.f = Float(f)
        super(COEFFS, self).__init__()


@node_type('COMPARISON_QUANTITY')
class COMPARISON_QUANTITY(Ident):
    def __new__(cls, name):
        return super(COMPARISON_QUANTITY, cls).__new__(cls, name)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(COMPARISON_QUANTITY, self).__str__())


@node_type('COMPU_METHOD')
class COMPU_METHOD(A2lNode):
    __slots__ = 'name', 'long_identifier', 'conversion_type', 'format', 'unit', 'formula', 'coeffs', 'compu_tab_ref', 'ref_unit', 

    def __init__(self, name, long_identifier, conversion_type, format, unit, args):
        self.name = Ident(name)
        self.long_identifier = String(long_identifier)
        self.conversion_type = enum_conversion_type(conversion_type)
        self.format = String(format)
        self.unit = String(unit)
        self.formula = None
        self.coeffs = None
        self.compu_tab_ref = None
        self.ref_unit = None
        super(COMPU_METHOD, self).__init__(*args)


@node_type('COMPU_TAB')
class COMPU_TAB(A2lNode):
    __slots__ = 'name', 'long_identifier', 'conversion_type', 'number_value_pair', 'in_val_out_val', 'default_value', 

    def __init__(self, name, long_identifier, conversion_type, number_value_pair, args):
        self.name = Ident(name)
        self.long_identifier = String(long_identifier)
        self.conversion_type = enum_conversion_type(conversion_type)
        self.number_value_pair = Int(number_value_pair)
        self.in_val_out_val = list()  # TODO: change in_val_out_val by value_pair...
        self.default_value = None
        super(COMPU_TAB, self).__init__(*args)


@node_type('COMPU_TAB_REF')
class COMPU_TAB_REF(Ident):
    def __new__(cls, conversion_table):
        return super(COMPU_TAB_REF, cls).__new__(cls, conversion_table)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(COMPU_TAB_REF, self).__str__())


@node_type('COMPU_VTAB')
class COMPU_VTAB(A2lNode):
    __slots__ = 'name', 'long_identifier', 'conversion_type', 'number_value_pair', 'in_val_out_val', 'default_value', 

    def __init__(self, name, long_identifier, conversion_type, number_value_pair, args):
        self.name = Ident(name)
        self.long_identifier = String(long_identifier)
        self.conversion_type = enum_conversion_type(conversion_type)
        self.number_value_pair = Int(number_value_pair)
        self.in_val_out_val = list()  # TODO: change in_val_out_val by value_pair...
        self.default_value = None
        super(COMPU_VTAB, self).__init__(*args)


@node_type('COMPU_VTAB_RANGE')
class COMPU_VTAB_RANGE(A2lNode):
    __slots__ = 'name', 'long_identifier', 'number_value_triple', 'in_val_out_val', 'default_value', 

    def __init__(self, name, long_identifier, number_value_triple, args):
        self.name = Ident(name)
        self.long_identifier = String(long_identifier)
        self.number_value_triple = Int(number_value_triple)
        self.in_val_out_val = list()  # TODO: change in_val_out_val by value_pair...
        self.default_value = None
        super(COMPU_VTAB_RANGE, self).__init__(*args)


@node_type('CPU_TYPE')
class CPU_TYPE(String):
    def __new__(cls, cpu_identifier):
        return super(CPU_TYPE, cls).__new__(cls, cpu_identifier)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(CPU_TYPE, self).__str__())


@node_type('CURVE_AXIS_REF')
class CURVE_AXIS_REF(Ident):
    def __new__(cls, curve_axis):
        return super(CURVE_AXIS_REF, cls).__new__(cls, curve_axis)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(CURVE_AXIS_REF, self).__str__())


@node_type('CUSTOMER')
class CUSTOMER(String):
    def __new__(cls, customer):
        return super(CUSTOMER, cls).__new__(cls, customer)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(CUSTOMER, self).__str__())


@node_type('CUSTOMER_NO')
class CUSTOMER_NO(String):
    def __new__(cls, number):
        return super(CUSTOMER_NO, cls).__new__(cls, number)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(CUSTOMER_NO, self).__str__())


@node_type('DATA_SIZE')
class DATA_SIZE(Int):
    def __new__(cls, size):
        return super(DATA_SIZE, cls).__new__(cls, size)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(DATA_SIZE, self).__str__())


@node_type('DEFAULT_VALUE')
class DEFAULT_VALUE(String):
    def __new__(cls, display_string):
        return super(DEFAULT_VALUE, cls).__new__(cls, display_string)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(DEFAULT_VALUE, self).__str__())


@node_type('DEF_CHARACTERISTIC')
class DEF_CHARACTERISTIC(A2lNode):
    __slots__ = 'identifier', 

    def __init__(self, args):
        self.identifier = list()
        super(DEF_CHARACTERISTIC, self).__init__(*args)


@node_type('DEPENDENT_CHARACTERISTIC')
class DEPENDENT_CHARACTERISTIC(A2lNode):
    __slots__ = 'formula', 'characteristic', 

    def __init__(self, formula, args):
        self.formula = String(formula)
        self.characteristic = list()  # TODO: defined as (Characteristic)* in specification, one or more?
        super(DEPENDENT_CHARACTERISTIC, self).__init__(*args)


@node_type('DEPOSIT')
class DEPOSIT(enum_mode):
    def __new__(cls, mode):
        return super(DEPOSIT, cls).__new__(cls, mode)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(DEPOSIT, self).__str__())


@node_type('DISPLAY_IDENTIFIER')
class DISPLAY_IDENTIFIER(Ident):
    def __new__(cls, display_name):
        return super(DISPLAY_IDENTIFIER, cls).__new__(cls, display_name)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(DISPLAY_IDENTIFIER, self).__str__())


@node_type('DIST_OP_X')
class DIST_OP_X(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(DIST_OP_X, self).__init__()


@node_type('DIST_OP_Y')
class DIST_OP_Y(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(DIST_OP_Y, self).__init__()


@node_type('DIST_OP_Z')
class DIST_OP_Z(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(DIST_OP_Z, self).__init__()


@node_type('ECU')
class ECU(String):
    def __new__(cls, control_unit):
        return super(ECU, cls).__new__(cls, control_unit)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(ECU, self).__str__())


@node_type('ECU_ADDRESS')
class ECU_ADDRESS(Long):
    def __new__(cls, address):
        return super(ECU_ADDRESS, cls).__new__(cls, address)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(ECU_ADDRESS, self).__str__())


@node_type('ECU_ADDRESS_EXTENSION')
class ECU_ADDRESS_EXTENSION(Int):
    def __new__(cls, extension):
        return super(ECU_ADDRESS_EXTENSION, cls).__new__(cls, extension)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(ECU_ADDRESS_EXTENSION, self).__str__())


@node_type('ECU_CALIBRATION_OFFSET')
class ECU_CALIBRATION_OFFSET(Long):
    def __new__(cls, offset):
        return super(ECU_CALIBRATION_OFFSET, cls).__new__(cls, offset)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(ECU_CALIBRATION_OFFSET, self).__str__())


@node_type('EPK')
class EPK(String):
    def __new__(cls, identifier):
        return super(EPK, cls).__new__(cls, identifier)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(EPK, self).__str__())


@node_type('ERROR_MASK')
class ERROR_MASK(Long):
    def __new__(cls, mask):
        return super(ERROR_MASK, cls).__new__(cls, mask)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(ERROR_MASK, self).__str__())


@node_type('EXTENDED_LIMITS')
class EXTENDED_LIMITS(A2lNode):
    __slots__ = 'lower_limit', 'upper_limit', 

    def __init__(self, lower_limit, upper_limit, ):
        self.lower_limit = Float(lower_limit)
        self.upper_limit = Float(upper_limit)
        super(EXTENDED_LIMITS, self).__init__()


@node_type('FIX_AXIS_PAR')
class FIX_AXIS_PAR(A2lNode):
    __slots__ = 'offset', 'shift', 'numberapo', 

    def __init__(self, offset, shift, numberapo, ):
        self.offset = Int(offset)
        self.shift = Int(shift)
        self.numberapo = Int(numberapo)
        super(FIX_AXIS_PAR, self).__init__()


@node_type('FIX_AXIS_PAR_DIST')
class FIX_AXIS_PAR_DIST(A2lNode):
    __slots__ = 'offset', 'distance', 'numberapo', 

    def __init__(self, offset, distance, numberapo, ):
        self.offset = Int(offset)
        self.distance = Int(distance)
        self.numberapo = Int(numberapo)
        super(FIX_AXIS_PAR_DIST, self).__init__()


@node_type('FIX_AXIS_PAR_LIST')
class FIX_AXIS_PAR_LIST(A2lNode):
    __slots__ = 'axis_pts_value', 

    def __init__(self, args):
        self.axis_pts_value = list()
        super(FIX_AXIS_PAR_LIST, self).__init__(*args)


@node_type('FIX_NO_AXIS_PTS_X')
class FIX_NO_AXIS_PTS_X(Int):
    def __new__(cls, number_of_axis_points):
        return super(FIX_NO_AXIS_PTS_X, cls).__new__(cls, number_of_axis_points)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(FIX_NO_AXIS_PTS_X, self).__str__())


@node_type('FIX_NO_AXIS_PTS_Y')
class FIX_NO_AXIS_PTS_Y(Int):
    def __new__(cls, number_of_axis_points):
        return super(FIX_NO_AXIS_PTS_Y, cls).__new__(cls, number_of_axis_points)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(FIX_NO_AXIS_PTS_Y, self).__str__())


@node_type('FIX_NO_AXIS_PTS_Z')
class FIX_NO_AXIS_PTS_Z(Int):
    def __new__(cls, number_of_axis_points):
        return super(FIX_NO_AXIS_PTS_Z, cls).__new__(cls, number_of_axis_points)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(FIX_NO_AXIS_PTS_Z, self).__str__())


@node_type('FNC_VALUES')
class FNC_VALUES(A2lNode):
    __slots__ = 'position', 'data_type', 'index_mode', 'addr_type', 

    def __init__(self, position, data_type, index_mode, addr_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        self.index_mode = enum_index_mode(index_mode)
        self.addr_type = AddrType(addr_type)
        super(FNC_VALUES, self).__init__()


@node_type('FORMAT')
class FORMAT(String):
    def __new__(cls, format_string):
        return super(FORMAT, cls).__new__(cls, format_string)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(FORMAT, self).__str__())


@node_type('FORMULA')
class FORMULA(A2lNode):
    __slots__ = 'f', 'formula_inv', 

    def __init__(self, f, args):
        self.f = String(f)
        self.formula_inv = None
        super(FORMULA, self).__init__(*args)


@node_type('FORMULA_INV')
class FORMULA_INV(String):
    def __new__(cls, function):
        return super(FORMULA_INV, cls).__new__(cls, function)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(FORMULA_INV, self).__str__())


@node_type('FRAME')
class FRAME(A2lNode):
    __slots__ = 'name', 'long_identifier', 'scaling_unit', 'rate', 'frame_measurement', 'if_data', 

    def __init__(self, name, long_identifier, scaling_unit, rate, args):
        self.name = Ident(name)
        self.long_identifier = String(long_identifier)
        self.scaling_unit = Int(scaling_unit)
        self.rate = Long(rate)
        self.frame_measurement = None
        self.if_data = dict()
        super(FRAME, self).__init__(*args)


@node_type('FRAME_MEASUREMENT')
class FRAME_MEASUREMENT(A2lNode):
    __slots__ = 'identifier', 

    def __init__(self, args):
        self.identifier = list()
        super(FRAME_MEASUREMENT, self).__init__(*args)


@node_type('FUNCTION')
class FUNCTION(A2lNode):
    __slots__ = 'name', 'long_identifier', 'annotation', 'def_characteristic', 'ref_characteristic', 'in_measurement', 'out_measurement', 'loc_measurement', 'sub_function', 'function_version', 

    def __init__(self, name, long_identifier, args):
        self.name = Ident(name)
        self.long_identifier = String(long_identifier)
        self.annotation = list()
        self.def_characteristic = None
        self.ref_characteristic = None
        self.in_measurement = None
        self.out_measurement = None
        self.loc_measurement = None
        self.sub_function = None
        self.function_version = None
        super(FUNCTION, self).__init__(*args)


@node_type('FUNCTION_LIST')
class FUNCTION_LIST(A2lNode):
    __slots__ = 'name', 

    def __init__(self, args):
        self.name = list()
        super(FUNCTION_LIST, self).__init__(*args)


@node_type('FUNCTION_VERSION')
class FUNCTION_VERSION(String):
    def __new__(cls, version_identifier):
        return super(FUNCTION_VERSION, cls).__new__(cls, version_identifier)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(FUNCTION_VERSION, self).__str__())


@node_type('GROUP')
class GROUP(A2lNode):
    __slots__ = 'group_name', 'group_long_identifier', 'annotation', 'root', 'ref_characteristic', 'ref_measurement', 'function_list', 'sub_group', 

    def __init__(self, group_name, group_long_identifier, args):
        self.group_name = Ident(group_name)
        self.group_long_identifier = String(group_long_identifier)
        self.annotation = list()
        self.root = None
        self.ref_characteristic = None
        self.ref_measurement = None
        self.function_list = None
        self.sub_group = None
        super(GROUP, self).__init__(*args)


@node_type('GUARD_RAILS')
class GUARD_RAILS(ConstString):
    pass


@node_type('HEADER')
class HEADER(A2lNode):
    __slots__ = 'comment', 'version', 'project_no', 

    def __init__(self, comment, args):
        self.comment = String(comment)
        self.version = None
        self.project_no = None
        super(HEADER, self).__init__(*args)


@node_type('IDENTIFICATION')
class IDENTIFICATION(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(IDENTIFICATION, self).__init__()


@node_type('IN_MEASUREMENT')
class IN_MEASUREMENT(A2lNode):
    __slots__ = 'identifier', 

    def __init__(self, args):
        self.identifier = list()
        super(IN_MEASUREMENT, self).__init__(*args)


@node_type('LEFT_SHIFT')
class LEFT_SHIFT(Long):
    def __new__(cls, bit_count):
        return super(LEFT_SHIFT, cls).__new__(cls, bit_count)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(LEFT_SHIFT, self).__str__())


@node_type('LOC_MEASUREMENT')
class LOC_MEASUREMENT(A2lNode):
    __slots__ = 'identifier', 

    def __init__(self, args):
        self.identifier = list()
        super(LOC_MEASUREMENT, self).__init__(*args)


@node_type('MAP_LIST')
class MAP_LIST(A2lNode):
    __slots__ = 'name', 

    def __init__(self, args):
        self.name = list()
        super(MAP_LIST, self).__init__(*args)


@node_type('MATRIX_DIM')
class MATRIX_DIM(A2lNode):
    __slots__ = 'x', 'y', 'z', 

    def __init__(self, x, y, z, ):
        self.x = Int(x)
        self.y = Int(y)
        self.z = Int(z)
        super(MATRIX_DIM, self).__init__()


@node_type('MAX_GRAD')
class MAX_GRAD(Float):
    def __new__(cls, max_gradient):
        return super(MAX_GRAD, cls).__new__(cls, max_gradient)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(MAX_GRAD, self).__str__())


@node_type('MAX_REFRESH')
class MAX_REFRESH(A2lNode):
    __slots__ = 'scaling_unit', 'rate', 

    def __init__(self, scaling_unit, rate, ):
        self.scaling_unit = Int(scaling_unit)
        self.rate = Long(rate)
        super(MAX_REFRESH, self).__init__()


@node_type('MEASUREMENT')
class MEASUREMENT(A2lNode):
    __slots__ = 'name', 'long_identifier', 'data_type', 'conversion', 'resolution', 'accuracy', 'lower_limit', 'upper_limit', 'display_identifier', 'read_write', 'format', 'array_size', 'bit_mask', 'bit_operation', 'byte_order', 'max_refresh', 'virtual', 'function_list', 'ecu_address', 'error_mask', 'ref_memory_segment', 'annotation', 'if_data', 'matrix_dim', 'ecu_address_extension', 

    def __init__(self, name, long_identifier, data_type, conversion, resolution, accuracy, lower_limit, upper_limit, args):
        self.name = Ident(name)
        self.long_identifier = String(long_identifier)
        self.data_type = DataType(data_type)
        self.conversion = Ident(conversion)
        self.resolution = Int(resolution)
        self.accuracy = Float(accuracy)
        self.lower_limit = Float(lower_limit)
        self.upper_limit = Float(upper_limit)
        self.display_identifier = None
        self.read_write = None
        self.format = None
        self.array_size = None
        self.bit_mask = None
        self.bit_operation = None
        self.byte_order = None
        self.max_refresh = None
        self.virtual = None
        self.function_list = None
        self.ecu_address = None
        self.error_mask = None
        self.ref_memory_segment = None
        self.annotation = list()
        self.if_data = dict()
        self.matrix_dim = None
        self.ecu_address_extension = None
        super(MEASUREMENT, self).__init__(*args)


@node_type('MEMORY_LAYOUT')
class MEMORY_LAYOUT(A2lNode):
    __slots__ = 'prg_type', 'address', 'size', 'offset', 'if_data', 

    def __init__(self, prg_type, address, size, offset, args):
        self.prg_type = enum_prg_type(prg_type)
        self.address = Long(address)
        self.size = Long(size)
        self.offset = list(offset)
        self.if_data = dict()
        super(MEMORY_LAYOUT, self).__init__(*args)


@node_type('MEMORY_SEGMENT')
class MEMORY_SEGMENT(A2lNode):
    __slots__ = 'name', 'long_identifier', 'prg_type', 'memory_type', 'attribute', 'address', 'size', 'offset', 'if_data', 

    def __init__(self, name, long_identifier, prg_type, memory_type, attribute, address, size, offset, args):
        self.name = Ident(name)
        self.long_identifier = String(long_identifier)
        self.prg_type = enum_prg_type(prg_type)
        self.memory_type = enum_memory_type(memory_type)
        self.attribute = enum_attribute(attribute)
        self.address = Long(address)
        self.size = Long(size)
        self.offset = list(offset)
        self.if_data = dict()
        super(MEMORY_SEGMENT, self).__init__(*args)


@node_type('MODULE')
class MODULE(A2lNode):
    __slots__ = 'name', 'long_identifier', 'a2ml', 'mod_par', 'mod_common', 'if_data', 'characteristic', 'axis_pts', 'measurement', 'compu_method', 'compu_tab', 'compu_vtab', 'compu_vtab_range', 'function', 'group', 'record_layout', 'variant_coding', 'frame', 'user_rights', 'unit', 

    def __init__(self, name, long_identifier, args):
        self.name = Ident(name)
        self.long_identifier = String(long_identifier)
        self.a2ml = None
        self.mod_par = None
        self.mod_common = None
        self.if_data = dict()
        self.characteristic = list()
        self.axis_pts = list()
        self.measurement = list()
        self.compu_method = list()
        self.compu_tab = list()
        self.compu_vtab = list()
        self.compu_vtab_range = list()
        self.function = list()
        self.group = list()
        self.record_layout = list()
        self.variant_coding = None
        self.frame = None
        self.user_rights = list()
        self.unit = list()
        super(MODULE, self).__init__(*args)


@node_type('MOD_COMMON')
class MOD_COMMON(A2lNode):
    __slots__ = 'comment', 's_rec_layout', 'deposit', 'byte_order', 'data_size', 'alignment_byte', 'alignment_word', 'alignment_long', 'alignment_float32_ieee', 'alignment_float64_ieee', 

    def __init__(self, comment, args):
        self.comment = String(comment)
        self.s_rec_layout = None
        self.deposit = None
        self.byte_order = None
        self.data_size = None
        self.alignment_byte = None
        self.alignment_word = None
        self.alignment_long = None
        self.alignment_float32_ieee = None
        self.alignment_float64_ieee = None
        super(MOD_COMMON, self).__init__(*args)


@node_type('MOD_PAR')
class MOD_PAR(A2lNode):
    __slots__ = 'comment', 'version', 'addr_epk', 'epk', 'supplier', 'customer', 'customer_no', 'user', 'phone_no', 'ecu', 'cpu_type', 'no_of_interfaces', 'ecu_calibration_offset', 'calibration_method', 'memory_layout', 'memory_segment', 'system_constant', 

    def __init__(self, comment, args):
        self.comment = String(comment)
        self.version = None
        self.addr_epk = list()
        self.epk = None
        self.supplier = None
        self.customer = None
        self.customer_no = None
        self.user = None
        self.phone_no = None
        self.ecu = None
        self.cpu_type = None
        self.no_of_interfaces = None
        self.ecu_calibration_offset = None
        self.calibration_method = list()
        self.memory_layout = list()
        self.memory_segment = list()
        self.system_constant = list()
        super(MOD_PAR, self).__init__(*args)


@node_type('MONOTONY')
class MONOTONY(monotony_enum):
    def __new__(cls, monotony):
        return super(MONOTONY, cls).__new__(cls, monotony)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(MONOTONY, self).__str__())


@node_type('NO_AXIS_PTS_X')
class NO_AXIS_PTS_X(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(NO_AXIS_PTS_X, self).__init__()


@node_type('NO_AXIS_PTS_Y')
class NO_AXIS_PTS_Y(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(NO_AXIS_PTS_Y, self).__init__()


@node_type('NO_AXIS_PTS_Z')
class NO_AXIS_PTS_Z(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(NO_AXIS_PTS_Z, self).__init__()


@node_type('NO_OF_INTERFACES')
class NO_OF_INTERFACES(Int):
    def __new__(cls, number_of_interfaces):
        return super(NO_OF_INTERFACES, cls).__new__(cls, number_of_interfaces)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(NO_OF_INTERFACES, self).__str__())


@node_type('NO_RESCALE_X')
class NO_RESCALE_X(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(NO_RESCALE_X, self).__init__()


@node_type('NO_RESCALE_Y')
class NO_RESCALE_Y(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(NO_RESCALE_Y, self).__init__()


@node_type('NO_RESCALE_Z')
class NO_RESCALE_Z(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(NO_RESCALE_Z, self).__init__()


@node_type('NUMBER')
class NUMBER(Int):
    def __new__(cls, number):
        return super(NUMBER, cls).__new__(cls, number)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(NUMBER, self).__str__())


@node_type('OFFSET_X')
class OFFSET_X(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(OFFSET_X, self).__init__()


@node_type('OFFSET_Y')
class OFFSET_Y(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(OFFSET_Y, self).__init__()


@node_type('OFFSET_Z')
class OFFSET_Z(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(OFFSET_Z, self).__init__()


@node_type('OUT_MEASUREMENT')
class OUT_MEASUREMENT(A2lNode):
    __slots__ = 'identifier', 

    def __init__(self, args):
        self.identifier = list()
        super(OUT_MEASUREMENT, self).__init__(*args)


@node_type('PHONE_NO')
class PHONE_NO(String):
    def __new__(cls, phone_number):
        return super(PHONE_NO, cls).__new__(cls, phone_number)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(PHONE_NO, self).__str__())


@node_type('PROJECT')
class PROJECT(A2lNode):
    __slots__ = 'name', 'long_identifier', 'header', 'module', 

    def __init__(self, name, long_identifier, args):
        self.name = Ident(name)
        self.long_identifier = String(long_identifier)
        self.header = None
        self.module = list()
        super(PROJECT, self).__init__(*args)


@node_type('PROJECT_NO')
class PROJECT_NO(Ident):
    def __new__(cls, project_number):
        return super(PROJECT_NO, cls).__new__(cls, project_number)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(PROJECT_NO, self).__str__())


@node_type('READ_ONLY')
class READ_ONLY(ConstString):
    pass


@node_type('READ_WRITE')
class READ_WRITE(ConstString):
    pass


@node_type('RECORD_LAYOUT')
class RECORD_LAYOUT(A2lNode):
    __slots__ = 'name', 'fnc_values', 'identification', 'axis_pts_x', 'axis_pts_y', 'axis_pts_z', 'axis_rescale_x', 'axis_rescale_y', 'axis_rescale_z', 'no_axis_pts_x', 'no_axis_pts_y', 'no_axis_pts_z', 'no_rescale_x', 'no_rescale_y', 'no_rescale_z', 'fix_no_axis_pts_x', 'fix_no_axis_pts_y', 'fix_no_axis_pts_z', 'src_addr_x', 'src_addr_y', 'src_addr_z', 'rip_addr_x', 'rip_addr_y', 'rip_addr_z', 'rip_addr_w', 'shift_op_x', 'shift_op_y', 'shift_op_z', 'offset_x', 'offset_y', 'offset_z', 'dist_op_x', 'dist_op_y', 'dist_op_z', 'alignment_byte', 'alignment_word', 'alignment_long', 'alignment_float32_ieee', 'alignment_float64_ieee', 'reserved', 

    def __init__(self, name, args):
        self.name = Ident(name)
        self.fnc_values = None
        self.identification = None
        self.axis_pts_x = None
        self.axis_pts_y = None
        self.axis_pts_z = None
        self.axis_rescale_x = None
        self.axis_rescale_y = None
        self.axis_rescale_z = None
        self.no_axis_pts_x = None
        self.no_axis_pts_y = None
        self.no_axis_pts_z = None
        self.no_rescale_x = None
        self.no_rescale_y = None
        self.no_rescale_z = None
        self.fix_no_axis_pts_x = None
        self.fix_no_axis_pts_y = None
        self.fix_no_axis_pts_z = None
        self.src_addr_x = None
        self.src_addr_y = None
        self.src_addr_z = None
        self.rip_addr_x = None
        self.rip_addr_y = None
        self.rip_addr_z = None
        self.rip_addr_w = None
        self.shift_op_x = None
        self.shift_op_y = None
        self.shift_op_z = None
        self.offset_x = None
        self.offset_y = None
        self.offset_z = None
        self.dist_op_x = None
        self.dist_op_y = None
        self.dist_op_z = None
        self.alignment_byte = None
        self.alignment_word = None
        self.alignment_long = None
        self.alignment_float32_ieee = None
        self.alignment_float64_ieee = None
        self.reserved = list()
        super(RECORD_LAYOUT, self).__init__(*args)


@node_type('REF_CHARACTERISTIC')
class REF_CHARACTERISTIC(A2lNode):
    __slots__ = 'identifier', 

    def __init__(self, args):
        self.identifier = list()
        super(REF_CHARACTERISTIC, self).__init__(*args)


@node_type('REF_GROUP')
class REF_GROUP(A2lNode):
    __slots__ = 'identifier', 

    def __init__(self, args):
        self.identifier = list()
        super(REF_GROUP, self).__init__(*args)


@node_type('REF_MEASUREMENT')
class REF_MEASUREMENT(A2lNode):
    __slots__ = 'identifier', 

    def __init__(self, args):
        self.identifier = list()
        super(REF_MEASUREMENT, self).__init__(*args)


@node_type('REF_MEMORY_SEGMENT')
class REF_MEMORY_SEGMENT(Ident):
    def __new__(cls, name):
        return super(REF_MEMORY_SEGMENT, cls).__new__(cls, name)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(REF_MEMORY_SEGMENT, self).__str__())


@node_type('REF_UNIT')
class REF_UNIT(Ident):
    def __new__(cls, unit):
        return super(REF_UNIT, cls).__new__(cls, unit)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(REF_UNIT, self).__str__())


@node_type('RESERVED')
class RESERVED(A2lNode):
    __slots__ = 'position', 'data_size', 

    def __init__(self, position, data_size, ):
        self.position = Int(position)
        self.data_size = DataSize(data_size)
        super(RESERVED, self).__init__()


@node_type('RIGHT_SHIFT')
class RIGHT_SHIFT(Long):
    def __new__(cls, bit_count):
        return super(RIGHT_SHIFT, cls).__new__(cls, bit_count)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(RIGHT_SHIFT, self).__str__())


@node_type('RIP_ADDR_W')
class RIP_ADDR_W(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(RIP_ADDR_W, self).__init__()


@node_type('RIP_ADDR_X')
class RIP_ADDR_X(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(RIP_ADDR_X, self).__init__()


@node_type('RIP_ADDR_Y')
class RIP_ADDR_Y(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(RIP_ADDR_Y, self).__init__()


@node_type('RIP_ADDR_Z')
class RIP_ADDR_Z(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(RIP_ADDR_Z, self).__init__()


@node_type('ROOT')
class ROOT(ConstString):
    pass


@node_type('SHIFT_OP_X')
class SHIFT_OP_X(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(SHIFT_OP_X, self).__init__()


@node_type('SHIFT_OP_Y')
class SHIFT_OP_Y(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(SHIFT_OP_Y, self).__init__()


@node_type('SHIFT_OP_Z')
class SHIFT_OP_Z(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(SHIFT_OP_Z, self).__init__()


@node_type('SIGN_EXTEND')
class SIGN_EXTEND(ConstString):
    pass


@node_type('SI_EXPONENTS')
class SI_EXPONENTS(A2lNode):
    __slots__ = 'length', 'mass', 'time', 'electric_current', 'temperature', 'amount_of_substance', 'luminous_intensity', 

    def __init__(self, length, mass, time, electric_current, temperature, amount_of_substance, luminous_intensity, ):
        self.length = Int(length)
        self.mass = Int(mass)
        self.time = Int(time)
        self.electric_current = Int(electric_current)
        self.temperature = Int(temperature)
        self.amount_of_substance = Int(amount_of_substance)
        self.luminous_intensity = Int(luminous_intensity)
        super(SI_EXPONENTS, self).__init__()


@node_type('SRC_ADDR_X')
class SRC_ADDR_X(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(SRC_ADDR_X, self).__init__()


@node_type('SRC_ADDR_Y')
class SRC_ADDR_Y(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(SRC_ADDR_Y, self).__init__()


@node_type('SRC_ADDR_Z')
class SRC_ADDR_Z(A2lNode):
    __slots__ = 'position', 'data_type', 

    def __init__(self, position, data_type, ):
        self.position = Int(position)
        self.data_type = DataType(data_type)
        super(SRC_ADDR_Z, self).__init__()


@node_type('SUB_FUNCTION')
class SUB_FUNCTION(A2lNode):
    __slots__ = 'identifier', 

    def __init__(self, args):
        self.identifier = list()
        super(SUB_FUNCTION, self).__init__(*args)


@node_type('SUB_GROUP')
class SUB_GROUP(A2lNode):
    __slots__ = 'identifier', 

    def __init__(self, args):
        self.identifier = list()
        super(SUB_GROUP, self).__init__(*args)


@node_type('SUPPLIER')
class SUPPLIER(String):
    def __new__(cls, manufacturer):
        return super(SUPPLIER, cls).__new__(cls, manufacturer)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(SUPPLIER, self).__str__())


@node_type('SYSTEM_CONSTANT')
class SYSTEM_CONSTANT(A2lNode):
    __slots__ = 'name', 'value', 

    def __init__(self, name, value, ):
        self.name = String(name)
        self.value = String(value)
        super(SYSTEM_CONSTANT, self).__init__()


@node_type('S_REC_LAYOUT')
class S_REC_LAYOUT(Ident):
    def __new__(cls, name):
        return super(S_REC_LAYOUT, cls).__new__(cls, name)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(S_REC_LAYOUT, self).__str__())


@node_type('UNIT')
class UNIT(A2lNode):
    __slots__ = 'name', 'long_identifier', 'display', 'type', 'si_exponents', 'ref_unit', 'unit_conversion', 

    def __init__(self, name, long_identifier, display, type, args):
        self.name = Ident(name)
        self.long_identifier = String(long_identifier)
        self.display = String(display)
        self.type = enum_type(type)
        self.si_exponents = None
        self.ref_unit = None
        self.unit_conversion = None
        super(UNIT, self).__init__(*args)


@node_type('UNIT_CONVERSION')
class UNIT_CONVERSION(A2lNode):
    __slots__ = 'gradient', 'offset', 

    def __init__(self, gradient, offset, ):
        self.gradient = Float(gradient)
        self.offset = Float(offset)
        super(UNIT_CONVERSION, self).__init__()


@node_type('USER')
class USER(String):
    def __new__(cls, user_name):
        return super(USER, cls).__new__(cls, user_name)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(USER, self).__str__())


@node_type('USER_RIGHTS')
class USER_RIGHTS(A2lNode):
    __slots__ = 'user_level_id', 'ref_group', 'read_only', 

    def __init__(self, user_level_id, args):
        self.user_level_id = Ident(user_level_id)
        self.ref_group = list()
        self.read_only = None
        super(USER_RIGHTS, self).__init__(*args)


@node_type('VARIANT_CODING')
class VARIANT_CODING(A2lNode):
    __slots__ = 'var_separator', 'var_naming', 'var_criterion', 'var_forbidden_comb', 'var_characteristic', 

    def __init__(self, args):
        self.var_separator = None
        self.var_naming = None
        self.var_criterion = list()
        self.var_forbidden_comb = list()
        self.var_characteristic = list()
        super(VARIANT_CODING, self).__init__(*args)


@node_type('VAR_ADDRESS')
class VAR_ADDRESS(A2lNode):
    __slots__ = 'address', 

    def __init__(self, args):
        self.address = list()
        super(VAR_ADDRESS, self).__init__(*args)


@node_type('VAR_CHARACTERISTIC')
class VAR_CHARACTERISTIC(A2lNode):
    __slots__ = 'name', 'criterion_name', 'var_address', 

    def __init__(self, name, args):
        self.name = Ident(name)
        self.criterion_name = list()
        self.var_address = None
        super(VAR_CHARACTERISTIC, self).__init__(*args)


@node_type('VAR_CRITERION')
class VAR_CRITERION(A2lNode):
    __slots__ = 'name', 'long_identifier', 'value', 'var_measurement', 'var_selection_characteristic', 

    def __init__(self, name, long_identifier, value, args):
        self.name = Ident(name)
        self.long_identifier = String(long_identifier)
        self.value = list(value)
        self.var_measurement = None
        self.var_selection_characteristic = None
        super(VAR_CRITERION, self).__init__(*args)


@node_type('VAR_FORBIDDEN_COMB')
class VAR_FORBIDDEN_COMB(A2lNode):
    __slots__ = 'criterion', 

    def __init__(self, args):
        self.criterion = list()
        super(VAR_FORBIDDEN_COMB, self).__init__(*args)


@node_type('VAR_MEASUREMENT')
class VAR_MEASUREMENT(Ident):
    def __new__(cls, name):
        return super(VAR_MEASUREMENT, cls).__new__(cls, name)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(VAR_MEASUREMENT, self).__str__())


@node_type('VAR_NAMING')
class VAR_NAMING(enum_tag):
    def __new__(cls, tag):
        return super(VAR_NAMING, cls).__new__(cls, tag)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(VAR_NAMING, self).__str__())


@node_type('VAR_SELECTION_CHARACTERISTIC')
class VAR_SELECTION_CHARACTERISTIC(Ident):
    def __new__(cls, name):
        return super(VAR_SELECTION_CHARACTERISTIC, cls).__new__(cls, name)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(VAR_SELECTION_CHARACTERISTIC, self).__str__())


@node_type('VAR_SEPARATOR')
class VAR_SEPARATOR(String):
    def __new__(cls, separator):
        return super(VAR_SEPARATOR, cls).__new__(cls, separator)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(VAR_SEPARATOR, self).__str__())


@node_type('VERSION')
class VERSION(String):
    def __new__(cls, version_identifier):
        return super(VERSION, cls).__new__(cls, version_identifier)

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super(VERSION, self).__str__())


@node_type('VIRTUAL')
class VIRTUAL(A2lNode):
    __slots__ = 'measuring_channel', 

    def __init__(self, args):
        self.measuring_channel = list()
        super(VIRTUAL, self).__init__(*args)


@node_type('VIRTUAL_CHARACTERISTIC')
class VIRTUAL_CHARACTERISTIC(A2lNode):
    __slots__ = 'formula', 'characteristic', 

    def __init__(self, formula, args):
        self.formula = String(formula)
        self.characteristic = list()
        super(VIRTUAL_CHARACTERISTIC, self).__init__(*args)

