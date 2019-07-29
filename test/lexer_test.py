"""
@project: pya2l
@file: lexer_test.py
@author: Guillaume Sottas
@date: 19.02.2019
"""

import pytest

from unittest.mock import mock_open, patch
from pya2l.parser.exception import A2lLexerException
from pya2l.parser.grammar.lexer import Lexer


@pytest.mark.parametrize('s, t, v', [
    pytest.param('A2ML', 'A2ML', 'A2ML', id='token A2ML'),
    pytest.param('A2ML_VERSION', 'A2ML_VERSION', 'A2ML_VERSION', id='token A2ML_VERSION'),
    pytest.param('ABSOLUTE', 'ABSOLUTE', 'ABSOLUTE', id='token ABSOLUTE'),
    pytest.param('ADDR_EPK', 'ADDR_EPK', 'ADDR_EPK', id='token ADDR_EPK'),
    pytest.param('ALIGNMENT_BYTE', 'ALIGNMENT_BYTE', 'ALIGNMENT_BYTE', id='token ALIGNMENT_BYTE'),
    pytest.param('ALIGNMENT_FLOAT32_IEEE', 'ALIGNMENT_FLOAT32_IEEE', 'ALIGNMENT_FLOAT32_IEEE',
                 id='token ALIGNMENT_FLOAT32_IEEE'),
    pytest.param('ALIGNMENT_FLOAT64_IEEE', 'ALIGNMENT_FLOAT64_IEEE', 'ALIGNMENT_FLOAT64_IEEE',
                 id='token ALIGNMENT_FLOAT64_IEEE'),
    pytest.param('ALIGNMENT_LONG', 'ALIGNMENT_LONG', 'ALIGNMENT_LONG', id='token ALIGNMENT_LONG'),
    pytest.param('ALIGNMENT_WORD', 'ALIGNMENT_WORD', 'ALIGNMENT_WORD', id='token ALIGNMENT_WORD'),
    pytest.param('ALTERNATE_CURVES', 'ALTERNATE_CURVES', 'ALTERNATE_CURVES', id='token ALTERNATE_CURVES'),
    pytest.param('ALTERNATE_WITH_X', 'ALTERNATE_WITH_X', 'ALTERNATE_WITH_X', id='token ALTERNATE_WITH_X'),
    pytest.param('ALTERNATE_WITH_Y', 'ALTERNATE_WITH_Y', 'ALTERNATE_WITH_Y', id='token ALTERNATE_WITH_Y'),
    pytest.param('ANNOTATION', 'ANNOTATION', 'ANNOTATION', id='token ANNOTATION'),
    pytest.param('ANNOTATION_LABEL', 'ANNOTATION_LABEL', 'ANNOTATION_LABEL', id='token ANNOTATION_LABEL'),
    pytest.param('ANNOTATION_ORIGIN', 'ANNOTATION_ORIGIN', 'ANNOTATION_ORIGIN', id='token ANNOTATION_ORIGIN'),
    pytest.param('ANNOTATION_TEXT', 'ANNOTATION_TEXT', 'ANNOTATION_TEXT', id='token ANNOTATION_TEXT'),
    pytest.param('ARRAY_SIZE', 'ARRAY_SIZE', 'ARRAY_SIZE', id='token ARRAY_SIZE'),
    pytest.param('ASAP2_VERSION', 'ASAP2_VERSION', 'ASAP2_VERSION', id='token ASAP2_VERSION'),
    pytest.param('ASCII', 'ASCII', 'ASCII', id='token ASCII'),
    pytest.param('AXIS_DESCR', 'AXIS_DESCR', 'AXIS_DESCR', id='token AXIS_DESCR'),
    pytest.param('AXIS_PTS', 'AXIS_PTS', 'AXIS_PTS', id='token AXIS_PTS'),
    pytest.param('AXIS_PTS_REF', 'AXIS_PTS_REF', 'AXIS_PTS_REF', id='token AXIS_PTS_REF'),
    pytest.param('AXIS_PTS_X', 'AXIS_PTS_X', 'AXIS_PTS_X', id='token AXIS_PTS_X'),
    pytest.param('AXIS_PTS_Y', 'AXIS_PTS_Y', 'AXIS_PTS_Y', id='token AXIS_PTS_Y'),
    pytest.param('AXIS_PTS_Z', 'AXIS_PTS_Z', 'AXIS_PTS_Z', id='token AXIS_PTS_Z'),
    pytest.param('AXIS_RESCALE_X', 'AXIS_RESCALE_X', 'AXIS_RESCALE_X', id='token AXIS_RESCALE_X'),
    pytest.param('AXIS_RESCALE_Y', 'AXIS_RESCALE_Y', 'AXIS_RESCALE_Y', id='token AXIS_RESCALE_Y'),
    pytest.param('AXIS_RESCALE_Z', 'AXIS_RESCALE_Z', 'AXIS_RESCALE_Z', id='token AXIS_RESCALE_Z'),
    pytest.param('BIT_MASK', 'BIT_MASK', 'BIT_MASK', id='token BIT_MASK'),
    pytest.param('BIT_OPERATION', 'BIT_OPERATION', 'BIT_OPERATION', id='token BIT_OPERATION'),
    pytest.param('BYTE', 'BYTE', 'BYTE', id='token BYTE'),
    pytest.param('BYTE_ORDER', 'BYTE_ORDER', 'BYTE_ORDER', id='token BYTE_ORDER'),
    pytest.param('CALIBRATION', 'CALIBRATION', 'CALIBRATION', id='token CALIBRATION'),
    pytest.param('CALIBRATION_ACCESS', 'CALIBRATION_ACCESS', 'CALIBRATION_ACCESS', id='token CALIBRATION_ACCESS'),
    pytest.param('CALIBRATION_HANDLE', 'CALIBRATION_HANDLE', 'CALIBRATION_HANDLE', id='token CALIBRATION_HANDLE'),
    pytest.param('CALIBRATION_METHOD', 'CALIBRATION_METHOD', 'CALIBRATION_METHOD', id='token CALIBRATION_METHOD'),
    pytest.param('CALIBRATION_VARIABLES', 'CALIBRATION_VARIABLES', 'CALIBRATION_VARIABLES',
                 id='token CALIBRATION_VARIABLES'),
    pytest.param('CHARACTERISTIC', 'CHARACTERISTIC', 'CHARACTERISTIC', id='token CHARACTERISTIC'),
    pytest.param('CODE', 'CODE', 'CODE', id='token CODE'),
    pytest.param('COEFFS', 'COEFFS', 'COEFFS', id='token COEFFS'),
    pytest.param('COLUMN_DIR', 'COLUMN_DIR', 'COLUMN_DIR', id='token COLUMN_DIR'),
    pytest.param('COMPARISON_QUANTITY', 'COMPARISON_QUANTITY', 'COMPARISON_QUANTITY', id='token COMPARISON_QUANTITY'),
    pytest.param('COMPU_METHOD', 'COMPU_METHOD', 'COMPU_METHOD', id='token COMPU_METHOD'),
    pytest.param('COMPU_TAB', 'COMPU_TAB', 'COMPU_TAB', id='token COMPU_TAB'),
    pytest.param('COMPU_TAB_REF', 'COMPU_TAB_REF', 'COMPU_TAB_REF', id='token COMPU_TAB_REF'),
    pytest.param('COMPU_VTAB', 'COMPU_VTAB', 'COMPU_VTAB', id='token COMPU_VTAB'),
    pytest.param('COMPU_VTAB_RANGE', 'COMPU_VTAB_RANGE', 'COMPU_VTAB_RANGE', id='token COMPU_VTAB_RANGE'),
    pytest.param('COM_AXIS', 'COM_AXIS', 'COM_AXIS', id='token COM_AXIS'),
    pytest.param('CPU_TYPE', 'CPU_TYPE', 'CPU_TYPE', id='token CPU_TYPE'),
    pytest.param('CUBOID', 'CUBOID', 'CUBOID', id='token CUBOID'),
    pytest.param('CURVE', 'CURVE', 'CURVE', id='token CURVE'),
    pytest.param('CURVE_AXIS', 'CURVE_AXIS', 'CURVE_AXIS', id='token CURVE_AXIS'),
    pytest.param('CURVE_AXIS_REF', 'CURVE_AXIS_REF', 'CURVE_AXIS_REF', id='token CURVE_AXIS_REF'),
    pytest.param('CUSTOMER', 'CUSTOMER', 'CUSTOMER', id='token CUSTOMER'),
    pytest.param('CUSTOMER_NO', 'CUSTOMER_NO', 'CUSTOMER_NO', id='token CUSTOMER_NO'),
    pytest.param('DATA', 'DATA', 'DATA', id='token DATA'),
    pytest.param('DATA_SIZE', 'DATA_SIZE', 'DATA_SIZE', id='token DATA_SIZE'),
    pytest.param('DEFAULT_VALUE', 'DEFAULT_VALUE', 'DEFAULT_VALUE', id='token DEFAULT_VALUE'),
    pytest.param('DEF_CHARACTERISTIC', 'DEF_CHARACTERISTIC', 'DEF_CHARACTERISTIC', id='token DEF_CHARACTERISTIC'),
    pytest.param('DEPENDENT_CHARACTERISTIC', 'DEPENDENT_CHARACTERISTIC', 'DEPENDENT_CHARACTERISTIC',
                 id='token DEPENDENT_CHARACTERISTIC'),
    pytest.param('DEPOSIT', 'DEPOSIT', 'DEPOSIT', id='token DEPOSIT'),
    pytest.param('DERIVED', 'DERIVED', 'DERIVED', id='token DERIVED'),
    pytest.param('DIFFERENCE', 'DIFFERENCE', 'DIFFERENCE', id='token DIFFERENCE'),
    pytest.param('DIRECT', 'DIRECT', 'DIRECT', id='token DIRECT'),
    pytest.param('DISPLAY_IDENTIFIER', 'DISPLAY_IDENTIFIER', 'DISPLAY_IDENTIFIER', id='token DISPLAY_IDENTIFIER'),
    pytest.param('DIST_OP_X', 'DIST_OP_X', 'DIST_OP_X', id='token DIST_OP_X'),
    pytest.param('DIST_OP_Y', 'DIST_OP_Y', 'DIST_OP_Y', id='token DIST_OP_Y'),
    pytest.param('DIST_OP_Z', 'DIST_OP_Z', 'DIST_OP_Z', id='token DIST_OP_Z'),
    pytest.param('ECU', 'ECU', 'ECU', id='token ECU'),
    pytest.param('ECU_ADDRESS', 'ECU_ADDRESS', 'ECU_ADDRESS', id='token ECU_ADDRESS'),
    pytest.param('ECU_ADDRESS_EXTENSION', 'ECU_ADDRESS_EXTENSION', 'ECU_ADDRESS_EXTENSION',
                 id='token ECU_ADDRESS_EXTENSION'),
    pytest.param('ECU_CALIBRATION_OFFSET', 'ECU_CALIBRATION_OFFSET', 'ECU_CALIBRATION_OFFSET',
                 id='token ECU_CALIBRATION_OFFSET'),
    pytest.param('EEPROM', 'EEPROM', 'EEPROM', id='token EEPROM'),
    pytest.param('EPK', 'EPK', 'EPK', id='token EPK'),
    pytest.param('EPROM', 'EPROM', 'EPROM', id='token EPROM'),
    pytest.param('ERROR_MASK', 'ERROR_MASK', 'ERROR_MASK', id='token ERROR_MASK'),
    pytest.param('EXCLUDE_FROM_FLASH', 'EXCLUDE_FROM_FLASH', 'EXCLUDE_FROM_FLASH', id='token EXCLUDE_FROM_FLASH'),
    pytest.param('EXTENDED_LIMITS', 'EXTENDED_LIMITS', 'EXTENDED_LIMITS', id='token EXTENDED_LIMITS'),
    pytest.param('EXTENDED_SI', 'EXTENDED_SI', 'EXTENDED_SI', id='token EXTENDED_SI'),
    pytest.param('EXTERN', 'EXTERN', 'EXTERN', id='token EXTERN'),
    pytest.param('FIX_AXIS', 'FIX_AXIS', 'FIX_AXIS', id='token FIX_AXIS'),
    pytest.param('FIX_AXIS_PAR', 'FIX_AXIS_PAR', 'FIX_AXIS_PAR', id='token FIX_AXIS_PAR'),
    pytest.param('FIX_AXIS_PAR_DIST', 'FIX_AXIS_PAR_DIST', 'FIX_AXIS_PAR_DIST', id='token FIX_AXIS_PAR_DIST'),
    pytest.param('FIX_AXIS_PAR_LIST', 'FIX_AXIS_PAR_LIST', 'FIX_AXIS_PAR_LIST', id='token FIX_AXIS_PAR_LIST'),
    pytest.param('FIX_NO_AXIS_PTS_X', 'FIX_NO_AXIS_PTS_X', 'FIX_NO_AXIS_PTS_X', id='token FIX_NO_AXIS_PTS_X'),
    pytest.param('FIX_NO_AXIS_PTS_Y', 'FIX_NO_AXIS_PTS_Y', 'FIX_NO_AXIS_PTS_Y', id='token FIX_NO_AXIS_PTS_Y'),
    pytest.param('FIX_NO_AXIS_PTS_Z', 'FIX_NO_AXIS_PTS_Z', 'FIX_NO_AXIS_PTS_Z', id='token FIX_NO_AXIS_PTS_Z'),
    pytest.param('FLASH', 'FLASH', 'FLASH', id='token FLASH'),
    pytest.param('FLOAT32_IEEE', 'FLOAT32_IEEE', 'FLOAT32_IEEE', id='token FLOAT32_IEEE'),
    pytest.param('FLOAT64_IEEE', 'FLOAT64_IEEE', 'FLOAT64_IEEE', id='token FLOAT64_IEEE'),
    pytest.param('FNC_VALUES', 'FNC_VALUES', 'FNC_VALUES', id='token FNC_VALUES'),
    pytest.param('FORM', 'FORM', 'FORM', id='token FORM'),
    pytest.param('FORMAT', 'FORMAT', 'FORMAT', id='token FORMAT'),
    pytest.param('FORMULA', 'FORMULA', 'FORMULA', id='token FORMULA'),
    pytest.param('FORMULA_INV', 'FORMULA_INV', 'FORMULA_INV', id='token FORMULA_INV'),
    pytest.param('FRAME', 'FRAME', 'FRAME', id='token FRAME'),
    pytest.param('FRAME_MEASUREMENT', 'FRAME_MEASUREMENT', 'FRAME_MEASUREMENT', id='token FRAME_MEASUREMENT'),
    pytest.param('FUNCTION', 'FUNCTION', 'FUNCTION', id='token FUNCTION'),
    pytest.param('FUNCTION_LIST', 'FUNCTION_LIST', 'FUNCTION_LIST', id='token FUNCTION_LIST'),
    pytest.param('FUNCTION_VERSION', 'FUNCTION_VERSION', 'FUNCTION_VERSION', id='token FUNCTION_VERSION'),
    pytest.param('GROUP', 'GROUP', 'GROUP', id='token GROUP'),
    pytest.param('GUARD_RAILS', 'GUARD_RAILS', 'GUARD_RAILS', id='token GUARD_RAILS'),
    pytest.param('HEADER', 'HEADER', 'HEADER', id='token HEADER'),
    pytest.param('IDENTIFICATION', 'IDENTIFICATION', 'IDENTIFICATION', id='token IDENTIFICATION'),
    pytest.param('IF_DATA', 'IF_DATA', 'IF_DATA', id='token IF_DATA'),
    pytest.param('INDEX_DECR', 'INDEX_DECR', 'INDEX_DECR', id='token INDEX_DECR'),
    pytest.param('INDEX_INCR', 'INDEX_INCR', 'INDEX_INCR', id='token INDEX_INCR'),
    pytest.param('INTERN', 'INTERN', 'INTERN', id='token INTERN'),
    pytest.param('IN_MEASUREMENT', 'IN_MEASUREMENT', 'IN_MEASUREMENT', id='token IN_MEASUREMENT'),
    pytest.param('LEFT_SHIFT', 'LEFT_SHIFT', 'LEFT_SHIFT', id='token LEFT_SHIFT'),
    pytest.param('LOC_MEASUREMENT', 'LOC_MEASUREMENT', 'LOC_MEASUREMENT', id='token LOC_MEASUREMENT'),
    pytest.param('LONG', 'LONG', 'LONG', id='token LONG'),
    pytest.param('MAP', 'MAP', 'MAP', id='token MAP'),
    pytest.param('MAP_LIST', 'MAP_LIST', 'MAP_LIST', id='token MAP_LIST'),
    pytest.param('MATRIX_DIM', 'MATRIX_DIM', 'MATRIX_DIM', id='token MATRIX_DIM'),
    pytest.param('MAX_GRAD', 'MAX_GRAD', 'MAX_GRAD', id='token MAX_GRAD'),
    pytest.param('MAX_REFRESH', 'MAX_REFRESH', 'MAX_REFRESH', id='token MAX_REFRESH'),
    pytest.param('MEASUREMENT', 'MEASUREMENT', 'MEASUREMENT', id='token MEASUREMENT'),
    pytest.param('MEMORY_LAYOUT', 'MEMORY_LAYOUT', 'MEMORY_LAYOUT', id='token MEMORY_LAYOUT'),
    pytest.param('MEMORY_SEGMENT', 'MEMORY_SEGMENT', 'MEMORY_SEGMENT', id='token MEMORY_SEGMENT'),
    pytest.param('MODULE', 'MODULE', 'MODULE', id='token MODULE'),
    pytest.param('MOD_COMMON', 'MOD_COMMON', 'MOD_COMMON', id='token MOD_COMMON'),
    pytest.param('MOD_PAR', 'MOD_PAR', 'MOD_PAR', id='token MOD_PAR'),
    pytest.param('MONOTONY', 'MONOTONY', 'MONOTONY', id='token MONOTONY'),
    pytest.param('MON_DECREASE', 'MON_DECREASE', 'MON_DECREASE', id='token MON_DECREASE'),
    pytest.param('MON_INCREASE', 'MON_INCREASE', 'MON_INCREASE', id='token MON_INCREASE'),
    pytest.param('MSB_FIRST', 'MSB_FIRST', 'MSB_FIRST', id='token MSB_FIRST'),
    pytest.param('MSB_LAST', 'MSB_LAST', 'MSB_LAST', id='token MSB_LAST'),
    pytest.param('NOT_IN_MCD_SYSTEM', 'NOT_IN_MCD_SYSTEM', 'NOT_IN_MCD_SYSTEM', id='token NOT_IN_MCD_SYSTEM'),
    pytest.param('NO_AXIS_PTS_X', 'NO_AXIS_PTS_X', 'NO_AXIS_PTS_X', id='token NO_AXIS_PTS_X'),
    pytest.param('NO_AXIS_PTS_Y', 'NO_AXIS_PTS_Y', 'NO_AXIS_PTS_Y', id='token NO_AXIS_PTS_Y'),
    pytest.param('NO_AXIS_PTS_Z', 'NO_AXIS_PTS_Z', 'NO_AXIS_PTS_Z', id='token NO_AXIS_PTS_Z'),
    pytest.param('NO_CALIBRATION', 'NO_CALIBRATION', 'NO_CALIBRATION', id='token NO_CALIBRATION'),
    pytest.param('NO_OF_INTERFACES', 'NO_OF_INTERFACES', 'NO_OF_INTERFACES', id='token NO_OF_INTERFACES'),
    pytest.param('NO_RESCALE_X', 'NO_RESCALE_X', 'NO_RESCALE_X', id='token NO_RESCALE_X'),
    pytest.param('NO_RESCALE_Y', 'NO_RESCALE_Y', 'NO_RESCALE_Y', id='token NO_RESCALE_Y'),
    pytest.param('NO_RESCALE_Z', 'NO_RESCALE_Z', 'NO_RESCALE_Z', id='token NO_RESCALE_Z'),
    pytest.param('NUMBER', 'NUMBER', 'NUMBER', id='token NUMBER'),
    pytest.param('OFFLINE_CALIBRATION', 'OFFLINE_CALIBRATION', 'OFFLINE_CALIBRATION', id='token OFFLINE_CALIBRATION'),
    pytest.param('OFFLINE_DATA', 'OFFLINE_DATA', 'OFFLINE_DATA', id='token OFFLINE_DATA'),
    pytest.param('OFFSET_X', 'OFFSET_X', 'OFFSET_X', id='token OFFSET_X'),
    pytest.param('OFFSET_Y', 'OFFSET_Y', 'OFFSET_Y', id='token OFFSET_Y'),
    pytest.param('OFFSET_Z', 'OFFSET_Z', 'OFFSET_Z', id='token OFFSET_Z'),
    pytest.param('OUT_MEASUREMENT', 'OUT_MEASUREMENT', 'OUT_MEASUREMENT', id='token OUT_MEASUREMENT'),
    pytest.param('PBYTE', 'PBYTE', 'PBYTE', id='token PBYTE'),
    pytest.param('PHONE_NO', 'PHONE_NO', 'PHONE_NO', id='token PHONE_NO'),
    pytest.param('PLONG', 'PLONG', 'PLONG', id='token PLONG'),
    pytest.param('PRG_CODE', 'PRG_CODE', 'PRG_CODE', id='token PRG_CODE'),
    pytest.param('PRG_DATA', 'PRG_DATA', 'PRG_DATA', id='token PRG_DATA'),
    pytest.param('PRG_RESERVED', 'PRG_RESERVED', 'PRG_RESERVED', id='token PRG_RESERVED'),
    pytest.param('PROJECT', 'PROJECT', 'PROJECT', id='token PROJECT'),
    pytest.param('PROJECT_NO', 'PROJECT_NO', 'PROJECT_NO', id='token PROJECT_NO'),
    pytest.param('PWORD', 'PWORD', 'PWORD', id='token PWORD'),
    pytest.param('RAM', 'RAM', 'RAM', id='token RAM'),
    pytest.param('RAT_FUNC', 'RAT_FUNC', 'RAT_FUNC', id='token RAT_FUNC'),
    pytest.param('READ_ONLY', 'READ_ONLY', 'READ_ONLY', id='token READ_ONLY'),
    pytest.param('READ_WRITE', 'READ_WRITE', 'READ_WRITE', id='token READ_WRITE'),
    pytest.param('RECORD_LAYOUT', 'RECORD_LAYOUT', 'RECORD_LAYOUT', id='token RECORD_LAYOUT'),
    pytest.param('REF_CHARACTERISTIC', 'REF_CHARACTERISTIC', 'REF_CHARACTERISTIC', id='token REF_CHARACTERISTIC'),
    pytest.param('REF_GROUP', 'REF_GROUP', 'REF_GROUP', id='token REF_GROUP'),
    pytest.param('REF_MEASUREMENT', 'REF_MEASUREMENT', 'REF_MEASUREMENT', id='token REF_MEASUREMENT'),
    pytest.param('REF_MEMORY_SEGMENT', 'REF_MEMORY_SEGMENT', 'REF_MEMORY_SEGMENT', id='token REF_MEMORY_SEGMENT'),
    pytest.param('REF_UNIT', 'REF_UNIT', 'REF_UNIT', id='token REF_UNIT'),
    pytest.param('REGISTER', 'REGISTER', 'REGISTER', id='token REGISTER'),
    pytest.param('RESERVED', 'RESERVED', 'RESERVED', id='token RESERVED'),
    pytest.param('RES_AXIS', 'RES_AXIS', 'RES_AXIS', id='token RES_AXIS'),
    pytest.param('RIGHT_SHIFT', 'RIGHT_SHIFT', 'RIGHT_SHIFT', id='token RIGHT_SHIFT'),
    pytest.param('RIP_ADDR_W', 'RIP_ADDR_W', 'RIP_ADDR_W', id='token RIP_ADDR_W'),
    pytest.param('RIP_ADDR_X', 'RIP_ADDR_X', 'RIP_ADDR_X', id='token RIP_ADDR_X'),
    pytest.param('RIP_ADDR_Y', 'RIP_ADDR_Y', 'RIP_ADDR_Y', id='token RIP_ADDR_Y'),
    pytest.param('RIP_ADDR_Z', 'RIP_ADDR_Z', 'RIP_ADDR_Z', id='token RIP_ADDR_Z'),
    pytest.param('ROM', 'ROM', 'ROM', id='token ROM'),
    pytest.param('ROOT', 'ROOT', 'ROOT', id='token ROOT'),
    pytest.param('ROW_DIR', 'ROW_DIR', 'ROW_DIR', id='token ROW_DIR'),
    pytest.param('SBYTE', 'SBYTE', 'SBYTE', id='token SBYTE'),
    pytest.param('SERAM', 'SERAM', 'SERAM', id='token SERAM'),
    pytest.param('SHIFT_OP_X', 'SHIFT_OP_X', 'SHIFT_OP_X', id='token SHIFT_OP_X'),
    pytest.param('SHIFT_OP_Y', 'SHIFT_OP_Y', 'SHIFT_OP_Y', id='token SHIFT_OP_Y'),
    pytest.param('SHIFT_OP_Z', 'SHIFT_OP_Z', 'SHIFT_OP_Z', id='token SHIFT_OP_Z'),
    pytest.param('SIGN_EXTEND', 'SIGN_EXTEND', 'SIGN_EXTEND', id='token SIGN_EXTEND'),
    pytest.param('SI_EXPONENTS', 'SI_EXPONENTS', 'SI_EXPONENTS', id='token SI_EXPONENTS'),
    pytest.param('SLONG', 'SLONG', 'SLONG', id='token SLONG'),
    pytest.param('SRC_ADDR_X', 'SRC_ADDR_X', 'SRC_ADDR_X', id='token SRC_ADDR_X'),
    pytest.param('SRC_ADDR_Y', 'SRC_ADDR_Y', 'SRC_ADDR_Y', id='token SRC_ADDR_Y'),
    pytest.param('SRC_ADDR_Z', 'SRC_ADDR_Z', 'SRC_ADDR_Z', id='token SRC_ADDR_Z'),
    pytest.param('STD_AXIS', 'STD_AXIS', 'STD_AXIS', id='token STD_AXIS'),
    pytest.param('STRICT_DECREASE', 'STRICT_DECREASE', 'STRICT_DECREASE', id='token STRICT_DECREASE'),
    pytest.param('STRICT_INCREASE', 'STRICT_INCREASE', 'STRICT_INCREASE', id='token STRICT_INCREASE'),
    pytest.param('SUB_FUNCTION', 'SUB_FUNCTION', 'SUB_FUNCTION', id='token SUB_FUNCTION'),
    pytest.param('SUB_GROUP', 'SUB_GROUP', 'SUB_GROUP', id='token SUB_GROUP'),
    pytest.param('SUPPLIER', 'SUPPLIER', 'SUPPLIER', id='token SUPPLIER'),
    pytest.param('SWORD', 'SWORD', 'SWORD', id='token SWORD'),
    pytest.param('SYSTEM_CONSTANT', 'SYSTEM_CONSTANT', 'SYSTEM_CONSTANT', id='token SYSTEM_CONSTANT'),
    pytest.param('S_REC_LAYOUT', 'S_REC_LAYOUT', 'S_REC_LAYOUT', id='token S_REC_LAYOUT'),
    pytest.param('TAB_INTP', 'TAB_INTP', 'TAB_INTP', id='token TAB_INTP'),
    pytest.param('TAB_NOINTP', 'TAB_NOINTP', 'TAB_NOINTP', id='token TAB_NOINTP'),
    pytest.param('TAB_VERB', 'TAB_VERB', 'TAB_VERB', id='token TAB_VERB'),
    pytest.param('UBYTE', 'UBYTE', 'UBYTE', id='token UBYTE'),
    pytest.param('ULONG', 'ULONG', 'ULONG', id='token ULONG'),
    pytest.param('UNIT', 'UNIT', 'UNIT', id='token UNIT'),
    pytest.param('UNIT_CONVERSION', 'UNIT_CONVERSION', 'UNIT_CONVERSION', id='token UNIT_CONVERSION'),
    pytest.param('USER', 'USER', 'USER', id='token USER'),
    pytest.param('USER_RIGHTS', 'USER_RIGHTS', 'USER_RIGHTS', id='token USER_RIGHTS'),
    pytest.param('UWORD', 'UWORD', 'UWORD', id='token UWORD'),
    pytest.param('VALUE', 'VALUE', 'VALUE', id='token VALUE'),
    pytest.param('VAL_BLK', 'VAL_BLK', 'VAL_BLK', id='token VAL_BLK'),
    pytest.param('VARIABLES', 'VARIABLES', 'VARIABLES', id='token VARIABLES'),
    pytest.param('VARIANT_CODING', 'VARIANT_CODING', 'VARIANT_CODING', id='token VARIANT_CODING'),
    pytest.param('VAR_ADDRESS', 'VAR_ADDRESS', 'VAR_ADDRESS', id='token VAR_ADDRESS'),
    pytest.param('VAR_CHARACTERISTIC', 'VAR_CHARACTERISTIC', 'VAR_CHARACTERISTIC', id='token VAR_CHARACTERISTIC'),
    pytest.param('VAR_CRITERION', 'VAR_CRITERION', 'VAR_CRITERION', id='token VAR_CRITERION'),
    pytest.param('VAR_FORBIDDEN_COMB', 'VAR_FORBIDDEN_COMB', 'VAR_FORBIDDEN_COMB', id='token VAR_FORBIDDEN_COMB'),
    pytest.param('VAR_MEASUREMENT', 'VAR_MEASUREMENT', 'VAR_MEASUREMENT', id='token VAR_MEASUREMENT'),
    pytest.param('VAR_NAMING', 'VAR_NAMING', 'VAR_NAMING', id='token VAR_NAMING'),
    pytest.param('VAR_SELECTION_CHARACTERISTIC', 'VAR_SELECTION_CHARACTERISTIC', 'VAR_SELECTION_CHARACTERISTIC',
                 id='token VAR_SELECTION_CHARACTERISTIC'),
    pytest.param('VAR_SEPARATOR', 'VAR_SEPARATOR', 'VAR_SEPARATOR', id='token VAR_SEPARATOR'),
    pytest.param('VERSION', 'VERSION', 'VERSION', id='token VERSION'),
    pytest.param('VIRTUAL', 'VIRTUAL', 'VIRTUAL', id='token VIRTUAL'),
    pytest.param('VIRTUAL_CHARACTERISTIC', 'VIRTUAL_CHARACTERISTIC', 'VIRTUAL_CHARACTERISTIC',
                 id='token VIRTUAL_CHARACTERISTIC'),
    pytest.param('WORD', 'WORD', 'WORD', id='token WORD')])
