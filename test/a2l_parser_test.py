"""
@project: parser
@file: a2l_parser_test.py
@author: Guillaume Sottas
@date: 06.04.2018
"""

import pytest

from pya2l.parser.exception import A2lFormatException
from pya2l.parser.grammar.parser import A2lParser as Parser

idents = (
    pytest.param('name', 'name', id='valid ident'),
    # pytest.param('0', None, id='invalid ident', marks=pytest.mark.xfail(raises=A2lFormatException, strict=True))
)

floats = (pytest.param('0.0', 0.0, id='zero'),)

ints = (pytest.param('0', 0, id='zero'),)

longs = (pytest.param('0', 0, id='zero'),)

strings = (pytest.param('\"\"', '', id='valid string'),)

addr_types = (
    pytest.param('PBYTE', 'PBYTE', id='1 byte'),
    pytest.param('PWORD', 'PWORD', id='2 byte'),
    pytest.param('PLONG', 'PLONG', id='4 byte'),
    pytest.param('DIRECT', 'DIRECT', id='direct'))

data_sizes = (
    pytest.param('BYTE', 'BYTE', id='byte'),
    pytest.param('WORD', 'WORD', id='word'),
    pytest.param('LONG', 'LONG', id='long'))

data_types = (
    pytest.param('UBYTE', 'UBYTE', id='uint8'),
    pytest.param('SBYTE', 'SBYTE', id='sint8'),
    pytest.param('UWORD', 'UWORD', id='uint16'),
    pytest.param('SWORD', 'SWORD', id='sint16'),
    pytest.param('ULONG', 'ULONG', id='uint32'),
    pytest.param('SLONG', 'SLONG', id='sint32'),
    pytest.param('FLOAT32_IEEE', 'FLOAT32_IEEE', id='f32'),
    pytest.param('FLOAT64_IEEE', 'FLOAT64_IEEE', id='f64'))

index_orders = (
    pytest.param('INDEX_INCR', 'INDEX_INCR', id='increasing'),
    pytest.param('INDEX_DECR', 'INDEX_DECR', id='decreasing'))

enum_prg_type_memory_layout_strings = (
    pytest.param('PRG_CODE', 'PRG_CODE', id='PRG_CODE'),
    pytest.param('PRG_DATA', 'PRG_DATA', id='PRG_DATA'),
    pytest.param('PRG_RESERVED', 'PRG_RESERVED', id='PRG_RESERVED'))

enum_prg_type_memory_segment_strings = (
    pytest.param('CODE', 'CODE', id='CODE'),
    pytest.param('DATA', 'DATA', id='DATA'),
    pytest.param('OFFLINE_DATA', 'OFFLINE_DATA', id='OFFLINE_DATA'),
    pytest.param('VARIABLES', 'VARIABLES', id='VARIABLES'),
    pytest.param('SERAM', 'SERAM', id='SERAM'),
    pytest.param('RESERVED', 'RESERVED', id='RESERVED'),
    pytest.param('CALIBRATION_VARIABLES', 'CALIBRATION_VARIABLES', id='CALIBRATION_VARIABLES'),
    pytest.param('EXCLUDE_FROM_FLASH', 'EXCLUDE_FROM_FLASH', id='EXCLUDE_FROM_FLASH'))

enum_type_characteristic_strings = (
    pytest.param('VALUE', 'VALUE', id='VALUE'),
    pytest.param('CURVE', 'CURVE', id='CURVE'),
    pytest.param('MAP', 'MAP', id='MAP'),
    pytest.param('CUBOID', 'CUBOID', id='CUBOID'),
    pytest.param('VAL_BLK', 'VAL_BLK', id='VAL_BLK'),
    pytest.param('ASCII', 'ASCII', id='ASCII'))

enum_memory_type_strings = (
    pytest.param('RAM', 'RAM', id='RAM'),
    pytest.param('EEPROM', 'EEPROM', id='EEPROM'),
    pytest.param('EPROM', 'EPROM', id='EPROM'),
    pytest.param('ROM', 'ROM', id='ROM'),
    pytest.param('REGISTER', 'REGISTER', id='REGISTER'),
    pytest.param('FLASH', 'FLASH', id='FLASH'))


enum_unit_type_strings = (
    pytest.param('EXTENDED_SI', 'EXTENDED_SI', id='EXTENDED_SI'),
    pytest.param('DERIVED', 'DERIVED', id='DERIVED'))


enum_attribute_memory_segment_strings = (
    pytest.param('INTERN', 'INTERN', id='INTERN'),
    pytest.param('EXTERN', 'EXTERN', id='EXTERN'))


enum_attribute_axis_descr_string_strings = (
    pytest.param('STD_AXIS', 'STD_AXIS', id='STD_AXIS'),
    pytest.param('FIX_AXIS', 'FIX_AXIS', id='FIX_AXIS'),
    pytest.param('COM_AXIS', 'COM_AXIS', id='COM_AXIS'),
    pytest.param('RES_AXIS', 'RES_AXIS', id='RES_AXIS'),
    pytest.param('CURVE_AXIS', 'CURVE_AXIS', id='CURVE_AXIS'))

enum_conversion_type_compu_method_strings = (
    pytest.param('TAB_INTP', 'TAB_INTP', id='TAB_INTP'),
    pytest.param('TAB_NOINTP', 'TAB_NOINTP', id='TAB_NOINTP'),
    pytest.param('TAB_VERB', 'TAB_VERB', id='TAB_VERB'),
    pytest.param('RAT_FUNC', 'RAT_FUNC', id='RAT_FUNC'),
    pytest.param('FORM', 'FORM', id='FORM'))

enum_conversion_type_compu_tab_strings = (
    pytest.param('TAB_INTP', 'TAB_INTP', id='TAB_INTP'),
    pytest.param('TAB_NOINTP', 'TAB_NOINTP', id='TAB_NOINTP'))

enum_conversion_type_compu_vtab_strings = (pytest.param('TAB_VERB', 'TAB_VERB', id='TAB_VERB'),)

enum_index_mode_fnc_values_strings = (
    pytest.param('COLUMN_DIR', 'COLUMN_DIR', id='COLUMN_DIR'),
    pytest.param('ROW_DIR', 'ROW_DIR', id='ROW_DIR'),
    pytest.param('ALTERNATE_WITH_X', 'ALTERNATE_WITH_X', id='ALTERNATE_WITH_X'),
    pytest.param('ALTERNATE_WITH_Y', 'ALTERNATE_WITH_Y', id='ALTERNATE_WITH_Y'),
    pytest.param('ALTERNATE_CURVES', 'ALTERNATE_CURVES', id='ALTERNATE_CURVES'))

enum_var_naming_tag = (pytest.param('NUMERIC', 'NUMERIC', id='NUMERIC'),)

offset_strings = (pytest.param('0 0 0 0 0', [0, 0, 0, 0, 0], id='valid offset'),)

empty_string = ''

bit_operation_string_minimal = '/begin BIT_OPERATION {} /end BIT_OPERATION'

annotation_string_minimal = '/begin ANNOTATION {} /end ANNOTATION'

axis_descr_string_minimal = '/begin AXIS_DESCR STD_AXIS _ _ 0 0.0 0.0 {} /end AXIS_DESCR'

axis_pts_string_minimal = '/begin AXIS_PTS _ "" 0 _ _ 0.0 _ 0 0.0 0.0 {} /end AXIS_PTS'

frame_string_minimal = '/begin FRAME _ "" 0 0 {} /end FRAME'

# TODO: move with enums
enum_byte_order = (
    pytest.param('MSB_FIRST', 'MSB_FIRST', id='MSB_FIRST'),
    pytest.param('MSB_LAST', 'MSB_LAST', id='MSB_LAST'))

enum_calibration_access = (
    pytest.param('CALIBRATION', 'CALIBRATION', id='CALIBRATION'),
    pytest.param('NO_CALIBRATION', 'NO_CALIBRATION', id='NO_CALIBRATION'),
    pytest.param('NOT_IN_MCD_SYSTEM', 'NOT_IN_MCD_SYSTEM', id='NOT_IN_MCD_SYSTEM'),
    pytest.param('OFFLINE_CALIBRATION', 'OFFLINE_CALIBRATION', id='OFFLINE_CALIBRATION'))

calibration_method_string_minimal = '/begin CALIBRATION_METHOD "" 0 {} /end CALIBRATION_METHOD'


@pytest.fixture()
def calibration_method_string(request):
    s = '''/begin CALIBRATION_METHOD
        {string}
        {long}
        {calibration_handle}
        /end CALIBRATION_METHOD'''.format(string='""', long='0', calibration_handle='')
    return '\n'.join(s for _ in range(request.param))


characteristic_string_minimal = '/begin CHARACTERISTIC _ "" VALUE 0 _ 0.0 _ 0.0 0.0 {} /end CHARACTERISTIC'
calibration_handle_string_minimal = '/begin CALIBRATION_HANDLE {} /end CALIBRATION_HANDLE'

compu_method_string_minimal = '/begin COMPU_METHOD _ "" TAB_INTP "" "" {} /end COMPU_METHOD'
compu_tab_string_minimal = '/begin COMPU_TAB _ "" TAB_INTP 0 {} /end COMPU_TAB'

compu_vtab_string_minimal = '/begin COMPU_VTAB _ "" TAB_VERB 0 {} /end COMPU_VTAB'

compu_vtab_range_string_minimal = '/begin COMPU_VTAB_RANGE _ "" 0 {} /end COMPU_VTAB_RANGE'
curve_axis_ref_strings = [
    pytest.param('CURVE_AXIS_REF _', '_', id='valid CURVE_AXIS_REF'),
    # pytest.param('CURVE_AXIS_REF ',
    #              None,
    #              id='invalid CURVE_AXIS_REF',
    #              marks=pytest.mark.xfail(raises=A2lFormatException, strict=True))
]


@pytest.fixture()
def dependent_characteristic_string(request):
    s = '''/begin DEPENDENT_CHARACTERISTIC
    {string}
    {ident}
    /end DEPENDENT_CHARACTERISTIC'''.format(string='""', ident='_')
    return '\n'.join(s for _ in range(request.param))


enum_mode_deposit = (
    pytest.param('ABSOLUTE', 'ABSOLUTE', id='valid DEPOSIT'),
    pytest.param('DIFFERENCE', 'DIFFERENCE', id='valid DEPOSIT'))


@pytest.fixture()
def extended_limits_string(request):
    s = '''EXTENDED_LIMITS {float} {float}'''.format(float='0.0')
    return '\n'.join(s for _ in range(request.param))


formula_inv_strings = [
    pytest.param('FORMULA_INV ""', '', id='valid FORMULA_INV'),
]

frame_strings = ['/begin FRAME {ident} {string} {int} {long} {frame_measurement} {if_data} /end FRAME']
frame_measurement_strings = ['/begin FRAME_MEASUREMENT {ident} /end FRAME_MEASUREMENT']

function_string_minimal = '/begin FUNCTION _ "" {} /end FUNCTION'

group_string_minimal = '/begin GROUP _ "" {} /end GROUP'

header_string_minimal = '/begin HEADER "" {} /end HEADER'


@pytest.fixture()
def header_string(request):
    s = '''/begin HEADER
    {string}
    {version}
    {project_no}
    /end HEADER'''.format(string='""', version=empty_string, project_no=empty_string)
    return '\n'.join(s for _ in range(request.param))


@pytest.fixture()
def map_list_string(request):
    s = '''/begin MAP_LIST
    {ident}
    /end MAP_LIST'''.format(ident='_')
    return '\n'.join(s for _ in range(request.param))


@pytest.fixture()
def matrix_dim_string(request):
    s = '''MATRIX_DIM {int} {int} {int}'''.format(int='0')
    return '\n'.join(s for _ in range(request.param))


max_refresh_strings = ['MAX_REFRESH {int} {long}']


@pytest.fixture()
def max_refresh_string(request):
    s = '''MAX_REFRESH {int} {long}'''.format(int='0', long='0')
    return '\n'.join(s for _ in range(request.param))


measurement_string_minimal = '/begin MEASUREMENT _ "" UBYTE _ 0 0.0 0.0 0.0 {} /end MEASUREMENT'

memory_layout_strings = ['/begin MEMORY_LAYOUT {enum_prg_type} {long} {long} {offset} {if_data} /end MEMORY_LAYOUT']


@pytest.fixture()
def memory_layout_string(request):
    s = '''/begin MEMORY_LAYOUT
    {enum_prg_type}
    {long}
    {long}
    {offset}
    {if_data}
    /end MEMORY_LAYOUT'''.format(enum_prg_type='PRG_CODE', long='0', offset='0 0 0 0 0', if_data='')
    return '\n'.join(s for _ in range(request.param))


module_string_minimal = '/begin MODULE _ "" {} /end MODULE'


@pytest.fixture()
def module_string(request):
    s = '''/begin MODULE {ident}
    {string}
    {a2ml}
    {mod_par}
    {mod_common}
    {if_data}
    {characteristic}
    {axis_pts}
    {measurement}
    {compu_method}
    {compu_tab}
    {compu_vtab}
    {compu_vtab_range}
    {function}
    {group}
    {record_layout}
    {variant_coding}
    {frame}
    {user_rights}
    {unit}
    /end MODULE'''.format(ident='_',
                          string='""',
                          a2ml=empty_string,
                          mod_par=empty_string,
                          mod_common=empty_string,
                          if_data=empty_string,
                          characteristic=empty_string,
                          axis_pts=empty_string,
                          measurement=empty_string,
                          compu_method=empty_string,
                          compu_tab=empty_string,
                          compu_vtab=empty_string,
                          compu_vtab_range=empty_string,
                          function=empty_string,
                          group=empty_string,
                          record_layout=empty_string,
                          variant_coding=empty_string,
                          frame=empty_string,
                          user_rights=empty_string,
                          unit=empty_string)
    return '\n'.join(s for _ in range(request.param))


mod_common_string_minimal = '/begin MOD_COMMON "" {} /end MOD_COMMON'

mod_par_string_minimal = '/begin MOD_PAR "" {} /end MOD_PAR'

enum_monotony = (
    pytest.param('MON_INCREASE', 'MON_INCREASE', id='MON_INCREASE'),
    pytest.param('MON_DECREASE', 'MON_DECREASE', id='MON_DECREASE'),
    pytest.param('STRICT_INCREASE', 'STRICT_INCREASE', id='STRICT_INCREASE'),
    pytest.param('STRICT_DECREASE', 'STRICT_DECREASE', id='STRICT_DECREASE'))

out_measurement_strings = [
    pytest.param('/begin OUT_MEASUREMENT /end OUT_MEASUREMENT',
                 0,
                 id='no identifier'),
    pytest.param('/begin OUT_MEASUREMENT {ident} /end OUT_MEASUREMENT',
                 1,
                 id='one identifier'),
    pytest.param('/begin OUT_MEASUREMENT {ident} {ident} /end OUT_MEASUREMENT',
                 2,
                 id='two identifier')
]

project_strings = [
    pytest.param('/begin PROJECT {ident} {string} {header} {module} /end PROJECT', id='PROJECT HEADER MODULE'),
    pytest.param('/begin PROJECT {ident} {string} {module} {header} /end PROJECT', id='PROJECT MODULE HEADER'),
    pytest.param('/begin PROJECT {ident} {string} {module} {header} /end PROJECT', id='PROJECT MODULE HEADER MODULE')
]
project_string_minimal = '/begin PROJECT _ "" {} /end PROJECT'
project_no_strings = [pytest.param('PROJECT_NO _', '_', id='valid PROJECT_NO')]

record_layout_string_minimal = '/begin RECORD_LAYOUT _ {} /end RECORD_LAYOUT'

ref_characteristic_strings = [
    pytest.param('/begin REF_CHARACTERISTIC /end REF_CHARACTERISTIC',
                 0,
                 id='no identifier'),
    pytest.param('/begin REF_CHARACTERISTIC {ident} /end REF_CHARACTERISTIC',
                 1,
                 id='one identifier'),
    pytest.param('/begin REF_CHARACTERISTIC {ident} {ident} /end REF_CHARACTERISTIC',
                 2,
                 id='two identifier')
]

ref_group_strings = ['/begin REF_GROUP {ident} /end REF_GROUP']

