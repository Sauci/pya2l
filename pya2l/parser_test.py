"""
@project: parser
@file: a2l_parser_test.py
@author: Guillaume Sottas
@date: 06.04.2018
"""

import pytest

from .parser import A2lParser as Parser


def is_iterable(e):
    try:
        iter(e)
        return True
    except TypeError:
        return False


idents = (
    pytest.param('name', 'name', id='valid ident'),
    # pytest.param('0', None, id='invalid ident', marks=pytest.mark.xfail(raises=A2lFormatException, strict=True))
)

floats = (pytest.param('0.0', 0.0, id='zero'),)

ints = (pytest.param('0', 0, id='zero'),)

longs = (pytest.param('0', 0, id='zero'),)

strings = (pytest.param('\"\"', '', id='valid string'), pytest.param('\"asd\"', 'asd', id='valid string'),)

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

enum_index_modes = (
    pytest.param('ROW_DIR', 'ROW_DIR', id='row'),
    pytest.param('COLUMN_DIR', 'COLUMN_DIR', id='column'))

index_increments = (
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
    pytest.param('/begin PROJECT {ident} {string} {module} {header} {module} /end PROJECT', id='PROJECT MODULE HEADER MODULE')
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
    lookup = dict(AXIS_DESCR=axis_descr_string_minimal,
                  AXIS_PTS=axis_pts_string_minimal,
                  CHARACTERISTIC=characteristic_string_minimal,
                  COMPU_METHOD=compu_method_string_minimal,
                  FUNCTION=function_string_minimal,
                  GROUP=group_string_minimal,
                  HEADER=header_string_minimal,
                  MEASUREMENT=measurement_string_minimal,
                  MOD_PAR=mod_par_string_minimal,
                  MODULE=module_string_minimal,
                  PROJECT=project_string_minimal,
                  RECORD_LAYOUT=record_layout_string_minimal,
                  VARIANT_CODING=variant_coding_string_minimal)
    result = None
    prefix = ['PROJECT']
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
    lookup = dict(ANNOTATION=annotation_string_minimal,  # TODO: check.
                  AXIS_DESCR=axis_descr_string_minimal,
                  AXIS_PTS=axis_pts_string_minimal,
                  BIT_OPERATION=bit_operation_string_minimal,  # TODO: check.
                  CHARACTERISTIC=characteristic_string_minimal,
                  COMPU_METHOD=compu_method_string_minimal,
                  COMPU_TAB=compu_tab_string_minimal,
                  COMPU_VTAB=compu_vtab_string_minimal,
                  COMPU_VTAB_RANGE=compu_vtab_range_string_minimal,
                  FRAME=frame_string_minimal,
                  FUNCTION=function_string_minimal,
                  GROUP=group_string_minimal,
                  MEASUREMENT=measurement_string_minimal,
                  MOD_COMMON=mod_common_string_minimal,
                  MOD_PAR=mod_par_string_minimal,
                  MODULE=module_string_minimal,
                  PROJECT=project_string_minimal,
                  RECORD_LAYOUT=record_layout_string_minimal,
                  UNIT=unit_string_minimal,
                  USER_RIGHTS=user_rights_string_minimal,
                  VARIANT_CODING=variant_coding_string_minimal)
    result = None
    prefix = ['PROJECT', 'MODULE', 0]
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
    lookup = dict(VAR_ADDRESS=var_address_string_minimal,
                  VAR_CHARACTERISTIC=var_characteristic_string_minimal,
                  VAR_CRITERION=var_criterion_string_minimal)
    result = None
    prefix = ['PROJECT', 'MODULE', 0, 'VARIANT_CODING']
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
    lookup = dict(CALIBRATION_HANDLE=calibration_handle_string_minimal)
    result = None
    prefix = ['PROJECT', 'MODULE', 0, 'MOD_PAR', 'CALIBRATION_METHOD', 0]
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
    lookup = dict(FORMULA='/begin FORMULA "" {} /end FORMULA')
    result = None
    prefix = ['PROJECT', 'MODULE', 0, 'COMPU_METHOD', 0]
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
    pass  # pytest.xfail('implement me...')


@pytest.mark.parametrize('e', ['A2ML_VERSION {int} {int} /begin PROJECT _ "" /end PROJECT'])
@pytest.mark.parametrize('s, v', ints)
def test_a2ml_version(e, s, v):
    with Parser() as p:
        ast = p.tree_from_a2l(e.format(int=s).encode())
        assert ast.A2ML_VERSION.VersionNo.Value == v
        assert ast.A2ML_VERSION.UpgradeNo.Value == v


@pytest.mark.parametrize('project', [
    pytest.param(['MODULE', 0, 'MOD_PAR', 'ADDR_EPK', 0], id='MOD_PAR')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('ADDR_EPK {}')])
@pytest.mark.parametrize('s, v', longs)
def test_addr_epk(project, e, s, v):
    with Parser() as p:
        addr_epk = get_node_from_ast(p.tree_from_a2l(project[0].format(e.format(s)).encode()), project[1])
        assert addr_epk.Address.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['MOD_COMMON', 'ALIGNMENT_BYTE'], id='MOD_COMMON'),
    pytest.param(['RECORD_LAYOUT', 0, 'ALIGNMENT_BYTE'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('ALIGNMENT_BYTE {}')])
@pytest.mark.parametrize('s, v', ints)
def test_alignment_byte(module, e, s, v):
    with Parser() as p:
        alignment_byte = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert alignment_byte.AlignmentBorder.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['MOD_COMMON', 'ALIGNMENT_FLOAT32_IEEE'], id='MOD_COMMON'),
    pytest.param(['RECORD_LAYOUT', 0, 'ALIGNMENT_FLOAT32_IEEE'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('ALIGNMENT_FLOAT32_IEEE {}')])
@pytest.mark.parametrize('s, v', ints)
def test_alignment_float32_ieee(module, e, s, v):
    with Parser() as p:
        alignment_float32_ieee = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert alignment_float32_ieee.AlignmentBorder.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['MOD_COMMON', 'ALIGNMENT_FLOAT64_IEEE'], id='MOD_COMMON'),
    pytest.param(['RECORD_LAYOUT', 0, 'ALIGNMENT_FLOAT64_IEEE'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('ALIGNMENT_FLOAT64_IEEE {}')])
@pytest.mark.parametrize('s, v', ints)
def test_alignment_float64_ieee(module, e, s, v):
    with Parser() as p:
        alignment_float64_ieee = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert alignment_float64_ieee.AlignmentBorder.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['MOD_COMMON', 'ALIGNMENT_LONG'], id='MOD_COMMON'),
    pytest.param(['RECORD_LAYOUT', 0, 'ALIGNMENT_LONG'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('ALIGNMENT_LONG {}')])
@pytest.mark.parametrize('s, v', ints)
def test_alignment_long(module, e, s, v):
    with Parser() as p:
        alignment_long = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert alignment_long.AlignmentBorder.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['MOD_COMMON', 'ALIGNMENT_WORD'], id='MOD_COMMON'),
    pytest.param(['RECORD_LAYOUT', 0, 'ALIGNMENT_WORD'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('ALIGNMENT_WORD {}')])
@pytest.mark.parametrize('s, v', ints)
def test_alignment_word(module, e, s, v):
    with Parser() as p:
        alignment_word = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert alignment_word.AlignmentBorder.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['AXIS_PTS', 0, 'ANNOTATION', 0], id='AXIS_PTS'),
    pytest.param(['MEASUREMENT', 0, 'ANNOTATION', 0], id='MEASUREMENT'),
    pytest.param(['CHARACTERISTIC', 0, 'ANNOTATION', 0], id='CHARACTERISTIC'),
    pytest.param(['CHARACTERISTIC', 0, 'AXIS_DESCR', 0, 'ANNOTATION', 0], id='AXIS_DESCR'),
    pytest.param(['FUNCTION', 0, 'ANNOTATION', 0], id='FUNCTION'),
    pytest.param(['GROUP', 0, 'ANNOTATION', 0], id='GROUP')], indirect=True)
def test_annotation(module):
    with Parser() as p:
        annotation = get_node_from_ast(p.tree_from_a2l(module[0].format('').encode()), module[1])
        assert annotation.ANNOTATION_LABEL.is_none
        assert annotation.ANNOTATION_ORIGIN.is_none
        assert annotation.ANNOTATION_TEXT.is_none


@pytest.mark.parametrize('module', [
    pytest.param(['AXIS_PTS', 0, 'ANNOTATION', 0, 'ANNOTATION_LABEL'], id='AXIS_PTS'),
    pytest.param(['MEASUREMENT', 0, 'ANNOTATION', 0, 'ANNOTATION_LABEL'], id='MEASUREMENT'),
    pytest.param(['CHARACTERISTIC', 0, 'ANNOTATION', 0, 'ANNOTATION_LABEL'], id='CHARACTERISTIC'),
    pytest.param(['CHARACTERISTIC', 0, 'AXIS_DESCR', 0, 'ANNOTATION', 0, 'ANNOTATION_LABEL'], id='AXIS_DESCR'),
    pytest.param(['FUNCTION', 0, 'ANNOTATION', 0, 'ANNOTATION_LABEL'], id='FUNCTION'),
    pytest.param(['GROUP', 0, 'ANNOTATION', 0, 'ANNOTATION_LABEL'], id='GROUP')
], indirect=True)
@pytest.mark.parametrize('e', ['ANNOTATION_LABEL {}'])
@pytest.mark.parametrize('s, v', strings)
def test_annotation_label(module, e, s, v):
    with Parser() as p:
        annotation_label = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert annotation_label.Label.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['AXIS_PTS', 0, 'ANNOTATION', 0, 'ANNOTATION_ORIGIN'], id='AXIS_PTS'),
    pytest.param(['MEASUREMENT', 0, 'ANNOTATION', 0, 'ANNOTATION_ORIGIN'], id='MEASUREMENT'),
    pytest.param(['CHARACTERISTIC', 0, 'ANNOTATION', 0, 'ANNOTATION_ORIGIN'], id='CHARACTERISTIC'),
    pytest.param(['CHARACTERISTIC', 0, 'AXIS_DESCR', 0, 'ANNOTATION', 0, 'ANNOTATION_ORIGIN'], id='AXIS_DESCR'),
    pytest.param(['FUNCTION', 0, 'ANNOTATION', 0, 'ANNOTATION_ORIGIN'], id='FUNCTION'),
    pytest.param(['GROUP', 0, 'ANNOTATION', 0, 'ANNOTATION_ORIGIN'], id='GROUP')
], indirect=True)
@pytest.mark.parametrize('e', ['ANNOTATION_ORIGIN {}'])
@pytest.mark.parametrize('s, v', strings)
def test_annotation_origin(module, e, s, v):
    with Parser() as p:
        annotation_origin = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert annotation_origin.Origin.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['AXIS_PTS', 0, 'ANNOTATION', 0, 'ANNOTATION_TEXT'], id='AXIS_PTS'),
    pytest.param(['MEASUREMENT', 0, 'ANNOTATION', 0, 'ANNOTATION_TEXT'], id='MEASUREMENT'),
    pytest.param(['CHARACTERISTIC', 0, 'ANNOTATION', 0, 'ANNOTATION_TEXT'], id='CHARACTERISTIC'),
    pytest.param(['CHARACTERISTIC', 0, 'AXIS_DESCR', 0, 'ANNOTATION', 0, 'ANNOTATION_TEXT'], id='AXIS_DESCR'),
    pytest.param(['FUNCTION', 0, 'ANNOTATION', 0, 'ANNOTATION_TEXT'], id='FUNCTION'),
    pytest.param(['GROUP', 0, 'ANNOTATION', 0, 'ANNOTATION_TEXT'], id='GROUP')], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('''/begin ANNOTATION_TEXT /end ANNOTATION_TEXT''', 0, id='no text'),
    pytest.param('''/begin ANNOTATION_TEXT {s} /end ANNOTATION_TEXT''', 1, id='one text'),
    pytest.param('''/begin ANNOTATION_TEXT {s} {s} /end ANNOTATION_TEXT''', 2, id='two text')])
@pytest.mark.parametrize('s, v', strings)
def test_annotation_text(module, e, count, s, v):
    with Parser() as p:
        annotation_text = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s=s)).encode()), module[1])
        assert is_iterable(annotation_text.AnnotationText)
        assert len(annotation_text.AnnotationText) == count
        for text in annotation_text.AnnotationText:
            assert text.Value == v


@pytest.mark.parametrize('module', [pytest.param(['MEASUREMENT', 0, 'ARRAY_SIZE'], id='MEASUREMENT')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('ARRAY_SIZE {}')])
@pytest.mark.parametrize('s, v', ints)
def test_array_size(module, e, s, v):
    with Parser() as p:
        array_size = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert array_size.Number.Value == v


@pytest.mark.parametrize('s', [
    'ASAP2_VERSION {int} {int} /begin PROJECT _ "" /end PROJECT'])  # TODO: create a root fixture containing PROJECT, ASAP2_VERSION and A2ML_VERSION
@pytest.mark.parametrize('int_string, int_value', ints)
def test_asap2_version(s, int_string, int_value):
    with Parser() as p:
        ast = p.tree_from_a2l(s.format(int=int_string).encode())
        assert ast.ASAP2_VERSION.VersionNo.Value == int_value
        assert ast.ASAP2_VERSION.UpgradeNo.Value == int_value


