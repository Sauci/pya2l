"""
@project: a2l_parser
@file: lexer.py
@author: Guillaume Sottas
@date: 20.03.2018
"""

import ply.lex as lex


class KeywordsList(dict):
    def __init__(self, *keywords):
        super(KeywordsList, self).__init__([(kw, kw.encode('string-escape')) for kw in set(keywords)])


top_level_keywords = KeywordsList('A2ML_VERSION',
                                  'ASAP2_VERSION',
                                  'HEADER',
                                  'MODULE',
                                  'PROJECT')

primary_keywords = KeywordsList('A2ML',
                                'AXIS_PTS',
                                'BLOB',
                                'CHARACTERISTIC',
                                'COMPU_METHOD',
                                'COMPU_TAB',
                                'COMPU_VTAB',
                                'COMPU_VTAB_RANGE',
                                'FRAME',
                                'FUNCTION',
                                'GROUP',
                                'IF_DATA',
                                'INSTANCE',
                                'MEASUREMENT',
                                'MOD_COMMON',
                                'MOD_PAR',
                                'RECORD_LAYOUT',
                                'TRANSFORMER',
                                'TYPEDEF_AXIS',
                                'TYPEDEF_BLOB',
                                'TYPEDEF_CHARACTERISTIC',
                                'TYPEDEF_MEASUREMENT',
                                'TYPEDEF_STRUCTURE',
                                'UNIT',
                                'USER_RIGHTS',
                                'VARIANT_CODING')