def test_a2l_keywords(s, t, v):
    lexer = Lexer().build()
    lexer.instance.input(s)
    token = lexer.instance.token()
    assert token.type == t
    assert token.value == v


@pytest.mark.parametrize('s, t, v', [
    pytest.param('A2ML block', 'block', 'block', id='token block'),
    pytest.param('A2ML char', 'char', 'char', id='token char'),
    pytest.param('A2ML double', 'double', 'double', id='token double'),
    pytest.param('A2ML enum', 'enum', 'enum', id='token enum'),
    pytest.param('A2ML float', 'float', 'float', id='token float'),
    pytest.param('A2ML int', 'int', 'int', id='token int'),
    pytest.param('A2ML long', 'long', 'long', id='token long'),
    pytest.param('A2ML struct', 'struct', 'struct', id='token struct'),
    pytest.param('A2ML taggedstruct', 'taggedstruct', 'taggedstruct', id='token taggedstruct'),
    pytest.param('A2ML taggedunion', 'taggedunion', 'taggedunion', id='token taggedunion'),
    pytest.param('A2ML uchar', 'uchar', 'uchar', id='token uchar'),
    pytest.param('A2ML uint', 'uint', 'uint', id='token uint'),
    pytest.param('A2ML ulong', 'ulong', 'ulong', id='token ulong')])