@pytest.mark.parametrize('module', [pytest.param(['CHARACTERISTIC', 0], id='CHARACTERISTIC')], indirect=True)
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
    {step_size}
    {phys_unit}
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
    with Parser() as p:
        axis_descr = get_node_from_ast(p.tree_from_a2l(module[0].format(s.format(
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
            curve_axis_ref=empty_string,
            step_size=empty_string,
            phys_unit=empty_string)).encode()), module[1] + ['AXIS_DESCR', 0])
        assert axis_descr.Attribute == enum_attribute_value
        assert axis_descr.InputQuantity.Value == ident_value
        assert axis_descr.Conversion.Value == ident_value
        assert axis_descr.MaxAxisPoints.Value == int_value
        assert axis_descr.LowerLimit.Value == float_value
        assert axis_descr.UpperLimit.Value == float_value
        assert axis_descr.READ_ONLY.is_none
        assert axis_descr.FORMAT.is_none
        assert axis_descr.AXIS_PTS_REF.is_none
        assert axis_descr.MAX_GRAD.is_none
        assert axis_descr.MONOTONY.is_none
        assert axis_descr.BYTE_ORDER.is_none
        assert axis_descr.FIX_AXIS_PAR.is_none
        assert axis_descr.FIX_AXIS_PAR_DIST.is_none
        assert axis_descr.FIX_AXIS_PAR_LIST.is_none
        assert axis_descr.DEPOSIT.is_none
        assert is_iterable(axis_descr.ANNOTATION)
        assert axis_descr.EXTENDED_LIMITS.is_none
        assert axis_descr.CURVE_AXIS_REF.is_none
        assert axis_descr.STEP_SIZE.is_none
        assert axis_descr.PHYS_UNIT.is_none


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
    {symbol_link}
    {step_size}
    {phys_unit}
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
    with Parser() as p:
        axis_pts = p.tree_from_a2l(project_string_minimal.format(module_string_minimal.format(s.format(
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
            ecu_address_extension=empty_string,
            symbol_link=empty_string,
            step_size=empty_string,
            phys_unit=empty_string))).encode()).PROJECT.MODULE[0].AXIS_PTS[0]
        assert axis_pts.Name.Value == ident_value
        assert axis_pts.LongIdentifier.Value == string_value
        assert axis_pts.Address.Value == long_value
        assert axis_pts.InputQuantity.Value == ident_value
        assert axis_pts.DepositR.Value == ident_value
        assert axis_pts.MaxDiff.Value == float_value
        assert axis_pts.Conversion.Value == ident_value
        assert axis_pts.MaxAxisPoints.Value == int_value
        assert axis_pts.LowerLimit.Value == float_value
        assert axis_pts.UpperLimit.Value == float_value
        assert axis_pts.DISPLAY_IDENTIFIER.is_none
        assert axis_pts.READ_ONLY.is_none
        assert axis_pts.FORMAT.is_none
        assert axis_pts.DEPOSIT.is_none
        assert axis_pts.BYTE_ORDER.is_none
        assert axis_pts.FUNCTION_LIST.is_none
        assert axis_pts.REF_MEMORY_SEGMENT.is_none
        assert axis_pts.GUARD_RAILS.is_none
        assert is_iterable(axis_pts.ANNOTATION)
        assert axis_pts.EXTENDED_LIMITS.is_none
        assert axis_pts.CALIBRATION_ACCESS.is_none
        assert axis_pts.ECU_ADDRESS_EXTENSION.is_none
        assert axis_pts.SYMBOL_LINK.is_none
        assert axis_pts.STEP_SIZE.is_none
        assert axis_pts.PHYS_UNIT.is_none


@pytest.mark.parametrize('module', [
    pytest.param(['CHARACTERISTIC', 0, 'AXIS_DESCR', 0, 'AXIS_PTS_REF'], id='AXIS_DESCR')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('AXIS_PTS_REF {}')])
@pytest.mark.parametrize('s, v', idents)
def test_axis_pts_ref(module, e, s, v):
    with Parser() as p:
        axis_pts_ref = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert axis_pts_ref.AxisPoints.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'AXIS_PTS_X'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['AXIS_PTS_X {int} {data_type} {index_order} {addr_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
@pytest.mark.parametrize('index_order_string, index_order_value', index_increments)
@pytest.mark.parametrize('addr_type_string, addr_type_value', addr_types)
def test_axis_pts_x(module,
                    s,
                    int_string, int_value,
                    data_type_string, data_type_value,
                    index_order_string, index_order_value,
                    addr_type_string, addr_type_value):
    with Parser() as p:
        axis_pts_x = get_node_from_ast(p.tree_from_a2l(module[0].format(s.format(int=int_string,
                                                                                 data_type=data_type_string,
                                                                                 index_order=index_order_string,
                                                                                 addr_type=addr_type_string)).encode()),
                                       module[1])
        assert axis_pts_x.Position.Value == int_value
        assert axis_pts_x.DataType.Value == data_type_value
        assert axis_pts_x.IndexIncr.Value == index_order_value
        assert axis_pts_x.Addressing.Value == addr_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'AXIS_PTS_Y'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['AXIS_PTS_Y {int} {data_type} {index_order} {addr_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
@pytest.mark.parametrize('index_order_string, index_order_value', index_increments)
@pytest.mark.parametrize('addr_type_string, addr_type_value', addr_types)
def test_axis_pts_y(module,
                    s,
                    int_string, int_value,
                    data_type_string, data_type_value,
                    index_order_string, index_order_value,
                    addr_type_string, addr_type_value):
    with Parser() as p:
        axis_pts_y = get_node_from_ast(p.tree_from_a2l(module[0].format(s.format(int=int_string,
                                                                                 data_type=data_type_string,
                                                                                 index_order=index_order_string,
                                                                                 addr_type=addr_type_string)).encode()),
                                       module[1])
        assert axis_pts_y.Position.Value == int_value
        assert axis_pts_y.DataType.Value == data_type_value
        assert axis_pts_y.IndexIncr.Value == index_order_value
        assert axis_pts_y.Addressing.Value == addr_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'AXIS_PTS_Z'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['AXIS_PTS_Z {int} {data_type} {index_order} {addr_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
@pytest.mark.parametrize('index_order_string, index_order_value', index_increments)
@pytest.mark.parametrize('addr_type_string, addr_type_value', addr_types)
def test_axis_pts_z(module,
                    s,
                    int_string, int_value,
                    data_type_string, data_type_value,
                    index_order_string, index_order_value,
                    addr_type_string, addr_type_value):
    with Parser() as p:
        axis_pts_z = get_node_from_ast(p.tree_from_a2l(module[0].format(s.format(int=int_string,
                                                                                 data_type=data_type_string,
                                                                                 index_order=index_order_string,
                                                                                 addr_type=addr_type_string)).encode()),
                                       module[1])
        assert axis_pts_z.Position.Value == int_value
        assert axis_pts_z.DataType.Value == data_type_value
        assert axis_pts_z.IndexIncr.Value == index_order_value
        assert axis_pts_z.Addressing.Value == addr_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'AXIS_RESCALE_X'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['AXIS_RESCALE_X {int} {data_type} {int} {index_order} {addr_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
@pytest.mark.parametrize('index_incr_string, index_incr_value', index_increments)
@pytest.mark.parametrize('addr_type_string, addr_type_value', addr_types)
def test_axis_rescale_x(module,
                        s,
                        int_string, int_value,
                        data_type_string, data_type_value,
                        index_incr_string, index_incr_value,
                        addr_type_string, addr_type_value):
    with Parser() as p:
        axis_rescale_x = get_node_from_ast(p.tree_from_a2l(module[0].format(s.format(int=int_string,
                                                                                     data_type=data_type_string,
                                                                                     index_order=index_incr_string,
                                                                                     addr_type=addr_type_string)).encode()),
                                           module[1])
        assert axis_rescale_x.Position.Value == int_value
        assert axis_rescale_x.DataType.Value == data_type_value
        assert axis_rescale_x.MaxNumberOfRescalePairs.Value == int_value
        assert axis_rescale_x.IndexIncr.Value == index_incr_value
        assert axis_rescale_x.Addressing.Value == addr_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'AXIS_RESCALE_Y'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['AXIS_RESCALE_Y {int} {data_type} {int} {index_order} {addr_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
@pytest.mark.parametrize('index_incr_string, index_incr_value', index_increments)
@pytest.mark.parametrize('addr_type_string, addr_type_value', addr_types)
def test_axis_rescale_y(module,
                        s,
                        int_string, int_value,
                        data_type_string, data_type_value,
                        index_incr_string, index_incr_value,
                        addr_type_string, addr_type_value):
    with Parser() as p:
        axis_rescale_y = get_node_from_ast(p.tree_from_a2l(module[0].format(s.format(int=int_string,
                                                                                     data_type=data_type_string,
                                                                                     index_order=index_incr_string,
                                                                                     addr_type=addr_type_string)).encode()),
                                           module[1])
        assert axis_rescale_y.Position.Value == int_value
        assert axis_rescale_y.DataType.Value == data_type_value
        assert axis_rescale_y.MaxNumberOfRescalePairs.Value == int_value
        assert axis_rescale_y.IndexIncr.Value == index_incr_value
        assert axis_rescale_y.Addressing.Value == addr_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'AXIS_RESCALE_Z'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['AXIS_RESCALE_Z {int} {data_type} {int} {index_order} {addr_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
@pytest.mark.parametrize('index_incr_string, index_incr_value', index_increments)
@pytest.mark.parametrize('addr_type_string, addr_type_value', addr_types)
def test_axis_rescale_z(module,
                        s,
                        int_string, int_value,
                        data_type_string, data_type_value,
                        index_incr_string, index_incr_value,
                        addr_type_string, addr_type_value):
    with Parser() as p:
        axis_rescale_z = get_node_from_ast(p.tree_from_a2l(module[0].format(s.format(int=int_string,
                                                                                     data_type=data_type_string,
                                                                                     index_order=index_incr_string,
                                                                                     addr_type=addr_type_string)).encode()),
                                           module[1])
        assert axis_rescale_z.Position.Value == int_value
        assert axis_rescale_z.DataType.Value == data_type_value
        assert axis_rescale_z.MaxNumberOfRescalePairs.Value == int_value
        assert axis_rescale_z.IndexIncr.Value == index_incr_value
        assert axis_rescale_z.Addressing.Value == addr_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['CHARACTERISTIC', 0, 'BIT_MASK'], id='CHARACTERISTIC'),
    pytest.param(['MEASUREMENT', 0, 'BIT_MASK'], id='MEASUREMENT')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('BIT_MASK {}')])
@pytest.mark.parametrize('s, v', longs)
def test_bit_mask(module, e, s, v):
    with Parser() as p:
        bit_mask = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert bit_mask.Mask.Value == v


@pytest.mark.parametrize('module', [pytest.param(['MEASUREMENT', 0, 'BIT_OPERATION'], id='MEASUREMENT')], indirect=True)
def test_bit_operation(module):
    with Parser() as p:
        bit_operation = get_node_from_ast(p.tree_from_a2l(module[0].format('').encode()), module[1])
        assert bit_operation.LEFT_SHIFT.is_none
        assert bit_operation.RIGHT_SHIFT.is_none
        assert bit_operation.SIGN_EXTEND.is_none


@pytest.mark.parametrize('module', [
    pytest.param(['AXIS_PTS', 0, 'BYTE_ORDER'], id='AXIS_PTS'),
    pytest.param(['CHARACTERISTIC', 0, 'BYTE_ORDER'], id='CHARACTERISTIC'),
    pytest.param(['CHARACTERISTIC', 0, 'AXIS_DESCR', 0, 'BYTE_ORDER'], id='AXIS_DESCR'),
    pytest.param(['MEASUREMENT', 0, 'BYTE_ORDER'], id='MEASUREMENT'),
    pytest.param(['MOD_COMMON', 'BYTE_ORDER'], id='MOD_COMMON')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('BYTE_ORDER {}')])
@pytest.mark.parametrize('s, v', enum_byte_order)
def test_byte_order(module, e, s, v):
    with Parser() as p:
        byte_order = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert byte_order.ByteOrder == v


@pytest.mark.parametrize('module', [
    pytest.param(['CHARACTERISTIC', 0, 'CALIBRATION_ACCESS'], id='CHARACTERISTIC'),
    pytest.param(['AXIS_PTS', 0, 'CALIBRATION_ACCESS'], id='AXIS_PTS')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('CALIBRATION_ACCESS {}')])
@pytest.mark.parametrize('s, v', enum_calibration_access)
def test_calibration_access(module, e, s, v):
    with Parser() as p:
        calibration_access = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert calibration_access.Type == v


@pytest.mark.parametrize('calibration_method', [
    pytest.param(['CALIBRATION_HANDLE', 0], id='CALIBRATION_METHOD')], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('', 0, id='no handle'),
    pytest.param('{long}', 1, id='one handle'),
    pytest.param('{long} {long}', 2, id='two handle')])
@pytest.mark.parametrize('s, v', longs)
def test_calibration_handle(calibration_method, e, count, s, v):
    with Parser() as p:
        calibration_handle = get_node_from_ast(p.tree_from_a2l(calibration_method[0].format(e.format(long=s)).encode()),
                                               calibration_method[1])
        assert is_iterable(calibration_handle.Handle)
        assert len(calibration_handle.Handle) == count
        for handle in calibration_handle.Handle:
            assert handle.Value == v


@pytest.mark.parametrize('module', [pytest.param(['MOD_PAR', 'CALIBRATION_METHOD', 0], id='MOD_PAR')], indirect=True)
@pytest.mark.parametrize('s', ['/begin CALIBRATION_METHOD {string} {long} /end CALIBRATION_METHOD'])
@pytest.mark.parametrize('string_string, string_value', strings)
@pytest.mark.parametrize('long_string, long_value', longs)
def test_calibration_method(module, s, string_string, string_value, long_string, long_value):
    with Parser() as p:
        calibration_method = get_node_from_ast(
            p.tree_from_a2l(module[0].format(s.format(string=string_string, long=long_string)).encode()), module[1])
        assert calibration_method.Method.Value == string_value
        assert calibration_method.Version.Value == long_value
        assert is_iterable(calibration_method.CALIBRATION_HANDLE)


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
    {discrete}
    {symbol_link}
    {step_size}
    {phys_unit}
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
    with Parser() as p:
        characteristic = p.tree_from_a2l(project_string_minimal.format(module_string_minimal.format(s.format(
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
            ecu_address_extension=empty_string,
            discrete=empty_string,
            symbol_link=empty_string,
            step_size=empty_string,
            phys_unit=empty_string))).encode()).PROJECT.MODULE[0].CHARACTERISTIC[0]
        assert characteristic.Name.Value == ident_value
        assert characteristic.LongIdentifier.Value == string_value
        assert characteristic.Type == enum_type_value
        assert characteristic.Address.Value == long_value
        assert characteristic.Deposit.Value == ident_value
        assert characteristic.MaxDiff.Value == float_value
        assert characteristic.Conversion.Value == ident_value
        assert characteristic.LowerLimit.Value == float_value
        assert characteristic.UpperLimit.Value == float_value
        assert characteristic.DISPLAY_IDENTIFIER.is_none
        assert characteristic.FORMAT.is_none
        assert characteristic.BYTE_ORDER.is_none
        assert characteristic.BIT_MASK.is_none
        assert characteristic.FUNCTION_LIST.is_none
        assert characteristic.NUMBER.is_none
        assert characteristic.EXTENDED_LIMITS.is_none
        assert characteristic.READ_ONLY.is_none
        assert characteristic.GUARD_RAILS.is_none
        assert characteristic.MAP_LIST.is_none
        assert characteristic.MAX_REFRESH.is_none
        assert characteristic.DEPENDENT_CHARACTERISTIC.is_none
        assert characteristic.VIRTUAL_CHARACTERISTIC.is_none
        assert characteristic.REF_MEMORY_SEGMENT.is_none
        assert is_iterable(characteristic.ANNOTATION)
        assert characteristic.COMPARISON_QUANTITY.is_none
        assert is_iterable(characteristic.AXIS_DESCR)
        assert characteristic.CALIBRATION_ACCESS.is_none
        assert characteristic.MATRIX_DIM.is_none
        assert characteristic.ECU_ADDRESS_EXTENSION.is_none
        assert characteristic.DISCRETE.is_none
        assert characteristic.SYMBOL_LINK.is_none
        assert characteristic.STEP_SIZE.is_none
        assert characteristic.PHYS_UNIT.is_none


@pytest.mark.parametrize('module', [pytest.param(['COMPU_METHOD', 0, 'COEFFS'], id='COMPU_METHOD')], indirect=True)
@pytest.mark.parametrize('s', ['COEFFS {float} {float} {float} {float} {float} {float}'])
@pytest.mark.parametrize('float_string, float_value', floats)
def test_coeffs(module, s, float_string, float_value):
    with Parser() as p:
        coeffs = get_node_from_ast(p.tree_from_a2l(module[0].format(s.format(float=float_string)).encode()), module[1])
        assert coeffs.A.Value == float_value
        assert coeffs.B.Value == float_value
        assert coeffs.C.Value == float_value
        assert coeffs.D.Value == float_value
        assert coeffs.E.Value == float_value
        assert coeffs.F.Value == float_value


@pytest.mark.parametrize('module', [
    pytest.param(['CHARACTERISTIC', 0, 'COMPARISON_QUANTITY'], id='CHARACTERISTIC')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('COMPARISON_QUANTITY {}')])
@pytest.mark.parametrize('s, v', idents)
def test_comparison_quantity(module, e, s, v):
    with Parser() as p:
        comparison_quantity = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert comparison_quantity.Name.Value == v


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
    with Parser() as p:
        compu_method = p.tree_from_a2l(project_string_minimal.format(module_string_minimal.format(s.format(
            ident=ident_string,
            string=string_string,
            enum_conversion_type=conversion_type_string,
            formula=empty_string,
            coeffs=empty_string,
            compu_tab_ref=empty_string,
            ref_unit=empty_string))).encode()).PROJECT.MODULE[0].COMPU_METHOD[0]
        assert compu_method.Name.Value == ident_value
        assert compu_method.LongIdentifier.Value == string_value
        assert compu_method.ConversionType == conversion_type_value
        assert compu_method.Format.Value == string_value
        assert compu_method.Unit.Value == string_value
        assert compu_method.FORMULA.is_none
        assert compu_method.COEFFS.is_none
        assert compu_method.COMPU_TAB_REF.is_none
        assert compu_method.REF_UNIT.is_none


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
    with Parser() as p:
        compu_tab = p.tree_from_a2l(project_string_minimal.format(module_string_minimal.format(s.format(
            ident=ident_string,
            string=string_string,
            enum_conversion_type=conversion_type_string,
            int=int_string,
            default_value=empty_string,
            in_val_out_val=in_val_out_val_string))).encode()).PROJECT.MODULE[0].COMPU_TAB[0]
        assert compu_tab.Name.Value == ident_value
        assert compu_tab.LongIdentifier.Value == string_value
        assert compu_tab.ConversionType == conversion_type_value
        assert compu_tab.NumberValuePairs.Value == int_value
        assert is_iterable(compu_tab.InValOutVal)
        assert [(e.InVal.Value, e.OutVal.Value) for e in compu_tab.InValOutVal] == in_val_out_val_value
        assert compu_tab.DEFAULT_VALUE.is_none


@pytest.mark.parametrize('module', [
    pytest.param(['COMPU_METHOD', 0, 'COMPU_TAB_REF'], id='COMPU_METHOD')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('COMPU_TAB_REF {}')])
@pytest.mark.parametrize('s, v', idents)
def test_compu_tab_ref(module, e, s, v):
    with Parser() as p:
        compu_tab_ref = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert compu_tab_ref.ConversionTable.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['CHARACTERISTIC', 0, 'SYMBOL_LINK'], id='CHARACTERISTIC'),
    pytest.param(['MEASUREMENT', 0, 'SYMBOL_LINK'], id='MEASUREMENT'),
    pytest.param(['AXIS_PTS', 0, 'SYMBOL_LINK'], id='AXIS_PTS')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('SYMBOL_LINK {} {}')])