ref_measurement_strings = [
    pytest.param('/begin REF_MEASUREMENT /end REF_MEASUREMENT',
                 0,
                 id='no identifier'),
    pytest.param('/begin REF_MEASUREMENT {ident} /end REF_MEASUREMENT',
                 1,
                 id='one identifier'),
    pytest.param('/begin REF_MEASUREMENT {ident} {ident} /end REF_MEASUREMENT',
                 2,
                 id='two identifier')
]

reserved_strings = [
    pytest.param('', 0, id='no reserved'),
    pytest.param('RESERVED {int} {data_size}', 1, id='one reserved'),
    pytest.param('RESERVED {int} {data_size} RESERVED {int} {data_size}', 2, id='two reserved')
]

si_exponents_strings = ['/begin SI_EXPONENTS {int} {int} {int} {int} {int} {int} {int} /end SI_EXPONENTS']


@pytest.fixture()
def system_constant_string(request):
    s = '''SYSTEM_CONSTANT {string} {string}'''.format(string='""')
    return '\n'.join(s for _ in range(request.param))


unit_string_minimal = '/begin UNIT _ "" "" EXTENDED_SI {} /end UNIT'
unit_conversion_strings = ['/begin UNIT_CONVERSION {float} {float} /end UNIT_CONVERSION']

user_rights_string_minimal = '/begin USER_RIGHTS _ {} /end USER_RIGHTS'

variant_coding_string_minimal = '/begin VARIANT_CODING {} /end VARIANT_CODING'
var_address_strings = ['/begin VAR_ADDRESS {address} /end VAR_ADDRESS']
var_address_string_minimal = '/begin VAR_ADDRESS {} /end VAR_ADDRESS'

var_characteristic_string_minimal = '/begin VAR_CHARACTERISTIC _ {} /end VAR_CHARACTERISTIC'

var_criterion_string_minimal = '/begin VAR_CRITERION _ "" {} /end VAR_CRITERION'


@pytest.fixture()
def virtual_characteristic_string(request):
    s = '''/begin VIRTUAL_CHARACTERISTIC
    {string}
    {ident}
    /end VIRTUAL_CHARACTERISTIC'''.format(string='""', ident='_')
    return '\n'.join(s for _ in range(request.param))


@pytest.fixture()
def project(request):
    lookup = dict(axis_descr=axis_descr_string_minimal,
                  axis_pts=axis_pts_string_minimal,
                  characteristic=characteristic_string_minimal,
                  compu_method=compu_method_string_minimal,
                  function=function_string_minimal,
                  group=group_string_minimal,
                  header=header_string_minimal,
                  measurement=measurement_string_minimal,
                  mod_par=mod_par_string_minimal,
                  module=module_string_minimal,
                  project=project_string_minimal,
                  record_layout=record_layout_string_minimal,
                  variant_coding=variant_coding_string_minimal)
    result = None
    prefix = ['project']
    for element in prefix + request.param:
        try:
            if result:
                result = result.format(lookup[element])
            else:
                result = lookup[element]
        except KeyError:
            continue
    return result, prefix + request.param


@pytest.fixture()
def module(request):
    lookup = dict(annotation=annotation_string_minimal,  # TODO: check.
                  axis_descr=axis_descr_string_minimal,
                  axis_pts=axis_pts_string_minimal,
                  bit_operation=bit_operation_string_minimal,  # TODO: check.
                  characteristic=characteristic_string_minimal,
                  compu_method=compu_method_string_minimal,
                  compu_tab=compu_tab_string_minimal,
                  compu_vtab=compu_vtab_string_minimal,
                  compu_vtab_range=compu_vtab_range_string_minimal,
                  frame=frame_string_minimal,
                  function=function_string_minimal,
                  group=group_string_minimal,
                  measurement=measurement_string_minimal,
                  mod_common=mod_common_string_minimal,
                  mod_par=mod_par_string_minimal,
                  module=module_string_minimal,
                  project=project_string_minimal,
                  record_layout=record_layout_string_minimal,
                  unit=unit_string_minimal,
                  user_rights=user_rights_string_minimal,
                  variant_coding=variant_coding_string_minimal)
    result = None
    prefix = ['project', 'module', 0]
    for element in prefix + request.param:
        try:
            if result:
                result = result.format(lookup[element])
            else:
                result = lookup[element]
        except KeyError:
            continue
    return result, prefix + request.param


@pytest.fixture()
def variant_coding(request):
    lookup = dict(var_address=var_address_string_minimal,
                  var_characteristic=var_characteristic_string_minimal,
                  var_criterion=var_criterion_string_minimal)
    result = None
    prefix = ['project', 'module', 0, 'variant_coding']
    for element in prefix + request.param:
        try:
            if result:
                result = result.format(lookup[element])
            else:
                result = lookup[element]
        except KeyError:
            continue
    return project_string_minimal.format(
        module_string_minimal.format(
            variant_coding_string_minimal.format(result))), prefix + request.param


@pytest.fixture()
def calibration_method(request):
    lookup = dict(calibration_handle=calibration_handle_string_minimal)
    result = None
    prefix = ['project', 'module', 0, 'mod_par', 'calibration_method', 0]
    for element in prefix + request.param:
        try:
            if result:
                result = result.format(lookup[element])
            else:
                result = lookup[element]
        except KeyError:
            continue
    return project_string_minimal.format(
        module_string_minimal.format(
            mod_par_string_minimal.format(
                calibration_method_string_minimal.format(result)))), prefix + request.param


@pytest.fixture()
def compu_method(request):
    lookup = dict(formula='/begin FORMULA "" {} /end FORMULA')
    result = None
    prefix = ['project', 'module', 0, 'compu_method', 0]
    for element in prefix + request.param:
        try:
            if result:
                result = result.format(lookup[element])
            else:
                result = lookup[element]
        except KeyError:
            continue
    return project_string_minimal.format(
        module_string_minimal.format(
            compu_method_string_minimal.format(result))), prefix + request.param


def get_node_from_ast(ast, path):
    result = ast
    for element in path:
        try:
            result = getattr(result, element)
        except TypeError:
            result = result[element]
    return result


def test_a2l():
    pytest.xfail('implement me...')


@pytest.mark.parametrize('e', ['A2ML_VERSION {int} {int}'])
@pytest.mark.parametrize('s, v', ints)
def test_a2ml_version(e, s, v):
    p = Parser(e.format(int=s))
    assert p.ast.a2ml_version.version_no == v
    assert p.ast.a2ml_version.upgrade_no == v


@pytest.mark.parametrize('project', [
    pytest.param(['module', 0, 'mod_par', 'addr_epk', 0], id='MOD_PAR')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('ADDR_EPK {}')])
@pytest.mark.parametrize('s, v', longs)
def test_addr_epk(project, e, s, v):
    p = Parser(project[0].format(e.format(s)))
    version = get_node_from_ast(p.ast, project[1])
    assert version == v