def test_a2ml_keywords(s, t, v):
    lexer = Lexer().build()
    lexer.instance.input(s)
    lexer.instance.token()
    token = lexer.instance.token()
    assert token.type == t
    assert token.value == v


@pytest.mark.parametrize('s, v', [
    pytest.param('/*_*/', None, id='inline C-style comment'),
    pytest.param('/*\n_*/', None, id='LF multiline C-style comment'),
    pytest.param('/*\r_*/', None, id='CR multiline C-style comment'),
    pytest.param('/*\r\n_*/', None, id='CRLF multiline C-style comment'),
    pytest.param('//_\n', None, id='LF-terminated C++-style comment'),
    pytest.param('//_\r', None, id='CR-terminated C++-style comment'),
    pytest.param('//_\r\n', None, id='CRLF-terminated C++-style comment'),
    pytest.param('\r', None, id='CR new line'),
    pytest.param('\n', None, id='LF new line'),
    pytest.param('\r\n', None, id='CRLF new line')])
def test_ignored_tokens(s, v):
    lexer = Lexer().build()
    lexer.instance.input(s)
    token = lexer.instance.token()
    assert token == v


@pytest.mark.parametrize('s, t, v', [
    pytest.param('/begin', 'begin', '/begin', id='keyword begin'),
    # pytest.param('{', 'begin', '{', id='curly begin'),
    pytest.param('/end', 'end', '/end', id='keyword end'),
    # pytest.param('}', 'end', '}', id='curly end')
])
def test_begin_end_tokens(s, t, v):
    lexer = Lexer().build()
    lexer.instance.input(s)
    token = lexer.instance.token()
    assert token.type == t
    assert token.value == v