@pytest.mark.parametrize('string_string, string_value', strings)
@pytest.mark.parametrize('long_string, long_value', longs)
def test_symbol_link(module, e, string_string, string_value, long_string, long_value):
    with Parser() as p:
        symbol_link = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(string_string, long_string)).encode()), module[1])
        assert symbol_link.SymbolName.Value == string_value
        assert symbol_link.Offset.Value == long_value


@pytest.mark.parametrize('module', [
    pytest.param(['CHARACTERISTIC', 0, 'STEP_SIZE'], id='CHARACTERISTIC'),
    pytest.param(['CHARACTERISTIC', 0, 'AXIS_DESCR', 0, 'STEP_SIZE'], id='AXIS_DESCR'),
    pytest.param(['AXIS_PTS', 0, 'STEP_SIZE'], id='AXIS_PTS')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('STEP_SIZE {}')])
@pytest.mark.parametrize('s, v', floats)
def test_step_size(module, e, s, v):
    with Parser() as p:
        step_size = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert step_size.StepSize.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['CHARACTERISTIC', 0, 'PHYS_UNIT'], id='CHARACTERISTIC'),
    pytest.param(['MEASUREMENT', 0, 'PHYS_UNIT'], id='MEASUREMENT'),
    pytest.param(['CHARACTERISTIC', 0, 'AXIS_DESCR', 0, 'PHYS_UNIT'], id='AXIS_DESCR'),
    pytest.param(['AXIS_PTS', 0, 'PHYS_UNIT'], id='AXIS_PTS')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('PHYS_UNIT {}')])
@pytest.mark.parametrize('s, v', strings)
def test_phys_unit(module, e, s, v):
    with Parser() as p:
        phys_unit = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert phys_unit.Unit.Value == v


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
    with Parser() as p:
        compu_vtab = p.tree_from_a2l(project_string_minimal.format(module_string_minimal.format(s.format(
            ident=ident_string,
            string=string_string,
            enum_conversion_type=conversion_type_string,
            int=int_string,
            default_value=empty_string,
            in_val_out_val=in_val_out_val_string))).encode()).PROJECT.MODULE[0].COMPU_VTAB[0]
        assert compu_vtab.Name.Value == ident_value
        assert compu_vtab.LongIdentifier.Value == string_value
        assert compu_vtab.ConversionType == conversion_type_value
        assert compu_vtab.NumberValuePairs.Value == int_value
        assert is_iterable(compu_vtab.InValOutVal)
        assert [(e.InVal.Value, e.OutVal.Value) for e in compu_vtab.InValOutVal] == in_val_out_val_value
        assert compu_vtab.DEFAULT_VALUE.is_none


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
    with Parser() as p:
        compu_vtab_range = p.tree_from_a2l(project_string_minimal.format(module_string_minimal.format(s.format(
            ident=ident_string,
            string=string_string,
            int=int_string,
            default_value=empty_string,
            in_val_out_val=in_val_out_val_string))).encode()).PROJECT.MODULE[0].COMPU_VTAB_RANGE[0]
        assert compu_vtab_range.Name.Value == ident_value
        assert compu_vtab_range.LongIdentifier.Value == string_value
        assert compu_vtab_range.NumberOfValuesTriples.Value == int_value
        assert is_iterable(compu_vtab_range.InValMinInValMaxOutVal)
        assert [(e.InValMin.Value, e.InValMax.Value, e.OutVal.Value) for e in compu_vtab_range.InValMinInValMaxOutVal] \
               == in_val_out_val_value
        assert compu_vtab_range.DEFAULT_VALUE.is_none


@pytest.mark.parametrize('module', [pytest.param(['MOD_PAR', 'CPU_TYPE'], id='MOD_PAR')], indirect=True)
@pytest.mark.parametrize('s', [pytest.param('CPU_TYPE {}')])
@pytest.mark.parametrize('string_string, string_value', strings)
def test_cpu_type(module, s, string_string, string_value):
    with Parser() as p:
        cpu_type = get_node_from_ast(p.tree_from_a2l(module[0].format(s.format(string_string)).encode()), module[1])
        assert cpu_type.Cpu.Value == string_value


@pytest.mark.parametrize('module', [
    pytest.param(['CHARACTERISTIC', 0, 'AXIS_DESCR', 0, 'CURVE_AXIS_REF'], id='AXIS_DESCR')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('CURVE_AXIS_REF {}')])
@pytest.mark.parametrize('s, v', idents)
def test_curve_axis_ref(module, e, s, v):
    with Parser() as p:
        curve_axis_ref = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert curve_axis_ref.CurveAxis.Value == v


@pytest.mark.parametrize('module', [pytest.param(['MOD_PAR', 'CUSTOMER'], id='MOD_PAR')], indirect=True)
@pytest.mark.parametrize('s', [pytest.param('CUSTOMER {}')])
@pytest.mark.parametrize('string_string, string_value', strings)
def test_customer(module, s, string_string, string_value):
    with Parser() as p:
        customer = get_node_from_ast(p.tree_from_a2l(module[0].format(s.format(string_string)).encode()), module[1])
        assert customer.Customer.Value == string_value


@pytest.mark.parametrize('module', [pytest.param(['MOD_PAR', 'CUSTOMER_NO'], id='MOD_PAR')], indirect=True)
@pytest.mark.parametrize('s', [pytest.param('CUSTOMER_NO {}')])
@pytest.mark.parametrize('string_string, string_value', strings)
def test_customer_no(module, s, string_string, string_value):
    with Parser() as p:
        customer_no = get_node_from_ast(p.tree_from_a2l(module[0].format(s.format(string_string)).encode()), module[1])
        assert customer_no.Number.Value == string_value


@pytest.mark.parametrize('module', [pytest.param(['MOD_COMMON', 'DATA_SIZE'], id='MOD_COMMON')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('DATA_SIZE {}')])
@pytest.mark.parametrize('s, v', ints)
def test_data_size(module, e, s, v):
    with Parser() as p:
        data_size = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert data_size.Size.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['COMPU_TAB', 0, 'DEFAULT_VALUE'], id='COMPU_TAB'),
    pytest.param(['COMPU_VTAB', 0, 'DEFAULT_VALUE'], id='COMPU_VTAB'),
    pytest.param(['COMPU_VTAB_RANGE', 0, 'DEFAULT_VALUE'], id='COMPU_VTAB_RANGE')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('DEFAULT_VALUE {}')])
@pytest.mark.parametrize('s, v', strings)
def test_default_value(module, e, s, v):
    with Parser() as p:
        default_value = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert default_value.DisplayString.Value == v


@pytest.mark.parametrize('module', [pytest.param(['FUNCTION', 0, 'DEF_CHARACTERISTIC'], id='FUNCTION')], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('/begin DEF_CHARACTERISTIC /end DEF_CHARACTERISTIC', 0, id='no identifier'),
    pytest.param('/begin DEF_CHARACTERISTIC {ident} /end DEF_CHARACTERISTIC', 1, id='one identifier'),
    pytest.param('/begin DEF_CHARACTERISTIC {ident} {ident} /end DEF_CHARACTERISTIC', 2, id='two identifier')])
@pytest.mark.parametrize('s, v', idents)
def test_def_characteristic(module, e, count, s, v):
    with Parser() as p:
        def_characteristic = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(ident=s)).encode()), module[1])
        assert is_iterable(def_characteristic.Identifier)
        assert len(def_characteristic.Identifier) == count
        for identifier in def_characteristic.Identifier:
            assert identifier.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['CHARACTERISTIC', 0, 'DEPENDENT_CHARACTERISTIC'], id='CHARACTERISTIC')], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('/begin DEPENDENT_CHARACTERISTIC {string} /end DEPENDENT_CHARACTERISTIC', 0,
                 id='no characteristic'),
    pytest.param('/begin DEPENDENT_CHARACTERISTIC {string} {ident} /end DEPENDENT_CHARACTERISTIC', 1,
                 id='one characteristic'),
    pytest.param('/begin DEPENDENT_CHARACTERISTIC {string} {ident} {ident} /end DEPENDENT_CHARACTERISTIC', 2,
                 id='two characteristic')])
