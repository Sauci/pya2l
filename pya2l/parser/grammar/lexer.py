"""
@project: pya2l
@file: lexer.py
@author: Guillaume Sottas
@date: 20.03.2018
"""

import os
import ply.lex as lex

from pya2l.parser.exception import A2lLexerException
from pya2l.parser.type import String

a2l_keywords = dict((k, k) for k in {
    'A2ML',
    'A2ML_VERSION',  # TODO: check, as not defined in specification's keyword list.
    'ABSOLUTE',
    #    'ADDRESS_MAPPING' defined but used in IF_DATA node.
    'ADDR_EPK',
    'ALIGNMENT_BYTE',
    'ALIGNMENT_FLOAT32_IEEE',
    'ALIGNMENT_FLOAT64_IEEE',
    'ALIGNMENT_LONG',
    'ALIGNMENT_WORD',
    'ALTERNATE_CURVES',
    'ALTERNATE_WITH_X',
    'ALTERNATE_WITH_Y',
    'ANNOTATION',
    'ANNOTATION_LABEL',
    'ANNOTATION_ORIGIN',
    'ANNOTATION_TEXT',
    'ARRAY_SIZE',
    'ASAP2_VERSION',
    'ASCII',
    'AXIS_DESCR',
    'AXIS_PTS',
    'AXIS_PTS_REF',
    'AXIS_PTS_X',
    'AXIS_PTS_Y',
    'AXIS_PTS_Z',
    'AXIS_RESCALE_X',
    'AXIS_RESCALE_Y',
    'AXIS_RESCALE_Z',
    'BIT_MASK',
    'BIT_OPERATION',
    'BYTE',
    'BYTE_ORDER',
    'CALIBRATION',
    'CALIBRATION_ACCESS',
    'CALIBRATION_HANDLE',
    'CALIBRATION_METHOD',
    'CALIBRATION_VARIABLES',
    'CHARACTERISTIC',
    #    'CHECKSUM' defined but used in IF_DATA node.
    'CODE',
    'COEFFS',
    'COLUMN_DIR',
    'COMPARISON_QUANTITY',
    'COMPU_METHOD',
    'COMPU_TAB',
    'COMPU_TAB_REF',
    'COMPU_VTAB',
    'COMPU_VTAB_RANGE',
    'COM_AXIS',
    'CPU_TYPE',
    'CUBOID',
    'CURVE',
    'CURVE_AXIS',
    'CURVE_AXIS_REF',
    'CUSTOMER',
    'CUSTOMER_NO',
    'DATA',
    'DATA_SIZE',
    'DEFAULT_VALUE',
    'DEF_CHARACTERISTIC',
    'DEPENDENT_CHARACTERISTIC',
    'DEPOSIT',
    'DERIVED',
    'DIFFERENCE',
    'DIRECT',
    'DISPLAY_IDENTIFIER',
    'DIST_OP_X',
    'DIST_OP_Y',
    'DIST_OP_Z',
    #    'DP_BLOB' defined but used in IF_DATA node.
    'ECU',
    'ECU_ADDRESS',
    'ECU_ADDRESS_EXTENSION',
    'ECU_CALIBRATION_OFFSET',
    'EEPROM',
    'EPK',
    'EPROM',
    'ERROR_MASK',
    #    'EVENT_GROUP' defined but used in IF_DATA node.
    'EXCLUDE_FROM_FLASH',
    'EXTENDED_LIMITS',
    'EXTENDED_SI',
    'EXTERN',
    'FIX_AXIS',
    'FIX_AXIS_PAR',
    'FIX_AXIS_PAR_DIST',
    'FIX_AXIS_PAR_LIST',
    'FIX_NO_AXIS_PTS_X',
    'FIX_NO_AXIS_PTS_Y',
    'FIX_NO_AXIS_PTS_Z',
    'FLASH',
    'FLOAT32_IEEE',
    'FLOAT64_IEEE',
    'FNC_VALUES',
    'FORM',
    'FORMAT',
    'FORMULA',
    'FORMULA_INV',
    'FRAME',
    'FRAME_MEASUREMENT',
    'FUNCTION',
    'FUNCTION_LIST',
    'FUNCTION_VERSION',
    'GROUP',
    'GUARD_RAILS',
    'HEADER',
    'IDENTIFICATION',
    'IF_DATA',
    'INDEX_DECR',
    'INDEX_INCR',
    'INTERN',
    'IN_MEASUREMENT',  # TODO: check, as not defined in specification's keyword list.
    #    'KP_BLOB' defined but used in IF_DATA node.
    'LEFT_SHIFT',  # TODO: check, as not defined in specification's keyword list.
    'LOC_MEASUREMENT',  # TODO: check, as not defined in specification's keyword list.
    'LONG',
    'MAP',
    'MAP_LIST',
    'MATRIX_DIM',
    'MAX_GRAD',
    'MAX_REFRESH',
    'MEASUREMENT',
    'MEMORY_LAYOUT',
    'MEMORY_SEGMENT',
    'MODULE',
    'MOD_COMMON',
    'MOD_PAR',
    'MONOTONY',
    'MON_DECREASE',
    'MON_INCREASE',
    'MSB_FIRST',
    'MSB_LAST',
    #    'MULTIPLEX' defined but used in IF_DATA node.
    'NOT_IN_MCD_SYSTEM',
    'NO_AXIS_PTS_X',
    'NO_AXIS_PTS_Y',
    'NO_AXIS_PTS_Z',
    'NO_CALIBRATION',
    'NO_OF_INTERFACES',
    'NO_RESCALE_X',
    'NO_RESCALE_Y',
    'NO_RESCALE_Z',
    'NUMBER',
    #    'NUMERIC' is used in VAR_NAMING node, as an enum element. as this enumeration will probably be updated in
    #    future releases of the standard, any value will be accepted.
    'OFFLINE_CALIBRATION',
    'OFFLINE_DATA',
    'OFFSET_X',
    'OFFSET_Y',
    'OFFSET_Z',
    'OUT_MEASUREMENT',  # TODO: check, as not defined in specification's keyword list.
    #    'PA_BLOB' defined but used in IF_DATA node.
    'PBYTE',
    'PHONE_NO',
    'PLONG',
    'PRG_CODE',
    'PRG_DATA',
    'PRG_RESERVED',
    'PROJECT',
    'PROJECT_NO',
    'PWORD',
    #    'QP_BLOB' defined but used in IF_DATA node.
    'RAM',
    #    'RASTER' defined but used in IF_DATA node.
    'RAT_FUNC',
    'READ_ONLY',
    'READ_WRITE',
    'RECORD_LAYOUT',
    'REF_CHARACTERISTIC',
    'REF_GROUP',  # TODO: check, as not defined in specification's keyword list.
    'REF_MEASUREMENT',
    'REF_MEMORY_SEGMENT',
    'REF_UNIT',
    'REGISTER',
    'RESERVED',
    'RES_AXIS',  # TODO: check, as not defined in specification's keyword list.
    'RIGHT_SHIFT',
    'RIP_ADDR_W',
    'RIP_ADDR_X',
    'RIP_ADDR_Y',
    'RIP_ADDR_Z',
    'ROM',
    'ROOT',
    'ROW_DIR',
    'SBYTE',
    #    'SEED_KEY' defined but used in IF_DATA node.
    'SERAM',
    'SHIFT_OP_X',
    'SHIFT_OP_Y',
    'SHIFT_OP_Z',
    'SIGN_EXTEND',
    'SI_EXPONENTS',
    'SLONG',
    #    'SOURCE' defined but used in IF_DATA node.
    'SRC_ADDR_X',
    'SRC_ADDR_Y',
    'SRC_ADDR_Z',
    'STD_AXIS',
    'STRICT_DECREASE',
    'STRICT_INCREASE',
    'SUB_FUNCTION',  # TODO: check, as not defined in specification's keyword list.
    'SUB_GROUP',  # TODO: check, as not defined in specification's keyword list.
    'SUPPLIER',
    'SWORD',
    'SYSTEM_CONSTANT',
    'S_REC_LAYOUT',
    'TAB_INTP',
    'TAB_NOINTP',
    'TAB_VERB',
    #    'TP_BLOB' defined but used in IF_DATA node.
    'UBYTE',
    'ULONG',
    'UNIT',
    'UNIT_CONVERSION',
    'USER',
    'USER_RIGHTS',
    'UWORD',
    'VALUE',
    'VAL_BLK',
    'VARIABLES',
    'VARIANT_CODING',
    'VAR_ADDRESS',
    'VAR_CHARACTERISTIC',
    'VAR_CRITERION',
    'VAR_FORBIDDEN_COMB',
    'VAR_MEASUREMENT',
    'VAR_NAMING',
    'VAR_SELECTION_CHARACTERISTIC',
    'VAR_SEPARATOR',
    'VERSION',
    'VIRTUAL',
    'VIRTUAL_CHARACTERISTIC',
    'WORD'
})

