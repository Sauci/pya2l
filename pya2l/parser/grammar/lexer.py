"""
@project: a2l_parser
@file: lexer.py
@author: Guillaume Sottas
@date: 20.03.2018
"""

import os
import ply.lex as lex


class KeywordsList(dict):
    def __init__(self, keywords):
        super(KeywordsList, self).__init__([(kw, kw) for kw in set(keywords)])  # .encode('string-escape')


keywords = KeywordsList(('A2ML_VERSION',
                         'ASAP2_VERSION',
                         'AVAILABLE_EVENT_LIST',
                         'HEADER',
                         'MODULE',
                         'PROJECT',

                         'A2ML',
                         'AXIS_PTS',
                         # 'BLOB',
                         'CHARACTERISTIC',
                         'COMPU_METHOD',
                         'COMPU_TAB',
                         'COMPU_VTAB',
                         'COMPU_VTAB_RANGE',
                         'DEFAULT_EVENT_LIST',
                         'FRAME',
                         'FUNCTION',
                         'GROUP',
                         'IF_DATA',
                         # 'INSTANCE',
                         'MEASUREMENT',
                         'MOD_COMMON',
                         'MOD_PAR',
                         'RECORD_LAYOUT',
                         # 'TRANSFORMER',
                         # 'TYPEDEF_AXIS',
                         # 'TYPEDEF_BLOB',
                         # 'TYPEDEF_CHARACTERISTIC',
                         # 'TYPEDEF_MEASUREMENT',
                         # 'TYPEDEF_STRUCTURE',
                         'UNIT',
                         'USER_RIGHTS',
                         'VARIANT_CODING',
                         'ADDRESS_EXTENSION_FREE',
                         'ADDRESS_EXTENSION_ODT',
                         'ADDRESS_EXTENSION_DAQ',
                         'ADDRESS_MAPPING',
                         'ADDR_EPK',
                         'ALIGNMENT_BYTE',
                         'ALIGNMENT_FLOAT32_IEEE',
                         'ALIGNMENT_FLOAT64_IEEE',
                         # 'ALIGNMENT_INT64',
                         'ALIGNMENT_LONG',
                         'ALIGNMENT_WORD',
                         'ANNOTATION',
                         'ANNOTATION_LABEL',
                         'ANNOTATION_ORIGIN',
                         'ANNOTATION_TEXT',
                         'ARRAY_SIZE',
                         'AXIS_DESCR',
                         'AXIS_PTS_REF',
                         'AXIS_PTS_X',
                         'AXIS_PTS_Y',
                         'AXIS_PTS_Z',
                         # 'AXIS_PTS_4',
                         # 'AXIS_PTS_5',
                         'AXIS_RESCALE_X',
                         'AXIS_RESCALE_Y',
                         'AXIS_RESCALE_Z',
                         'BIT_MASK',
                         'BIT_OPERATION',
                         'BYTE_ORDER',
                         'CALIBRATION_ACCESS',
                         'CALIBRATION_HANDLE',
                         # 'CALIBRATION_HANDLE_TEXT',
                         'CALIBRATION_METHOD',
                         'COEFFS',
                         'COEFFS_LINEAR',
                         'COMPARISON_QUANTITY',
                         'COMPU_TAB_REF',
                         'CPU_TYPE',
                         'CURVE_AXIS_REF',
                         'CUSTOMER',
                         'CUSTOMER_NO',
                         'DAQ',
                         'DAQ_EVENT',
                         'DAQ_LIST',
                         'DAQ_LIST_TYPE',
                         'DAQ_STIM',
                         'DATA_SIZE',
                         'DEFAULT_VALUE',
                         'DEFAULT_VALUE_NUMERIC',
                         'DEF_CHARACTERISTIC',
                         'DEPENDENT_CHARACTERISTIC',
                         'DEPOSIT',
                         # 'DISCRETE',
                         'DISPLAY_IDENTIFIER',
                         'DIST_OP_X',
                         'DIST_OP_Y',
                         'DIST_OP_Z',
                         'DYNAMIC',
                         # 'DIST_OP_4',
                         # 'DIST_OP_5',
                         'ECU',
                         'ECU_ADDRESS',
                         'ECU_ADDRESS_EXTENSION',
                         'ECU_CALIBRATION_OFFSET',
                         'EPK',
                         'ERROR_MASK',
                         'EVENT',
                         'EVENT_FIXED',
                         'EXTENDED_LIMITS',
                         'FIRST_PID',
                         'FIX_AXIS_PAR',
                         'FIX_AXIS_PAR_DIST',
                         'FIX_AXIS_PAR_LIST',
                         'FIX_NO_AXIS_PTS_X',
                         'FIX_NO_AXIS_PTS_Y',
                         'FIX_NO_AXIS_PTS_Z',
                         # 'FIX_NO_AXIS_PTS_4',
                         # 'FIX_NO_AXIS_PTS_5',
                         'FNC_VALUES',
                         'FORMAT',
                         'FORMULA',
                         'FORMULA_INV',
                         'FRAME_MEASUREMENT',
                         'FREEZE_SUPPORTED',
                         'FUNCTION_LIST',
                         'FUNCTION_VERSION',
                         'GRANULARITY_ODT_ENTRY_SIZE_DAQ_BYTE',
                         'GRANULARITY_ODT_ENTRY_SIZE_DAQ_WORD',
                         'GRANULARITY_ODT_ENTRY_SIZE_DAQ_DWORD',
                         'GRANULARITY_ODT_ENTRY_SIZE_DAQ_DLONG',
                         'GUARD_RAILS',
                         'IDENTIFICATION',
                         'IDENTIFICATION_FIELD_TYPE_ABSOLUTE',
                         'IDENTIFICATION_FIELD_TYPE_RELATIVE_BYTE',
                         'IDENTIFICATION_FIELD_TYPE_RELATIVE_WORD',
                         'IDENTIFICATION_FIELD_TYPE_RELATIVE_WORD_ALIGNED',
                         'IF_DATA',
                         'IN_MEASUREMENT',
                         # 'LAYOUT',
                         'LEFT_SHIFT',
                         'LINEAR',
                         'LOC_MEASUREMENT',
                         'MAP_LIST',
                         'MATRIX_DIM',
                         'MAX_BLOCK_SIZE',
                         'MAX_GRAD',
                         'MAX_ODT',
                         'MAX_ODT_ENTRIES',
                         'MAX_REFRESH',
                         'MEMORY_LAYOUT',
                         'MEMORY_SEGMENT',
                         'MONOTONY',
                         'NO_AXIS_PTS_X',
                         'NO_AXIS_PTS_Y',
                         'NO_AXIS_PTS_Z',
                         # 'NO_AXIS_PTS_4',
                         # 'NO_AXIS_PTS_5',
                         'NO_OVERLOAD_INDICATION',
                         'NO_OF_INTERFACES',
                         'NO_RESCALE_X',
                         'NO_RESCALE_Y',
                         'NO_RESCALE_Z',
                         'NUMBER',
                         'OFFSET_X',
                         'OFFSET_Y',
                         'OFFSET_Z',
                         # 'OFFSET_4',
                         # 'OFFSET_5',
                         'OPTIMISATION_TYPE_DEFAULT',
                         'OPTIMISATION_TYPE_ODT_TYPE_16',
                         'OPTIMISATION_TYPE_ODT_TYPE_32',
                         'OPTIMISATION_TYPE_ODT_TYPE_64',
                         'OPTIMISATION_TYPE_ODT_TYPE_ALIGNMENT',
                         'OPTIMISATION_TYPE_MAX_ENTRY_SIZE',
                         'OUT_MEASUREMENT',
                         'OVERLOAD_INDICATION_EVENT',
                         'OVERLOAD_INDICATION_PID',
                         'PAG',
                         'PGM',
                         'PHONE_NO',
                         # 'PHYS_UNIT',
                         'PRESCALER_SUPPORTED',
                         'PROJECT_NO',
                         'PROTOCOL_LAYER',
                         'READ_ONLY',
                         'READ_WRITE',
                         'REF_CHARACTERISTIC',
                         'REF_GROUP',
                         'REF_MEASUREMENT',
                         'REF_MEMORY_SEGMENT',
                         'REF_UNIT',
                         'RESERVED',
                         'RIGHT_SHIFT',
                         'RIP_ADDR_W',
                         'RIP_ADDR_X',
                         'RIP_ADDR_Y',
                         'RIP_ADDR_Z',
                         # 'RIP_ADDR_4',
                         # 'RIP_ADDR_5',
                         'ROOT',
                         'SECTOR',
                         'SHIFT_OP_X',
                         'SHIFT_OP_Y',
                         'SHIFT_OP_Z',
                         # 'SHIFT_OP_4',
                         # 'SHIFT_OP_5',
                         'SIGN_EXTEND',
                         'SI_EXPONENTS',
                         'SRC_ADDR_X',
                         'SRC_ADDR_Y',
                         'SRC_ADDR_Z',
                         # 'SRC_ADDR_4',
                         # 'SRC_ADDR_5',
                         'STATIC',
                         # 'STATIC_RECORD_LAYOUT',
                         # 'STATUS_STRING_REF',
                         # 'STEP_SIZE',
                         'STIM',
                         'SUB_FUNCTION',
                         'SUB_GROUP',
                         'SUPPLIER',
                         # 'SYMBOL_LINK',
                         'SYSTEM_CONSTANT',
                         'S_REC_LAYOUT',
                         'UNIT_CONVERSION',
                         'USER',
                         'TIMESTAMP_SUPPORTED',
                         'TIMESTAMP_FIXED',
                         'VAR_ADDRESS',
                         'VAR_CHARACTERISTIC',
                         'VAR_CRITERION',
                         'VAR_FORBIDDEN_COMB',
                         'VAR_MEASUREMENT',
                         'VAR_NAMING',
                         'VAR_SELECTION_CHARACTERISTIC',
                         # 'VAR_SEPERATOR',
                         'VERSION',
                         'VIRTUAL',
                         'VIRTUAL_CHARACTERISTIC',
                         'XCP',
                         'RASTER',
                         'EVENT_GROUP',
                         'SEED_KEY',
                         'CHECKSUM',
                         'TP_BLOB',
                         'SOURCE',
                         'QP_BLOB',

                         'SEGMENT',
                         'PAGE',
                         'INIT_SEGMENT',
                         'ECU_ACCESS_NOT_ALLOWED',
                         'ECU_ACCESS_WITHOUT_XCP_ONLY',
                         'ECU_ACCESS_WITH_XCP_ONLY',
                         'ECU_ACCESS_DONT_CARE',
                         'XCP_READ_ACCESS_NOT_ALLOWED',
                         'XCP_READ_ACCESS_WITHOUT_ECU_ONLY',
                         'XCP_READ_ACCESS_WITH_ECU_ONLY',
                         'XCP_READ_ACCESS_DONT_CARE',
                         'XCP_WRITE_ACCESS_NOT_ALLOWED',
                         'XCP_WRITE_ACCESS_WITHOUT_ECU_ONLY',
                         'XCP_WRITE_ACCESS_WITH_ECU_ONLY',
                         'XCP_WRITE_ACCESS_DONT_CARE',

                         'XCP_ON_CAN',
                         'XCP_ON_TCP_IP',
                         'XCP_ON_UDP_IP',
                         'HOST_NAME',
                         'ADDRESS',
                         'CAN_ID_BROADCAST',
                         'CAN_ID_MASTER',
                         'CAN_ID_SLAVE',
                         'BAUDRATE',
                         'SAMPLE_POINT',
                         'SAMPLE_RATE',
                         'BTL_CYCLES',
                         'SJW',
                         'SYNC_EDGE',
                         'DAQ_LIST_CAN_ID',
                         'SINGLE',
                         'DUAL',
                         'TRIPLE',
                         'FIXED_EVENT_LIST',

                         'VARIABLE',
                         'FIXED',

                         'DP_BLOB',
                         'BA_BLOB',

                         'KP_BLOB',
                         'PA_BLOB',

                         'UBYTE',
                         'SBYTE',
                         'UWORD',
                         'SWORD',
                         'ULONG',
                         'SLONG',
                         'A_UINT64',
                         'A_INT64',
                         'FLOAT32_IEEE',
                         'FLOAT64_IEEE',

                         'BYTE',
                         'WORD',
                         'LONG',

                         'PBYTE',
                         'PWORD',
                         'PLONG',
                         'DIRECT',

                         'INDEX_INCR',
                         'INDEX_DECR',

                         'VALUE',
                         'CURVE',
                         'MAP',
                         'CUBOID',
                         'VAL_BLK',
                         'ASCII',

                         'MSB_FIRST',
                         'MSB_LAST',

                         'MON_INCREASE',
                         'MON_DECREASE',
                         'STRICT_INCREASE',
                         'STRICT_DECREASE',

                         'STD_AXIS',
                         'FIX_AXIS',
                         'COM_AXIS',
                         'RES_AXIS',
                         'CURVE_AXIS',

                         'CALIBRATION',
                         'NO_CALIBRATION',
                         'NOT_IN_MCD_SYSTEM',
                         'OFFLINE_CALIBRATION',

                         'ABSOLUTE',
                         'DIFFERENCE',

                         'TAB_INTP',
                         'TAB_NOINTP',
                         'TAB_VERB',
                         'RAT_FUNC',
                         'FORM',
                         'IDENTICAL',

                         'TAB_INTP',
                         'TAB_NOINTP',

                         'TAB_VERB',

                         'COLUMN_DIR',
                         'ROW_DIR',
                         'ALTERNATE_WITH_X',
                         'ALTERNATE_WITH_Y',
                         'ALTERNATE_CURVES',

                         'VAR_SEPARATOR',

                         'EXTENDED_SI',
                         'DERIVED',

                         'PRG_CODE',
                         'PRG_DATA',
                         'PRG_RESERVED',

                         'CODE',
                         'DATA',
                         'OFFLINE_DATA',
                         'VARIABLES',
                         'SERAM',
                         'RESERVED',
                         'RESUME_SUPPORTED',
                         'CALIBRATION_VARIABLES',
                         'EXCLUDE_FROM_FLASH',

                         'RAM',
                         'EEPROM',
                         'EPROM',
                         'ROM',
                         'REGISTER',
                         'FLASH',

                         'INTERN',
                         'EXTERN',

                         'block',

                         'struct',
                         'taggedstruct',
                         'taggedunion',
                         'enum',

                         'char',
                         'int',
                         'long',
                         'uchar',
                         'uint',
                         'ulong',
                         'double',
                         'float'))