@pytest.mark.parametrize('string_string, string_value', strings)
@pytest.mark.parametrize('ident_string, ident_value', idents)
def test_dependent_characteristic(module, e, count, string_string, string_value, ident_string, ident_value):
    with Parser() as p:
        dependent_characteristic = get_node_from_ast(
            p.tree_from_a2l(module[0].format(e.format(string=string_string, ident=ident_string)).encode()), module[1])
        assert dependent_characteristic.Formula.Value == string_value
        assert is_iterable(dependent_characteristic.Characteristic)
        assert len(dependent_characteristic.Characteristic) == count
        for characteristic in dependent_characteristic.Characteristic:
            assert characteristic.Value == ident_value


@pytest.mark.parametrize('module', [
    pytest.param(['MOD_COMMON', 'DEPOSIT'], id='MOD_COMMON'),
    pytest.param(['CHARACTERISTIC', 0, 'AXIS_DESCR', 0, 'DEPOSIT'], id='AXIS_DESCR'),
    pytest.param(['AXIS_PTS', 0, 'DEPOSIT'], id='AXIS_PTS')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('DEPOSIT {}')])
@pytest.mark.parametrize('s, v', enum_mode_deposit)
def test_deposit(module, e, s, v):
    with Parser() as p:
        deposit = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert deposit.Mode == v


@pytest.mark.parametrize('module', [
    pytest.param(['MEASUREMENT', 0, 'DISCRETE'], id='MEASUREMENT'),
    pytest.param(['CHARACTERISTIC', 0, 'DISCRETE'], id='CHARACTERISTIC')], indirect=True)
@pytest.mark.parametrize('e, a', [pytest.param('DISCRETE', True), pytest.param('', False)])
def test_discrete(module, e, a):
    with Parser() as p:
        discrete = get_node_from_ast(p.tree_from_a2l(module[0].format(e).encode()), module[1])
        assert discrete.is_none is not a


@pytest.mark.parametrize('module', [
    pytest.param(['MEASUREMENT', 0, 'DISPLAY_IDENTIFIER'], id='MEASUREMENT'),
    pytest.param(['CHARACTERISTIC', 0, 'DISPLAY_IDENTIFIER'], id='CHARACTERISTIC'),
    pytest.param(['AXIS_PTS', 0, 'DISPLAY_IDENTIFIER'], id='AXIS_PTS')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('DISPLAY_IDENTIFIER {}')])
@pytest.mark.parametrize('s, v', idents)
def test_display_identifier(module, e, s, v):
    with Parser() as p:
        display_identifier = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert display_identifier.DisplayName.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'DIST_OP_X'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['DIST_OP_X {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_dist_op_x(module,
                   s,
                   int_string, int_value,
                   data_type_string, data_type_value):
    with Parser() as p:
        dist_op_x = get_node_from_ast(
            p.tree_from_a2l(module[0].format(s.format(int=int_string, data_type=data_type_string)).encode()), module[1])
        assert dist_op_x.Position.Value == int_value
        assert dist_op_x.DataType.Value == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'DIST_OP_Y'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['DIST_OP_Y {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_dist_op_y(module,
                   s,
                   int_string, int_value,
                   data_type_string, data_type_value):
    with Parser() as p:
        dist_op_y = get_node_from_ast(
            p.tree_from_a2l(module[0].format(s.format(int=int_string, data_type=data_type_string)).encode()), module[1])
        assert dist_op_y.Position.Value == int_value
        assert dist_op_y.DataType.Value == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'DIST_OP_Z'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['DIST_OP_Z {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_dist_op_z(module,
                   s,
                   int_string, int_value,
                   data_type_string, data_type_value):
    with Parser() as p:
        dist_op_z = get_node_from_ast(
            p.tree_from_a2l(module[0].format(s.format(int=int_string, data_type=data_type_string)).encode()), module[1])
        assert dist_op_z.Position.Value == int_value
        assert dist_op_z.DataType.Value == data_type_value


@pytest.mark.parametrize('module', [pytest.param(['MOD_PAR', 'ECU'], id='MOD_PAR')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('ECU {}')])
@pytest.mark.parametrize('s, v', strings)
def test_ecu(module, e, s, v):
    with Parser() as p:
        ecu = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert ecu.ControlUnit.Value == v


@pytest.mark.parametrize('module', [pytest.param(['MEASUREMENT', 0, 'ECU_ADDRESS'], id='MEASUREMENT')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('ECU_ADDRESS {}')])
@pytest.mark.parametrize('s, v', longs)
def test_ecu_address(module, e, s, v):
    with Parser() as p:
        ecu_address = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert ecu_address.Address.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['CHARACTERISTIC', 0, 'ECU_ADDRESS_EXTENSION'], id='CHARACTERISTIC'),
    pytest.param(['MEASUREMENT', 0, 'ECU_ADDRESS_EXTENSION'], id='MEASUREMENT'),
    pytest.param(['AXIS_PTS', 0, 'ECU_ADDRESS_EXTENSION'], id='AXIS_PTS')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('ECU_ADDRESS_EXTENSION {}')])
@pytest.mark.parametrize('s, v', ints)
def test_ecu_address_extension(module, e, s, v):
    with Parser() as p:
        ecu_address_extension = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert ecu_address_extension.Extension.Value == v


@pytest.mark.parametrize('module', [pytest.param(['MOD_PAR', 'ECU_CALIBRATION_OFFSET'], id='MOD_PAR')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('ECU_CALIBRATION_OFFSET {}')])
@pytest.mark.parametrize('s, v', longs)
def test_ecu_calibration_offset(module, e, s, v):
    with Parser() as p:
        ecu_calibration_offset = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert ecu_calibration_offset.Offset.Value == v


@pytest.mark.parametrize('module', [pytest.param(['MOD_PAR', 'EPK'], id='MOD_PAR')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('EPK {}')])
@pytest.mark.parametrize('s, v', strings)
def test_epk(module, e, s, v):
    with Parser() as p:
        epk = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert epk.Identifier.Value == v


@pytest.mark.parametrize('module', [pytest.param(['MEASUREMENT', 0, 'ERROR_MASK'], id='MEASUREMENT')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('ERROR_MASK {}')])
@pytest.mark.parametrize('s, v', longs)
def test_error_mask(module, e, s, v):
    with Parser() as p:
        error_mask = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert error_mask.Mask.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['CHARACTERISTIC', 0, 'AXIS_DESCR', 0, 'EXTENDED_LIMITS'], id='AXIS_DESCR'),
    pytest.param(['AXIS_PTS', 0, 'EXTENDED_LIMITS'], id='AXIS_PTS')], indirect=True)
@pytest.mark.parametrize('e', ['EXTENDED_LIMITS {float} {float}'])
@pytest.mark.parametrize('s, v', floats)
def test_extended_limits(module, e, s, v):
    with Parser() as p:
        extended_limits = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(float=s)).encode()), module[1])
        assert extended_limits.LowerLimit.Value == v
        assert extended_limits.UpperLimit.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['CHARACTERISTIC', 0, 'AXIS_DESCR', 0, 'FIX_AXIS_PAR'], id='AXIS_DESCR')], indirect=True)
@pytest.mark.parametrize('e', ['FIX_AXIS_PAR {int} {int} {int}'])
@pytest.mark.parametrize('s, v', ints)
def test_fix_axis_par(module, e, s, v):
    with Parser() as p:
        fix_axis_par = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(int=s)).encode()), module[1])
        assert fix_axis_par.Offset.Value == v
        assert fix_axis_par.Shift.Value == v
        assert fix_axis_par.Numberapo.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['CHARACTERISTIC', 0, 'AXIS_DESCR', 0, 'FIX_AXIS_PAR_DIST'], id='AXIS_DESCR')], indirect=True)
@pytest.mark.parametrize('e', ['FIX_AXIS_PAR_DIST {int} {int} {int}'])
@pytest.mark.parametrize('s, v', ints)
def test_fix_axis_par_dist(module, e, s, v):
    with Parser() as p:
        fix_axis_par_dist = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(int=s)).encode()), module[1])
        assert fix_axis_par_dist.Offset.Value == v
        assert fix_axis_par_dist.Distance.Value == v
        assert fix_axis_par_dist.Numberapo.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['CHARACTERISTIC', 0, 'AXIS_DESCR', 0, 'FIX_AXIS_PAR_LIST'], id='AXIS_DESCR')], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('/begin FIX_AXIS_PAR_LIST /end FIX_AXIS_PAR_LIST', 0, id='no axis_pts_value'),
    pytest.param('/begin FIX_AXIS_PAR_LIST {float} /end FIX_AXIS_PAR_LIST', 1, id='one axis_pts_value'),
    pytest.param('/begin FIX_AXIS_PAR_LIST {float} {float} /end FIX_AXIS_PAR_LIST', 2, id='two axis_pts_value')])
@pytest.mark.parametrize('s, v', floats)
def test_fix_axis_par_list(module, e, count, s, v):
    with Parser() as p:
        fix_axis_par_list = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(float=s)).encode()), module[1])
        assert is_iterable(fix_axis_par_list.AxisPtsValue)
        assert len(fix_axis_par_list.AxisPtsValue) == count
        for axis_pts_value in fix_axis_par_list.AxisPtsValue:
            assert axis_pts_value.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'FIX_NO_AXIS_PTS_X'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', ['FIX_NO_AXIS_PTS_X {}'])
@pytest.mark.parametrize('s, v', ints)
def test_fix_no_axis_pts_x(module, e, s, v):
    with Parser() as p:
        fix_no_axis_pts_x = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert fix_no_axis_pts_x.NumberOfAxisPoints.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'FIX_NO_AXIS_PTS_Y'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', ['FIX_NO_AXIS_PTS_Y {}'])
@pytest.mark.parametrize('s, v', ints)
def test_fix_no_axis_pts_y(module, e, s, v):
    with Parser() as p:
        fix_no_axis_pts_y = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert fix_no_axis_pts_y.NumberOfAxisPoints.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'FIX_NO_AXIS_PTS_Z'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', ['FIX_NO_AXIS_PTS_Z {}'])
@pytest.mark.parametrize('s, v', ints)
def test_fix_no_axis_pts_z(module, e, s, v):
    with Parser() as p:
        fix_no_axis_pts_z = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert fix_no_axis_pts_z.NumberOfAxisPoints.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'FNC_VALUES'], id='RECORD_LAYOUT')], indirect=True)
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
    with Parser() as p:
        fnc_values = get_node_from_ast(p.tree_from_a2l(module[0].format(s.format(int=int_string,
                                                                                 data_type=data_type_string,
                                                                                 enum_index_mode=enum_index_mode_string,
                                                                                 addr_type=addr_type_string)).encode()),
                                       module[1])
        assert fnc_values.Position.Value == int_value
        assert fnc_values.DataType.Value == data_type_value
        assert fnc_values.IndexMode == enum_index_mode_value
        assert fnc_values.AddressType.Value == addr_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['CHARACTERISTIC', 0, 'FORMAT'], id='MOD_PAR'),
    pytest.param(['CHARACTERISTIC', 0, 'AXIS_DESCR', 0, 'FORMAT'], id='AXIS_DESCR'),
    pytest.param(['MEASUREMENT', 0, 'FORMAT'], id='MEASUREMENT'),
    pytest.param(['AXIS_PTS', 0, 'FORMAT'], id='AXIS_PTS')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('FORMAT {}')])
@pytest.mark.parametrize('s, v', strings)
def test_format(module, e, s, v):
    with Parser() as p:
        format = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert format.FormatString.Value == v


@pytest.mark.parametrize('module', [pytest.param(['COMPU_METHOD', 0, 'FORMULA'], id='COMPU_METHOD')], indirect=True)
@pytest.mark.parametrize('e', ['/begin FORMULA {} /end FORMULA'])
@pytest.mark.parametrize('s, v', strings)
def test_formula(module, e, s, v):
    with Parser() as p:
        formula = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert formula.FX.Value == v
        assert formula.FORMULA_INV.is_none


@pytest.mark.parametrize('compu_method', [pytest.param(['FORMULA', 'FORMULA_INV'], id='COMPU_METHOD')], indirect=True)
@pytest.mark.parametrize('e', ['FORMULA_INV {}'])
@pytest.mark.parametrize('s, v', strings)
def test_formula_inv(compu_method, e, s, v):
    with Parser() as p:
        formula_inv = get_node_from_ast(p.tree_from_a2l(compu_method[0].format(e.format(s)).encode()), compu_method[1])
        assert formula_inv.GX.Value == v


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
    with Parser() as p:
        frame = p.tree_from_a2l(project_string_minimal.format(module_string_minimal.format(s.format(
            ident=ident_string,
            string=string_string,
            int=int_string,
            long=long_string,
            frame_measurement=empty_string,
            if_data=empty_string))).encode()).PROJECT.MODULE[0].FRAME
        assert frame.Name.Value == ident_value
        assert frame.LongIdentifier.Value == string_value
        assert frame.ScalingUnit.Value == int_value
        assert frame.Rate.Value == long_value
        assert frame.FRAME_MEASUREMENT.is_none


@pytest.mark.parametrize('module', [pytest.param(['FRAME', 'FRAME_MEASUREMENT'], id='FRAME')], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('FRAME_MEASUREMENT', 0, id='no identifier'),
    pytest.param('FRAME_MEASUREMENT {ident}', 1, id='one identifier'),
    pytest.param('FRAME_MEASUREMENT {ident} {ident}', 2, id='two identifier')])