@pytest.mark.parametrize('s, t, v', [
    pytest.param('""', 'S', '', id='empty string'),
    pytest.param('"_"', 'S', '_', id='single character string'),
    pytest.param('"__"', 'S', '__', id='multiple character string')])
def test_string_tokens(s, t, v):
    lexer = Lexer().build()
    lexer.instance.input(s)
    token = lexer.instance.token()
    assert token.type == t
    assert token.value == v


@pytest.mark.parametrize('s, t, v', [
    pytest.param('0', 'N', 0, id='decimal 0'),
    pytest.param('-0', 'N', 0, id='explicitly negative decimal 0'),
    pytest.param('+0', 'N', 0, id='explicitly positive decimal 0'),
    pytest.param('0x0', 'N', 0, id='hexadecimal 0 lower case'),
    pytest.param('0X0', 'N', 0, id='hexadecimal 0 upper case'),
    pytest.param('-0x0', 'N', 0, id='explicitly negative hexadecimal 0'),
    pytest.param('+0x0', 'N', 0, id='explicitly positive hexadecimal 0'),
    pytest.param('0.0', 'N', 0.0, id='floating 0'),
    pytest.param('0.0e0', 'N', 0.0, id='floating 0 with lower case exponent'),
    pytest.param('0.0E0', 'N', 0.0, id='floating 0 with upper case exponent'),
    pytest.param('0e-0', 'N', 0.0, id='floating 0 with explicitly negative exponent'),
    pytest.param('0e+0', 'N', 0.0, id='floating 0 with explicitly positive exponent')])