secondary_keywords = KeywordsList('ADDR_EPK',
                                  'ALIGNMENT_BYTE',
                                  'ALIGNMENT_FLOAT32_IEEE',
                                  'ALIGNMENT_FLOAT64_IEEE',
                                  'ALIGNMENT_INT64',
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
                                  'AXIS_PTS_4',
                                  'AXIS_PTS_5',
                                  'AXIS_RESCALE_X',
                                  'AXIS_RESCALE_Y',
                                  'AXIS_RESCALE_Z',
                                  'BIT_MASK',
                                  'BIT_OPERATION',
                                  'BYTE_ORDER',
                                  'CALIBRATION_ACCESS',
                                  'CALIBRATION_HANDLE',
                                  'CALIBRATION_HANDLE_TEXT',
                                  'CALIBRATION_METHOD',
                                  'COEFFS',
                                  'COEFFS_LINEAR',
                                  'COMPARISON_QUANTITY',
                                  'COMPU_TAB_REF',
                                  'CPU_TYPE',
                                  'CURVE_AXIS_REF',
                                  'CUSTOMER',
                                  'CUSTOMER_NO',
                                  'DATA_SIZE',
                                  'DEFAULT_VALUE',
                                  'DEFAULT_VALUE_NUMERIC',
                                  'DEF_CHARACTERISTIC',
                                  'DEPENDENT_CHARACTERISTIC',
                                  'DEPOSIT',
                                  'DISCRETE',
                                  'DISPLAY_IDENTIFIER',
                                  'DIST_OP_X',
                                  'DIST_OP_Y',
                                  'DIST_OP_Z',
                                  'DIST_OP_4',
                                  'DIST_OP_5',
                                  'ECU',
                                  'ECU_ADDRESS',
                                  'ECU_ADDRESS_EXTENSION',
                                  'ECU_CALIBRATION_OFFSET',
                                  'EPK',
                                  'ERROR_MASK',
                                  'EXTENDED_LIMITS',
                                  'FIX_AXIS_PAR',
                                  'FIX_AXIS_PAR_DIST',
                                  'FIX_AXIS_PAR_LIST',
                                  'FIX_NO_AXIS_PTS_X',
                                  'FIX_NO_AXIS_PTS_Y',
                                  'FIX_NO_AXIS_PTS_Z',
                                  'FIX_NO_AXIS_PTS_4',
                                  'FIX_NO_AXIS_PTS_5',
                                  'FNC_VALUES',
                                  'FORMAT',
                                  'FORMULA',
                                  'FORMULA_INV',
                                  'FRAME_MEASUREMENT',
                                  'FUNCTION_LIST',
                                  'FUNCTION_VERSION',
                                  'GUARD_RAILS',
                                  'IDENTIFICATION',
                                  'IF_DATA',
                                  'IN_MEASUREMENT',
                                  'LAYOUT',
                                  'LEFT_SHIFT',
                                  'LOC_MEASUREMENT',
                                  'MAP_LIST',
                                  'MATRIX_DIM',
                                  'MAX_GRAD',
                                  'MAX_REFRESH',
                                  'MEMORY_LAYOUT',
                                  'MEMORY_SEGMENT',
                                  'MONOTONY',
                                  'NO_AXIS_PTS_X',
                                  'NO_AXIS_PTS_Y',
                                  'NO_AXIS_PTS_Z',
                                  'NO_AXIS_PTS_4',
                                  'NO_AXIS_PTS_5',
                                  'NO_OF_INTERFACES',
                                  'NO_RESCALE_X',
                                  'NO_RESCALE_Y',
                                  'NO_RESCALE_Z',
                                  'NUMBER',
                                  'OFFSET_X',
                                  'OFFSET_Y',
                                  'OFFSET_Z',
                                  'OFFSET_4',
                                  'OFFSET_5',
                                  'OUT_MEASUREMENT',
                                  'PHONE_NO',
                                  'PHYS_UNIT',
                                  'PROJECT_NO',
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
                                  'RIP_ADDR_4',
                                  'RIP_ADDR_5',
                                  'ROOT',
                                  'SHIFT_OP_X',
                                  'SHIFT_OP_Y',
                                  'SHIFT_OP_Z',
                                  'SHIFT_OP_4',
                                  'SHIFT_OP_5',
                                  'SIGN_EXTEND',
                                  'SI_EXPONENTS',
                                  'SRC_ADDR_X',
                                  'SRC_ADDR_Y',
                                  'SRC_ADDR_Z',
                                  'SRC_ADDR_4',
                                  'SRC_ADDR_5',
                                  'STATIC_RECORD_LAYOUT',
                                  'STATUS_STRING_REF',
                                  'STEP_SIZE',
                                  'SUB_FUNCTION',
                                  'SUB_GROUP',
                                  'SUPPLIER',
                                  'SYMBOL_LINK',
                                  'SYSTEM_CONSTANT',
                                  'UNIT_CONVERSION',
                                  'USER',
                                  'VAR_ADDRESS',
                                  'VAR_CHARACTERISTIC',
                                  'VAR_CRITERION',
                                  'VAR_FORBIDDEN_COMB',
                                  'VAR_MEASUREMENT',
                                  'VAR_NAMING',
                                  'VAR_SELECTION_CHARACTERISTIC',
                                  'VAR_SEPERATOR',
                                  'VERSION',
                                  'VIRTUAL',
                                  'VIRTUAL_CHARACTERISTIC')

datatype_keywords = KeywordsList('UBYTE',
                                 'SBYTE',
                                 'UWORD',
                                 'SWORD',
                                 'ULONG',
                                 'SLONG',
                                 'A_UINT64',
                                 'A_INT64',
                                 'FLOAT32_IEEE',
                                 'FLOAT64_IEEE')

datasize_keywords = KeywordsList('BYTE',
                                 'WORD',
                                 'LONG')

addrtype_keywords = KeywordsList('PBYTE',
                                 'PWORD',
                                 'PLONG',
                                 'DIRECT')

indexorder_keywords = KeywordsList('INDEX_INCR',
                                   'INDEX_DECR')

characteristic_type_keywords = KeywordsList('VALUE',
                                            'CURVE',
                                            'MAP',
                                            'CUBOID',
                                            'VAL_BLK',
                                            'ASCII')

byte_order_keywords = KeywordsList('MSB_FIRST',
                                   'MSB_LAST')