@pytest.mark.parametrize('s, v', idents)
def test_frame_measurement(module, e, count, s, v):
    with Parser() as p:
        frame_measurement = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(ident=s)).encode()), module[1])
        assert is_iterable(frame_measurement.Identifier)
        assert len(frame_measurement.Identifier) == count
        for identifier in frame_measurement.Identifier:
            assert identifier.Value == v


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
    with Parser() as p:
        function = p.tree_from_a2l(project_string_minimal.format(module_string_minimal.format(s.format(
            ident=ident_string,
            string=string_string,
            annotation=empty_string,
            def_characteristic=empty_string,
            ref_characteristic=empty_string,
            in_measurement=empty_string,
            out_measurement=empty_string,
            loc_measurement=empty_string,
            sub_function=empty_string,
            function_version=empty_string))).encode()).PROJECT.MODULE[0].FUNCTION[0]
        assert function.Name.Value == ident_value
        assert function.LongIdentifier.Value == string_value
        assert is_iterable(function.ANNOTATION)
        assert function.DEF_CHARACTERISTIC.is_none
        assert function.REF_CHARACTERISTIC.is_none
        assert function.IN_MEASUREMENT.is_none
        assert function.OUT_MEASUREMENT.is_none
        assert function.LOC_MEASUREMENT.is_none
        assert function.SUB_FUNCTION.is_none
        assert function.FUNCTION_VERSION.is_none


@pytest.mark.parametrize('module', [
    pytest.param(['AXIS_PTS', 0, 'FUNCTION_LIST'], id='AXIS_PTS'),
    pytest.param(['CHARACTERISTIC', 0, 'FUNCTION_LIST'], id='CHARACTERISTIC'),
    pytest.param(['MEASUREMENT', 0, 'FUNCTION_LIST'], id='MEASUREMENT'),
    pytest.param(['GROUP', 0, 'FUNCTION_LIST'], id='GROUP')], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('/begin FUNCTION_LIST /end FUNCTION_LIST', 0, id='no name'),
    pytest.param('/begin FUNCTION_LIST {ident} /end FUNCTION_LIST', 1, id='one name'),
    pytest.param('/begin FUNCTION_LIST {ident} {ident} /end FUNCTION_LIST', 2, id='two name')])
@pytest.mark.parametrize('s, v', idents)
def test_function_list(module, e, count, s, v):
    with Parser() as p:
        function_list = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(ident=s)).encode()), module[1])
        assert len(function_list.Name) == count
        for name in function_list.Name:
            assert name.Value == v


@pytest.mark.parametrize('module', [pytest.param(['FUNCTION', 0, 'FUNCTION_VERSION'], id='FUNCTION')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('FUNCTION_VERSION {}')])
@pytest.mark.parametrize('s, v', strings)
def test_function_version(module, e, s, v):
    with Parser() as p:
        function_version = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert function_version.VersionIdentifier.Value == v


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
    with Parser() as p:
        group = p.tree_from_a2l(project_string_minimal.format(module_string_minimal.format(s.format(
            ident=ident_string,
            string=string_string,
            annotation=empty_string,
            root=empty_string,
            ref_characteristic=empty_string,
            ref_measurement=empty_string,
            function_list=empty_string,
            sub_group=empty_string))).encode()).PROJECT.MODULE[0].GROUP[0]
        assert group.GroupName.Value == ident_value
        assert group.GroupLongIdentifier.Value == string_value
        assert is_iterable(group.ANNOTATION)
        assert group.ROOT.is_none
        assert group.REF_CHARACTERISTIC.is_none
        assert group.REF_MEASUREMENT.is_none
        assert group.FUNCTION_LIST.is_none
        assert group.SUB_GROUP.is_none


@pytest.mark.parametrize('module', [
    pytest.param(['CHARACTERISTIC', 0, 'GUARD_RAILS'], id='CHARACTERISTIC'),
    pytest.param(['AXIS_PTS', 0, 'GUARD_RAILS'], id='AXIS_PTS')], indirect=True)
@pytest.mark.parametrize('e, a', [pytest.param('GUARD_RAILS', True), pytest.param('', False)])
def test_guard_rails(module, e, a):
    with Parser() as p:
        guard_rails = get_node_from_ast(p.tree_from_a2l(module[0].format(e).encode()), module[1])
        assert guard_rails.is_none is not a


# TODO: check if fully tested.
@pytest.mark.parametrize('e', ['/begin HEADER {string} {version} {project_no} /end HEADER'])
@pytest.mark.parametrize('s, v', strings)
def test_header(e, s, v):
    with Parser() as p:
        ast = p.tree_from_a2l(project_string_minimal.format(e.format(string=s,
                                                                     version=empty_string,
                                                                     project_no=empty_string)).encode())
        assert ast.PROJECT.HEADER.Comment.Value == v
        assert ast.PROJECT.HEADER.VERSION.is_none
        assert ast.PROJECT.HEADER.PROJECT_NO.is_none


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'IDENTIFICATION'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', ['IDENTIFICATION {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_identification(module,
                        e,
                        int_string, int_value,
                        data_type_string, data_type_value):
    with Parser() as p:
        identification = get_node_from_ast(
            p.tree_from_a2l(module[0].format(e.format(int=int_string, data_type=data_type_string)).encode()), module[1])
        assert identification.Position.Value == int_value
        assert identification.DataType.Value == data_type_value


@pytest.mark.parametrize('module', [pytest.param(['FUNCTION', 0, 'IN_MEASUREMENT'], id='FUNCTION')], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('/begin IN_MEASUREMENT /end IN_MEASUREMENT', 0, id='no identifier'),
    pytest.param('/begin IN_MEASUREMENT {ident} /end IN_MEASUREMENT', 1, id='one identifier'),
    pytest.param('/begin IN_MEASUREMENT {ident} {ident} /end IN_MEASUREMENT', 2, id='two identifier')])
@pytest.mark.parametrize('s, v', idents)
def test_in_measurement(module, e, count, s, v):
    with Parser() as p:
        in_measurement = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(ident=s)).encode()), module[1])
        assert is_iterable(in_measurement.Identifier)
        assert len(in_measurement.Identifier) == count
        for identifier in in_measurement.Identifier:
            assert identifier.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['MEASUREMENT', 0, 'BIT_OPERATION', 'LEFT_SHIFT'], id='MEASUREMENT')], indirect=True)
@pytest.mark.parametrize('e', ['LEFT_SHIFT {}'])
@pytest.mark.parametrize('s, v', longs)
def test_left_shift(module, e, s, v):
    with Parser() as p:
        left_shift = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert left_shift.BitCount.Value == v


@pytest.mark.parametrize('module', [pytest.param(['FUNCTION', 0, 'LOC_MEASUREMENT'], id='FUNCTION'), ], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('/begin LOC_MEASUREMENT /end LOC_MEASUREMENT', 0, id='no identifier'),
    pytest.param('/begin LOC_MEASUREMENT {ident} /end LOC_MEASUREMENT', 1, id='one identifier'),
    pytest.param('/begin LOC_MEASUREMENT {ident} {ident} /end LOC_MEASUREMENT', 2, id='two identifier')])
@pytest.mark.parametrize('s, v', idents)
def test_loc_measurement(module, e, count, s, v):
    with Parser() as p:
        loc_measurement = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(ident=s)).encode()), module[1])
        assert is_iterable(loc_measurement.Identifier)
        assert len(loc_measurement.Identifier) == count
        for identifier in loc_measurement.Identifier:
            assert identifier.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['CHARACTERISTIC', 0, 'MAP_LIST'], id='CHARACTERISTIC')], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('/begin MAP_LIST /end MAP_LIST', 0, id='no ident'),
    pytest.param('/begin MAP_LIST {ident} /end MAP_LIST', 1, id='one ident'),
    pytest.param('/begin MAP_LIST {ident} {ident} /end MAP_LIST', 2, id='two ident')])
@pytest.mark.parametrize('s, v', idents)
def test_map_list(module, e, count, s, v):
    with Parser() as p:
        map_list = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(ident=s)).encode()), module[1])
        assert is_iterable(map_list.Name)
        assert len(map_list.Name) == count
        for name in map_list.Name:
            assert name.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['MEASUREMENT', 0, 'MATRIX_DIM'], id='MEASUREMENT'),
    pytest.param(['CHARACTERISTIC', 0, 'MATRIX_DIM'], id='CHARACTERISTIC')], indirect=True)
@pytest.mark.parametrize('e', ['MATRIX_DIM {int} {int} {int}'])
@pytest.mark.parametrize('s, v', ints)
def test_matrix_dim(module, e, s, v):
    with Parser() as p:
        matrix_dim = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(int=s)).encode()), module[1])
        assert matrix_dim.XDim.Value == v
        assert matrix_dim.YDim.Value == v
        assert matrix_dim.ZDim.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['CHARACTERISTIC', 0, 'AXIS_DESCR', 0, 'MAX_GRAD'], id='AXIS_DESCR')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('MAX_GRAD {}')])
@pytest.mark.parametrize('s, v', floats)
def test_max_grad(module, e, s, v):
    with Parser() as p:
        max_grad = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert max_grad.MaxGradient.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['CHARACTERISTIC', 0, 'MAX_REFRESH'], id='CHARACTERISTIC'),
    pytest.param(['MEASUREMENT', 0, 'MAX_REFRESH'], id='MEASUREMENT')], indirect=True)
@pytest.mark.parametrize('s', max_refresh_strings)
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('long_string, long_value', longs)
def test_max_refresh(module, s, int_string, int_value, long_string, long_value):
    with Parser() as p:
        max_refresh = get_node_from_ast(p.tree_from_a2l(module[0].format(s.format(int=int_string, long=long_string)).encode()),
                                        module[1])
        assert max_refresh.ScalingUnit.Value == int_value
        assert max_refresh.Rate.Value == long_value


@pytest.mark.parametrize('module', [
    pytest.param(['MEASUREMENT', 0, 'LAYOUT'], id='MEASUREMENT')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('LAYOUT {}')])
@pytest.mark.parametrize('s, v', enum_index_modes)
def test_layout(module, e, s, v):
    with Parser() as p:
        layout = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert layout.IndexMode == v


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
    {discrete}
    {layout}
    {symbol_link}
    {phys_unit}
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
    with Parser() as p:
        measurement = p.tree_from_a2l(project_string_minimal.format(module_string_minimal.format(s.format(
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
            ecu_address_extension=empty_string,
            discrete=empty_string,
            layout=empty_string,
            symbol_link=empty_string,
            phys_unit=empty_string))).encode()).PROJECT.MODULE[0].MEASUREMENT[0]
        assert measurement.Name.Value == ident_value
        assert measurement.LongIdentifier.Value == string_value
        assert measurement.DataType.Value == data_type_value
        assert measurement.Conversion.Value == ident_value
        assert measurement.Resolution.Value == int_value
        assert measurement.Accuracy.Value == float_value
        assert measurement.LowerLimit.Value == float_value
        assert measurement.UpperLimit.Value == float_value
        assert measurement.DISPLAY_IDENTIFIER.is_none
        assert measurement.READ_WRITE.is_none
        assert measurement.FORMAT.is_none
        assert measurement.ARRAY_SIZE.is_none
        assert measurement.BIT_MASK.is_none
        assert measurement.BIT_OPERATION.is_none
        assert measurement.BYTE_ORDER.is_none
        assert measurement.MAX_REFRESH.is_none
        assert measurement.VIRTUAL.is_none
        assert measurement.ERROR_MASK.is_none
        assert measurement.FUNCTION_LIST.is_none
        assert measurement.ECU_ADDRESS.is_none
        assert measurement.REF_MEMORY_SEGMENT.is_none
        assert is_iterable(measurement.ANNOTATION)
        assert measurement.MATRIX_DIM.is_none
        assert measurement.ECU_ADDRESS_EXTENSION.is_none
        assert measurement.DISCRETE.is_none
        assert measurement.LAYOUT.is_none
        assert measurement.SYMBOL_LINK.is_none
        assert measurement.PHYS_UNIT.is_none


@pytest.mark.parametrize('module', [pytest.param(['MOD_PAR', 'MEMORY_LAYOUT', 0], id='MOD_PAR')], indirect=True)
@pytest.mark.parametrize('s', memory_layout_strings)
@pytest.mark.parametrize('enum_prg_type_string, enum_prg_type_value', enum_prg_type_memory_layout_strings)
@pytest.mark.parametrize('long_string, long_value', longs)
@pytest.mark.parametrize('offset_string, offset_value', offset_strings)
def test_memory_layout(module,
                       s,
                       enum_prg_type_string, enum_prg_type_value,
                       long_string, long_value,
                       offset_string, offset_value):
    with Parser() as p:
        memory_layout = get_node_from_ast(p.tree_from_a2l(module[0].format(s.format(enum_prg_type=enum_prg_type_string,
                                                                                    long=long_string,
                                                                                    offset=offset_string,
                                                                                    if_data=empty_string)).encode()),
                                          module[1])
        assert memory_layout.PrgType == enum_prg_type_value
        assert memory_layout.Address.Value == long_value
        assert memory_layout.Size.Value == long_value
        assert [o.Value for o in memory_layout.Offset] == offset_value