a2ml_keywords = dict((k, k) for k in {
    'block',
    'char',
    'double',
    'enum',
    'float',
    'int',
    'long',
    'struct',
    'taggedstruct',
    'taggedunion',
    'uchar',
    'uint',
    'ulong'
})

if_data_keywords = dict((k, k) for k in {})

tokens = tuple(set(list(a2l_keywords.values()) + \
                   list(a2ml_keywords.values()) + \
                   list(if_data_keywords.values()) + \
                   [
                       r'N',
                       r'S',
                       r'I',
                       r'begin',
                       r'end',
                       r'include',
                       r'PO',
                       r'PC',
                       r'CO',
                       r'CC',
                       r'BO',
                       r'BC',
                       r'SC',
                       r'ASTERISK',
                       r'EQ',
                       r'COMMA'
                   ]))

states = (
    ('a2ml', 'exclusive'),
    ('ifdata', 'exclusive')
)

t_ANY_ignore = ' \t'


@lex.TOKEN(r'(/\*(.|\n)*?\*/)')
def t_ANY_ignore_C_COMMENT(token):
    token.lexer.lineno += len(token.value.splitlines())


@lex.TOKEN(r'(\/{2}.+\n)')
def t_ANY_ignore_CPP_COMMENT(token):
    token.lexer.lineno += len(token.value.splitlines())