axis_descr_attribute_keywords = KeywordsList('STD_AXIS',
                                             'FIX_AXIS',
                                             'COM_AXIS',
                                             'RES_AXIS',
                                             'CURVE_AXIS')

calibration_access_type_keywords = KeywordsList('CALIBRATION',
                                                'NO_CALIBRATION',
                                                'NOT_IN_MCD_SYSTEM',
                                                'OFFLINE_CALIBRATION')

deposit_mode_keywords = KeywordsList('ABSOLUTE',
                                     'DIFFERENCE')

compu_method_keywords = KeywordsList('TAB_INTP',
                                     'TAB_NOINTP',
                                     'TAB_VERB',
                                     'RAT_FUNC',
                                     'FORM',
                                     'IDENTICAL')

compu_tab_conversion_type_keywords = KeywordsList('TAB_INTP',
                                                  'TAB_NOINTP')

compu_vtab_conversion_type_keywords = KeywordsList('TAB_VERB')

fnc_values_index_mode_keywords = KeywordsList('COLUMN_DIR',
                                              'ROW_DIR',
                                              'ALTERNATE_WITH_X',
                                              'ALTERNATE_WITH_Y',
                                              'ALTERNATE_CURVES')

var_separator_keywords = KeywordsList('VAR_SEPARATOR')

unit_type_keywords = KeywordsList('EXTENDED_SI',
                                  'DERIVED')

reserved_keywords = dict(top_level_keywords.items() + \
                         primary_keywords.items() + \
                         secondary_keywords.items() + \
                         datatype_keywords.items() + \
                         datasize_keywords.items() + \
                         addrtype_keywords.items() + \
                         indexorder_keywords.items() + \
 \
                         characteristic_type_keywords.items() + \
                         byte_order_keywords.items() + \
                         axis_descr_attribute_keywords.items() + \
                         calibration_access_type_keywords.items() + \
                         deposit_mode_keywords.items() + \
                         compu_method_keywords.items() + \
                         compu_tab_conversion_type_keywords.items() + \
                         compu_vtab_conversion_type_keywords.items() + \
                         fnc_values_index_mode_keywords.items() + \
                         var_separator_keywords.items() + \
                         unit_type_keywords.items())

tokens = reserved_keywords.values() + [
    r'C_COMMENT',
    r'CPP_COMMENT',
    r'NUMERIC',
    r'STRING',
    r'IDENT',
    r'begin',
    r'end',
    r'RAW_TEXT'
]

t_ignore = ' \t\r\n'


@lex.TOKEN(r'(/\*(.|\n)*?\*/)')
def t_ignore_C_COMMENT(token):
    pass


@lex.TOKEN(r'(\/{2}.+\n)')
def t_ignore_CPP_COMMENT(token):
    pass


@lex.TOKEN(r'(\/begin)')
def t_begin(token):
    return token


@lex.TOKEN(r'(\/end)')
def t_end(token):
    return token


@lex.TOKEN(r'"[^"]{0,}"')
def t_STRING(token):
    token.value = token.value[1:-1]
    return token


@lex.TOKEN(r'[+-]{0,1}(([0]{1}[Xx]{1}[A-Fa-f0-9]{1,})|(\d+(\.\d*)?))')
def t_NUMERIC(token):
    try:
        token.value = int(token.value, 10)
    except ValueError:
        try:
            token.value = int(token.value, 16)
        except ValueError:
            try:
                token.value = float(token.value)
            except ValueError:
                raise Exception('internal regular expression issue...')
            except:
                raise
        except:
            raise
    except:
        raise
    return token


@lex.TOKEN(r'[A-Za-z0-9_]{1}[^\s]{0,}')
def t_IDENT(token):
    try:
        token.type = reserved_keywords[token.value]
    except KeyError:
        pass
    except:
        raise
    return token


@lex.TOKEN(r'.+')
def t_RAW_TEXT(token):
    return token


def t_error(token):
    print('invalid character at line ' + str(token.lineno) + ', position ' + str(token.lexpos))
    token.lexer.skip(1)


lexer = lex.lex()