@pytest.mark.parametrize('module', [pytest.param(['MOD_PAR', 'MEMORY_SEGMENT', 0], id='MOD_PAR')], indirect=True)
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
    with Parser() as p:
        memory_segment = get_node_from_ast(p.tree_from_a2l(module[0].format(s.format(ident=ident_string,
                                                                                     string=string_string,
                                                                                     enum_prg_type=enum_prg_type_string,
                                                                                     enum_memory_type=enum_memory_type_string,
                                                                                     enum_attribute=enum_attribute_string,
                                                                                     long=long_string,
                                                                                     offset=offset_string,
                                                                                     if_data=empty_string)).encode()),
                                           module[1])
        assert memory_segment.Name.Value == ident_value
        assert memory_segment.LongIdentifier.Value == string_value
        assert memory_segment.PrgType == enum_prg_type_value
        assert memory_segment.MemoryType == enum_memory_type_value
        assert memory_segment.Attribute == enum_attribute_value
        assert memory_segment.Address.Value == long_value
        assert memory_segment.Size.Value == long_value
        assert [o.Value for o in memory_segment.Offset] == offset_value


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
    with Parser() as p:
        module = p.tree_from_a2l(project_string_minimal.format(s.format(ident=ident_string,
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
                                                                        unit=empty_string)).encode()).PROJECT.MODULE[0]
        assert module.Name.Value == ident_value
        assert module.LongIdentifier.Value == string_value
        assert module.A2ML.is_none
        assert module.MOD_PAR.is_none
        assert module.MOD_COMMON.is_none
        assert is_iterable(module.IF_DATA)
        assert is_iterable(module.CHARACTERISTIC)
        assert is_iterable(module.AXIS_PTS)
        assert is_iterable(module.MEASUREMENT)
        assert is_iterable(module.COMPU_METHOD)
        assert is_iterable(module.COMPU_TAB)
        assert is_iterable(module.COMPU_VTAB)
        assert is_iterable(module.COMPU_VTAB_RANGE)
        assert is_iterable(module.FUNCTION)
        assert is_iterable(module.GROUP)
        assert is_iterable(module.RECORD_LAYOUT)
        assert module.VARIANT_CODING.is_none
        assert module.FRAME.is_none
        assert is_iterable(module.USER_RIGHTS)
        assert is_iterable(module.UNIT)


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
    with Parser() as p:
        mod_common = p.tree_from_a2l(project_string_minimal.format(module_string_minimal.format(s.format(
            string=string_string,
            s_rec_layout=empty_string,
            deposit=empty_string,
            byte_order=empty_string,
            data_size=empty_string,
            alignment_byte=empty_string,
            alignment_word=empty_string,
            alignment_long=empty_string,
            alignment_float32_ieee=empty_string,
            alignment_float64_ieee=empty_string))).encode()).PROJECT.MODULE[0].MOD_COMMON
        assert mod_common.Comment.Value == string_value
        assert mod_common.S_REC_LAYOUT.is_none
        assert mod_common.DEPOSIT.is_none
        assert mod_common.BYTE_ORDER.is_none
        assert mod_common.DATA_SIZE.is_none
        assert mod_common.ALIGNMENT_BYTE.is_none
        assert mod_common.ALIGNMENT_WORD.is_none
        assert mod_common.ALIGNMENT_LONG.is_none
        assert mod_common.ALIGNMENT_FLOAT32_IEEE.is_none
        assert mod_common.ALIGNMENT_FLOAT64_IEEE.is_none


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
    with Parser() as p:
        mod_par = p.tree_from_a2l(project_string_minimal.format(module_string_minimal.format(s.format(
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
            system_constant=empty_string))).encode()).PROJECT.MODULE[0].MOD_PAR
        assert mod_par.Comment.Value == string_value
        assert mod_par.VERSION.is_none
        assert is_iterable(mod_par.ADDR_EPK)
        assert mod_par.EPK.is_none
        assert mod_par.SUPPLIER.is_none
        assert mod_par.CUSTOMER.is_none
        assert mod_par.CUSTOMER_NO.is_none
        assert mod_par.USER.is_none
        assert mod_par.PHONE_NO.is_none
        assert mod_par.ECU.is_none
        assert mod_par.CPU_TYPE.is_none
        assert mod_par.NO_OF_INTERFACES.is_none
        assert mod_par.ECU_CALIBRATION_OFFSET.is_none
        assert is_iterable(mod_par.CALIBRATION_METHOD)
        assert is_iterable(mod_par.MEMORY_LAYOUT)
        assert is_iterable(mod_par.MEMORY_SEGMENT)
        assert is_iterable(mod_par.SYSTEM_CONSTANT)


@pytest.mark.parametrize('module', [
    pytest.param(['CHARACTERISTIC', 0, 'AXIS_DESCR', 0, 'MONOTONY'], id='AXIS_DESCR')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('MONOTONY {}')])
@pytest.mark.parametrize('s, v', enum_monotony)
def test_monotony(module, e, s, v):
    with Parser() as p:
        monotony = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert monotony.Monotony == v


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'NO_AXIS_PTS_X'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['NO_AXIS_PTS_X {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_no_axis_pts_x(module, s, int_string, int_value, data_type_string, data_type_value):
    with Parser() as p:
        no_axis_pts_x = get_node_from_ast(
            p.tree_from_a2l(module[0].format(s.format(int=int_string, data_type=data_type_string)).encode()), module[1])
        assert no_axis_pts_x.Position.Value == int_value
        assert no_axis_pts_x.DataType.Value == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'NO_AXIS_PTS_Y'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['NO_AXIS_PTS_Y {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_no_axis_pts_y(module, s, int_string, int_value, data_type_string, data_type_value):
    with Parser() as p:
        no_axis_pts_y = get_node_from_ast(
            p.tree_from_a2l(module[0].format(s.format(int=int_string, data_type=data_type_string)).encode()), module[1])
        assert no_axis_pts_y.Position.Value == int_value
        assert no_axis_pts_y.DataType.Value == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'NO_AXIS_PTS_Z'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['NO_AXIS_PTS_Z {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_no_axis_pts_z(module, s, int_string, int_value, data_type_string, data_type_value):
    with Parser() as p:
        no_axis_pts_z = get_node_from_ast(
            p.tree_from_a2l(module[0].format(s.format(int=int_string, data_type=data_type_string)).encode()), module[1])
        assert no_axis_pts_z.Position.Value == int_value
        assert no_axis_pts_z.DataType.Value == data_type_value


@pytest.mark.parametrize('module', [pytest.param(['MOD_PAR', 'NO_OF_INTERFACES'], id='MOD_PAR')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('NO_OF_INTERFACES {}')])
@pytest.mark.parametrize('s, v', ints)
def test_no_of_interfaces(module, e, s, v):
    with Parser() as p:
        no_of_interfaces = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert no_of_interfaces.Num.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'NO_RESCALE_X'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['NO_RESCALE_X {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_no_rescale_x(module, s, int_string, int_value, data_type_string, data_type_value):
    with Parser() as p:
        no_rescale_x = get_node_from_ast(
            p.tree_from_a2l(module[0].format(s.format(int=int_string, data_type=data_type_string)).encode()), module[1])
        assert no_rescale_x.Position.Value == int_value
        assert no_rescale_x.DataType.Value == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'NO_RESCALE_Y'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['NO_RESCALE_Y {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_no_rescale_y(module, s, int_string, int_value, data_type_string, data_type_value):
    with Parser() as p:
        no_rescale_y = get_node_from_ast(
            p.tree_from_a2l(module[0].format(s.format(int=int_string, data_type=data_type_string)).encode()), module[1])
        assert no_rescale_y.Position.Value == int_value
        assert no_rescale_y.DataType.Value == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'NO_RESCALE_Z'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['NO_RESCALE_Z {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_no_rescale_z(module, s, int_string, int_value, data_type_string, data_type_value):
    with Parser() as p:
        no_rescale_z = get_node_from_ast(
            p.tree_from_a2l(module[0].format(s.format(int=int_string, data_type=data_type_string)).encode()), module[1])
        assert no_rescale_z.Position.Value == int_value
        assert no_rescale_z.DataType.Value == data_type_value


@pytest.mark.parametrize('module', [pytest.param(['CHARACTERISTIC', 0, 'NUMBER'], id='CHARACTERISTIC')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('NUMBER {}')])
@pytest.mark.parametrize('s, v', ints)
def test_number(module, e, s, v):
    with Parser() as p:
        number = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert number.Number.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'OFFSET_X'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['OFFSET_X {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_offset_x(module, s, int_string, int_value, data_type_string, data_type_value):
    with Parser() as p:
        offset_x = get_node_from_ast(
            p.tree_from_a2l(module[0].format(s.format(int=int_string, data_type=data_type_string)).encode()), module[1])
        assert offset_x.Position.Value == int_value
        assert offset_x.DataType.Value == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'OFFSET_Y'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['OFFSET_Y {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_offset_y(module, s, int_string, int_value, data_type_string, data_type_value):
    with Parser() as p:
        offset_y = get_node_from_ast(
            p.tree_from_a2l(module[0].format(s.format(int=int_string, data_type=data_type_string)).encode()), module[1])
        assert offset_y.Position.Value == int_value
        assert offset_y.DataType.Value == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'OFFSET_Z'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['OFFSET_Z {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_offset_z(module, s, int_string, int_value, data_type_string, data_type_value):
    with Parser() as p:
        offset_z = get_node_from_ast(
            p.tree_from_a2l(module[0].format(s.format(int=int_string, data_type=data_type_string)).encode()), module[1])
        assert offset_z.Position.Value == int_value
        assert offset_z.DataType.Value == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['FUNCTION', 0, 'OUT_MEASUREMENT'], id='FUNCTION'), ], indirect=True)
@pytest.mark.parametrize('s, identifier_count', out_measurement_strings)
@pytest.mark.parametrize('ident_string, ident_value', idents)
def test_out_measurement(module, s, identifier_count, ident_string, ident_value):
    with Parser() as p:
        out_measurement = get_node_from_ast(p.tree_from_a2l(module[0].format(s.format(ident=ident_string)).encode()),
                                            module[1])
        assert is_iterable(out_measurement.Identifier)
        assert len(out_measurement.Identifier) == identifier_count
        for identifier in out_measurement.Identifier:
            assert identifier.Value == ident_value


@pytest.mark.parametrize('module', [pytest.param(['MOD_PAR', 'PHONE_NO'], id='MOD_PAR')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('PHONE_NO {}')])
@pytest.mark.parametrize('s, v', strings)
def test_phone_no(module, e, s, v):
    with Parser() as p:
        phone_no = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert phone_no.TelNum.Value == v


@pytest.mark.parametrize('s', project_strings)
@pytest.mark.parametrize('ident_string, ident_value', idents)
@pytest.mark.parametrize('string_string, string_value', strings)
@pytest.mark.parametrize('header_string', [
    pytest.param(0, id='no HEADER'),
    pytest.param(1, id='one HEADER')
], indirect=True)
@pytest.mark.parametrize('module_string', [
    pytest.param(0, id='no MODULE'),
    pytest.param(1, id='one MODULE'),
    pytest.param(2, id='two MODULE')
], indirect=True)
def test_project(s, ident_string, ident_value, string_string, string_value, header_string, module_string):
    with Parser() as p:
        ast = p.tree_from_a2l(s.format(ident=ident_string,
                                       string=string_string,
                                       header=header_string,
                                       module=module_string).encode())
        assert ast.PROJECT.Name.Value == ident_value
        assert ast.PROJECT.LongIdentifier.Value == string_value


@pytest.mark.parametrize('project', [pytest.param(['HEADER', 'PROJECT_NO'], id='HEADER')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('PROJECT_NO {}')])
@pytest.mark.parametrize('s, v', idents)
def test_project_no(project, e, s, v):
    with Parser() as p:
        project_no = get_node_from_ast(p.tree_from_a2l(project[0].format(e.format(s)).encode()), project[1])
        assert project_no.ProjectNumber.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['CHARACTERISTIC', 0, 'READ_ONLY'], id='CHARACTERISTIC'),
    pytest.param(['AXIS_PTS', 0, 'READ_ONLY'], id='AXIS_PTS'),
    pytest.param(['CHARACTERISTIC', 0, 'AXIS_DESCR', 0, 'READ_ONLY'], id='AXIS_DESCR'),
    pytest.param(['USER_RIGHTS', 0, 'READ_ONLY'], id='USER_RIGHTS')], indirect=True)
@pytest.mark.parametrize('e, a', [pytest.param('READ_ONLY', True), pytest.param('', False)])
def test_read_only(module, e, a):
    with Parser() as p:
        read_only = get_node_from_ast(p.tree_from_a2l(module[0].format(e).encode()), module[1])
        assert read_only.is_none is not a


@pytest.mark.parametrize('module', [pytest.param(['MEASUREMENT', 0, 'READ_WRITE'], id='MEASUREMENT')], indirect=True)
@pytest.mark.parametrize('e, a', [pytest.param('READ_WRITE', True), pytest.param('', False)])
def test_read_write(module, e, a):
    with Parser() as p:
        read_write = get_node_from_ast(p.tree_from_a2l(module[0].format(e).encode()), module[1])
        assert read_write.is_none is not a


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
    with Parser() as p:
        record_layout = p.tree_from_a2l(project_string_minimal.format(module_string_minimal.format(s.format(
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
            reserved=empty_string))).encode()).PROJECT.MODULE[0].RECORD_LAYOUT[0]
        assert record_layout.Name.Value == ident_value
        assert record_layout.FNC_VALUES.is_none
        assert record_layout.IDENTIFICATION.is_none
        assert record_layout.AXIS_PTS_X.is_none
        assert record_layout.AXIS_PTS_Y.is_none
        assert record_layout.AXIS_PTS_Z.is_none
        assert record_layout.AXIS_RESCALE_X.is_none
        assert record_layout.AXIS_RESCALE_Y.is_none
        assert record_layout.AXIS_RESCALE_Z.is_none
        assert record_layout.NO_AXIS_PTS_X.is_none
        assert record_layout.NO_AXIS_PTS_Y.is_none
        assert record_layout.NO_AXIS_PTS_Z.is_none
        assert record_layout.NO_RESCALE_X.is_none
        assert record_layout.NO_RESCALE_Y.is_none
        assert record_layout.NO_RESCALE_Z.is_none
        assert record_layout.FIX_NO_AXIS_PTS_X.is_none
        assert record_layout.FIX_NO_AXIS_PTS_Y.is_none
        assert record_layout.FIX_NO_AXIS_PTS_Z.is_none
        assert record_layout.SRC_ADDR_X.is_none
        assert record_layout.SRC_ADDR_Y.is_none
        assert record_layout.SRC_ADDR_Z.is_none
        assert record_layout.RIP_ADDR_W.is_none
        assert record_layout.RIP_ADDR_X.is_none
        assert record_layout.RIP_ADDR_Y.is_none
        assert record_layout.RIP_ADDR_Z.is_none
        assert record_layout.SHIFT_OP_X.is_none
        assert record_layout.SHIFT_OP_Y.is_none
        assert record_layout.SHIFT_OP_Z.is_none
        assert record_layout.OFFSET_X.is_none
        assert record_layout.OFFSET_Y.is_none
        assert record_layout.OFFSET_Z.is_none
        assert record_layout.DIST_OP_X.is_none
        assert record_layout.DIST_OP_Y.is_none
        assert record_layout.DIST_OP_Z.is_none
        assert record_layout.ALIGNMENT_BYTE.is_none
        assert record_layout.ALIGNMENT_WORD.is_none
        assert record_layout.ALIGNMENT_LONG.is_none
        assert record_layout.ALIGNMENT_FLOAT32_IEEE.is_none
        assert record_layout.ALIGNMENT_FLOAT64_IEEE.is_none
        assert is_iterable(record_layout.RESERVED)


@pytest.mark.parametrize('module', [
    pytest.param(['FUNCTION', 0, 'REF_CHARACTERISTIC'], id='FUNCTION'),
    pytest.param(['GROUP', 0, 'REF_CHARACTERISTIC'], id='GROUP'),
], indirect=True)
@pytest.mark.parametrize('s, identifier_count', ref_characteristic_strings)
@pytest.mark.parametrize('ident_string, ident_value', idents)
def test_ref_characteristic(module, s, identifier_count, ident_string, ident_value):
    with Parser() as p:
        ref_characteristic = get_node_from_ast(p.tree_from_a2l(module[0].format(s.format(ident=ident_string)).encode()),
                                               module[1])
        assert is_iterable(ref_characteristic.Identifier)
        assert len(ref_characteristic.Identifier) == identifier_count
        for identifier in ref_characteristic.Identifier:
            assert identifier.Value == ident_value


@pytest.mark.parametrize('module', [pytest.param(['USER_RIGHTS', 0, 'REF_GROUP', 0], id='USER_RIGHTS')], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('/begin REF_GROUP /end REF_GROUP', 0, id='no identifier'),
    pytest.param('/begin REF_GROUP {ident} /end REF_GROUP', 1, id='one identifier'),
    pytest.param('/begin REF_GROUP {ident} {ident} /end REF_GROUP', 2, id='two identifier')])
@pytest.mark.parametrize('s, v', idents)
def test_ref_group(module, e, count, s, v):
    with Parser() as p:
        ref_group = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(ident=s)).encode()), module[1])
        assert is_iterable(ref_group.Identifier)
        assert len(ref_group.Identifier) == count
        for identifier in ref_group.Identifier:
            assert identifier.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['GROUP', 0, 'REF_MEASUREMENT'], id='GROUP'),
], indirect=True)
@pytest.mark.parametrize('s, identifier_count', ref_measurement_strings)
@pytest.mark.parametrize('ident_string, ident_value', idents)
def test_ref_measurement(module, s, identifier_count, ident_string, ident_value):
    with Parser() as p:
        ref_measurement = get_node_from_ast(p.tree_from_a2l(module[0].format(s.format(ident=ident_string)).encode()),
                                            module[1])
        assert is_iterable(ref_measurement.Identifier)
        assert len(ref_measurement.Identifier) == identifier_count
        for identifier in ref_measurement.Identifier:
            assert identifier.Value == ident_value