@lex.TOKEN(r'((\r\n)|(\r)|(\n))')
def t_ANY_ignore_NEW_LINE(token):
    token.lexer.lineno += 1


t_ANY_PO = r'\('
t_ANY_PC = r'\)'
t_ANY_CO = r'\{'
t_ANY_CC = r'\}'
t_ANY_BO = r'\['
t_ANY_BC = r'\]'
t_ANY_SC = r';'
t_ANY_ASTERISK = r'\*'
t_ANY_EQ = r'='
t_ANY_COMMA = r','


@lex.TOKEN(r'(\/begin)')
def t_ANY_begin(token):
    return token


@lex.TOKEN(r'(\/end)')
def t_ANY_end(token):
    return token


@lex.TOKEN(r'"(?:[^"\\]|\\.)*"')
def t_ANY_S(token):
    token.value = String(token.value[1:-1])
    return token


@lex.TOKEN(r'[+-]?(([0]{1}[Xx]{1}[A-Fa-f0-9]+)|(\d+(\.(\d*([eE][+-]?\d+)?)?|([eE][+-]?\d+)?)?))')
def t_ANY_N(token):
    try:
        token.value = int(token.value, 10)
    except ValueError:
        try:
            token.value = int(token.value, 16)
        except ValueError:
            token.value = float(token.value)
    return token


@lex.TOKEN(r'[A-Za-z_][A-Za-z0-9_\.\[\]]*')
def t_INITIAL_I(token):
    if token.value == 'IF_DATA':
        token.type = token.value
        token.lexer.push_state('ifdata')
    elif token.value == 'A2ML':
        token.type = token.value
        token.lexer.push_state('a2ml')
    else:
        try:
            token.type = a2l_keywords[token.value.split('[')[0]]
        except KeyError:
            pass
    return token


@lex.TOKEN(r'[A-Za-z_][A-Za-z0-9_]{0,}')
def t_a2ml_I(token):
    if token.value == 'A2ML':
        token.type = token.value
        token.lexer.pop_state()
    else:
        try:
            token.type = a2ml_keywords[token.value]
        except KeyError:
            pass
    return token


@lex.TOKEN(r'[A-Za-z_][A-Za-z0-9_\.\[\]]*')
def t_ifdata_I(token):
    if token.value == 'IF_DATA':
        token.type = token.value
        token.lexer.pop_state()
    else:
        try:
            token.type = if_data_keywords[token.value.split('[')[0]]
        except KeyError:
            pass
    return token


lexer_stack = list()


@lex.TOKEN(r'\/include\s*?"[^"]+"')
def t_ANY_ignore_include(token):
    filename = token.value.replace('/include', '').strip(' "')
    new_lexer = token.lexer.clone()
    new_lexer.lineno, new_lexer.lexpos = 1, 0
    with open(filename, 'r') as fp:
        new_lexer.input(fp.read())
    lexer_stack.append(new_lexer)
    return new_lexer.token()


def t_ANY_error(token):
    raise A2lLexerException(token.value[0], token.lineno, token.lexpos)


lexer = lex.lex(optimize=False, outputdir=os.path.dirname(os.path.realpath(__file__)), lextab='lextab')


def token_function():
    if len(lexer_stack):
        token = lexer_stack[-1].token()
    else:
        token = lexer.token()
    if not token and len(lexer_stack):
        lexer_stack.pop()
        token = token_function()
    return token