def test_numeric_tokens(s, t, v):
    lexer = Lexer().build()
    lexer.instance.input(s)
    token = lexer.instance.token()
    assert token.type == t
    assert token.value == v


@pytest.mark.parametrize('i, s', [
    pytest.param('INITIAL', (['IF_DATA', 'ifdata'], ['IF_DATA', 'INITIAL']), id='from initial to if_data to initial'),
    pytest.param('INITIAL', (['A2ML', 'a2ml'], ['A2ML', 'INITIAL']), id='from initial to a2ml to initial')])
def test_state_switch(i, s):
    lexer = Lexer().build()
    assert lexer.instance.lexstate == i
    for t, s in s:
        lexer.instance.input(t)
        lexer.instance.token()
        assert lexer.instance.lexstate == s


@pytest.mark.parametrize('s, t, v', [
    pytest.param('_[0]', 'I', '_[0]')])
def test_identifier_with_array_state_initial(s, t, v):
    lexer = Lexer().build()
    lexer.instance.input(s)
    token = lexer.instance.token()
    assert token.type == t
    assert token.value == v


@pytest.mark.parametrize('s, t, v', [
    pytest.param('A2ML _', 'I', '_', id='no array specifier in identifier'),
    pytest.param('A2ML _[0]', 'I', '_', id='array specifier in identifier')])