@pytest.mark.parametrize('module', [
    pytest.param(['CHARACTERISTIC', 0, 'REF_MEMORY_SEGMENT'], id='CHARACTERISTIC'),
    pytest.param(['MEASUREMENT', 0, 'REF_MEMORY_SEGMENT'], id='MEASUREMENT'),
    pytest.param(['AXIS_PTS', 0, 'REF_MEMORY_SEGMENT'], id='AXIS_PTS')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('REF_MEMORY_SEGMENT {}')])
@pytest.mark.parametrize('s, v', idents)
def test_ref_memory_segment(module, e, s, v):
    with Parser() as p:
        ref_memory_segment = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert ref_memory_segment.Name.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['COMPU_METHOD', 0, 'REF_UNIT'], id='COMPU_METHOD'),
    pytest.param(['UNIT', 0, 'REF_UNIT'], id='UNIT')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('REF_UNIT {}')])
@pytest.mark.parametrize('s, v', idents)
def test_ref_unit(module, e, s, v):
    with Parser() as p:
        ref_unit = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert ref_unit.Unit.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'RESERVED'], id='RECORD_LAYOUT')
], indirect=True)
@pytest.mark.parametrize('s, reserved_count', reserved_strings)
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_size_string, data_size_value', data_sizes)
def test_reserved(module,
                  s, reserved_count,
                  int_string, int_value,
                  data_size_string, data_size_value):
    with Parser() as p:
        reserved = get_node_from_ast(
            p.tree_from_a2l(module[0].format(s.format(int=int_string, data_size=data_size_string)).encode()), module[1])
        assert is_iterable(reserved)
        assert len(reserved) == reserved_count
        for e in reserved:
            assert e.Position.Value == int_value
            assert e.DataSize == data_size_value


@pytest.mark.parametrize('module', [
    pytest.param(['MEASUREMENT', 0, 'BIT_OPERATION', 'RIGHT_SHIFT'], id='MEASUREMENT')], indirect=True)
@pytest.mark.parametrize('e', ['RIGHT_SHIFT {}'])
@pytest.mark.parametrize('s, v', longs)
def test_right_shift(module, e, s, v):
    with Parser() as p:
        right_shift = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert right_shift.BitCount.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'RIP_ADDR_W'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['RIP_ADDR_W {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_rip_addr_w(module, s, int_string, int_value, data_type_string, data_type_value):
    with Parser() as p:
        rip_addr_w = get_node_from_ast(
            p.tree_from_a2l(module[0].format(s.format(int=int_string, data_type=data_type_string)).encode()), module[1])
        assert rip_addr_w.Position.Value == int_value
        assert rip_addr_w.DataType.Value == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'RIP_ADDR_X'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['RIP_ADDR_X {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_rip_addr_x(module, s, int_string, int_value, data_type_string, data_type_value):
    with Parser() as p:
        rip_addr_x = get_node_from_ast(
            p.tree_from_a2l(module[0].format(s.format(int=int_string, data_type=data_type_string)).encode()), module[1])
        assert rip_addr_x.Position.Value == int_value
        assert rip_addr_x.DataType.Value == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'RIP_ADDR_Y'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['RIP_ADDR_Y {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_rip_addr_y(module, s, int_string, int_value, data_type_string, data_type_value):
    with Parser() as p:
        rip_addr_y = get_node_from_ast(
            p.tree_from_a2l(module[0].format(s.format(int=int_string, data_type=data_type_string)).encode()), module[1])
        assert rip_addr_y.Position.Value == int_value
        assert rip_addr_y.DataType.Value == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'RIP_ADDR_Z'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('s', ['RIP_ADDR_Z {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_rip_addr_z(module, s, int_string, int_value, data_type_string, data_type_value):
    with Parser() as p:
        rip_addr_z = get_node_from_ast(
            p.tree_from_a2l(module[0].format(s.format(int=int_string, data_type=data_type_string)).encode()), module[1])
        assert rip_addr_z.Position.Value == int_value
        assert rip_addr_z.DataType.Value == data_type_value


@pytest.mark.parametrize('module', [pytest.param(['GROUP', 0, 'ROOT'], id='GROUP')], indirect=True)
@pytest.mark.parametrize('e, a', [pytest.param('ROOT', True), pytest.param('', False)])
def test_root(module, e, a):
    with Parser() as p:
        root = get_node_from_ast(p.tree_from_a2l(module[0].format(e).encode()), module[1])
        assert root.is_none is not a


@pytest.mark.parametrize('module', [pytest.param(['MOD_COMMON', 'S_REC_LAYOUT'], id='MOD_COMMON')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('S_REC_LAYOUT {}')])
@pytest.mark.parametrize('s, v', idents)
def test_s_rec_layout(module, e, s, v):
    with Parser() as p:
        s_rec_layout = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert s_rec_layout.Name.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'SHIFT_OP_X'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', ['SHIFT_OP_X {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_shift_op_x(module, e, int_string, int_value, data_type_string, data_type_value):
    with Parser() as p:
        shift_op_x = get_node_from_ast(
            p.tree_from_a2l(module[0].format(e.format(int=int_string, data_type=data_type_string)).encode()), module[1])
        assert shift_op_x.Position.Value == int_value
        assert shift_op_x.DataType.Value == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'SHIFT_OP_Y'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', ['SHIFT_OP_Y {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_shift_op_y(module, e, int_string, int_value, data_type_string, data_type_value):
    with Parser() as p:
        shift_op_y = get_node_from_ast(
            p.tree_from_a2l(module[0].format(e.format(int=int_string, data_type=data_type_string)).encode()), module[1])
        assert shift_op_y.Position.Value == int_value
        assert shift_op_y.DataType.Value == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'SHIFT_OP_Z'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', ['SHIFT_OP_Z {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_shift_op_z(module, e, int_string, int_value, data_type_string, data_type_value):
    with Parser() as p:
        shift_op_z = get_node_from_ast(
            p.tree_from_a2l(module[0].format(e.format(int=int_string, data_type=data_type_string)).encode()), module[1])
        assert shift_op_z.Position.Value == int_value
        assert shift_op_z.DataType.Value == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['UNIT', 0, 'SI_EXPONENTS'], id='UNIT')], indirect=True)
@pytest.mark.parametrize('e', ['SI_EXPONENTS {int} {int} {int} {int} {int} {int} {int}'])
@pytest.mark.parametrize('s, v', ints)
def test_si_exponents(module, e, s, v):
    with Parser() as p:
        si_exponents = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(int=s)).encode()), module[1])
        assert si_exponents.Length.Value == v
        assert si_exponents.Mass.Value == v
        assert si_exponents.Time.Value == v
        assert si_exponents.ElectricCurrent.Value == v
        assert si_exponents.Temperature.Value == v
        assert si_exponents.AmountOfSubstance.Value == v
        assert si_exponents.LuminousIntensity.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['MEASUREMENT', 0, 'BIT_OPERATION', 'SIGN_EXTEND'], id='MEASUREMENT')], indirect=True)
@pytest.mark.parametrize('e, a', [pytest.param('SIGN_EXTEND', True), pytest.param('', False)])
def test_sign_extend(module, e, a):
    with Parser() as p:
        sign_extend = get_node_from_ast(p.tree_from_a2l(module[0].format(e).encode()), module[1])
        assert sign_extend.is_none is not a


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'SRC_ADDR_X'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', ['SRC_ADDR_X {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_src_addr_x(module, e, int_string, int_value, data_type_string, data_type_value):
    with Parser() as p:
        src_addr_x = get_node_from_ast(
            p.tree_from_a2l(module[0].format(e.format(int=int_string, data_type=data_type_string)).encode()), module[1])
        assert src_addr_x.Position.Value == int_value
        assert src_addr_x.DataType.Value == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'SRC_ADDR_Y'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', ['SRC_ADDR_Y {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_src_addr_y(module, e, int_string, int_value, data_type_string, data_type_value):
    with Parser() as p:
        src_addr_y = get_node_from_ast(
            p.tree_from_a2l(module[0].format(e.format(int=int_string, data_type=data_type_string)).encode()), module[1])
        assert src_addr_y.Position.Value == int_value
        assert src_addr_y.DataType.Value == data_type_value


@pytest.mark.parametrize('module', [
    pytest.param(['RECORD_LAYOUT', 0, 'SRC_ADDR_Z'], id='RECORD_LAYOUT')], indirect=True)
@pytest.mark.parametrize('e', ['SRC_ADDR_Z {int} {data_type}'])
@pytest.mark.parametrize('int_string, int_value', ints)
@pytest.mark.parametrize('data_type_string, data_type_value', data_types)
def test_src_addr_z(module, e, int_string, int_value, data_type_string, data_type_value):
    with Parser() as p:
        src_addr_z = get_node_from_ast(
            p.tree_from_a2l(module[0].format(e.format(int=int_string, data_type=data_type_string)).encode()), module[1])
        assert src_addr_z.Position.Value == int_value
        assert src_addr_z.DataType.Value == data_type_value


@pytest.mark.parametrize('module', [pytest.param(['FUNCTION', 0, 'SUB_FUNCTION'], id='FUNCTION'), ], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('/begin SUB_FUNCTION /end SUB_FUNCTION', 0, id='no identifier'),
    pytest.param('/begin SUB_FUNCTION {ident} /end SUB_FUNCTION', 1, id='one identifier'),
    pytest.param('/begin SUB_FUNCTION {ident} {ident} /end SUB_FUNCTION', 2, id='two identifier')])
@pytest.mark.parametrize('s, v', idents)
def test_sub_function(module, e, count, s, v):
    with Parser() as p:
        sub_function = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(ident=s)).encode()), module[1])
        assert is_iterable(sub_function.Identifier)
        assert len(sub_function.Identifier) == count
        for identifier in sub_function.Identifier:
            assert identifier.Value == v