tokens = list(keywords.values()) + [
    r'NUMERIC',
    r'STRING',
    r'IDENT',
    r'begin',
    r'end',
    r'PARENTHESE_OPEN',
    r'PARENTHESE_CLOSE',
    r'CURLY_OPEN',
    r'CURLY_CLOSE',
    r'BRACE_OPEN',
    r'BRACE_CLOSE',
    r'SEMICOLON',
    r'ASTERISK',
    r'EQUAL',
    r'COMMA'
]

t_ignore = ' \t\r\n'


@lex.TOKEN(r'(/\*(.|\n)*?\*/)')
def t_ignore_C_COMMENT(token):
    pass


@lex.TOKEN(r'(\/{2}.+\n)')
def t_ignore_CPP_COMMENT(token):
    pass


t_PARENTHESE_OPEN = r'\('
t_PARENTHESE_CLOSE = r'\)'
t_CURLY_OPEN = r'\{'
t_CURLY_CLOSE = r'\}'
t_BRACE_OPEN = r'\['
t_BRACE_CLOSE = r'\]'
t_SEMICOLON = r';'
t_ASTERISK = r'\*'
t_EQUAL = r'='
t_COMMA = r','


@lex.TOKEN(r'(\/begin)')
def t_begin(token):
    return token


@lex.TOKEN(r'(\/end)')
def t_end(token):
    return token


@lex.TOKEN(r'"(?:[^"\\]|\\.)*"')
def t_STRING(token):
    token.value = token.value[1:-1]
    return token


@lex.TOKEN(r'[+-]?(([0]{1}[Xx]{1}[A-Fa-f0-9]+)|(\d+(\.(\d*([eE][+-]?\d+)?)?|([eE][+-]?\d+)?)?))')
def t_NUMERIC(token):
    try:
        token.value = int(token.value, 10)
    except ValueError:
        try:
            token.value = int(token.value, 16)
        except ValueError:
            token.value = float(token.value)
    return token


@lex.TOKEN(r'[A-Za-z_][A-Za-z0-9_\.\[\]]*')
def t_IDENT(token):
    try:
        token.type = keywords[token.value.split('[')[0]]
    except KeyError:
        pass
    return token


def t_error(token):
    print('invalid character at line ' + str(token.lineno) + ', position ' + str(token.lexpos))
    token.lexer.skip(1)


lexer = lex.lex(optimize=True, outputdir=os.path.dirname(os.path.realpath(__file__)), lextab='lextab')