def test_identifier_with_array_specifier_state_a2ml(s, t, v):
    lexer = Lexer().build()
    lexer.instance.input(s)
    lexer.instance.token()
    assert lexer.instance.lexstate == 'a2ml'
    token = lexer.instance.token()
    assert token.type == t
    assert token.value == v


@pytest.mark.parametrize('s, e', [
    pytest.param('.', '')])
def test_lexer_exception(s, e):
    lexer = Lexer().build()
    lexer.instance.input(s)
    with pytest.raises(A2lLexerException):
        lexer.instance.token()


@pytest.mark.parametrize('n', [
    pytest.param(0, id='nesting level 1'),
    pytest.param(9, id='nesting level 10'),
    pytest.param(99, id='nesting level 100')])
def test_nested_include(n):
    lexer = Lexer().build()
    lexer.instance.input('/include level_0')
    with patch('pya2l.parser.grammar.lexer.open', new_callable=mock_open, read_data='/include "level_1"') as mo:
        mo.side_effect = [mo.return_value] + \
                         [mock_open(read_data='/include level_{}'.format(l + 2)).return_value for l in range(n)] + \
                         [mock_open(read_data=str(n)).return_value]
        token = lexer.instance.token()
        assert token.value == n


def test_invalid_include_file():
    lexer = Lexer().build()
    lexer.instance.input('/include level_0')
    with pytest.raises(IOError) as e:
        with patch('pya2l.parser.grammar.lexer.open') as mo:
            mo.side_effect = IOError
            lexer.instance.token()
    assert str(e.value) == 'unable to find included file "level_0"'