@pytest.mark.parametrize('module', [
    pytest.param(['mod_common', 'alignment_byte'], id='MOD_COMMON'),
    pytest.param(['record_layout', 0, 'alignment_byte'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('ALIGNMENT_BYTE {}')])
@pytest.mark.parametrize('s, v', ints)
def test_alignment_byte(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    alignment_byte = get_node_from_ast(p.ast, module[1])
    assert alignment_byte == v


@pytest.mark.parametrize('module', [
    pytest.param(['mod_common', 'alignment_float32_ieee'], id='MOD_COMMON'),
    pytest.param(['record_layout', 0, 'alignment_float32_ieee'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('ALIGNMENT_FLOAT32_IEEE {}')])
@pytest.mark.parametrize('s, v', ints)
def test_alignment_float32_ieee(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    alignment_float32_ieee = get_node_from_ast(p.ast, module[1])
    assert alignment_float32_ieee == v


@pytest.mark.parametrize('module', [
    pytest.param(['mod_common', 'alignment_float64_ieee'], id='MOD_COMMON'),
    pytest.param(['record_layout', 0, 'alignment_float64_ieee'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('ALIGNMENT_FLOAT64_IEEE {}')])
@pytest.mark.parametrize('s, v', ints)
def test_alignment_float64_ieee(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    alignment_float64_ieee = get_node_from_ast(p.ast, module[1])
    assert alignment_float64_ieee == v


@pytest.mark.parametrize('module', [
    pytest.param(['mod_common', 'alignment_long'], id='MOD_COMMON'),
    pytest.param(['record_layout', 0, 'alignment_long'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('ALIGNMENT_LONG {}')])
@pytest.mark.parametrize('s, v', ints)
def test_alignment_long(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    alignment_long = get_node_from_ast(p.ast, module[1])
    assert alignment_long == v


@pytest.mark.parametrize('module', [
    pytest.param(['mod_common', 'alignment_word'], id='MOD_COMMON'),
    pytest.param(['record_layout', 0, 'alignment_word'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('ALIGNMENT_WORD {}')])
@pytest.mark.parametrize('s, v', ints)
def test_alignment_word(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    alignment_word = get_node_from_ast(p.ast, module[1])
    assert alignment_word == v


@pytest.mark.parametrize('module', [
    pytest.param(['axis_pts', 0, 'annotation', 0], id='AXIS_PTS'),
    pytest.param(['measurement', 0, 'annotation', 0], id='MEASUREMENT'),
    pytest.param(['characteristic', 0, 'annotation', 0], id='CHARACTERISTIC'),
    pytest.param(['characteristic', 0, 'axis_descr', 0, 'annotation', 0], id='AXIS_DESCR'),
    pytest.param(['function', 0, 'annotation', 0], id='FUNCTION'),
    pytest.param(['group', 0, 'annotation', 0], id='GROUP')], indirect=True)
def test_annotation(module):
    p = Parser(module[0].format(''))
    annotation = get_node_from_ast(p.ast, module[1])
    assert annotation.annotation_label is None
    assert annotation.annotation_origin is None
    assert annotation.annotation_text is None


@pytest.mark.parametrize('module', [
    pytest.param(['axis_pts', 0, 'annotation', 0, 'annotation_label'], id='AXIS_PTS'),
    pytest.param(['measurement', 0, 'annotation', 0, 'annotation_label'], id='MEASUREMENT'),
    pytest.param(['characteristic', 0, 'annotation', 0, 'annotation_label'], id='CHARACTERISTIC'),
    pytest.param(['characteristic', 0, 'axis_descr', 0, 'annotation', 0, 'annotation_label'], id='AXIS_DESCR'),
    pytest.param(['function', 0, 'annotation', 0, 'annotation_label'], id='FUNCTION'),
    pytest.param(['group', 0, 'annotation', 0, 'annotation_label'], id='GROUP')
], indirect=True)
@pytest.mark.parametrize('e', ['ANNOTATION_LABEL {}'])
@pytest.mark.parametrize('s, v', strings)
def test_annotation_label(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    annotation_label = get_node_from_ast(p.ast, module[1])
    assert annotation_label == v


@pytest.mark.parametrize('module', [
    pytest.param(['axis_pts', 0, 'annotation', 0, 'annotation_origin'], id='AXIS_PTS'),
    pytest.param(['measurement', 0, 'annotation', 0, 'annotation_origin'], id='MEASUREMENT'),
    pytest.param(['characteristic', 0, 'annotation', 0, 'annotation_origin'], id='CHARACTERISTIC'),
    pytest.param(['characteristic', 0, 'axis_descr', 0, 'annotation', 0, 'annotation_origin'], id='AXIS_DESCR'),
    pytest.param(['function', 0, 'annotation', 0, 'annotation_origin'], id='FUNCTION'),
    pytest.param(['group', 0, 'annotation', 0, 'annotation_origin'], id='GROUP')
], indirect=True)
@pytest.mark.parametrize('e', ['ANNOTATION_ORIGIN {}'])
@pytest.mark.parametrize('s, v', strings)
def test_annotation_origin(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    annotation_origin = get_node_from_ast(p.ast, module[1])
    assert annotation_origin == v


@pytest.mark.parametrize('module', [
    pytest.param(['axis_pts', 0, 'annotation', 0, 'annotation_text'], id='AXIS_PTS'),
    pytest.param(['measurement', 0, 'annotation', 0, 'annotation_text'], id='MEASUREMENT'),
    pytest.param(['characteristic', 0, 'annotation', 0, 'annotation_text'], id='CHARACTERISTIC'),
    pytest.param(['characteristic', 0, 'axis_descr', 0, 'annotation', 0, 'annotation_text'], id='AXIS_DESCR'),
    pytest.param(['function', 0, 'annotation', 0, 'annotation_text'], id='FUNCTION'),
    pytest.param(['group', 0, 'annotation', 0, 'annotation_text'], id='GROUP')], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('''/begin ANNOTATION_TEXT /end ANNOTATION_TEXT''', 0, id='no text'),
    pytest.param('''/begin ANNOTATION_TEXT {s} /end ANNOTATION_TEXT''', 1, id='one text'),
    pytest.param('''/begin ANNOTATION_TEXT {s} {s} /end ANNOTATION_TEXT''', 2, id='two text')])
@pytest.mark.parametrize('s, v', strings)
def test_annotation_text(module, e, count, s, v):
    p = Parser(module[0].format(e.format(s=s)))
    annotation_text = get_node_from_ast(p.ast, module[1])
    assert type(annotation_text.text) is list
    assert len(annotation_text.text) == count
    for text in annotation_text.text:
        assert text == v


@pytest.mark.parametrize('module', [pytest.param(['measurement', 0, 'array_size'], id='MEASUREMENT')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('ARRAY_SIZE {}')])
@pytest.mark.parametrize('s, v', ints)
def test_array_size(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    array_size = get_node_from_ast(p.ast, module[1])
    assert array_size == v


@pytest.mark.parametrize('s', ['ASAP2_VERSION {int} {int}'])
@pytest.mark.parametrize('int_string, int_value', ints)
def test_asap2_version(s, int_string, int_value):
    p = Parser(s.format(int=int_string))
    assert p.ast.asap2_version.version_no == int_value
    assert p.ast.asap2_version.upgrade_no == int_value


@pytest.mark.parametrize('module', [pytest.param(['characteristic', 0], id='CHARACTERISTIC')], indirect=True)
@pytest.mark.parametrize('s', ['''/begin AXIS_DESCR 
    {enum_attribute}
    {ident}
    {ident}
    {int}
    {float}
    {float}
    {read_only}
    {format}
    {annotation}
    {axis_pts_ref}
    {max_grad}
    {monotony}
    {byte_order}
    {extended_limits}
    {fix_axis_par}
    {fix_axis_par_dist}
    {fix_axis_par_list}
    {deposit}
    {curve_axis_ref}
    /end AXIS_DESCR'''])
@pytest.mark.parametrize('enum_attribute_string, enum_attribute_value', enum_attribute_axis_descr_string_strings)
@pytest.mark.parametrize('ident_string, ident_value', idents)
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('float_string, float_value', floats)
def test_axis_descr(module,
                    s,
                    enum_attribute_string, enum_attribute_value,
                    ident_string, ident_value,
                    int_string, int_value,
                    float_string, float_value):
    p = Parser(module[0].format(s.format(
        enum_attribute=enum_attribute_string,
        ident=ident_string,
        int=int_string,
        float=float_string,
        read_only=empty_string,
        format=empty_string,
        axis_pts_ref=empty_string,
        max_grad=empty_string,
        monotony=empty_string,
        byte_order=empty_string,
        fix_axis_par=empty_string,
        fix_axis_par_dist=empty_string,
        fix_axis_par_list=empty_string,
        deposit=empty_string,
        annotation=empty_string,
        extended_limits=empty_string,
        curve_axis_ref=empty_string)))
    axis_descr = get_node_from_ast(p.ast, module[1] + ['axis_descr', 0])
    assert axis_descr.attribute == enum_attribute_value
    assert axis_descr.input_quantity == ident_value
    assert axis_descr.conversion == ident_value
    assert axis_descr.max_axis_points == int_value
    assert axis_descr.lower_limit == float_value
    assert axis_descr.upper_limit == float_value
    assert axis_descr.read_only is None
    assert axis_descr.format is None
    assert axis_descr.axis_pts_ref is None
    assert axis_descr.max_grad is None
    assert axis_descr.monotony is None
    assert axis_descr.byte_order is None
    assert axis_descr.fix_axis_par is None
    assert axis_descr.fix_axis_par_dist is None
    assert axis_descr.fix_axis_par_list is None
    assert axis_descr.deposit is None
    assert type(axis_descr.annotation) is list
    assert axis_descr.extended_limits is None
    assert axis_descr.curve_axis_ref is None


@pytest.mark.parametrize('s', [
    '''/begin AXIS_PTS
    {ident}
    {string}
    {long}
    {ident}
    {ident}
    {float}
    {ident}
    {int}
    {float}
    {float}
    {display_identifier}
    {read_only}
    {format}
    {deposit}
    {byte_order}
    {function_list}
    {ref_memory_segment}
    {guard_rails}
    {extended_limits}
    {annotation}
    {if_data}
    {calibration_access}
    {ecu_address_extension}
    /end AXIS_PTS'''])
@pytest.mark.parametrize('ident_string, ident_value', idents)
@pytest.mark.parametrize('string_string, string_value', strings)
@pytest.mark.parametrize('long_string, long_value', longs)
@pytest.mark.parametrize('float_string, float_value', floats)
@pytest.mark.parametrize('int_string, int_value', ints)
def test_axis_pts(s,
                  ident_string, ident_value,
                  string_string, string_value,
                  long_string, long_value,
                  float_string, float_value,
                  int_string, int_value):
    p = Parser(project_string_minimal.format(module_string_minimal.format(s.format(
        ident=ident_string,
        string=string_string,
        long=long_string,
        float=float_string,
        int=int_string,
        display_identifier=empty_string,
        read_only=empty_string,
        format=empty_string,
        deposit=empty_string,
        byte_order=empty_string,
        function_list=empty_string,
        ref_memory_segment=empty_string,
        guard_rails=empty_string,
        if_data=empty_string,
        annotation=empty_string,
        extended_limits=empty_string,
        calibration_access=empty_string,
        ecu_address_extension=empty_string))))
    axis_pts = p.ast.project.module[0].axis_pts[0]
    assert axis_pts.name == ident_value
    assert axis_pts.long_identifier == string_value
    assert axis_pts.address == long_value
    assert axis_pts.input_quantity == ident_value
    # TODO: axis_pts.deposit positional parameter is overridden by optional DEPOSIT parameter, is it correct?
    # assert axis_pts.deposit == ident_value
    assert axis_pts.max_diff == float_value
    assert axis_pts.conversion == ident_value
    assert axis_pts.max_axis_points == int_value
    assert axis_pts.lower_limit == float_value
    assert axis_pts.upper_limit == float_value
    assert axis_pts.display_identifier is None
    assert axis_pts.read_only is None
    assert axis_pts.format is None
    assert axis_pts.deposit is None
    assert axis_pts.byte_order is None
    assert axis_pts.function_list is None
    assert axis_pts.ref_memory_segment is None
    assert axis_pts.guard_rails is None
    assert type(axis_pts.annotation) is list
    assert axis_pts.extended_limits is None
    assert axis_pts.calibration_access is None
    assert axis_pts.ecu_address_extension is None


@pytest.mark.parametrize('module', [
    pytest.param(['characteristic', 0, 'axis_descr', 0, 'axis_pts_ref'], id='AXIS_DESCR')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('AXIS_PTS_REF {}')])
@pytest.mark.parametrize('s, v', idents)
def test_axis_pts_ref(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    axis_pts_ref = get_node_from_ast(p.ast, module[1])
    assert axis_pts_ref == v


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'axis_pts_x'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['AXIS_PTS_X {int} {data_type} {index_order} {addr_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
@pytest.mark.parametrize('index_order_string, index_order_value', index_orders)
@pytest.mark.parametrize('addr_type_string, addr_type_value', addr_types)
def test_axis_pts_x(module,
                    s,
                    int_string, int_value,
                    data_type_string, data_type_value,
                    index_order_string, index_order_value,
                    addr_type_string, addr_type_value):
    p = Parser(module[0].format(s.format(int=int_string,
                                         data_type=data_type_string,
                                         index_order=index_order_string,
                                         addr_type=addr_type_string)))
    axis_pts_x = get_node_from_ast(p.ast, module[1])
    assert axis_pts_x.position == int_value
    assert axis_pts_x.data_type == data_type_value
    assert axis_pts_x.index_incr == index_order_value
    assert axis_pts_x.addressing == addr_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'axis_pts_y'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['AXIS_PTS_Y {int} {data_type} {index_order} {addr_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
@pytest.mark.parametrize('index_order_string, index_order_value', index_orders)
@pytest.mark.parametrize('addr_type_string, addr_type_value', addr_types)
def test_axis_pts_y(module,
                    s,
                    int_string, int_value,
                    data_type_string, data_type_value,
                    index_order_string, index_order_value,
                    addr_type_string, addr_type_value):
    p = Parser(module[0].format(s.format(int=int_string,
                                         data_type=data_type_string,
                                         index_order=index_order_string,
                                         addr_type=addr_type_string)))
    axis_pts_y = get_node_from_ast(p.ast, module[1])
    assert axis_pts_y.position == int_value
    assert axis_pts_y.data_type == data_type_value
    assert axis_pts_y.index_incr == index_order_value
    assert axis_pts_y.addressing == addr_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'axis_pts_z'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['AXIS_PTS_Z {int} {data_type} {index_order} {addr_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
@pytest.mark.parametrize('index_order_string, index_order_value', index_orders)
@pytest.mark.parametrize('addr_type_string, addr_type_value', addr_types)
def test_axis_pts_z(module,
                    s,
                    int_string, int_value,
                    data_type_string, data_type_value,
                    index_order_string, index_order_value,
                    addr_type_string, addr_type_value):
    p = Parser(module[0].format(s.format(int=int_string,
                                         data_type=data_type_string,
                                         index_order=index_order_string,
                                         addr_type=addr_type_string)))
    axis_pts_z = get_node_from_ast(p.ast, module[1])
    assert axis_pts_z.position == int_value
    assert axis_pts_z.data_type == data_type_value
    assert axis_pts_z.index_incr == index_order_value
    assert axis_pts_z.addressing == addr_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'axis_rescale_x'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['AXIS_RESCALE_X {int} {data_type} {int} {index_order} {addr_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
@pytest.mark.parametrize('index_order_string, index_order_value', index_orders)
@pytest.mark.parametrize('addr_type_string, addr_type_value', addr_types)
def test_axis_rescale_x(module,
                        s,
                        int_string, int_value,
                        data_type_string, data_type_value,
                        index_order_string, index_order_value,
                        addr_type_string, addr_type_value):
    p = Parser(module[0].format(s.format(int=int_string,
                                         data_type=data_type_string,
                                         index_order=index_order_string,
                                         addr_type=addr_type_string)))
    axis_rescale_x = get_node_from_ast(p.ast, module[1])
    assert axis_rescale_x.position == int_value
    assert axis_rescale_x.data_type == data_type_value
    assert axis_rescale_x.max_number_of_rescale_pairs == int_value
    assert axis_rescale_x.index_incr == index_order_value
    assert axis_rescale_x.addressing == addr_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'axis_rescale_y'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['AXIS_RESCALE_Y {int} {data_type} {int} {index_order} {addr_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
@pytest.mark.parametrize('index_order_string, index_order_value', index_orders)
@pytest.mark.parametrize('addr_type_string, addr_type_value', addr_types)
def test_axis_rescale_y(module,
                        s,
                        int_string, int_value,
                        data_type_string, data_type_value,
                        index_order_string, index_order_value,
                        addr_type_string, addr_type_value):
    p = Parser(module[0].format(s.format(int=int_string,
                                         data_type=data_type_string,
                                         index_order=index_order_string,
                                         addr_type=addr_type_string)))
    axis_rescale_y = get_node_from_ast(p.ast, module[1])
    assert axis_rescale_y.position == int_value
    assert axis_rescale_y.data_type == data_type_value
    assert axis_rescale_y.max_number_of_rescale_pairs == int_value
    assert axis_rescale_y.index_incr == index_order_value
    assert axis_rescale_y.addressing == addr_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'axis_rescale_z'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['AXIS_RESCALE_Z {int} {data_type} {int} {index_order} {addr_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
@pytest.mark.parametrize('index_order_string, index_order_value', index_orders)
@pytest.mark.parametrize('addr_type_string, addr_type_value', addr_types)
def test_axis_rescale_z(module,
                        s,
                        int_string, int_value,
                        data_type_string, data_type_value,
                        index_order_string, index_order_value,
                        addr_type_string, addr_type_value):
    p = Parser(module[0].format(s.format(int=int_string,
                                         data_type=data_type_string,
                                         index_order=index_order_string,
                                         addr_type=addr_type_string)))
    axis_rescale_z = get_node_from_ast(p.ast, module[1])
    assert axis_rescale_z.position == int_value
    assert axis_rescale_z.data_type == data_type_value
    assert axis_rescale_z.max_number_of_rescale_pairs == int_value
    assert axis_rescale_z.index_incr == index_order_value
    assert axis_rescale_z.addressing == addr_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['characteristic', 0, 'bit_mask'], id='CHARACTERISTIC'),
    pytest.param(['measurement', 0, 'bit_mask'], id='MEASUREMENT')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('BIT_MASK {}')])
@pytest.mark.parametrize('s, v', longs)
def test_bit_mask(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    bit_mask = get_node_from_ast(p.ast, module[1])
    assert bit_mask == v


@pytest.mark.parametrize('module', [pytest.param(['measurement', 0, 'bit_operation'], id='MEASUREMENT')], indirect=True)
def test_bit_operation(module):
    p = Parser(module[0].format(''))
    bit_operation = get_node_from_ast(p.ast, module[1])
    assert bit_operation.left_shift is None
    assert bit_operation.right_shift is None
    assert bit_operation.sign_extend is None


@pytest.mark.parametrize('module', [
    pytest.param(['axis_pts', 0, 'byte_order'], id='AXIS_PTS'),
    pytest.param(['characteristic', 0, 'byte_order'], id='CHARACTERISTIC'),
    pytest.param(['characteristic', 0, 'axis_descr', 0, 'byte_order'], id='AXIS_DESCR'),
    pytest.param(['measurement', 0, 'byte_order'], id='MEASUREMENT'),
    pytest.param(['mod_common', 'byte_order'], id='MOD_COMMON')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('BYTE_ORDER {}')])
@pytest.mark.parametrize('s, v', enum_byte_order)
def test_byte_order(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    byte_order = get_node_from_ast(p.ast, module[1])
    assert byte_order == v


@pytest.mark.parametrize('module', [
    pytest.param(['characteristic', 0, 'calibration_access'], id='CHARACTERISTIC'),
    pytest.param(['axis_pts', 0, 'calibration_access'], id='AXIS_PTS')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('CALIBRATION_ACCESS {}')])
@pytest.mark.parametrize('s, v', enum_calibration_access)
def test_calibration_access(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    calibration_access = get_node_from_ast(p.ast, module[1])
    assert calibration_access == v


@pytest.mark.parametrize('calibration_method', [
    pytest.param(['calibration_handle', 0], id='CALIBRATION_METHOD')], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('', 0, id='no handle', marks=pytest.mark.xfail(raises=A2lFormatException, strict=True)),
    pytest.param('{long}', 1, id='one handle'),
    pytest.param('{long} {long}', 2, id='two handle')])
@pytest.mark.parametrize('s, v', longs)
def test_calibration_handle(calibration_method, e, count, s, v):
    p = Parser(calibration_method[0].format(e.format(long=s)))
    calibration_handle = get_node_from_ast(p.ast, calibration_method[1])
    assert type(calibration_handle.handle) is list
    assert len(calibration_handle.handle) == count
    for handle in calibration_handle.handle:
        assert handle == v


@pytest.mark.parametrize('module', [pytest.param(['mod_par', 'calibration_method', 0], id='MOD_PAR')], indirect=True)
@pytest.mark.parametrize('s', ['/begin CALIBRATION_METHOD {string} {long} /end CALIBRATION_METHOD'])
@pytest.mark.parametrize('string_string, string_value', strings)
@pytest.mark.parametrize('long_string, long_value', longs)
def test_calibration_method(module, s, string_string, string_value, long_string, long_value):
    p = Parser(module[0].format(s.format(string=string_string, long=long_string)))
    calibration_method = get_node_from_ast(p.ast, module[1])
    assert calibration_method.method == string_value
    assert calibration_method.version == long_value
    assert type(calibration_method.calibration_handle) is list


@pytest.mark.parametrize('s', ['''
    /begin CHARACTERISTIC {ident} {string} {enum_type} {long} {ident} {float} {ident} {float} {float}
    {display_identifier}
    {format}
    {byte_order}
    {bit_mask}
    {function_list}
    {number}
    {extended_limits}
    {read_only}
    {guard_rails}
    {map_list}
    {max_refresh}
    {dependent_characteristic}
    {virtual_characteristic}
    {ref_memory_segment}
    {annotation}
    {comparison_quantity}
    {if_data}
    {axis_descr}
    {calibration_access}
    {matrix_dim}
    {ecu_address_extension}
    /end CHARACTERISTIC'''])
@pytest.mark.parametrize('ident_string, ident_value', idents)
@pytest.mark.parametrize('string_string, string_value', strings)
@pytest.mark.parametrize('enum_type_string, enum_type_value', enum_type_characteristic_strings)
@pytest.mark.parametrize('long_string, long_value', longs)
@pytest.mark.parametrize('float_string, float_value', floats)
def test_characteristic(s,
                        ident_string, ident_value,
                        string_string, string_value,
                        enum_type_string, enum_type_value,
                        long_string, long_value,
                        float_string, float_value):
    p = Parser(project_string_minimal.format(module_string_minimal.format(s.format(
        ident=ident_string,
        string=string_string,
        enum_type=enum_type_string,
        long=long_string,
        float=float_string,
        display_identifier=empty_string,
        format=empty_string,
        byte_order=empty_string,
        bit_mask=empty_string,
        function_list=empty_string,
        number=empty_string,
        extended_limits=empty_string,
        read_only=empty_string,
        guard_rails=empty_string,
        map_list=empty_string,
        max_refresh=empty_string,
        dependent_characteristic=empty_string,
        virtual_characteristic=empty_string,
        ref_memory_segment=empty_string,
        annotation=empty_string,
        comparison_quantity=empty_string,
        if_data=empty_string,
        axis_descr=empty_string,
        calibration_access=empty_string,
        matrix_dim=empty_string,
        ecu_address_extension=empty_string))))
    characteristic = p.ast.project.module[0].characteristic[0]
    assert characteristic.name == ident_value
    assert characteristic.long_identifier == string_value
    assert characteristic.type == enum_type_value
    assert characteristic.address == long_value
    assert characteristic.deposit == ident_value
    assert characteristic.max_diff == float_value
    assert characteristic.conversion == ident_value
    assert characteristic.lower_limit == float_value
    assert characteristic.upper_limit == float_value
    assert characteristic.display_identifier is None
    assert characteristic.format is None
    assert characteristic.byte_order is None
    assert characteristic.bit_mask is None
    assert characteristic.function_list is None
    assert characteristic.number is None
    assert characteristic.extended_limits is None
    assert characteristic.read_only is None
    assert characteristic.guard_rails is None
    assert characteristic.map_list is None
    assert characteristic.max_refresh is None
    assert characteristic.dependent_characteristic is None
    assert characteristic.virtual_characteristic is None
    assert characteristic.ref_memory_segment is None
    assert type(characteristic.annotation) is list
    assert characteristic.comparison_quantity is None
    assert type(characteristic.axis_descr) is list
    assert characteristic.calibration_access is None
    assert characteristic.matrix_dim is None
    assert characteristic.ecu_address_extension is None


@pytest.mark.parametrize('module', [pytest.param(['compu_method', 0, 'coeffs'], id='COMPU_METHOD')], indirect=True)
@pytest.mark.parametrize('s', ['COEFFS {float} {float} {float} {float} {float} {float}'])
@pytest.mark.parametrize('float_string, float_value', floats)
def test_coeffs(module, s, float_string, float_value):
    p = Parser(module[0].format(s.format(float=float_string)))
    coeffs = get_node_from_ast(p.ast, module[1])
    assert coeffs.a == float_value
    assert coeffs.b == float_value
    assert coeffs.c == float_value
    assert coeffs.d == float_value
    assert coeffs.e == float_value
    assert coeffs.f == float_value


@pytest.mark.parametrize('module', [
    pytest.param(['characteristic', 0, 'comparison_quantity'], id='CHARACTERISTIC')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('COMPARISON_QUANTITY {}')])
@pytest.mark.parametrize('s, v', idents)
def test_comparison_quantity(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    comparison_quantity = get_node_from_ast(p.ast, module[1])
    assert comparison_quantity == v


@pytest.mark.parametrize('s', ['''
    /begin COMPU_METHOD {ident} {string} {enum_conversion_type} {string} {string}
    {formula}
    {coeffs}
    {compu_tab_ref}
    {ref_unit}
    /end COMPU_METHOD'''])
@pytest.mark.parametrize('ident_string, ident_value', idents)
@pytest.mark.parametrize('string_string, string_value', strings)
@pytest.mark.parametrize('conversion_type_string, conversion_type_value', enum_conversion_type_compu_method_strings)
def test_compu_method(s,
                      ident_string, ident_value,
                      string_string, string_value,
                      conversion_type_string, conversion_type_value):
    p = Parser(project_string_minimal.format(module_string_minimal.format(s.format(
        ident=ident_string,
        string=string_string,
        enum_conversion_type=conversion_type_string,
        formula=empty_string,
        coeffs=empty_string,
        compu_tab_ref=empty_string,
        ref_unit=empty_string))))
    compu_method = p.ast.project.module[0].compu_method[0]
    assert compu_method.name == ident_value
    assert compu_method.long_identifier == string_value
    assert compu_method.conversion_type == conversion_type_value
    assert compu_method.format == string_value
    assert compu_method.unit == string_value
    assert compu_method.formula is None
    assert compu_method.coeffs is None
    assert compu_method.compu_tab_ref is None
    assert compu_method.ref_unit is None


@pytest.mark.parametrize('s', ['''
    /begin COMPU_TAB {ident} {string} {enum_conversion_type} {int} {in_val_out_val}
    {default_value}
    /end COMPU_TAB'''])
@pytest.mark.parametrize('ident_string, ident_value', idents)
@pytest.mark.parametrize('string_string, string_value', strings)
@pytest.mark.parametrize('conversion_type_string, conversion_type_value', enum_conversion_type_compu_tab_strings)
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('in_val_out_val_string, in_val_out_val_value, in_val_out_val_count', [
    pytest.param('', [], 0, id='no in_val_out_val'),
    pytest.param('0.0 0.0', [(0.0, 0.0)], 1, id='one in_val_out_val'),
    pytest.param('0.0 0.0 0.0 0.0', [(0.0, 0.0), (0.0, 0.0)], 2, id='two in_val_out_val')])
def test_compu_tab(s,
                   ident_string, ident_value,
                   string_string, string_value,
                   conversion_type_string, conversion_type_value,
                   int_string, int_value,
                   in_val_out_val_string, in_val_out_val_value, in_val_out_val_count):
    p = Parser(project_string_minimal.format(module_string_minimal.format(s.format(
        ident=ident_string,
        string=string_string,
        enum_conversion_type=conversion_type_string,
        int=int_string,
        default_value=empty_string,
        in_val_out_val=in_val_out_val_string))))
    compu_tab = p.ast.project.module[0].compu_tab[0]
    assert compu_tab.name == ident_value
    assert compu_tab.long_identifier == string_value
    assert compu_tab.conversion_type == conversion_type_value
    assert compu_tab.number_value_pair == int_value
    assert type(compu_tab.in_val_out_val) is list
    assert compu_tab.in_val_out_val == in_val_out_val_value
    assert compu_tab.default_value is None


@pytest.mark.parametrize('module', [
    pytest.param(['compu_method', 0, 'compu_tab_ref'], id='COMPU_METHOD')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('COMPU_TAB_REF {}')])
@pytest.mark.parametrize('s, v', idents)
def test_compu_tab_ref(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    compu_tab_ref = get_node_from_ast(p.ast, module[1])
    assert compu_tab_ref == v


@pytest.mark.parametrize('s', ['''
    /begin COMPU_VTAB {ident} {string} {enum_conversion_type} {int} {in_val_out_val}
    {default_value}
    /end COMPU_VTAB'''])
@pytest.mark.parametrize('ident_string, ident_value', idents)
@pytest.mark.parametrize('string_string, string_value', strings)
@pytest.mark.parametrize('conversion_type_string, conversion_type_value', enum_conversion_type_compu_vtab_strings)
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('in_val_out_val_string, in_val_out_val_value, in_val_out_val_count', [
    pytest.param('', [], 0, id='no in_val_out_val'),
    pytest.param('0.0 ""', [(0.0, '')], 1, id='one in_val_out_val'),
    pytest.param('0.0 "" 0.0 ""', [(0.0, ''), (0.0, '')], 2, id='two in_val_out_val')])
def test_compu_vtab(s,
                    ident_string, ident_value,
                    string_string, string_value,
                    conversion_type_string, conversion_type_value,
                    int_string, int_value,
                    in_val_out_val_string, in_val_out_val_value, in_val_out_val_count):
    p = Parser(project_string_minimal.format(module_string_minimal.format(s.format(
        ident=ident_string,
        string=string_string,
        enum_conversion_type=conversion_type_string,
        int=int_string,
        default_value=empty_string,
        in_val_out_val=in_val_out_val_string))))
    compu_vtab = p.ast.project.module[0].compu_vtab[0]
    assert compu_vtab.name == ident_value
    assert compu_vtab.long_identifier == string_value
    assert compu_vtab.conversion_type == conversion_type_value
    assert compu_vtab.number_value_pair == int_value
    assert type(compu_vtab.in_val_out_val) is list
    assert compu_vtab.in_val_out_val == in_val_out_val_value
    assert compu_vtab.default_value is None


@pytest.mark.parametrize('s', ['''
    /begin COMPU_VTAB_RANGE {ident} {string} {int} {in_val_out_val}
    {default_value}
    /end COMPU_VTAB_RANGE'''])
@pytest.mark.parametrize('ident_string, ident_value', idents)
@pytest.mark.parametrize('string_string, string_value', strings)
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('in_val_out_val_string, in_val_out_val_value, in_val_out_val_count', [
    pytest.param('', [], 0, id='no in_val_out_val'),
    pytest.param('0.0 0.0 ""', [(0.0, 0.0, '')], 1, id='one in_val_out_val'),
    pytest.param('0.0 0.0 "" 0.0 0.0 ""', [(0.0, 0.0, ''), (0.0, 0.0, '')], 2, id='two in_val_out_val')])
def test_compu_vtab_range(s,
                          ident_string, ident_value,
                          string_string, string_value,
                          int_string, int_value,
                          in_val_out_val_string, in_val_out_val_value, in_val_out_val_count):
    p = Parser(project_string_minimal.format(module_string_minimal.format(s.format(
        ident=ident_string,
        string=string_string,
        int=int_string,
        default_value=empty_string,
        in_val_out_val=in_val_out_val_string))))
    compu_vtab_range = p.ast.project.module[0].compu_vtab_range[0]
    assert compu_vtab_range.name == ident_value
    assert compu_vtab_range.long_identifier == string_value
    assert compu_vtab_range.number_value_triple == int_value
    assert type(compu_vtab_range.in_val_out_val) is list
    assert compu_vtab_range.in_val_out_val == in_val_out_val_value
    assert compu_vtab_range.default_value is None


@pytest.mark.parametrize('module', [pytest.param(['mod_par', 'cpu_type'], id='MOD_PAR')], indirect=True)
@pytest.mark.parametrize('s', [pytest.param('CPU_TYPE {}')])
@pytest.mark.parametrize('string_string, string_value', strings)
def test_cpu_type(module, s, string_string, string_value):
    p = Parser(module[0].format(s.format(string_string)))
    cpu_type = get_node_from_ast(p.ast, module[1])
    assert cpu_type == string_value


@pytest.mark.parametrize('module', [
    pytest.param(['characteristic', 0, 'axis_descr', 0, 'curve_axis_ref'], id='AXIS_DESCR')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('CURVE_AXIS_REF {}')])
@pytest.mark.parametrize('s, v', idents)
def test_curve_axis_ref(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    curve_axis_ref = get_node_from_ast(p.ast, module[1])
    assert curve_axis_ref == v


@pytest.mark.parametrize('module', [pytest.param(['mod_par', 'customer'], id='MOD_PAR')], indirect=True)
@pytest.mark.parametrize('s', [pytest.param('CUSTOMER {}')])
@pytest.mark.parametrize('string_string, string_value', strings)
def test_customer(module, s, string_string, string_value):
    p = Parser(module[0].format(s.format(string_string)))
    customer = get_node_from_ast(p.ast, module[1])
    assert customer == string_value


@pytest.mark.parametrize('module', [pytest.param(['mod_par', 'customer_no'], id='MOD_PAR')], indirect=True)
@pytest.mark.parametrize('s', [pytest.param('CUSTOMER_NO {}')])
@pytest.mark.parametrize('string_string, string_value', strings)
def test_customer_no(module, s, string_string, string_value):
    p = Parser(module[0].format(s.format(string_string)))
    customer_no = get_node_from_ast(p.ast, module[1])
    assert customer_no == string_value


@pytest.mark.parametrize('module', [pytest.param(['mod_common', 'data_size'], id='MOD_COMMON')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('DATA_SIZE {}')])
@pytest.mark.parametrize('s, v', ints)
def test_data_size(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    data_size = get_node_from_ast(p.ast, module[1])
    assert data_size == v


@pytest.mark.parametrize('module', [
    pytest.param(['compu_tab', 0, 'default_value'], id='COMPU_TAB'),
    pytest.param(['compu_vtab', 0, 'default_value'], id='COMPU_VTAB'),
    pytest.param(['compu_vtab_range', 0, 'default_value'], id='COMPU_VTAB_RANGE')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('DEFAULT_VALUE {}')])
@pytest.mark.parametrize('s, v', strings)
def test_default_value(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    default_value = get_node_from_ast(p.ast, module[1])
    assert default_value == v


@pytest.mark.parametrize('module', [pytest.param(['function', 0, 'def_characteristic'], id='FUNCTION')], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('/begin DEF_CHARACTERISTIC /end DEF_CHARACTERISTIC', 0, id='no identifier'),
    pytest.param('/begin DEF_CHARACTERISTIC {ident} /end DEF_CHARACTERISTIC', 1, id='one identifier'),
    pytest.param('/begin DEF_CHARACTERISTIC {ident} {ident} /end DEF_CHARACTERISTIC', 2, id='two identifier')])
@pytest.mark.parametrize('s, v', idents)
def test_def_characteristic(module, e, count, s, v):
    p = Parser(module[0].format(e.format(ident=s)))
    def_characteristic = get_node_from_ast(p.ast, module[1])
    assert type(def_characteristic.identifier) is list
    assert len(def_characteristic.identifier) == count
    for identifier in def_characteristic.identifier:
        assert identifier == v


@pytest.mark.parametrize('module', [
    pytest.param(['characteristic', 0, 'dependent_characteristic'], id='CHARACTERISTIC')], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('/begin DEPENDENT_CHARACTERISTIC {string} /end DEPENDENT_CHARACTERISTIC', 0,
                 id='no characteristic', marks=pytest.mark.xfail(raises=A2lFormatException, strict=True)),
    pytest.param('/begin DEPENDENT_CHARACTERISTIC {string} {ident} /end DEPENDENT_CHARACTERISTIC', 1,
                 id='one characteristic'),
    pytest.param('/begin DEPENDENT_CHARACTERISTIC {string} {ident} {ident} /end DEPENDENT_CHARACTERISTIC', 2,
                 id='two characteristic')])
@pytest.mark.parametrize('string_string, string_value', strings)
@pytest.mark.parametrize('ident_string, ident_value', idents)
def test_dependent_characteristic(module, e, count, string_string, string_value, ident_string, ident_value):
    p = Parser(module[0].format(e.format(string=string_string, ident=ident_string)))
    dependent_characteristic = get_node_from_ast(p.ast, module[1])
    assert dependent_characteristic.formula == string_value
    assert type(dependent_characteristic.characteristic) is list
    assert len(dependent_characteristic.characteristic) == count
    for characteristic in dependent_characteristic.characteristic:
        assert characteristic == ident_value


@pytest.mark.parametrize('module', [
    pytest.param(['mod_common', 'deposit'], id='MOD_COMMON'),
    pytest.param(['characteristic', 0, 'axis_descr', 0, 'deposit'], id='AXIS_DESCR'),
    pytest.param(['axis_pts', 0, 'deposit'], id='AXIS_PTS')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('DEPOSIT {}')])
@pytest.mark.parametrize('s, v', enum_mode_deposit)
def test_deposit(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    deposit = get_node_from_ast(p.ast, module[1])
    assert deposit == v


@pytest.mark.parametrize('module', [
    pytest.param(['measurement', 0, 'display_identifier'], id='MEASUREMENT'),
    pytest.param(['characteristic', 0, 'display_identifier'], id='CHARACTERISTIC'),
    pytest.param(['axis_pts', 0, 'display_identifier'], id='AXIS_PTS')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('DISPLAY_IDENTIFIER {}')])
@pytest.mark.parametrize('s, v', idents)
def test_display_identifier(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    display_identifier = get_node_from_ast(p.ast, module[1])
    assert display_identifier == v


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'dist_op_x'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['DIST_OP_X {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_dist_op_x(module,
                   s,
                   int_string, int_value,
                   data_type_string, data_type_value):
    p = Parser(module[0].format(s.format(int=int_string,
                                         data_type=data_type_string)))
    dist_op_x = get_node_from_ast(p.ast, module[1])
    assert dist_op_x.position == int_value
    assert dist_op_x.data_type == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'dist_op_y'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['DIST_OP_Y {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_dist_op_y(module,
                   s,
                   int_string, int_value,
                   data_type_string, data_type_value):
    p = Parser(module[0].format(s.format(int=int_string,
                                         data_type=data_type_string)))
    dist_op_y = get_node_from_ast(p.ast, module[1])
    assert dist_op_y.position == int_value
    assert dist_op_y.data_type == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'dist_op_z'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['DIST_OP_Z {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_dist_op_z(module,
                   s,
                   int_string, int_value,
                   data_type_string, data_type_value):
    p = Parser(module[0].format(s.format(int=int_string,
                                         data_type=data_type_string)))
    dist_op_z = get_node_from_ast(p.ast, module[1])
    assert dist_op_z.position == int_value
    assert dist_op_z.data_type == data_type_value


@pytest.mark.parametrize('module', [pytest.param(['mod_par', 'ecu'], id='MOD_PAR')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('ECU {}')])
@pytest.mark.parametrize('s, v', strings)
def test_ecu(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    ecu = get_node_from_ast(p.ast, module[1])
    assert ecu == v


@pytest.mark.parametrize('module', [pytest.param(['measurement', 0, 'ecu_address'], id='MEASUREMENT')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('ECU_ADDRESS {}')])
@pytest.mark.parametrize('s, v', longs)
def test_ecu_address(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    ecu_address = get_node_from_ast(p.ast, module[1])
    assert ecu_address == v


@pytest.mark.parametrize('module', [
    pytest.param(['characteristic', 0, 'ecu_address_extension'], id='CHARACTERISTIC'),
    pytest.param(['measurement', 0, 'ecu_address_extension'], id='MEASUREMENT'),
    pytest.param(['axis_pts', 0, 'ecu_address_extension'], id='AXIS_PTS')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('ECU_ADDRESS_EXTENSION {}')])
@pytest.mark.parametrize('s, v', ints)
def test_ecu_address_extension(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    ecu_address_extension = get_node_from_ast(p.ast, module[1])
    assert ecu_address_extension == v


@pytest.mark.parametrize('module', [pytest.param(['mod_par', 'ecu_calibration_offset'], id='MOD_PAR')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('ECU_CALIBRATION_OFFSET {}')])
@pytest.mark.parametrize('s, v', longs)
def test_ecu_calibration_offset(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    ecu_calibration_offset = get_node_from_ast(p.ast, module[1])
    assert ecu_calibration_offset == v


@pytest.mark.parametrize('module', [pytest.param(['mod_par', 'epk'], id='MOD_PAR')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('EPK {}')])
@pytest.mark.parametrize('s, v', strings)
def test_epk(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    epk = get_node_from_ast(p.ast, module[1])
    assert epk == v


@pytest.mark.parametrize('module', [pytest.param(['measurement', 0, 'error_mask'], id='MEASUREMENT')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('ERROR_MASK {}')])
@pytest.mark.parametrize('s, v', longs)
def test_error_mask(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    error_mask = get_node_from_ast(p.ast, module[1])
    assert error_mask == v


@pytest.mark.parametrize('module', [
    pytest.param(['characteristic', 0, 'axis_descr', 0, 'extended_limits'], id='AXIS_DESCR'),
    pytest.param(['axis_pts', 0, 'extended_limits'], id='AXIS_PTS')], indirect=True)
@pytest.mark.parametrize('e', ['EXTENDED_LIMITS {float} {float}'])
@pytest.mark.parametrize('s, v', floats)
def test_extended_limits(module, e, s, v):
    p = Parser(module[0].format(e.format(float=s)))
    extended_limits = get_node_from_ast(p.ast, module[1])
    assert extended_limits.lower_limit == v
    assert extended_limits.upper_limit == v


@pytest.mark.parametrize('module', [
    pytest.param(['characteristic', 0, 'axis_descr', 0, 'fix_axis_par'], id='AXIS_DESCR')], indirect=True)
@pytest.mark.parametrize('e', ['FIX_AXIS_PAR {int} {int} {int}'])
@pytest.mark.parametrize('s, v', ints)
def test_fix_axis_par(module, e, s, v):
    p = Parser(module[0].format(e.format(int=s)))
    fix_axis_par = get_node_from_ast(p.ast, module[1])
    assert fix_axis_par.offset == v
    assert fix_axis_par.shift == v
    assert fix_axis_par.numberapo == v


@pytest.mark.parametrize('module', [
    pytest.param(['characteristic', 0, 'axis_descr', 0, 'fix_axis_par_dist'], id='AXIS_DESCR')], indirect=True)
@pytest.mark.parametrize('e', ['FIX_AXIS_PAR_DIST {int} {int} {int}'])
@pytest.mark.parametrize('s, v', ints)
def test_fix_axis_par_dist(module, e, s, v):
    p = Parser(module[0].format(e.format(int=s)))
    fix_axis_par_dist = get_node_from_ast(p.ast, module[1])
    assert fix_axis_par_dist.offset == v
    assert fix_axis_par_dist.distance == v
    assert fix_axis_par_dist.numberapo == v


@pytest.mark.parametrize('module', [
    pytest.param(['characteristic', 0, 'axis_descr', 0, 'fix_axis_par_list'], id='AXIS_DESCR')], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('/begin FIX_AXIS_PAR_LIST /end FIX_AXIS_PAR_LIST', 0, id='no axis_pts_value'),
    pytest.param('/begin FIX_AXIS_PAR_LIST {float} /end FIX_AXIS_PAR_LIST', 1, id='one axis_pts_value'),
    pytest.param('/begin FIX_AXIS_PAR_LIST {float} {float} /end FIX_AXIS_PAR_LIST', 2, id='two axis_pts_value')])
@pytest.mark.parametrize('s, v', floats)
def test_fix_axis_par_list(module, e, count, s, v):
    p = Parser(module[0].format(e.format(float=s)))
    fix_axis_par_list = get_node_from_ast(p.ast, module[1])
    assert type(fix_axis_par_list.axis_pts_value) is list
    assert len(fix_axis_par_list.axis_pts_value) == count
    for axis_pts_value in fix_axis_par_list.axis_pts_value:
        assert axis_pts_value == v


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'fix_no_axis_pts_x'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', ['FIX_NO_AXIS_PTS_X {}'])
@pytest.mark.parametrize('s, v', ints)
def test_fix_no_axis_pts_x(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    fix_no_axis_pts_x = get_node_from_ast(p.ast, module[1])
    assert fix_no_axis_pts_x == v


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'fix_no_axis_pts_y'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', ['FIX_NO_AXIS_PTS_Y {}'])
@pytest.mark.parametrize('s, v', ints)
def test_fix_no_axis_pts_y(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    fix_no_axis_pts_y = get_node_from_ast(p.ast, module[1])
    assert fix_no_axis_pts_y == v


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'fix_no_axis_pts_z'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', ['FIX_NO_AXIS_PTS_Z {}'])
@pytest.mark.parametrize('s, v', ints)
def test_fix_no_axis_pts_z(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    fix_no_axis_pts_z = get_node_from_ast(p.ast, module[1])
    assert fix_no_axis_pts_z == v


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'fnc_values'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['FNC_VALUES {int} {data_type} {enum_index_mode} {addr_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
@pytest.mark.parametrize('enum_index_mode_string, enum_index_mode_value', enum_index_mode_fnc_values_strings)
@pytest.mark.parametrize('addr_type_string, addr_type_value', addr_types)
def test_fnc_values(module,
                    s,
                    int_string, int_value,
                    data_type_string, data_type_value,
                    enum_index_mode_string, enum_index_mode_value,
                    addr_type_string, addr_type_value):
    p = Parser(module[0].format(s.format(int=int_string,
                                         data_type=data_type_string,
                                         enum_index_mode=enum_index_mode_string,
                                         addr_type=addr_type_string)))
    fnc_values = get_node_from_ast(p.ast, module[1])
    assert fnc_values.position == int_value
    assert fnc_values.data_type == data_type_value
    assert fnc_values.index_mode == enum_index_mode_value
    assert fnc_values.addr_type == addr_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['characteristic', 0, 'format'], id='MOD_PAR'),
    pytest.param(['characteristic', 0, 'axis_descr', 0, 'format'], id='AXIS_DESCR'),
    pytest.param(['measurement', 0, 'format'], id='MEASUREMENT'),
    pytest.param(['axis_pts', 0, 'format'], id='AXIS_PTS')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('FORMAT {}')])
@pytest.mark.parametrize('s, v', strings)
def test_format(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    format_ = get_node_from_ast(p.ast, module[1])
    assert format_ == v


@pytest.mark.parametrize('module', [pytest.param(['compu_method', 0, 'formula'], id='COMPU_METHOD')], indirect=True)
@pytest.mark.parametrize('e', ['/begin FORMULA {} /end FORMULA'])
@pytest.mark.parametrize('s, v', strings)
def test_formula(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    formula = get_node_from_ast(p.ast, module[1])
    assert formula.f == v
    assert formula.formula_inv is None


@pytest.mark.parametrize('compu_method', [pytest.param(['formula', 'formula_inv'], id='COMPU_METHOD')], indirect=True)
@pytest.mark.parametrize('e', ['FORMULA_INV {}'])
@pytest.mark.parametrize('s, v', strings)
def test_formula_inv(compu_method, e, s, v):
    p = Parser(compu_method[0].format(e.format(s)))
    formula_inv = get_node_from_ast(p.ast, compu_method[1])
    assert formula_inv == v


@pytest.mark.parametrize('s', ['''
    /begin FRAME {ident} {string} {int} {long}
    {frame_measurement}
    {if_data}
    /end FRAME'''])
@pytest.mark.parametrize('ident_string, ident_value', idents)
@pytest.mark.parametrize('string_string, string_value', strings)
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('long_string, long_value', longs)
def test_frame(s,
               ident_string, ident_value,
               string_string, string_value,
               int_string, int_value,
               long_string, long_value):
    p = Parser(project_string_minimal.format(module_string_minimal.format(s.format(
        ident=ident_string,
        string=string_string,
        int=int_string,
        long=long_string,
        frame_measurement=empty_string,
        if_data=empty_string))))
    frame = p.ast.project.module[0].frame
    assert frame.name == ident_value
    assert frame.long_identifier == string_value
    assert frame.scaling_unit == int_value
    assert frame.rate == long_value
    assert frame.frame_measurement is None


@pytest.mark.parametrize('module', [pytest.param(['frame', 'frame_measurement'], id='FRAME')], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('FRAME_MEASUREMENT', 0, id='no identifier'),
    pytest.param('FRAME_MEASUREMENT {ident}', 1, id='one identifier'),
    pytest.param('FRAME_MEASUREMENT {ident} {ident}', 2, id='two identifier')])
@pytest.mark.parametrize('s, v', idents)
def test_frame_measurement(module, e, count, s, v):
    p = Parser(module[0].format(e.format(ident=s)))
    frame_measurement = get_node_from_ast(p.ast, module[1])
    assert type(frame_measurement.identifier) is list
    assert len(frame_measurement.identifier) == count
    for identifier in frame_measurement.identifier:
        assert identifier == v


@pytest.mark.parametrize('s', ['''
    /begin FUNCTION {ident} {string}
    {annotation}
    {def_characteristic}
    {ref_characteristic}
    {in_measurement}
    {out_measurement}
    {loc_measurement}
    {sub_function}
    {function_version}
    /end FUNCTION'''])
@pytest.mark.parametrize('ident_string, ident_value', idents)
@pytest.mark.parametrize('string_string, string_value', strings)
def test_function(s, ident_string, ident_value, string_string, string_value):
    p = Parser(project_string_minimal.format(module_string_minimal.format(s.format(
        ident=ident_string,
        string=string_string,
        annotation=empty_string,
        def_characteristic=empty_string,
        ref_characteristic=empty_string,
        in_measurement=empty_string,
        out_measurement=empty_string,
        loc_measurement=empty_string,
        sub_function=empty_string,
        function_version=empty_string))))
    function = p.ast.project.module[0].function[0]
    assert function.name == ident_value
    assert function.long_identifier == string_value
    assert type(function.annotation) is list
    assert function.def_characteristic is None
    assert function.ref_characteristic is None
    assert function.in_measurement is None
    assert function.out_measurement is None
    assert function.loc_measurement is None
    assert function.sub_function is None
    assert function.function_version is None


@pytest.mark.parametrize('module', [
    pytest.param(['axis_pts', 0, 'function_list'], id='AXIS_PTS'),
    pytest.param(['characteristic', 0, 'function_list'], id='CHARACTERISTIC'),
    pytest.param(['measurement', 0, 'function_list'], id='MEASUREMENT'),
    pytest.param(['group', 0, 'function_list'], id='GROUP')], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('/begin FUNCTION_LIST /end FUNCTION_LIST', None,
                 id='no name', marks=pytest.mark.xfail(raises=A2lFormatException, strict=True)),
    pytest.param('/begin FUNCTION_LIST {ident} /end FUNCTION_LIST', 1, id='one name'),
    pytest.param('/begin FUNCTION_LIST {ident} {ident} /end FUNCTION_LIST', 2, id='two name')])
@pytest.mark.parametrize('s, v', idents)
def test_function_list(module, e, count, s, v):
    p = Parser(module[0].format(e.format(ident=s)))
    function_list = get_node_from_ast(p.ast, module[1])
    assert len(function_list.name) == count
    for name in function_list.name:
        assert name == v


@pytest.mark.parametrize('module', [pytest.param(['function', 0, 'function_version'], id='FUNCTION')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('FUNCTION_VERSION {}')])
@pytest.mark.parametrize('s, v', strings)
def test_function_version(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    function_version = get_node_from_ast(p.ast, module[1])
    assert function_version == v


@pytest.mark.parametrize('s', ['''
    /begin GROUP {ident} {string}
    {annotation}
    {root}
    {ref_characteristic}
    {ref_measurement}
    {function_list}
    {sub_group}
    /end GROUP'''])
@pytest.mark.parametrize('ident_string, ident_value', idents)
@pytest.mark.parametrize('string_string, string_value', strings)
def test_group(s, ident_string, ident_value, string_string, string_value):
    p = Parser(project_string_minimal.format(module_string_minimal.format(s.format(
        ident=ident_string,
        string=string_string,
        annotation=empty_string,
        root=empty_string,
        ref_characteristic=empty_string,
        ref_measurement=empty_string,
        function_list=empty_string,
        sub_group=empty_string))))
    group = p.ast.project.module[0].group[0]
    assert group.group_name == ident_value
    assert group.group_long_identifier == string_value
    assert type(group.annotation) is list
    assert group.root is None
    assert group.ref_characteristic is None
    assert group.ref_measurement is None
    assert group.function_list is None
    assert group.sub_group is None


@pytest.mark.parametrize('module', [
    pytest.param(['characteristic', 0, 'guard_rails'], id='CHARACTERISTIC'),
    pytest.param(['axis_pts', 0, 'guard_rails'], id='AXIS_PTS')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('GUARD_RAILS')])
def test_guard_rails(module, e):
    p = Parser(module[0].format(e))
    guard_rails = get_node_from_ast(p.ast, module[1])
    assert guard_rails == e


# TODO: check if fully tested.
@pytest.mark.parametrize('e', ['/begin HEADER {string} {version} {project_no} /end HEADER'])
@pytest.mark.parametrize('s, v', strings)
def test_header(e, s, v):
    p = Parser(project_string_minimal.format(e.format(string=s,
                                                      version=empty_string,
                                                      project_no=empty_string)))
    assert p.ast.project.header.comment == v
    assert p.ast.project.header.version is None
    assert p.ast.project.header.project_no is None


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'identification'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', ['IDENTIFICATION {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_identification(module,
                        e,
                        int_string, int_value,
                        data_type_string, data_type_value):
    p = Parser(module[0].format(e.format(int=int_string, data_type=data_type_string)))
    identification = get_node_from_ast(p.ast, module[1])
    assert identification.position == int_value
    assert identification.data_type == data_type_value


@pytest.mark.parametrize('module', [pytest.param(['function', 0, 'in_measurement'], id='FUNCTION')], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('/begin IN_MEASUREMENT /end IN_MEASUREMENT', 0, id='no identifier'),
    pytest.param('/begin IN_MEASUREMENT {ident} /end IN_MEASUREMENT', 1, id='one identifier'),
    pytest.param('/begin IN_MEASUREMENT {ident} {ident} /end IN_MEASUREMENT', 2, id='two identifier')])
@pytest.mark.parametrize('s, v', idents)
def test_in_measurement(module, e, count, s, v):
    p = Parser(module[0].format(e.format(ident=s)))
    in_measurement = get_node_from_ast(p.ast, module[1])
    assert type(in_measurement.identifier) is list
    assert len(in_measurement.identifier) == count
    for identifier in in_measurement.identifier:
        assert identifier == v


@pytest.mark.parametrize('module', [
    pytest.param(['measurement', 0, 'bit_operation', 'left_shift'], id='MEASUREMENT')], indirect=True)
@pytest.mark.parametrize('e', ['LEFT_SHIFT {}'])
@pytest.mark.parametrize('s, v', longs)
def test_left_shift(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    left_shift = get_node_from_ast(p.ast, module[1])
    assert left_shift == v


@pytest.mark.parametrize('module', [pytest.param(['function', 0, 'loc_measurement'], id='FUNCTION'), ], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('/begin LOC_MEASUREMENT /end LOC_MEASUREMENT', 0, id='no identifier'),
    pytest.param('/begin LOC_MEASUREMENT {ident} /end LOC_MEASUREMENT', 1, id='one identifier'),
    pytest.param('/begin LOC_MEASUREMENT {ident} {ident} /end LOC_MEASUREMENT', 2, id='two identifier')])
@pytest.mark.parametrize('s, v', idents)
def test_loc_measurement(module, e, count, s, v):
    p = Parser(module[0].format(e.format(ident=s)))
    loc_measurement = get_node_from_ast(p.ast, module[1])
    assert type(loc_measurement.identifier) is list
    assert len(loc_measurement.identifier) == count
    for identifier in loc_measurement.identifier:
        assert identifier == v


@pytest.mark.parametrize('module', [
    pytest.param(['characteristic', 0, 'map_list'], id='CHARACTERISTIC')], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('/begin MAP_LIST /end MAP_LIST', 0, id='no ident'),
    pytest.param('/begin MAP_LIST {ident} /end MAP_LIST', 1, id='one ident'),
    pytest.param('/begin MAP_LIST {ident} {ident} /end MAP_LIST', 2, id='two ident')])
@pytest.mark.parametrize('s, v', idents)
def test_map_list(module, e, count, s, v):
    p = Parser(module[0].format(e.format(ident=s)))
    map_list = get_node_from_ast(p.ast, module[1])
    assert len(map_list.name) == count
    for name in map_list.name:
        assert name == v


@pytest.mark.parametrize('module', [
    pytest.param(['measurement', 0, 'matrix_dim'], id='MEASUREMENT'),
    pytest.param(['characteristic', 0, 'matrix_dim'], id='CHARACTERISTIC')], indirect=True)
@pytest.mark.parametrize('e', ['MATRIX_DIM {int} {int} {int}'])
@pytest.mark.parametrize('s, v', ints)
def test_matrix_dim(module, e, s, v):
    p = Parser(module[0].format(e.format(int=s)))
    matrix_dim = get_node_from_ast(p.ast, module[1])
    assert matrix_dim.x == v
    assert matrix_dim.y == v
    assert matrix_dim.z == v


@pytest.mark.parametrize('module', [
    pytest.param(['characteristic', 0, 'axis_descr', 0, 'max_grad'], id='AXIS_DESCR')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('MAX_GRAD {}')])
@pytest.mark.parametrize('s, v', floats)
def test_max_grad(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    max_grad = get_node_from_ast(p.ast, module[1])
    assert max_grad == v


@pytest.mark.parametrize('module', [
    pytest.param(['characteristic', 0, 'max_refresh'], id='CHARACTERISTIC'),
    pytest.param(['measurement', 0, 'max_refresh'], id='MEASUREMENT')], indirect=True)
@pytest.mark.parametrize('s', max_refresh_strings)
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('long_string, long_value', longs)
def test_max_refresh(module, s, int_string, int_value, long_string, long_value):
    p = Parser(module[0].format(s.format(int=int_string, long=long_string)))
    max_refresh = get_node_from_ast(p.ast, module[1])
    assert max_refresh.scaling_unit == int_value
    assert max_refresh.rate == long_value


@pytest.mark.parametrize('s', ['''
    /begin MEASUREMENT {ident} {string} {data_type} {ident} {int} {float} {float} {float}
    {display_identifier}
    {read_write}
    {format}
    {array_size}
    {bit_mask}
    {bit_operation}
    {byte_order}
    {max_refresh}
    {virtual}
    {function_list}
    {ecu_address}
    {error_mask}
    {ref_memory_segment}
    {annotation}
    {if_data}
    {matrix_dim}
    {ecu_address_extension}
    /end MEASUREMENT'''])
@pytest.mark.parametrize('ident_string, ident_value', idents)
@pytest.mark.parametrize('string_string, string_value', strings)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('float_string, float_value', floats)
def test_measurement(s,
                     ident_string, ident_value,
                     string_string, string_value,
                     data_type_string, data_type_value,
                     int_string, int_value,
                     float_string, float_value):
    p = Parser(project_string_minimal.format(module_string_minimal.format(s.format(
        ident=ident_string,
        string=string_string,
        data_type=data_type_string,
        int=int_string,
        float=float_string,
        display_identifier=empty_string,
        read_write=empty_string,
        format=empty_string,
        array_size=empty_string,
        bit_mask=empty_string,
        bit_operation=empty_string,
        byte_order=empty_string,
        max_refresh=empty_string,
        virtual=empty_string,
        error_mask=empty_string,
        function_list=empty_string,
        if_data=empty_string,
        ecu_address=empty_string,
        ref_memory_segment=empty_string,
        annotation=empty_string,
        matrix_dim=empty_string,
        ecu_address_extension=empty_string))))
    measurement = p.ast.project.module[0].measurement[0]
    assert measurement.name == ident_value
    assert measurement.long_identifier == string_value
    assert measurement.data_type == data_type_value
    assert measurement.conversion == ident_value
    assert measurement.resolution == int_value
    assert measurement.accuracy == float_value
    assert measurement.lower_limit == float_value
    assert measurement.upper_limit == float_value
    assert measurement.display_identifier is None
    assert measurement.read_write is None
    assert measurement.format is None
    assert measurement.array_size is None
    assert measurement.bit_mask is None
    assert measurement.bit_operation is None
    assert measurement.byte_order is None
    assert measurement.max_refresh is None
    assert measurement.virtual is None
    assert measurement.error_mask is None
    assert measurement.function_list is None
    assert measurement.ecu_address is None
    assert measurement.ref_memory_segment is None
    assert type(measurement.annotation) is list
    assert measurement.matrix_dim is None
    assert measurement.ecu_address_extension is None


@pytest.mark.parametrize('module', [pytest.param(['mod_par', 'memory_layout', 0], id='MOD_PAR')], indirect=True)
@pytest.mark.parametrize('s', memory_layout_strings)
@pytest.mark.parametrize('enum_prg_type_string, enum_prg_type_value', enum_prg_type_memory_layout_strings)
@pytest.mark.parametrize('long_string, long_value', longs)
@pytest.mark.parametrize('offset_string, offset_value', offset_strings)
def test_memory_layout(module,
                       s,
                       enum_prg_type_string, enum_prg_type_value,
                       long_string, long_value,
                       offset_string, offset_value):
    p = Parser(module[0].format(s.format(enum_prg_type=enum_prg_type_string,
                                         long=long_string,
                                         offset=offset_string,
                                         if_data=empty_string)))
    memory_layout = get_node_from_ast(p.ast, module[1])
    assert memory_layout.prg_type == enum_prg_type_value
    assert memory_layout.address == long_value
    assert memory_layout.size == long_value
    assert memory_layout.offset == offset_value


@pytest.mark.parametrize('module', [pytest.param(['mod_par', 'memory_segment', 0], id='MOD_PAR')], indirect=True)
@pytest.mark.parametrize('s', ['''
    /begin MEMORY_SEGMENT {ident} {string} {enum_prg_type} {enum_memory_type} {enum_attribute} {long} {long} {offset}
    {if_data}
    /end MEMORY_SEGMENT'''])
@pytest.mark.parametrize('ident_string, ident_value', idents)
@pytest.mark.parametrize('string_string, string_value', strings)
@pytest.mark.parametrize('enum_prg_type_string, enum_prg_type_value', enum_prg_type_memory_segment_strings)
@pytest.mark.parametrize('enum_memory_type_string, enum_memory_type_value', enum_memory_type_strings)
@pytest.mark.parametrize('enum_attribute_string, enum_attribute_value', enum_attribute_memory_segment_strings)
@pytest.mark.parametrize('long_string, long_value', longs)
@pytest.mark.parametrize('offset_string, offset_value', offset_strings)
def test_memory_segment(module,
                        s,
                        ident_string, ident_value,
                        string_string, string_value,
                        enum_prg_type_string, enum_prg_type_value,
                        enum_memory_type_string, enum_memory_type_value,
                        enum_attribute_string, enum_attribute_value,
                        long_string, long_value,
                        offset_string, offset_value):
    p = Parser(module[0].format(s.format(ident=ident_string,
                                         string=string_string,
                                         enum_prg_type=enum_prg_type_string,
                                         enum_memory_type=enum_memory_type_string,
                                         enum_attribute=enum_attribute_string,
                                         long=long_string,
                                         offset=offset_string,
                                         if_data=empty_string)))
    memory_segment = get_node_from_ast(p.ast, module[1])
    assert memory_segment.name == ident_value
    assert memory_segment.long_identifier == string_value
    assert memory_segment.prg_type == enum_prg_type_value
    assert memory_segment.memory_type == enum_memory_type_value
    assert memory_segment.attribute == enum_attribute_value
    assert memory_segment.address == long_value
    assert memory_segment.size == long_value
    assert memory_segment.offset == offset_value


@pytest.mark.parametrize('s', ['''
    /begin MODULE {ident} {string}
    {a2ml}
    {mod_par}
    {mod_common}
    {if_data}
    {characteristic}
    {axis_pts}
    {measurement}
    {compu_method}
    {compu_tab}
    {compu_vtab}
    {compu_vtab_range}
    {function}
    {group}
    {record_layout}
    {variant_coding}
    {frame}
    {user_rights}
    {unit}
    /end MODULE'''])
@pytest.mark.parametrize('ident_string, ident_value', idents)
@pytest.mark.parametrize('string_string, string_value', strings)
def test_module(s, ident_string, ident_value, string_string, string_value):
    p = Parser(project_string_minimal.format(s.format(ident=ident_string,
                                                      string=string_string,
                                                      a2ml=empty_string,
                                                      mod_par=empty_string,
                                                      mod_common=empty_string,
                                                      if_data=empty_string,
                                                      characteristic=empty_string,
                                                      axis_pts=empty_string,
                                                      measurement=empty_string,
                                                      compu_method=empty_string,
                                                      compu_tab=empty_string,
                                                      compu_vtab=empty_string,
                                                      compu_vtab_range=empty_string,
                                                      function=empty_string,
                                                      group=empty_string,
                                                      record_layout=empty_string,
                                                      variant_coding=empty_string,
                                                      frame=empty_string,
                                                      user_rights=empty_string,
                                                      unit=empty_string)))
    module = p.ast.project.module[0]
    assert module.name == ident_value
    assert module.long_identifier == string_value
    assert module.a2ml is None
    assert module.mod_par is None
    assert module.mod_common is None
    # assert type(module.if_data) is list
    assert type(module.characteristic) is list
    assert type(module.axis_pts) is list
    assert type(module.measurement) is list
    assert type(module.compu_method) is list
    assert type(module.compu_tab) is list
    assert type(module.compu_vtab) is list
    assert type(module.compu_vtab_range) is list
    assert type(module.function) is list
    assert type(module.group) is list
    assert type(module.record_layout) is list
    assert module.variant_coding is None
    assert module.frame is None
    assert type(module.user_rights) is list
    assert type(module.unit) is list


@pytest.mark.parametrize('s', ['''
    /begin MOD_COMMON {string}
    {s_rec_layout}
    {deposit}
    {byte_order}
    {data_size}
    {alignment_byte}
    {alignment_word}
    {alignment_long}
    {alignment_float32_ieee}
    {alignment_float64_ieee}
    /end MOD_COMMON'''])
@pytest.mark.parametrize('string_string, string_value', strings)
def test_mod_common(s, string_string, string_value):
    p = Parser(project_string_minimal.format(module_string_minimal.format(s.format(
        string=string_string,
        s_rec_layout=empty_string,
        deposit=empty_string,
        byte_order=empty_string,
        data_size=empty_string,
        alignment_byte=empty_string,
        alignment_word=empty_string,
        alignment_long=empty_string,
        alignment_float32_ieee=empty_string,
        alignment_float64_ieee=empty_string))))
    mod_common = p.ast.project.module[0].mod_common
    assert mod_common.comment == string_value
    assert mod_common.s_rec_layout is None
    assert mod_common.deposit is None
    assert mod_common.byte_order is None
    assert mod_common.data_size is None
    assert mod_common.alignment_byte is None
    assert mod_common.alignment_word is None
    assert mod_common.alignment_long is None
    assert mod_common.alignment_float32_ieee is None
    assert mod_common.alignment_float64_ieee is None


@pytest.mark.parametrize('s', ['''
    /begin MOD_PAR
    {string}
    {version}
    {addr_epk}
    {epk}
    {supplier}
    {customer}
    {customer_no}
    {user}
    {phone_no}
    {ecu}
    {cpu_type}
    {no_of_interfaces}
    {ecu_calibration_offset}
    {calibration_method}
    {memory_layout}
    {memory_segment}
    {system_constant}
    /end MOD_PAR'''])
@pytest.mark.parametrize('string_string, string_value', strings)
def test_mod_par(s, string_string, string_value):
    p = Parser(project_string_minimal.format(module_string_minimal.format(s.format(
        string=string_string,
        version=empty_string,
        addr_epk=empty_string,
        epk=empty_string,
        supplier=empty_string,
        customer=empty_string,
        customer_no=empty_string,
        user=empty_string,
        phone_no=empty_string,
        ecu=empty_string,
        cpu_type=empty_string,
        no_of_interfaces=empty_string,
        ecu_calibration_offset=empty_string,
        calibration_method=empty_string,
        memory_layout=empty_string,
        memory_segment=empty_string,
        system_constant=empty_string))))
    mod_par = p.ast.project.module[0].mod_par
    assert mod_par.comment == string_value
    assert mod_par.version is None
    assert type(mod_par.addr_epk) is list
    assert mod_par.epk is None
    assert mod_par.supplier is None
    assert mod_par.customer is None
    assert mod_par.customer_no is None
    assert mod_par.user is None
    assert mod_par.phone_no is None
    assert mod_par.ecu is None
    assert mod_par.cpu_type is None
    assert mod_par.no_of_interfaces is None
    assert mod_par.ecu_calibration_offset is None
    assert type(mod_par.calibration_method) is list
    assert type(mod_par.memory_layout) is list
    assert type(mod_par.memory_segment) is list
    assert type(mod_par.system_constant) is list


@pytest.mark.parametrize('module', [
    pytest.param(['characteristic', 0, 'axis_descr', 0, 'monotony'], id='AXIS_DESCR')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('MONOTONY {}')])
@pytest.mark.parametrize('s, v', enum_monotony)
def test_monotony(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    monotony = get_node_from_ast(p.ast, module[1])
    assert monotony == v


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'no_axis_pts_x'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['NO_AXIS_PTS_X {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_no_axis_pts_x(module, s, int_string, int_value, data_type_string, data_type_value):
    p = Parser(module[0].format(s.format(int=int_string, data_type=data_type_string)))
    no_axis_pts_x = get_node_from_ast(p.ast, module[1])
    assert no_axis_pts_x.position == int_value
    assert no_axis_pts_x.data_type == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'no_axis_pts_y'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['NO_AXIS_PTS_Y {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_no_axis_pts_y(module, s, int_string, int_value, data_type_string, data_type_value):
    p = Parser(module[0].format(s.format(int=int_string, data_type=data_type_string)))
    no_axis_pts_y = get_node_from_ast(p.ast, module[1])
    assert no_axis_pts_y.position == int_value
    assert no_axis_pts_y.data_type == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'no_axis_pts_z'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['NO_AXIS_PTS_Z {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_no_axis_pts_z(module, s, int_string, int_value, data_type_string, data_type_value):
    p = Parser(module[0].format(s.format(int=int_string, data_type=data_type_string)))
    no_axis_pts_z = get_node_from_ast(p.ast, module[1])
    assert no_axis_pts_z.position == int_value
    assert no_axis_pts_z.data_type == data_type_value


@pytest.mark.parametrize('module', [pytest.param(['mod_par', 'no_of_interfaces'], id='MOD_PAR')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('NO_OF_INTERFACES {}')])
@pytest.mark.parametrize('s, v', ints)
def test_no_of_interfaces(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    no_of_interfaces = get_node_from_ast(p.ast, module[1])
    assert no_of_interfaces == v


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'no_rescale_x'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['NO_RESCALE_X {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_no_rescale_x(module, s, int_string, int_value, data_type_string, data_type_value):
    p = Parser(module[0].format(s.format(int=int_string, data_type=data_type_string)))
    no_rescale_x = get_node_from_ast(p.ast, module[1])
    assert no_rescale_x.position == int_value
    assert no_rescale_x.data_type == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'no_rescale_y'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['NO_RESCALE_Y {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_no_rescale_y(module, s, int_string, int_value, data_type_string, data_type_value):
    p = Parser(module[0].format(s.format(int=int_string, data_type=data_type_string)))
    no_rescale_y = get_node_from_ast(p.ast, module[1])
    assert no_rescale_y.position == int_value
    assert no_rescale_y.data_type == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'no_rescale_z'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['NO_RESCALE_Z {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_no_rescale_z(module, s, int_string, int_value, data_type_string, data_type_value):
    p = Parser(module[0].format(s.format(int=int_string, data_type=data_type_string)))
    no_rescale_z = get_node_from_ast(p.ast, module[1])
    assert no_rescale_z.position == int_value
    assert no_rescale_z.data_type == data_type_value


@pytest.mark.parametrize('module', [pytest.param(['characteristic', 0, 'number'], id='CHARACTERISTIC')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('NUMBER {}')])
@pytest.mark.parametrize('s, v', ints)
def test_number(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    number = get_node_from_ast(p.ast, module[1])
    assert number == v


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'offset_x'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['OFFSET_X {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_offset_x(module, s, int_string, int_value, data_type_string, data_type_value):
    p = Parser(module[0].format(s.format(int=int_string, data_type=data_type_string)))
    offset_x = get_node_from_ast(p.ast, module[1])
    assert offset_x.position == int_value
    assert offset_x.data_type == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'offset_y'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['OFFSET_Y {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_offset_y(module, s, int_string, int_value, data_type_string, data_type_value):
    p = Parser(module[0].format(s.format(int=int_string, data_type=data_type_string)))
    offset_y = get_node_from_ast(p.ast, module[1])
    assert offset_y.position == int_value
    assert offset_y.data_type == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'offset_z'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['OFFSET_Z {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_offset_z(module, s, int_string, int_value, data_type_string, data_type_value):
    p = Parser(module[0].format(s.format(int=int_string, data_type=data_type_string)))
    offset_z = get_node_from_ast(p.ast, module[1])
    assert offset_z.position == int_value
    assert offset_z.data_type == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['function', 0, 'out_measurement'], id='FUNCTION'), ], indirect=True)
@pytest.mark.parametrize('s, identifier_count', out_measurement_strings)
@pytest.mark.parametrize('ident_string, ident_value', idents)
def test_out_measurement(module, s, identifier_count, ident_string, ident_value):
    p = Parser(module[0].format(s.format(ident=ident_string)))
    out_measurement = get_node_from_ast(p.ast, module[1])
    assert type(out_measurement.identifier) is list
    assert len(out_measurement.identifier) == identifier_count
    for identifier in out_measurement.identifier:
        assert identifier == ident_value


@pytest.mark.parametrize('module', [pytest.param(['mod_par', 'phone_no'], id='MOD_PAR')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('PHONE_NO {}')])
@pytest.mark.parametrize('s, v', strings)
def test_phone_no(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    phone_no = get_node_from_ast(p.ast, module[1])
    assert phone_no == v


@pytest.mark.parametrize('s', project_strings)
@pytest.mark.parametrize('ident_string, ident_value', idents)
@pytest.mark.parametrize('string_string, string_value', strings)
@pytest.mark.parametrize('header_string', [
    pytest.param(0, id='no HEADER'),
    pytest.param(1, id='one HEADER'),
    pytest.param(2, id='two HEADER', marks=pytest.mark.xfail(raises=A2lFormatException, reason='not implemented'))
], indirect=True)
@pytest.mark.parametrize('module_string', [
    pytest.param(0, id='no MODULE'),
    pytest.param(1, id='one MODULE'),
    pytest.param(2, id='two MODULE')
], indirect=True)
def test_project(s, ident_string, ident_value, string_string, string_value, header_string, module_string):
    p = Parser(s.format(ident=ident_string,
                        string=string_string,
                        header=header_string,
                        module=module_string))
    assert p.ast.project.name == ident_value
    assert p.ast.project.long_identifier == string_value


@pytest.mark.parametrize('project', [pytest.param(['header', 'project_no'], id='HEADER')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('PROJECT_NO {}')])
@pytest.mark.parametrize('s, v', idents)
def test_project_no(project, e, s, v):
    p = Parser(project[0].format(e.format(s)))
    project_no = get_node_from_ast(p.ast, project[1])
    assert project_no == v


@pytest.mark.parametrize('module', [
    pytest.param(['characteristic', 0, 'read_only'], id='CHARACTERISTIC'),
    pytest.param(['axis_pts', 0, 'read_only'], id='AXIS_PTS'),
    pytest.param(['characteristic', 0, 'axis_descr', 0, 'read_only'], id='AXIS_DESCR'),
    pytest.param(['user_rights', 0, 'read_only'], id='USER_RIGHTS')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('READ_ONLY')])
def test_read_only(module, e):
    p = Parser(module[0].format(e))
    read_only = get_node_from_ast(p.ast, module[1])
    assert read_only == e


@pytest.mark.parametrize('module', [pytest.param(['measurement', 0, 'read_write'], id='MEASUREMENT')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('READ_WRITE')])
def test_read_write(module, e):
    p = Parser(module[0].format(e))
    read_write = get_node_from_ast(p.ast, module[1])
    assert read_write == e


@pytest.mark.parametrize('s', ['''
    /begin RECORD_LAYOUT
    {ident}
    {fnc_values}
    {identification}
    {axis_pts_x}
    {axis_pts_y}
    {axis_pts_z}
    {axis_rescale_x}
    {axis_rescale_y}
    {axis_rescale_z}
    {no_axis_pts_x}
    {no_axis_pts_y}
    {no_axis_pts_z}
    {no_rescale_x}
    {no_rescale_y}
    {no_rescale_z}
    {fix_no_axis_pts_x}
    {fix_no_axis_pts_y}
    {fix_no_axis_pts_z}
    {src_addr_x}
    {src_addr_y}
    {src_addr_z}
    {rip_addr_x}
    {rip_addr_y}
    {rip_addr_z}
    {rip_addr_w}
    {shift_op_x}
    {shift_op_y}
    {shift_op_z}
    {offset_x}
    {offset_y}
    {offset_z}
    {dist_op_x}
    {dist_op_y}
    {dist_op_z}
    {alignment_byte}
    {alignment_word}
    {alignment_long}
    {alignment_float32_ieee}
    {alignment_float64_ieee}
    {reserved}
    /end RECORD_LAYOUT'''])
@pytest.mark.parametrize('ident_string, ident_value', idents)
def test_record_layout(s, ident_string, ident_value):
    p = Parser(project_string_minimal.format(module_string_minimal.format(s.format(
        ident=ident_string,
        fnc_values=empty_string,
        identification=empty_string,
        axis_pts_x=empty_string,
        axis_pts_y=empty_string,
        axis_pts_z=empty_string,
        axis_rescale_x=empty_string,
        axis_rescale_y=empty_string,
        axis_rescale_z=empty_string,
        no_axis_pts_x=empty_string,
        no_axis_pts_y=empty_string,
        no_axis_pts_z=empty_string,
        no_rescale_x=empty_string,
        no_rescale_y=empty_string,
        no_rescale_z=empty_string,
        fix_no_axis_pts_x=empty_string,
        fix_no_axis_pts_y=empty_string,
        fix_no_axis_pts_z=empty_string,
        src_addr_x=empty_string,
        src_addr_y=empty_string,
        src_addr_z=empty_string,
        rip_addr_x=empty_string,
        rip_addr_y=empty_string,
        rip_addr_z=empty_string,
        rip_addr_w=empty_string,
        shift_op_x=empty_string,
        shift_op_y=empty_string,
        shift_op_z=empty_string,
        offset_x=empty_string,
        offset_y=empty_string,
        offset_z=empty_string,
        dist_op_x=empty_string,
        dist_op_y=empty_string,
        dist_op_z=empty_string,
        alignment_byte=empty_string,
        alignment_word=empty_string,
        alignment_long=empty_string,
        alignment_float32_ieee=empty_string,
        alignment_float64_ieee=empty_string,
        reserved=empty_string))))
    record_layout = p.ast.project.module[0].record_layout[0]
    assert record_layout.name == ident_value
    assert record_layout.fnc_values is None
    assert record_layout.identification is None
    assert record_layout.axis_pts_x is None
    assert record_layout.axis_pts_y is None
    assert record_layout.axis_pts_z is None
    assert record_layout.axis_rescale_x is None
    assert record_layout.axis_rescale_y is None
    assert record_layout.axis_rescale_z is None
    assert record_layout.no_axis_pts_x is None
    assert record_layout.no_axis_pts_y is None
    assert record_layout.no_axis_pts_z is None
    assert record_layout.no_rescale_x is None
    assert record_layout.no_rescale_y is None
    assert record_layout.no_rescale_z is None
    assert record_layout.fix_no_axis_pts_x is None
    assert record_layout.fix_no_axis_pts_y is None
    assert record_layout.fix_no_axis_pts_z is None
    assert record_layout.src_addr_x is None
    assert record_layout.src_addr_y is None
    assert record_layout.src_addr_z is None
    assert record_layout.rip_addr_w is None
    assert record_layout.rip_addr_x is None
    assert record_layout.rip_addr_y is None
    assert record_layout.rip_addr_z is None
    assert record_layout.shift_op_x is None
    assert record_layout.shift_op_y is None
    assert record_layout.shift_op_z is None
    assert record_layout.offset_x is None
    assert record_layout.offset_y is None
    assert record_layout.offset_z is None
    assert record_layout.dist_op_x is None
    assert record_layout.dist_op_y is None
    assert record_layout.dist_op_z is None
    assert record_layout.alignment_byte is None
    assert record_layout.alignment_word is None
    assert record_layout.alignment_long is None
    assert record_layout.alignment_float32_ieee is None
    assert record_layout.alignment_float64_ieee is None
    assert type(record_layout.reserved) is list


@pytest.mark.parametrize('module', [
    pytest.param(['function', 0, 'ref_characteristic'], id='FUNCTION'),
    pytest.param(['group', 0, 'ref_characteristic'], id='GROUP'),
], indirect=True)
@pytest.mark.parametrize('s, identifier_count', ref_characteristic_strings)
@pytest.mark.parametrize('ident_string, ident_value', idents)
def test_ref_characteristic(module, s, identifier_count, ident_string, ident_value):
    p = Parser(module[0].format(s.format(ident=ident_string)))
    ref_characteristic = get_node_from_ast(p.ast, module[1])
    assert type(ref_characteristic.identifier) is list
    assert len(ref_characteristic.identifier) == identifier_count
    for identifier in ref_characteristic.identifier:
        assert identifier == ident_value


@pytest.mark.parametrize('module', [pytest.param(['user_rights', 0, 'ref_group', 0], id='USER_RIGHTS')], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('/begin REF_GROUP /end REF_GROUP', 0, id='no identifier'),
    pytest.param('/begin REF_GROUP {ident} /end REF_GROUP', 1, id='one identifier'),
    pytest.param('/begin REF_GROUP {ident} {ident} /end REF_GROUP', 2, id='two identifier')])
@pytest.mark.parametrize('s, v', idents)
def test_ref_group(module, e, count, s, v):
    p = Parser(module[0].format(e.format(ident=s)))
    ref_group = get_node_from_ast(p.ast, module[1])
    assert type(ref_group.identifier) is list
    assert len(ref_group.identifier) == count
    for identifier in ref_group.identifier:
        assert identifier == v


@pytest.mark.parametrize('module', [
    pytest.param(['group', 0, 'ref_measurement'], id='GROUP'),
], indirect=True)
@pytest.mark.parametrize('s, identifier_count', ref_measurement_strings)
@pytest.mark.parametrize('ident_string, ident_value', idents)
def test_ref_measurement(module, s, identifier_count, ident_string, ident_value):
    p = Parser(module[0].format(s.format(ident=ident_string)))
    ref_measurement = get_node_from_ast(p.ast, module[1])
    assert type(ref_measurement.identifier) is list
    assert len(ref_measurement.identifier) == identifier_count
    for identifier in ref_measurement.identifier:
        assert identifier == ident_value


@pytest.mark.parametrize('module', [
    pytest.param(['characteristic', 0, 'ref_memory_segment'], id='CHARACTERISTIC'),
    pytest.param(['measurement', 0, 'ref_memory_segment'], id='MEASUREMENT'),
    pytest.param(['axis_pts', 0, 'ref_memory_segment'], id='AXIS_PTS')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('REF_MEMORY_SEGMENT {}')])
@pytest.mark.parametrize('s, v', idents)
def test_ref_memory_segment(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    ref_memory_segment = get_node_from_ast(p.ast, module[1])
    assert ref_memory_segment == v


@pytest.mark.parametrize('module', [
    pytest.param(['compu_method', 0, 'ref_unit'], id='COMPU_METHOD'),
    pytest.param(['unit', 0, 'ref_unit'], id='UNIT')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('REF_UNIT {}')])
@pytest.mark.parametrize('s, v', idents)
def test_ref_unit(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    ref_unit = get_node_from_ast(p.ast, module[1])
    assert ref_unit == v


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'reserved'], id='RECORD_LAYOUT')
], indirect=True)
@pytest.mark.parametrize('s, reserved_count', reserved_strings)
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_size_string, data_size_value', data_sizes)
def test_reserved(module,
                  s, reserved_count,
                  int_string, int_value,
                  data_size_string, data_size_value):
    p = Parser(module[0].format(s.format(int=int_string,
                                         data_size=data_size_string)))
    reserved = get_node_from_ast(p.ast, module[1])
    assert type(reserved) is list
    assert len(reserved) == reserved_count
    for e in reserved:
        assert e.position == int_value
        assert e.data_size == data_size_value


@pytest.mark.parametrize('module', [
    pytest.param(['measurement', 0, 'bit_operation', 'right_shift'], id='MEASUREMENT')], indirect=True)
@pytest.mark.parametrize('e', ['RIGHT_SHIFT {}'])
@pytest.mark.parametrize('s, v', longs)
def test_right_shift(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    right_shift = get_node_from_ast(p.ast, module[1])
    assert right_shift == v


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'rip_addr_w'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['RIP_ADDR_W {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_rip_addr_w(module, s, int_string, int_value, data_type_string, data_type_value):
    p = Parser(module[0].format(s.format(int=int_string, data_type=data_type_string)))
    rip_addr_w = get_node_from_ast(p.ast, module[1])
    assert rip_addr_w.position == int_value
    assert rip_addr_w.data_type == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'rip_addr_x'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['RIP_ADDR_X {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_rip_addr_x(module, s, int_string, int_value, data_type_string, data_type_value):
    p = Parser(module[0].format(s.format(int=int_string, data_type=data_type_string)))
    rip_addr_x = get_node_from_ast(p.ast, module[1])
    assert rip_addr_x.position == int_value
    assert rip_addr_x.data_type == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'rip_addr_y'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['RIP_ADDR_Y {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_rip_addr_y(module, s, int_string, int_value, data_type_string, data_type_value):
    p = Parser(module[0].format(s.format(int=int_string, data_type=data_type_string)))
    rip_addr_y = get_node_from_ast(p.ast, module[1])
    assert rip_addr_y.position == int_value
    assert rip_addr_y.data_type == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'rip_addr_z'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['RIP_ADDR_Z {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_rip_addr_z(module, s, int_string, int_value, data_type_string, data_type_value):
    p = Parser(module[0].format(s.format(int=int_string, data_type=data_type_string)))
    rip_addr_z = get_node_from_ast(p.ast, module[1])
    assert rip_addr_z.position == int_value
    assert rip_addr_z.data_type == data_type_value


@pytest.mark.parametrize('module', [pytest.param(['group', 0, 'root'], id='GROUP')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('ROOT')])
def test_root(module, e):
    p = Parser(module[0].format(e))
    root = get_node_from_ast(p.ast, module[1])
    assert root == e


@pytest.mark.parametrize('module', [pytest.param(['mod_common', 's_rec_layout'], id='MOD_COMMON')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('S_REC_LAYOUT {}')])
@pytest.mark.parametrize('s, v', idents)
def test_s_rec_layout(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    s_rec_layout = get_node_from_ast(p.ast, module[1])
    assert s_rec_layout == v


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'shift_op_x'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', ['SHIFT_OP_X {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_shift_op_x(module, e, int_string, int_value, data_type_string, data_type_value):
    p = Parser(module[0].format(e.format(int=int_string, data_type=data_type_string)))
    shift_op_x = get_node_from_ast(p.ast, module[1])
    assert shift_op_x.position == int_value
    assert shift_op_x.data_type == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'shift_op_y'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', ['SHIFT_OP_Y {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_shift_op_y(module, e, int_string, int_value, data_type_string, data_type_value):
    p = Parser(module[0].format(e.format(int=int_string, data_type=data_type_string)))
    shift_op_y = get_node_from_ast(p.ast, module[1])
    assert shift_op_y.position == int_value
    assert shift_op_y.data_type == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'shift_op_z'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', ['SHIFT_OP_Z {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_shift_op_z(module, e, int_string, int_value, data_type_string, data_type_value):
    p = Parser(module[0].format(e.format(int=int_string, data_type=data_type_string)))
    shift_op_z = get_node_from_ast(p.ast, module[1])
    assert shift_op_z.position == int_value
    assert shift_op_z.data_type == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['unit', 0, 'si_exponents'], id='UNIT')], indirect=True)
@pytest.mark.parametrize('e', ['SI_EXPONENTS {int} {int} {int} {int} {int} {int} {int}'])
@pytest.mark.parametrize('s, v', ints)
def test_si_exponents(module, e, s, v):
    p = Parser(module[0].format(e.format(int=s)))
    si_exponents = get_node_from_ast(p.ast, module[1])
    assert si_exponents.length == v
    assert si_exponents.mass == v
    assert si_exponents.time == v
    assert si_exponents.electric_current == v
    assert si_exponents.temperature == v
    assert si_exponents.amount_of_substance == v
    assert si_exponents.luminous_intensity == v


@pytest.mark.parametrize('module', [
    pytest.param(['measurement', 0, 'bit_operation', 'sign_extend'], id='MEASUREMENT')], indirect=True)
@pytest.mark.parametrize('e', ['SIGN_EXTEND'])
def test_sign_extend(module, e):
    p = Parser(module[0].format(e))
    sign_extend = get_node_from_ast(p.ast, module[1])
    assert sign_extend == e


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'src_addr_x'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', ['SRC_ADDR_X {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_src_addr_x(module, e, int_string, int_value, data_type_string, data_type_value):
    p = Parser(module[0].format(e.format(int=int_string, data_type=data_type_string)))
    src_addr_x = get_node_from_ast(p.ast, module[1])
    assert src_addr_x.position == int_value
    assert src_addr_x.data_type == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'src_addr_y'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', ['SRC_ADDR_Y {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_src_addr_y(module, e, int_string, int_value, data_type_string, data_type_value):
    p = Parser(module[0].format(e.format(int=int_string, data_type=data_type_string)))
    src_addr_y = get_node_from_ast(p.ast, module[1])
    assert src_addr_y.position == int_value
    assert src_addr_y.data_type == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['record_layout', 0, 'src_addr_z'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', ['SRC_ADDR_Z {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_src_addr_z(module, e, int_string, int_value, data_type_string, data_type_value):
    p = Parser(module[0].format(e.format(int=int_string, data_type=data_type_string)))
    src_addr_z = get_node_from_ast(p.ast, module[1])
    assert src_addr_z.position == int_value
    assert src_addr_z.data_type == data_type_value


@pytest.mark.parametrize('module', [pytest.param(['function', 0, 'sub_function'], id='FUNCTION'), ], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('/begin SUB_FUNCTION /end SUB_FUNCTION', 0, id='no identifier'),
    pytest.param('/begin SUB_FUNCTION {ident} /end SUB_FUNCTION', 1, id='one identifier'),
    pytest.param('/begin SUB_FUNCTION {ident} {ident} /end SUB_FUNCTION', 2, id='two identifier')])
@pytest.mark.parametrize('s, v', idents)
def test_sub_function(module, e, count, s, v):
    p = Parser(module[0].format(e.format(ident=s)))
    sub_function = get_node_from_ast(p.ast, module[1])
    assert type(sub_function.identifier) is list
    assert len(sub_function.identifier) == count
    for identifier in sub_function.identifier:
        assert identifier == v


@pytest.mark.parametrize('module', [pytest.param(['group', 0, 'sub_group'], id='GROUP')], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('/begin SUB_GROUP /end SUB_GROUP', 0, id='no identifier'),
    pytest.param('/begin SUB_GROUP {ident} /end SUB_GROUP', 1, id='one identifier'),
    pytest.param('/begin SUB_GROUP {ident} {ident} /end SUB_GROUP', 2, id='two identifier')])
@pytest.mark.parametrize('s, v', idents)
def test_sub_group(module, e, count, s, v):
    p = Parser(module[0].format(e.format(ident=s)))
    sub_group = get_node_from_ast(p.ast, module[1])
    assert type(sub_group.identifier) is list
    assert len(sub_group.identifier) == count
    for identifier in sub_group.identifier:
        assert identifier == v


@pytest.mark.parametrize('module', [pytest.param(['mod_par', 'supplier'], id='MOD_PAR')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('SUPPLIER {}')])
@pytest.mark.parametrize('s, v', strings)
def test_supplier(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    supplier = get_node_from_ast(p.ast, module[1])
    assert supplier == v


@pytest.mark.parametrize('s', ['''
    /begin UNIT {ident} {string} {string} {type}
    {si_exponents}
    {ref_unit}
    {unit_conversion}
    /end UNIT'''])
@pytest.mark.parametrize('ident_string, ident_value', idents)
@pytest.mark.parametrize('string_string, string_value', strings)
@pytest.mark.parametrize('enum_type_string, enum_type_value', enum_unit_type_strings)
def test_unit(s,
              ident_string, ident_value,
              string_string, string_value,
              enum_type_string, enum_type_value):
    p = Parser(project_string_minimal.format(module_string_minimal.format(s.format(
        ident=ident_string,
        string=string_string,
        type=enum_type_string,
        si_exponents=empty_string,
        ref_unit=empty_string,
        unit_conversion=empty_string))))
    unit = p.ast.project.module[0].unit[0]
    assert unit.name == ident_value
    assert unit.long_identifier == string_value
    assert unit.display == string_value
    assert unit.type == enum_type_value
    assert unit.si_exponents is None
    assert unit.ref_unit is None
    assert unit.unit_conversion is None


@pytest.mark.parametrize('module', [pytest.param(['unit', 0, 'unit_conversion'], id='UNIT')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('UNIT_CONVERSION {float} {float}')])
@pytest.mark.parametrize('s, v', floats)
def test_unit_conversion(module, e, s, v):
    p = Parser(module[0].format(e.format(float=s)))
    unit_conversion = get_node_from_ast(p.ast, module[1])
    assert unit_conversion.gradient == v
    assert unit_conversion.offset == v


@pytest.mark.parametrize('module', [pytest.param(['mod_par', 'user'], id='MOD_PAR')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('USER {}')])
@pytest.mark.parametrize('s, v', strings)
def test_user(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    user = get_node_from_ast(p.ast, module[1])
    assert user == v


@pytest.mark.parametrize('s', ['''
    /begin USER_RIGHTS {ident}
    {ref_group}
    {read_only}
    /end USER_RIGHTS'''])
@pytest.mark.parametrize('ident_string, ident_value', idents)
def test_user_rights(s, ident_string, ident_value):
    p = Parser(project_string_minimal.format(module_string_minimal.format(s.format(
        ident=ident_string,
        ref_group=empty_string,
        read_only=empty_string))))
    user_rights = p.ast.project.module[0].user_rights[0]
    assert user_rights.user_level_id == ident_value
    assert type(user_rights.ref_group) is list
    assert user_rights.read_only is None


@pytest.mark.parametrize('variant_coding', [
    pytest.param(['var_characteristic', 0, 'var_address'], id='VARIANT_CODING')], indirect=True)
@pytest.mark.parametrize('s, v', [
    pytest.param('', [], id='no address'),
    pytest.param('0', [0], id='one address'),
    pytest.param('0 0', [0, 0], id='two address')])
def test_var_address(variant_coding, s, v):
    p = Parser(variant_coding[0].format(s))
    var_address = get_node_from_ast(p.ast, variant_coding[1])
    assert type(var_address.address) is list
    assert var_address.address == v


@pytest.mark.parametrize('module', [
    pytest.param(['variant_coding', 'var_characteristic', 0], id='VARIANT_CODING')], indirect=True)
@pytest.mark.parametrize('s', [
    '/begin VAR_CHARACTERISTIC {ident} {criterion_name} {var_address} /end VAR_CHARACTERISTIC'])
@pytest.mark.parametrize('ident_string, ident_value', idents)
@pytest.mark.parametrize('criterion_name_string, criterion_name_value', [
    pytest.param('', [], id='no criterion_name'),
    pytest.param('_', ['_'], id='one criterion_name'),
    pytest.param('_ _', ['_', '_'], id='no criterion_name')])
def test_var_characteristic(module, s, ident_string, ident_value, criterion_name_string, criterion_name_value):
    p = Parser(module[0].format(s.format(ident=ident_string,
                                         criterion_name=criterion_name_string,
                                         var_address=empty_string)))
    var_characteristic = get_node_from_ast(p.ast, module[1])
    assert var_characteristic.name == ident_value
    assert type(var_characteristic.criterion_name) is list
    assert var_characteristic.criterion_name == criterion_name_value
    assert var_characteristic.var_address is None


@pytest.mark.parametrize('module', [
    pytest.param(['variant_coding', 'var_criterion', 0], id='VARIANT_CODING'), ], indirect=True)
@pytest.mark.parametrize('s', ['''
    /begin VAR_CRITERION
    {ident}
    {string}
    {value}
    {var_measurement}
    {var_selection_characteristic}
    /end VAR_CRITERION'''])
@pytest.mark.parametrize('ident_string, ident_value', idents)
@pytest.mark.parametrize('string_string, string_value', strings)
@pytest.mark.parametrize('value_string, value_value', [
    pytest.param('', [], id='no value'),
    pytest.param('_', ['_'], id='one value'),
    pytest.param('_ _', ['_', '_'], id='two value')])
def test_var_criterion(module, s, ident_string, ident_value, string_string, string_value, value_string, value_value):
    p = Parser(module[0].format(s.format(ident=ident_string,
                                         string=string_string,
                                         value=value_string,
                                         var_measurement=empty_string,
                                         var_selection_characteristic=empty_string)))
    var_criterion = get_node_from_ast(p.ast, module[1])
    assert var_criterion.name == ident_value
    assert var_criterion.long_identifier == string_value
    assert type(var_criterion.value) is list
    assert var_criterion.value == value_value
    assert var_criterion.var_measurement is None
    assert var_criterion.var_selection_characteristic is None


@pytest.mark.parametrize('module', [
    pytest.param(['variant_coding', 'var_forbidden_comb', 0], id='VARIANT_CODING')], indirect=True)
@pytest.mark.parametrize('e', ['/begin VAR_FORBIDDEN_COMB {} /end VAR_FORBIDDEN_COMB'])
@pytest.mark.parametrize('s, v', [
    pytest.param('', [], id='no criterion'),
    pytest.param('_ _', [('_', '_')], id='one criterion'),
    pytest.param('_ _ _ _', [('_', '_'), ('_', '_')], id='two criterion')])
def test_var_forbidden_comb(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    var_forbidden_comb = get_node_from_ast(p.ast, module[1])
    assert type(var_forbidden_comb.criterion) is list
    assert var_forbidden_comb.criterion == v


@pytest.mark.parametrize('variant_coding', [
    pytest.param(['var_criterion', 0, 'var_measurement'], id='VARIANT_CODING')], indirect=True)
@pytest.mark.parametrize('s, v', [pytest.param('VAR_MEASUREMENT _', '_', id='VAR_MEASUREMENT')])
def test_var_measurement(variant_coding, s, v):
    p = Parser(variant_coding[0].format(s))
    var_measurement = get_node_from_ast(p.ast, variant_coding[1])
    assert var_measurement == v


@pytest.mark.parametrize('module', [pytest.param(['variant_coding', 'var_naming'], id='VARIANT_CODING')], indirect=True)
@pytest.mark.parametrize('e', ['VAR_NAMING {}'])
@pytest.mark.parametrize('s, v', enum_var_naming_tag)
def test_var_naming(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    var_naming = get_node_from_ast(p.ast, module[1])
    assert var_naming == v


@pytest.mark.parametrize('variant_coding', [
    pytest.param(['var_criterion', 0, 'var_selection_characteristic'], id='VARIANT_CODING')], indirect=True)
@pytest.mark.parametrize('e', ['VAR_SELECTION_CHARACTERISTIC {}'])
@pytest.mark.parametrize('s, v', idents)
def test_var_selection_characteristic(variant_coding, e, s, v):
    p = Parser(variant_coding[0].format(e.format(s)))
    var_selection_characteristic = get_node_from_ast(p.ast, variant_coding[1])
    assert var_selection_characteristic == v


@pytest.mark.parametrize('module', [
    pytest.param(['variant_coding', 'var_separator'], id='VARIANT_CODING')], indirect=True)
@pytest.mark.parametrize('e', ['VAR_SEPARATOR {}'])
@pytest.mark.parametrize('s, v', strings)
def test_var_separator(module, e, s, v):
    p = Parser(module[0].format(e.format(s)))
    var_separator = get_node_from_ast(p.ast, module[1])
    assert var_separator == v


@pytest.mark.parametrize('s', [
    '''/begin VARIANT_CODING
    {var_separator}
    {var_naming}
    {var_criterion}
    {var_forbidden_comb}
    {var_characteristic}
    /end VARIANT_CODING'''])
def test_variant_coding(s):
    p = Parser(project_string_minimal.format(module_string_minimal.format(s.format(
        var_separator=empty_string,
        var_naming=empty_string,
        var_criterion=empty_string,
        var_forbidden_comb=empty_string,
        var_characteristic=empty_string))))
    variant_coding = p.ast.project.module[0].variant_coding
    assert variant_coding.var_separator is None
    assert variant_coding.var_naming is None
    assert type(variant_coding.var_criterion) is list
    assert type(variant_coding.var_forbidden_comb) is list
    assert type(variant_coding.var_characteristic) is list


@pytest.mark.parametrize('project', [pytest.param(['header', 'version'], id='HEADER')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('VERSION {}')])
@pytest.mark.parametrize('s, v', strings)
def test_version(project, e, s, v):
    p = Parser(project[0].format(e.format(s)))
    version = get_node_from_ast(p.ast, project[1])
    assert version == v


@pytest.mark.parametrize('module', [pytest.param(['measurement', 0, 'virtual'], id='MEASUREMENT')], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('/begin VIRTUAL /end VIRTUAL', 0, id='no measuring_channel',
                 marks=pytest.mark.xfail(raises=A2lFormatException, strict=True)),
    pytest.param('/begin VIRTUAL {ident} /end VIRTUAL', 1, id='one measuring_channel'),
    pytest.param('/begin VIRTUAL {ident} {ident} /end VIRTUAL', 2, id='two measuring_channel')])
@pytest.mark.parametrize('s, v', idents)
def test_virtual(module, e, count, s, v):
    p = Parser(module[0].format(e.format(ident=s)))
    virtual = get_node_from_ast(p.ast, module[1])
    assert type(virtual.measuring_channel) is list
    assert len(virtual.measuring_channel) == count
    for measuring_channel in virtual.measuring_channel:
        assert measuring_channel == v


@pytest.mark.parametrize('module', [
    pytest.param(['characteristic', 0, 'virtual_characteristic'], id='CHARACTERISTIC')], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('/begin VIRTUAL_CHARACTERISTIC {string} /end VIRTUAL_CHARACTERISTIC', 0, id='no characteristic',
                 marks=pytest.mark.xfail(raises=A2lFormatException, strict=True)),
    pytest.param('/begin VIRTUAL_CHARACTERISTIC {string} {ident} /end VIRTUAL_CHARACTERISTIC', 1,
                 id='one characteristic'),
    pytest.param('/begin VIRTUAL_CHARACTERISTIC {string} {ident} {ident} /end VIRTUAL_CHARACTERISTIC', 2,
                 id='two characteristic')])
@pytest.mark.parametrize('string_string, string_value', strings)
@pytest.mark.parametrize('ident_string, ident_value', idents)
def test_virtual_characteristic(module, e, count, string_string, string_value, ident_string, ident_value):
    p = Parser(module[0].format(e.format(string=string_string, ident=ident_string)))
    virtual_characteristic = get_node_from_ast(p.ast, module[1])
    assert virtual_characteristic.formula == string_value
    assert len(virtual_characteristic.characteristic) == count
    for characteristic in virtual_characteristic.characteristic:
        assert characteristic == ident_value


@pytest.mark.parametrize('module', [pytest.param(['mod_par', 'system_constant', 0], id='MOD_PAR')], indirect=True)
@pytest.mark.parametrize('e', ['SYSTEM_CONSTANT {string} {string}'])
@pytest.mark.parametrize('s, v', strings)
def test_system_constant(module, e, s, v):
    p = Parser(module[0].format(e.format(string=s)))
    system_constant = get_node_from_ast(p.ast, module[1])
    assert system_constant.name == v
    assert system_constant.value == v


def test_get_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin CHARACTERISTIC
                    characteristic_name 
                    "characteristic long identifier" 
                    VALUE 
                    0 
                    DAMOS_SST 
                    0 
                    characteristic_conversion
                    0 
                    0
                /end CHARACTERISTIC
                /begin CHARACTERISTIC
                    characteristic_name 
                    "characteristic long identifier" 
                    VALUE 
                    0 
                    DAMOS_SST 
                    0 
                    characteristic_conversion
                    0 
                    0
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert len(a2l.nodes('PROJECT')) == 1
    assert len(a2l.nodes('MODULE')) == 1
    assert len(a2l.nodes('CHARACTERISTIC')) == 2
    assert len(a2l.nodes('MEASUREMENT')) == 0


def test_get_properties():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert set(a2l.ast.project.properties) == {'name', 'module', 'header', 'long_identifier'}


def test_type():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin CHARACTERISTIC
                    characteristic_name 
                    "characteristic long identifier" 
                    VALUE 
                    0 
                    DAMOS_SST 
                    0 
                    characteristic_conversion
                    0 
                    0
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.ast.project.module[0].characteristic[0].node == 'CHARACTERISTIC'