@pytest.mark.parametrize('module', [pytest.param(['GROUP', 0, 'SUB_GROUP'], id='GROUP')], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('/begin SUB_GROUP /end SUB_GROUP', 0, id='no identifier'),
    pytest.param('/begin SUB_GROUP {ident} /end SUB_GROUP', 1, id='one identifier'),
    pytest.param('/begin SUB_GROUP {ident} {ident} /end SUB_GROUP', 2, id='two identifier')])
@pytest.mark.parametrize('s, v', idents)
def test_sub_group(module, e, count, s, v):
    with Parser() as p:
        sub_group = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(ident=s)).encode()), module[1])
        assert is_iterable(sub_group.Identifier)
        assert len(sub_group.Identifier) == count
        for identifier in sub_group.Identifier:
            assert identifier.Value == v


@pytest.mark.parametrize('module', [pytest.param(['MOD_PAR', 'SUPPLIER'], id='MOD_PAR')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('SUPPLIER {}')])
@pytest.mark.parametrize('s, v', strings)
def test_supplier(module, e, s, v):
    with Parser() as p:
        supplier = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert supplier.Manufacturer.Value == v


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
    with Parser() as p:
        unit = p.tree_from_a2l(project_string_minimal.format(module_string_minimal.format(s.format(
            ident=ident_string,
            string=string_string,
            type=enum_type_string,
            si_exponents=empty_string,
            ref_unit=empty_string,
            unit_conversion=empty_string))).encode()).PROJECT.MODULE[0].UNIT[0]
        assert unit.Name.Value == ident_value
        assert unit.LongIdentifier.Value == string_value
        assert unit.Display.Value == string_value
        assert unit.Type == enum_type_value
        assert unit.SI_EXPONENTS.is_none
        assert unit.REF_UNIT.is_none
        assert unit.UNIT_CONVERSION.is_none


@pytest.mark.parametrize('module', [pytest.param(['UNIT', 0, 'UNIT_CONVERSION'], id='UNIT')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('UNIT_CONVERSION {float} {float}')])
@pytest.mark.parametrize('s, v', floats)
def test_unit_conversion(module, e, s, v):
    with Parser() as p:
        unit_conversion = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(float=s)).encode()), module[1])
        assert unit_conversion.Gradient.Value == v
        assert unit_conversion.Offset.Value == v


@pytest.mark.parametrize('module', [pytest.param(['MOD_PAR', 'USER'], id='MOD_PAR')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('USER {}')])
@pytest.mark.parametrize('s, v', strings)
def test_user(module, e, s, v):
    with Parser() as p:
        user = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert user.UserName.Value == v


@pytest.mark.parametrize('s', ['''
    /begin USER_RIGHTS {ident}
    {ref_group}
    {read_only}
    /end USER_RIGHTS'''])
@pytest.mark.parametrize('ident_string, ident_value', idents)
def test_user_rights(s, ident_string, ident_value):
    with Parser() as p:
        user_rights = p.tree_from_a2l(project_string_minimal.format(module_string_minimal.format(s.format(
            ident=ident_string,
            ref_group=empty_string,
            read_only=empty_string))).encode()).PROJECT.MODULE[0].USER_RIGHTS[0]
        assert user_rights.UserLevelId.Value == ident_value
        assert is_iterable(user_rights.REF_GROUP)
        assert user_rights.READ_ONLY.is_none


@pytest.mark.parametrize('variant_coding', [
    pytest.param(['VAR_CHARACTERISTIC', 0, 'VAR_ADDRESS'], id='VARIANT_CODING')], indirect=True)
@pytest.mark.parametrize('s, v', [
    pytest.param('', [], id='no address'),
    pytest.param('0', [0], id='one address'),
    pytest.param('0 0', [0, 0], id='two address')])
def test_var_address(variant_coding, s, v):
    with Parser() as p:
        var_address = get_node_from_ast(p.tree_from_a2l(variant_coding[0].format(s).encode()), variant_coding[1])
        assert is_iterable(var_address.Address)
        assert [v.Value for v in var_address.Address] == v


@pytest.mark.parametrize('module', [
    pytest.param(['VARIANT_CODING', 'VAR_CHARACTERISTIC', 0], id='VARIANT_CODING')], indirect=True)
@pytest.mark.parametrize('s', [
    '/begin VAR_CHARACTERISTIC {ident} {criterion_name} {var_address} /end VAR_CHARACTERISTIC'])
@pytest.mark.parametrize('ident_string, ident_value', idents)
@pytest.mark.parametrize('criterion_name_string, criterion_name_value', [
    pytest.param('', [], id='no criterion_name'),
    pytest.param('_', ['_'], id='one criterion_name'),
    pytest.param('_ _', ['_', '_'], id='no criterion_name')])
def test_var_characteristic(module, s, ident_string, ident_value, criterion_name_string, criterion_name_value):
    with Parser() as p:
        var_characteristic = get_node_from_ast(p.tree_from_a2l(module[0].format(s.format(ident=ident_string,
                                                                                         criterion_name=criterion_name_string,
                                                                                         var_address=empty_string)).encode()),
                                               module[1])
        assert var_characteristic.Name.Value == ident_value
        assert is_iterable(var_characteristic.CriterionName)
        assert [n.Value for n in var_characteristic.CriterionName] == criterion_name_value
        assert var_characteristic.VAR_ADDRESS.is_none


@pytest.mark.parametrize('module', [
    pytest.param(['VARIANT_CODING', 'VAR_CRITERION', 0], id='VARIANT_CODING'), ], indirect=True)
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
    with Parser() as p:
        var_criterion = get_node_from_ast(p.tree_from_a2l(module[0].format(s.format(ident=ident_string,
                                                                                    string=string_string,
                                                                                    value=value_string,
                                                                                    var_measurement=empty_string,
                                                                                    var_selection_characteristic=empty_string)).encode()),
                                          module[1])
        assert var_criterion.Name.Value == ident_value
        assert var_criterion.LongIdentifier.Value == string_value
        assert is_iterable(var_criterion.Value)
        assert [v.Value for v in var_criterion.Value] == value_value
        assert var_criterion.VAR_MEASUREMENT.is_none
        assert var_criterion.VAR_SELECTION_CHARACTERISTIC.is_none


@pytest.mark.parametrize('module', [
    pytest.param(['VARIANT_CODING', 'VAR_FORBIDDEN_COMB', 0], id='VARIANT_CODING')], indirect=True)
@pytest.mark.parametrize('e', ['/begin VAR_FORBIDDEN_COMB {} /end VAR_FORBIDDEN_COMB'])
@pytest.mark.parametrize('s, v', [
    pytest.param('', [], id='no criterion'),
    pytest.param('_ _', [('_', '_')], id='one criterion'),
    pytest.param('_ _ _ _', [('_', '_'), ('_', '_')], id='two criterion')])
def test_var_forbidden_comb(module, e, s, v):
    with Parser() as p:
        var_forbidden_comb = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert is_iterable(var_forbidden_comb.CriterionNameCriterionValue)
        assert [(e.CriterionName.Value,
                 e.CriterionValue.Value) for e in var_forbidden_comb.CriterionNameCriterionValue] == v


@pytest.mark.parametrize('variant_coding', [
    pytest.param(['VAR_CRITERION', 0, 'VAR_MEASUREMENT'], id='VARIANT_CODING')], indirect=True)
@pytest.mark.parametrize('s, v', [pytest.param('VAR_MEASUREMENT _', '_', id='VAR_MEASUREMENT')])
def test_var_measurement(variant_coding, s, v):
    with Parser() as p:
        var_measurement = get_node_from_ast(p.tree_from_a2l(variant_coding[0].format(s).encode()), variant_coding[1])
        assert var_measurement.Name.Value == v


@pytest.mark.parametrize('module', [pytest.param(['VARIANT_CODING', 'VAR_NAMING'], id='VARIANT_CODING')], indirect=True)
@pytest.mark.parametrize('e', ['VAR_NAMING {}'])
@pytest.mark.parametrize('s, v', enum_var_naming_tag)
def test_var_naming(module, e, s, v):
    with Parser() as p:
        var_naming = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert var_naming.Tag == v


@pytest.mark.parametrize('variant_coding', [
    pytest.param(['VAR_CRITERION', 0, 'VAR_SELECTION_CHARACTERISTIC'], id='VARIANT_CODING')], indirect=True)
@pytest.mark.parametrize('e', ['VAR_SELECTION_CHARACTERISTIC {}'])
@pytest.mark.parametrize('s, v', idents)
def test_var_selection_characteristic(variant_coding, e, s, v):
    with Parser() as p:
        var_selection_characteristic = get_node_from_ast(p.tree_from_a2l(variant_coding[0].format(e.format(s)).encode()),
                                                         variant_coding[1])
        assert var_selection_characteristic.Name.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['VARIANT_CODING', 'VAR_SEPARATOR'], id='VARIANT_CODING')], indirect=True)
@pytest.mark.parametrize('e', ['VAR_SEPARATOR {}'])
@pytest.mark.parametrize('s, v', strings)
def test_var_separator(module, e, s, v):
    with Parser() as p:
        var_separator = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(s)).encode()), module[1])
        assert var_separator.Separator.Value == v


@pytest.mark.parametrize('s', [
    '''/begin VARIANT_CODING
    {var_separator}
    {var_naming}
    {var_criterion}
    {var_forbidden_comb}
    {var_characteristic}
    /end VARIANT_CODING'''])
def test_variant_coding(s):
    with Parser() as p:
        variant_coding = p.tree_from_a2l(project_string_minimal.format(module_string_minimal.format(s.format(
            var_separator=empty_string,
            var_naming=empty_string,
            var_criterion=empty_string,
            var_forbidden_comb=empty_string,
            var_characteristic=empty_string))).encode()).PROJECT.MODULE[0].VARIANT_CODING
        assert variant_coding.VAR_SEPARATOR.is_none
        assert variant_coding.VAR_NAMING.is_none
        assert is_iterable(variant_coding.VAR_CRITERION)
        assert is_iterable(variant_coding.VAR_FORBIDDEN_COMB)
        assert is_iterable(variant_coding.VAR_CHARACTERISTIC)


@pytest.mark.parametrize('project', [pytest.param(['HEADER', 'VERSION'], id='HEADER')], indirect=True)
@pytest.mark.parametrize('e', [pytest.param('VERSION {}')])
@pytest.mark.parametrize('s, v', strings)
def test_version(project, e, s, v):
    with Parser() as p:
        version = get_node_from_ast(p.tree_from_a2l(project[0].format(e.format(s)).encode()), project[1])
        assert version.VersionIdentifier.Value == v


@pytest.mark.parametrize('module', [pytest.param(['MEASUREMENT', 0, 'VIRTUAL'], id='MEASUREMENT')], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('/begin VIRTUAL /end VIRTUAL', 0, id='no measuring_channel'),
    pytest.param('/begin VIRTUAL {ident} /end VIRTUAL', 1, id='one measuring_channel'),
    pytest.param('/begin VIRTUAL {ident} {ident} /end VIRTUAL', 2, id='two measuring_channel')])
@pytest.mark.parametrize('s, v', idents)
def test_virtual(module, e, count, s, v):
    with Parser() as p:
        virtual = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(ident=s)).encode()), module[1])
        assert is_iterable(virtual.MeasuringChannel)
        assert len(virtual.MeasuringChannel) == count
        for measuring_channel in virtual.MeasuringChannel:
            assert measuring_channel.Value == v


@pytest.mark.parametrize('module', [
    pytest.param(['CHARACTERISTIC', 0, 'VIRTUAL_CHARACTERISTIC'], id='CHARACTERISTIC')], indirect=True)
@pytest.mark.parametrize('e, count', [
    pytest.param('/begin VIRTUAL_CHARACTERISTIC {string} /end VIRTUAL_CHARACTERISTIC', 0, id='no characteristic'),
    pytest.param('/begin VIRTUAL_CHARACTERISTIC {string} {ident} /end VIRTUAL_CHARACTERISTIC', 1,
                 id='one characteristic'),
    pytest.param('/begin VIRTUAL_CHARACTERISTIC {string} {ident} {ident} /end VIRTUAL_CHARACTERISTIC', 2,
                 id='two characteristic')])
@pytest.mark.parametrize('string_string, string_value', strings)
@pytest.mark.parametrize('ident_string, ident_value', idents)
def test_virtual_characteristic(module, e, count, string_string, string_value, ident_string, ident_value):
    with Parser() as p:
        virtual_characteristic = get_node_from_ast(
            p.tree_from_a2l(module[0].format(e.format(string=string_string, ident=ident_string)).encode()), module[1])
        assert virtual_characteristic.Formula.Value == string_value
        assert is_iterable(virtual_characteristic.Characteristic)
        assert len(virtual_characteristic.Characteristic) == count
        for characteristic in virtual_characteristic.Characteristic:
            assert characteristic.Value == ident_value


@pytest.mark.parametrize('module', [pytest.param(['MOD_PAR', 'SYSTEM_CONSTANT', 0], id='MOD_PAR')], indirect=True)
@pytest.mark.parametrize('e', ['SYSTEM_CONSTANT {string} {string}'])
@pytest.mark.parametrize('s, v', strings)
def test_system_constant(module, e, s, v):
    with Parser() as p:
        system_constant = get_node_from_ast(p.tree_from_a2l(module[0].format(e.format(string=s)).encode()), module[1])
        assert system_constant.Name.Value == v
        assert system_constant.Value.Value == v


def test_get_properties():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
        /end PROJECT"""
    with Parser() as p:
        assert set(p.tree_from_a2l(a2l_string.encode()).PROJECT.properties) == {'Name', 'MODULE', 'HEADER', 'LongIdentifier'}
