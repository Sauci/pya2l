"""
@project: parser
@file: a2ml_parser_test.py
@author: Guillaume Sottas
@date: 28.12.2018
"""

import os
import pytest

from pya2l.parser.grammar.parser import A2lParser as Parser

uint = (
    pytest.param('0', 0),
    pytest.param('1', 1)
)

predefined_type_names = (
    pytest.param('char', id='signed char'),
    pytest.param('int', id='signed integer'),
    pytest.param('long', id='signed long'),
    pytest.param('uchar', id='unsigned char'),
    pytest.param('uint', id='unsigned integer'),
    pytest.param('ulong', id='unsigned long'),
    pytest.param('float', id='float'),
    pytest.param('double', id='double')
)

type_names = predefined_type_names + (
    pytest.param('struct {}', id='structure'),
    pytest.param('taggedstruct {}', id='tagged structure'),
    pytest.param('taggedunion {}', id='tagged union'),
    pytest.param('enum {"_"}', id='enumeration')
)


def generate_a2l_string(a2ml_string='', if_data_string=''):
    return """
        /begin PROJECT project ""
            /begin MODULE module ""
                /begin A2ML
                {a2ml_string}
                /end A2ML
                {if_data_string}
            /end MODULE
        /end PROJECT
    """.format(a2ml_string=a2ml_string, if_data_string=if_data_string)


@pytest.mark.parametrize('type_name, array_size, array_size_value, if_data_string', (
        ('int', '[1][2][3]', [1, 2, 3], '1 2 3 4 5 6'),
))
def test_array_size(type_name, array_size, array_size_value, if_data_string):
    a2ml_string = """block "IF_DATA" taggedunion {{
            "TAG" {type_name}{array_specifier};
        }};""".format(type_name=type_name, array_specifier=array_size)
    a2l_string = """/begin IF_DATA TAG {if_data_string} /end IF_DATA""".format(if_data_string=if_data_string)
    p = Parser(generate_a2l_string(a2ml_string=a2ml_string, if_data_string=a2l_string))
    for index in range(6):
        assert p.ast.project.module[0].if_data.TAG[index] == index + 1


@pytest.mark.parametrize('type_name', type_names)
def test_a2ml_root_type_definition(type_name):
    Parser(generate_a2l_string(a2ml_string='{};'.format(type_name)))


@pytest.mark.parametrize('container', (
        pytest.param('taggedunion', id='tagged union container'),
        pytest.param('taggedstruct', id='tagged structure container')))
@pytest.mark.parametrize('type_name, if_data_string, path, value', (
        ('char', '/begin IF_DATA TAG 0 /end IF_DATA', ['TAG'], 0),
        ('int', '/begin IF_DATA TAG 0 /end IF_DATA', ['TAG'], 0),
        ('long', '/begin IF_DATA TAG 0 /end IF_DATA', ['TAG'], 0),
        ('uchar', '/begin IF_DATA TAG 0 /end IF_DATA', ['TAG'], 0),
        ('uint', '/begin IF_DATA TAG 0 /end IF_DATA', ['TAG'], 0),
        ('ulong', '/begin IF_DATA TAG 0 /end IF_DATA', ['TAG'], 0),
        ('float', '/begin IF_DATA TAG 0 /end IF_DATA', ['TAG'], 0),
        ('double', '/begin IF_DATA TAG 0 /end IF_DATA', ['TAG'], 0),
        ('struct {int;}', '/begin IF_DATA TAG 0 /end IF_DATA', ['TAG'], [0]),
        ('taggedstruct {"_" int;}', '/begin IF_DATA TAG _ 0 /end IF_DATA', ['TAG', '_'], 0),
        ('taggedunion {"_" int;}', '/begin IF_DATA TAG _ 0 /end IF_DATA', ['TAG', '_'], 0),
        ('enum {"_"}', '/begin IF_DATA TAG _ /end IF_DATA', ['TAG'], '_'),
))
def test_a2ml_root_block_definition(container, type_name, if_data_string, path, value):
    a2ml_string = 'block "IF_DATA" {container} {{"TAG" {type_name};}};'.format(container=container, type_name=type_name)
    p = Parser(generate_a2l_string(a2ml_string=a2ml_string, if_data_string=if_data_string))
    node = p.ast.project.module[0].if_data
    for element in path:
        node = getattr(node, element)
    assert node == value


def test_a2ml_structure_flattening():
    a2ml_string = """block "IF_DATA" taggedunion {
        "TAG" struct {
            int; struct {int; struct {int; struct {int; int; struct {int; int; int; struct {int; int;};};};};};};
    };"""
    if_data_string = '/begin IF_DATA TAG 0 1 2 3 4 5 6 7 8 9 /end IF_DATA'
    p = Parser(generate_a2l_string(a2ml_string=a2ml_string, if_data_string=if_data_string))
    for index in range(10):
        assert p.ast.project.module[0].if_data.TAG[index] == index


@pytest.mark.parametrize('forward_definition_type, forward_definition_content, if_data_string, path, value', (
        ('struct', '{int;}', '/begin IF_DATA TAG 0 /end IF_DATA', ['TAG'], [0]),
        ('taggedstruct', '{"_" int;}', '/begin IF_DATA TAG _ 0 /end IF_DATA', ['TAG', '_'], 0),
        ('taggedunion', '{"_" int;}', '/begin IF_DATA TAG _ 0 /end IF_DATA', ['TAG', '_'], 0),
        ('enum', '{"_"}', '/begin IF_DATA TAG _ /end IF_DATA', ['TAG'], '_'),
))
def test_a2ml_forward_type_definition(forward_definition_type, forward_definition_content, if_data_string, path, value):
    a2ml_string = """{forward_definition_type} tag {forward_definition_content};
    block "IF_DATA" taggedunion {{
        "TAG" {forward_definition_type} tag;
    }};""".format(forward_definition_type=forward_definition_type,
                  forward_definition_content=forward_definition_content)
    p = Parser(generate_a2l_string(a2ml_string=a2ml_string, if_data_string=if_data_string))
    node = p.ast.project.module[0].if_data
    for element in path:
        node = getattr(node, element)
    assert node == value


@pytest.mark.parametrize('a2ml_string, if_data_string, value', (
        pytest.param("""block "IF_DATA" taggedunion {
            "TAG" taggedstruct {
                ("_" int)*;
            };
        };""", '/begin IF_DATA TAG /end IF_DATA', list(), id='empty tagged structure'),
        pytest.param("""block "IF_DATA" taggedunion {
            "TAG" taggedstruct {
                ("_" int)*;
            };
        };""", '/begin IF_DATA TAG _ 0 _ 1 /end IF_DATA', [0, 1], id='non empty tagged structure'),
        pytest.param("""block "IF_DATA" taggedunion {
            "TAG" taggedunion {
                "_" int;
            };
        };""", '/begin IF_DATA TAG /end IF_DATA', None, id='empty tagged union'),
        pytest.param("""block "IF_DATA" taggedunion {
            "TAG" taggedunion {
                "_" int;
            };
        };""", '/begin IF_DATA TAG _ 0 /end IF_DATA', 0, id='non empty tagged union'),
))
def test_a2ml_tagged_structure_multiplicity(a2ml_string, if_data_string, value):
    p = Parser(generate_a2l_string(a2ml_string=a2ml_string, if_data_string=if_data_string))
    assert p.ast.project.module[0].if_data.TAG._ == value


with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input', 'asap2_1_61.aml'), 'r') as fp:
    asap2_1_61 = fp.read()
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input', 'asap2_1_61_shared_type_definition.aml'),
          'r') as fp:
    asap2_1_61_shared_type_definition = fp.read()

a2ml_strings = (
    pytest.param(asap2_1_61, id='ASAP2 version 1.61'),
    pytest.param(asap2_1_61_shared_type_definition, id='ASAP2 version 1.61 with shared type definitions'))


@pytest.mark.parametrize('a2l_string', (pytest.param("""
        /begin PROJECT project ""
            /begin MODULE module ""
                /begin A2ML
                    block "IF_DATA" taggedunion {
                        "if_data_module" struct {
                            uint;
                        };
                        "if_data_memory_layout" struct {
                            uint[1];
                        };
                        "if_data_memory_segment" struct {
                            uint[2];
                        };
                        "if_data_characteristic" struct {
                            uint[3];
                        };
                        "if_data_axis_pts" struct {
                            uint[4];
                        };
                        "if_data_measurement" struct {
                            uint[5];
                        };
                        "if_data_frame" struct {
                            uint[6];
                        };
                    };
                /end A2ML
                /begin IF_DATA if_data_module
                    0
                /end IF_DATA
                /begin MOD_PAR ""
                    /begin MEMORY_LAYOUT PRG_CODE 0 0 0 0 0 0 0
                        /begin IF_DATA if_data_memory_layout
                            0
                        /end IF_DATA
                    /end MEMORY_LAYOUT
                    /begin MEMORY_SEGMENT _ "" CODE RAM INTERN 0 0 0 0 0 0 0
                        /begin IF_DATA if_data_memory_segment
                            1 2
                        /end IF_DATA
                    /end MEMORY_SEGMENT
                /end MOD_PAR
                /begin CHARACTERISTIC _ "" VALUE 0 _ 0.0 _ 0.0 0.0
                    /begin IF_DATA if_data_characteristic
                        3 4 5
                    /end IF_DATA
                /end CHARACTERISTIC
                /begin AXIS_PTS _ "" 0 _ _ 0.0 _ 0 0.0 0.0
                    /begin IF_DATA if_data_axis_pts
                        6 7 8 9
                    /end IF_DATA
                /end AXIS_PTS
                /begin MEASUREMENT _ "" UBYTE _ 0 0.0 0.0 0.0
                    /begin IF_DATA if_data_measurement
                        10 11 12 13 14
                    /end IF_DATA
                /end MEASUREMENT
                /begin FRAME _ "" 0 0
                    /begin IF_DATA if_data_frame
                        15 16 17 18 19 20
                    /end IF_DATA
                /end FRAME
            /end MODULE
        /end PROJECT
        """, id='fully defined node'),))
def test_if_data_memory_layout_node(a2l_string):
    p = Parser(a2l_string)
    assert p.ast.project.module[0].if_data.if_data_module[0] == 0
    assert p.ast.project.module[0].mod_par.memory_layout[0].if_data.if_data_memory_layout[0] == [0]
    assert p.ast.project.module[0].mod_par.memory_segment[0].if_data.if_data_memory_segment[0] == [1, 2]
    assert p.ast.project.module[0].characteristic[0].if_data.if_data_characteristic[0] == [3, 4, 5]
    assert p.ast.project.module[0].axis_pts[0].if_data.if_data_axis_pts[0] == [6, 7, 8, 9]
    assert p.ast.project.module[0].measurement[0].if_data.if_data_measurement[0] == [10, 11, 12, 13, 14]
    assert p.ast.project.module[0].frame.if_data.if_data_frame[0] == [15, 16, 17, 18, 19, 20]


@pytest.mark.parametrize('a2ml_string', a2ml_strings)
@pytest.mark.parametrize('a2l_string', (pytest.param("""
        /begin IF_DATA XCP
            /begin PROTOCOL_LAYER
                1
                2
                3
                4
                5
                6
                7
                8
                9
                10
                BYTE_ORDER_MSB_LAST
                ADDRESS_GRANULARITY_BYTE
                OPTIONAL_CMD GET_COMM_MODE_INFO
                OPTIONAL_CMD GET_ID
                COMMUNICATION_MODE_SUPPORTED BLOCK
                    SLAVE
                    MASTER 11 12
                INTERLEAVED 13
                SEED_AND_KEY_EXTERNAL_FUNCTION seed_and_key_external_function
            /end PROTOCOL_LAYER
        /end IF_DATA
        """, id='fully defined node'),))
def test_a2ml_protocol_layer_node(a2ml_string, a2l_string):
    p = Parser(generate_a2l_string(a2ml_string=a2ml_string, if_data_string=a2l_string))

    def node(): return p.ast.project.module[0].if_data

    assert node().XCP.PROTOCOL_LAYER[0] == 1
    assert node().XCP.PROTOCOL_LAYER[1] == 2
    assert node().XCP.PROTOCOL_LAYER[2] == 3
    assert node().XCP.PROTOCOL_LAYER[3] == 4
    assert node().XCP.PROTOCOL_LAYER[4] == 5
    assert node().XCP.PROTOCOL_LAYER[5] == 6
    assert node().XCP.PROTOCOL_LAYER[6] == 7
    assert node().XCP.PROTOCOL_LAYER[7] == 8
    assert node().XCP.PROTOCOL_LAYER[8] == 9
    assert node().XCP.PROTOCOL_LAYER[9] == 10
    assert node().XCP.PROTOCOL_LAYER[10] == 'BYTE_ORDER_MSB_LAST'
    assert node().XCP.PROTOCOL_LAYER[11] == 'ADDRESS_GRANULARITY_BYTE'
    assert node().XCP.PROTOCOL_LAYER.OPTIONAL_CMD == ['GET_COMM_MODE_INFO', 'GET_ID']
    assert node().XCP.PROTOCOL_LAYER.COMMUNICATION_MODE_SUPPORTED.BLOCK.SLAVE is True
    assert node().XCP.PROTOCOL_LAYER.COMMUNICATION_MODE_SUPPORTED.BLOCK.MASTER[0] == 11
    assert node().XCP.PROTOCOL_LAYER.COMMUNICATION_MODE_SUPPORTED.BLOCK.MASTER[1] == 12
    assert node().XCP.PROTOCOL_LAYER.COMMUNICATION_MODE_SUPPORTED.INTERLEAVED == 13
    assert node().XCP.PROTOCOL_LAYER.SEED_AND_KEY_EXTERNAL_FUNCTION == 'seed_and_key_external_function'
    assert node().XCP.SEGMENT is None
    assert node().XCP.DAQ is None
    assert node().XCP.PAG is None
    assert node().XCP.PGM is None
    assert node().XCP.DAQ_EVENT is None
    assert node().XCP.XCP_ON_CAN is None
    assert node().XCP.XCP_ON_SxI is None
    assert node().XCP.XCP_ON_TCP_IP is None
    assert node().XCP.XCP_ON_UDP_IP is None
    assert node().XCP.XCP_ON_USB is None


@pytest.mark.parametrize('a2ml_string', a2ml_strings)
@pytest.mark.parametrize('a2l_string', (pytest.param("""
        /begin IF_DATA XCP
            /begin SEGMENT
                1
                2
                3
                4
                5
                /begin CHECKSUM
                    XCP_USER_DEFINED
                    MAX_BLOCK_SIZE 6
                    EXTERNAL_FUNCTION external_function
                /end CHECKSUM
                /begin PAGE
                    7
                    ECU_ACCESS_NOT_ALLOWED
                    XCP_READ_ACCESS_NOT_ALLOWED
                    XCP_WRITE_ACCESS_NOT_ALLOWED
                    INIT_SEGMENT 8
                /end PAGE
                /begin PAGE
                    9
                    ECU_ACCESS_WITHOUT_XCP_ONLY
                    XCP_READ_ACCESS_WITHOUT_ECU_ONLY
                    XCP_WRITE_ACCESS_WITHOUT_ECU_ONLY
                    INIT_SEGMENT 10
                /end PAGE
                /begin ADDRESS_MAPPING
                    11
                    12
                    13
                /end ADDRESS_MAPPING
                /begin ADDRESS_MAPPING
                    14
                    15
                    16
                /end ADDRESS_MAPPING
                PGM_VERIFY 17
            /end SEGMENT
        /end IF_DATA
        """, id='fully defined node'),))
def test_a2ml_segment_node(a2ml_string, a2l_string):
    p = Parser(generate_a2l_string(a2ml_string=a2ml_string, if_data_string=a2l_string))

    def node(): return p.ast.project.module[0].if_data

    assert node().XCP.PROTOCOL_LAYER is None
    assert node().XCP.SEGMENT[0] == 1
    assert node().XCP.SEGMENT[1] == 2
    assert node().XCP.SEGMENT[2] == 3
    assert node().XCP.SEGMENT[3] == 4
    assert node().XCP.SEGMENT[4] == 5
    assert node().XCP.SEGMENT.CHECKSUM[0] == 'XCP_USER_DEFINED'
    assert node().XCP.SEGMENT.CHECKSUM.MAX_BLOCK_SIZE == 6
    assert node().XCP.SEGMENT.CHECKSUM.EXTERNAL_FUNCTION == 'external_function'
    assert node().XCP.SEGMENT.PAGE[0][0] == 7
    assert node().XCP.SEGMENT.PAGE[0][1] == 'ECU_ACCESS_NOT_ALLOWED'
    assert node().XCP.SEGMENT.PAGE[0][2] == 'XCP_READ_ACCESS_NOT_ALLOWED'
    assert node().XCP.SEGMENT.PAGE[0][3] == 'XCP_WRITE_ACCESS_NOT_ALLOWED'
    assert node().XCP.SEGMENT.PAGE[0].INIT_SEGMENT == 8
    assert node().XCP.SEGMENT.PAGE[1][0] == 9
    assert node().XCP.SEGMENT.PAGE[1][1] == 'ECU_ACCESS_WITHOUT_XCP_ONLY'
    assert node().XCP.SEGMENT.PAGE[1][2] == 'XCP_READ_ACCESS_WITHOUT_ECU_ONLY'
    assert node().XCP.SEGMENT.PAGE[1][3] == 'XCP_WRITE_ACCESS_WITHOUT_ECU_ONLY'
    assert node().XCP.SEGMENT.PAGE[1].INIT_SEGMENT == 10
    assert node().XCP.SEGMENT.ADDRESS_MAPPING[0][0] == 11
    assert node().XCP.SEGMENT.ADDRESS_MAPPING[0][1] == 12
    assert node().XCP.SEGMENT.ADDRESS_MAPPING[0][2] == 13
    assert node().XCP.SEGMENT.ADDRESS_MAPPING[1][0] == 14
    assert node().XCP.SEGMENT.ADDRESS_MAPPING[1][1] == 15
    assert node().XCP.SEGMENT.ADDRESS_MAPPING[1][2] == 16
    assert node().XCP.SEGMENT.PGM_VERIFY == 17
    assert node().XCP.DAQ is None
    assert node().XCP.PAG is None
    assert node().XCP.PGM is None
    assert node().XCP.DAQ_EVENT is None
    assert node().XCP.XCP_ON_CAN is None
    assert node().XCP.XCP_ON_SxI is None
    assert node().XCP.XCP_ON_TCP_IP is None
    assert node().XCP.XCP_ON_UDP_IP is None
    assert node().XCP.XCP_ON_USB is None


@pytest.mark.parametrize('a2ml_string', a2ml_strings)
@pytest.mark.parametrize('a2l_string', (pytest.param("""
        /begin IF_DATA XCP
            /begin DAQ
                STATIC
                1
                2
                3
                OPTIMISATION_TYPE_DEFAULT
                ADDRESS_EXTENSION_FREE
                IDENTIFICATION_FIELD_TYPE_ABSOLUTE
                GRANULARITY_ODT_ENTRY_SIZE_DAQ_BYTE
                4
                NO_OVERLOAD_INDICATION
                PRESCALER_SUPPORTED
                RESUME_SUPPORTED
                /begin STIM
                    GRANULARITY_ODT_ENTRY_SIZE_STIM_BYTE
                    5
                    BIT_STIM_SUPPORTED
                /end STIM
                /begin TIMESTAMP_SUPPORTED
                    6
                    NO_TIME_STAMP
                    UNIT_1NS
                    TIMESTAMP_FIXED
                /end TIMESTAMP_SUPPORTED
                PID_OFF_SUPPORTED
                /begin DAQ_LIST
                    7
                    DAQ_LIST_TYPE DAQ
                    MAX_ODT 8
                    MAX_ODT_ENTRIES 9
                    FIRST_PID 10
                    EVENT_FIXED 11
                    /begin PREDEFINED
                        /begin ODT
                            12
                            ODT_ENTRY 13 14 15 16 17
                            ODT_ENTRY 18 19 20 21 22
                        /end ODT
                        /begin ODT
                            23
                            ODT_ENTRY 24 25 26 27 28
                            ODT_ENTRY 29 30 31 32 33
                        /end ODT
                    /end PREDEFINED
                /end DAQ_LIST
                /begin DAQ_LIST
                    34
                    DAQ_LIST_TYPE STIM
                    MAX_ODT 35
                    MAX_ODT_ENTRIES 36
                    FIRST_PID 37
                    EVENT_FIXED 38
                    /begin PREDEFINED
                        /begin ODT
                            39
                            ODT_ENTRY 40 41 42 43 44
                            ODT_ENTRY 45 46 47 48 49
                        /end ODT
                        /begin ODT
                            50
                            ODT_ENTRY 51 52 53 54 55
                            ODT_ENTRY 56 57 58 59 60
                        /end ODT
                    /end PREDEFINED
                /end DAQ_LIST
                /begin EVENT
                    s1
                    s2
                    61
                    DAQ
                    62
                    63
                    64
                    65
                /end EVENT
                /begin EVENT
                    s3
                    s4
                    66
                    STIM
                    67
                    68
                    69
                    70
                /end EVENT
            /end DAQ
        /end IF_DATA
        """, id='fully defined node'),))
def test_a2ml_daq_node(a2ml_string, a2l_string):
    p = Parser(generate_a2l_string(a2ml_string=a2ml_string, if_data_string=a2l_string))

    def node(): return p.ast.project.module[0].if_data

    assert node().XCP.PROTOCOL_LAYER is None
    assert node().XCP.SEGMENT is None
    assert node().XCP.DAQ[0] == 'STATIC'
    assert node().XCP.DAQ[1] == 1
    assert node().XCP.DAQ[2] == 2
    assert node().XCP.DAQ[3] == 3
    assert node().XCP.DAQ[4] == 'OPTIMISATION_TYPE_DEFAULT'
    assert node().XCP.DAQ[5] == 'ADDRESS_EXTENSION_FREE'
    assert node().XCP.DAQ[6] == 'IDENTIFICATION_FIELD_TYPE_ABSOLUTE'
    assert node().XCP.DAQ[7] == 'GRANULARITY_ODT_ENTRY_SIZE_DAQ_BYTE'
    assert node().XCP.DAQ[8] == 4
    assert node().XCP.DAQ[9] == 'NO_OVERLOAD_INDICATION'
    assert node().XCP.DAQ.PRESCALER_SUPPORTED is True
    assert node().XCP.DAQ.RESUME_SUPPORTED is True
    assert node().XCP.DAQ.STIM[0] == 'GRANULARITY_ODT_ENTRY_SIZE_STIM_BYTE'
    assert node().XCP.DAQ.STIM[1] == 5
    assert node().XCP.DAQ.STIM.BIT_STIM_SUPPORTED is True
    assert node().XCP.DAQ.TIMESTAMP_SUPPORTED[0] == 6
    assert node().XCP.DAQ.TIMESTAMP_SUPPORTED[1] == 'NO_TIME_STAMP'
    assert node().XCP.DAQ.TIMESTAMP_SUPPORTED[2] == 'UNIT_1NS'
    assert node().XCP.DAQ.TIMESTAMP_SUPPORTED.TIMESTAMP_FIXED is True
    assert node().XCP.DAQ.DAQ_LIST[0][0] == 7
    assert node().XCP.DAQ.DAQ_LIST[0].DAQ_LIST_TYPE == 'DAQ'
    assert node().XCP.DAQ.DAQ_LIST[0].MAX_ODT == 8
    assert node().XCP.DAQ.DAQ_LIST[0].MAX_ODT_ENTRIES == 9
    assert node().XCP.DAQ.DAQ_LIST[0].FIRST_PID == 10
    assert node().XCP.DAQ.DAQ_LIST[0].EVENT_FIXED == 11
    assert node().XCP.DAQ.DAQ_LIST[0].PREDEFINED.ODT[0][0] == 12
    assert node().XCP.DAQ.DAQ_LIST[0].PREDEFINED.ODT[0].ODT_ENTRY[0][0] == 13
    assert node().XCP.DAQ.DAQ_LIST[0].PREDEFINED.ODT[0].ODT_ENTRY[0][1] == 14
    assert node().XCP.DAQ.DAQ_LIST[0].PREDEFINED.ODT[0].ODT_ENTRY[0][2] == 15
    assert node().XCP.DAQ.DAQ_LIST[0].PREDEFINED.ODT[0].ODT_ENTRY[0][3] == 16
    assert node().XCP.DAQ.DAQ_LIST[0].PREDEFINED.ODT[0].ODT_ENTRY[0][4] == 17
    assert node().XCP.DAQ.DAQ_LIST[0].PREDEFINED.ODT[0].ODT_ENTRY[1][0] == 18
    assert node().XCP.DAQ.DAQ_LIST[0].PREDEFINED.ODT[0].ODT_ENTRY[1][1] == 19
    assert node().XCP.DAQ.DAQ_LIST[0].PREDEFINED.ODT[0].ODT_ENTRY[1][2] == 20
    assert node().XCP.DAQ.DAQ_LIST[0].PREDEFINED.ODT[0].ODT_ENTRY[1][3] == 21
    assert node().XCP.DAQ.DAQ_LIST[0].PREDEFINED.ODT[0].ODT_ENTRY[1][4] == 22
    assert node().XCP.DAQ.DAQ_LIST[0].PREDEFINED.ODT[1][0] == 23
    assert node().XCP.DAQ.DAQ_LIST[0].PREDEFINED.ODT[1].ODT_ENTRY[0][0] == 24
    assert node().XCP.DAQ.DAQ_LIST[0].PREDEFINED.ODT[1].ODT_ENTRY[0][1] == 25
    assert node().XCP.DAQ.DAQ_LIST[0].PREDEFINED.ODT[1].ODT_ENTRY[0][2] == 26
    assert node().XCP.DAQ.DAQ_LIST[0].PREDEFINED.ODT[1].ODT_ENTRY[0][3] == 27
    assert node().XCP.DAQ.DAQ_LIST[0].PREDEFINED.ODT[1].ODT_ENTRY[0][4] == 28
    assert node().XCP.DAQ.DAQ_LIST[0].PREDEFINED.ODT[1].ODT_ENTRY[1][0] == 29
    assert node().XCP.DAQ.DAQ_LIST[0].PREDEFINED.ODT[1].ODT_ENTRY[1][1] == 30
    assert node().XCP.DAQ.DAQ_LIST[0].PREDEFINED.ODT[1].ODT_ENTRY[1][2] == 31
    assert node().XCP.DAQ.DAQ_LIST[0].PREDEFINED.ODT[1].ODT_ENTRY[1][3] == 32
    assert node().XCP.DAQ.DAQ_LIST[0].PREDEFINED.ODT[1].ODT_ENTRY[1][4] == 33
    assert node().XCP.DAQ.DAQ_LIST[1][0] == 34
    assert node().XCP.DAQ.DAQ_LIST[1].DAQ_LIST_TYPE == 'STIM'
    assert node().XCP.DAQ.DAQ_LIST[1].MAX_ODT == 35
    assert node().XCP.DAQ.DAQ_LIST[1].MAX_ODT_ENTRIES == 36
    assert node().XCP.DAQ.DAQ_LIST[1].FIRST_PID == 37
    assert node().XCP.DAQ.DAQ_LIST[1].EVENT_FIXED == 38
    assert node().XCP.DAQ.DAQ_LIST[1].PREDEFINED.ODT[0][0] == 39
    assert node().XCP.DAQ.DAQ_LIST[1].PREDEFINED.ODT[0].ODT_ENTRY[0][0] == 40
    assert node().XCP.DAQ.DAQ_LIST[1].PREDEFINED.ODT[0].ODT_ENTRY[0][1] == 41
    assert node().XCP.DAQ.DAQ_LIST[1].PREDEFINED.ODT[0].ODT_ENTRY[0][2] == 42
    assert node().XCP.DAQ.DAQ_LIST[1].PREDEFINED.ODT[0].ODT_ENTRY[0][3] == 43
    assert node().XCP.DAQ.DAQ_LIST[1].PREDEFINED.ODT[0].ODT_ENTRY[0][4] == 44
    assert node().XCP.DAQ.DAQ_LIST[1].PREDEFINED.ODT[0].ODT_ENTRY[1][0] == 45
    assert node().XCP.DAQ.DAQ_LIST[1].PREDEFINED.ODT[0].ODT_ENTRY[1][1] == 46
    assert node().XCP.DAQ.DAQ_LIST[1].PREDEFINED.ODT[0].ODT_ENTRY[1][2] == 47
    assert node().XCP.DAQ.DAQ_LIST[1].PREDEFINED.ODT[0].ODT_ENTRY[1][3] == 48
    assert node().XCP.DAQ.DAQ_LIST[1].PREDEFINED.ODT[0].ODT_ENTRY[1][4] == 49
    assert node().XCP.DAQ.DAQ_LIST[1].PREDEFINED.ODT[1][0] == 50
    assert node().XCP.DAQ.DAQ_LIST[1].PREDEFINED.ODT[1].ODT_ENTRY[0][0] == 51
    assert node().XCP.DAQ.DAQ_LIST[1].PREDEFINED.ODT[1].ODT_ENTRY[0][1] == 52
    assert node().XCP.DAQ.DAQ_LIST[1].PREDEFINED.ODT[1].ODT_ENTRY[0][2] == 53
    assert node().XCP.DAQ.DAQ_LIST[1].PREDEFINED.ODT[1].ODT_ENTRY[0][3] == 54
    assert node().XCP.DAQ.DAQ_LIST[1].PREDEFINED.ODT[1].ODT_ENTRY[0][4] == 55
    assert node().XCP.DAQ.DAQ_LIST[1].PREDEFINED.ODT[1].ODT_ENTRY[1][0] == 56
    assert node().XCP.DAQ.DAQ_LIST[1].PREDEFINED.ODT[1].ODT_ENTRY[1][1] == 57
    assert node().XCP.DAQ.DAQ_LIST[1].PREDEFINED.ODT[1].ODT_ENTRY[1][2] == 58
    assert node().XCP.DAQ.DAQ_LIST[1].PREDEFINED.ODT[1].ODT_ENTRY[1][3] == 59
    assert node().XCP.DAQ.DAQ_LIST[1].PREDEFINED.ODT[1].ODT_ENTRY[1][4] == 60
    assert node().XCP.DAQ.EVENT[0][0] == 's1'
    assert node().XCP.DAQ.EVENT[0][1] == 's2'
    assert node().XCP.DAQ.EVENT[0][2] == 61
    assert node().XCP.DAQ.EVENT[0][3] == 'DAQ'
    assert node().XCP.DAQ.EVENT[0][4] == 62
    assert node().XCP.DAQ.EVENT[0][5] == 63
    assert node().XCP.DAQ.EVENT[0][6] == 64
    assert node().XCP.DAQ.EVENT[0][7] == 65
    assert node().XCP.DAQ.EVENT[1][0] == 's3'
    assert node().XCP.DAQ.EVENT[1][1] == 's4'
    assert node().XCP.DAQ.EVENT[1][2] == 66
    assert node().XCP.DAQ.EVENT[1][3] == 'STIM'
    assert node().XCP.DAQ.EVENT[1][4] == 67
    assert node().XCP.DAQ.EVENT[1][5] == 68
    assert node().XCP.DAQ.EVENT[1][6] == 69
    assert node().XCP.DAQ.EVENT[1][7] == 70
    assert node().XCP.PAG is None
    assert node().XCP.PGM is None
    assert node().XCP.DAQ_EVENT is None
    assert node().XCP.XCP_ON_CAN is None
    assert node().XCP.XCP_ON_SxI is None
    assert node().XCP.XCP_ON_TCP_IP is None
    assert node().XCP.XCP_ON_UDP_IP is None
    assert node().XCP.XCP_ON_USB is None


@pytest.mark.parametrize('a2ml_string', a2ml_strings)
@pytest.mark.parametrize('a2l_string', (pytest.param("""
        /begin IF_DATA XCP
            /begin PAG
                1
                FREEZE_SUPPORTED
            /end PAG
        /end IF_DATA
        """, id='fully defined node'),))
def test_a2ml_pag_node(a2ml_string, a2l_string):
    p = Parser(generate_a2l_string(a2ml_string=a2ml_string, if_data_string=a2l_string))

    def node(): return p.ast.project.module[0].if_data

    assert node().XCP.PROTOCOL_LAYER is None
    assert node().XCP.SEGMENT is None
    assert node().XCP.DAQ is None
    assert node().XCP.PAG[0] == 1
    assert node().XCP.PAG.FREEZE_SUPPORTED is True
    assert node().XCP.PGM is None
    assert node().XCP.DAQ_EVENT is None
    assert node().XCP.XCP_ON_CAN is None
    assert node().XCP.XCP_ON_SxI is None
    assert node().XCP.XCP_ON_TCP_IP is None
    assert node().XCP.XCP_ON_UDP_IP is None
    assert node().XCP.XCP_ON_USB is None


@pytest.mark.parametrize('a2ml_string', a2ml_strings)
@pytest.mark.parametrize('a2l_string', (pytest.param("""
        /begin IF_DATA XCP
            /begin PGM
                PGM_MODE_ABSOLUTE
                1
                2
                /begin SECTOR
                    s1
                    3
                    4
                    5
                    6
                    7
                    8
                /end SECTOR
                /begin SECTOR
                    s2
                    9
                    10
                    11
                    12
                    13
                    14
                /end SECTOR
                COMMUNICATION_MODE_SUPPORTED
                    BLOCK
                        SLAVE
                        MASTER
                            15
                            16
                    INTERLEAVED 17
            /end PGM
        /end IF_DATA
        """, id='fully defined node'),))
def test_a2ml_pgm_node(a2ml_string, a2l_string):
    p = Parser(generate_a2l_string(a2ml_string=a2ml_string, if_data_string=a2l_string))

    def node(): return p.ast.project.module[0].if_data

    assert node().XCP.PROTOCOL_LAYER is None
    assert node().XCP.SEGMENT is None
    assert node().XCP.DAQ is None
    assert node().XCP.PAG is None
    assert node().XCP.PGM[0] == 'PGM_MODE_ABSOLUTE'
    assert node().XCP.PGM[1] == 1
    assert node().XCP.PGM[2] == 2
    assert node().XCP.PGM.SECTOR[0][0] == 's1'
    assert node().XCP.PGM.SECTOR[0][1] == 3
    assert node().XCP.PGM.SECTOR[0][2] == 4
    assert node().XCP.PGM.SECTOR[0][3] == 5
    assert node().XCP.PGM.SECTOR[0][4] == 6
    assert node().XCP.PGM.SECTOR[0][5] == 7
    assert node().XCP.PGM.SECTOR[0][6] == 8
    assert node().XCP.PGM.SECTOR[1][0] == 's2'
    assert node().XCP.PGM.SECTOR[1][1] == 9
    assert node().XCP.PGM.SECTOR[1][2] == 10
    assert node().XCP.PGM.SECTOR[1][3] == 11
    assert node().XCP.PGM.SECTOR[1][4] == 12
    assert node().XCP.PGM.SECTOR[1][5] == 13
    assert node().XCP.PGM.SECTOR[1][6] == 14
    assert node().XCP.PGM.COMMUNICATION_MODE_SUPPORTED.BLOCK.MASTER[0] == 15
    assert node().XCP.PGM.COMMUNICATION_MODE_SUPPORTED.BLOCK.MASTER[1] == 16
    assert node().XCP.PGM.COMMUNICATION_MODE_SUPPORTED.BLOCK.SLAVE is True
    assert node().XCP.PGM.COMMUNICATION_MODE_SUPPORTED.INTERLEAVED == 17
    assert node().XCP.DAQ_EVENT is None
    assert node().XCP.XCP_ON_CAN is None
    assert node().XCP.XCP_ON_SxI is None
    assert node().XCP.XCP_ON_TCP_IP is None
    assert node().XCP.XCP_ON_UDP_IP is None
    assert node().XCP.XCP_ON_USB is None


@pytest.mark.parametrize('a2ml_string', a2ml_strings)
@pytest.mark.parametrize('a2l_string', (pytest.param("""
        /begin IF_DATA XCP
            /begin DAQ_EVENT
                /begin FIXED_EVENT_LIST
                    EVENT 1
                    EVENT 2
                /end FIXED_EVENT_LIST
                /begin VARIABLE
                    /begin AVAILABLE_EVENT_LIST
                        EVENT 3
                        EVENT 4
                    /end AVAILABLE_EVENT_LIST
                    /begin DEFAULT_EVENT_LIST
                        EVENT 5
                        EVENT 6
                    /end DEFAULT_EVENT_LIST
                /end VARIABLE
            /end DAQ_EVENT
        /end IF_DATA
        """, id='fully defined node'),))
def test_a2ml_daq_event_node(a2ml_string, a2l_string):
    p = Parser(generate_a2l_string(a2ml_string=a2ml_string, if_data_string=a2l_string))

    def node(): return p.ast.project.module[0].if_data

    assert node().XCP.PROTOCOL_LAYER is None
    assert node().XCP.SEGMENT is None
    assert node().XCP.DAQ is None
    assert node().XCP.PAG is None
    assert node().XCP.PGM is None
    assert node().XCP.DAQ_EVENT.FIXED_EVENT_LIST.EVENT[0] == 1
    assert node().XCP.DAQ_EVENT.FIXED_EVENT_LIST.EVENT[1] == 2
    assert node().XCP.DAQ_EVENT.VARIABLE.AVAILABLE_EVENT_LIST.EVENT[0] == 3
    assert node().XCP.DAQ_EVENT.VARIABLE.AVAILABLE_EVENT_LIST.EVENT[1] == 4
    assert node().XCP.DAQ_EVENT.VARIABLE.DEFAULT_EVENT_LIST.EVENT[0] == 5
    assert node().XCP.DAQ_EVENT.VARIABLE.DEFAULT_EVENT_LIST.EVENT[1] == 6
    assert node().XCP.XCP_ON_CAN is None
    assert node().XCP.XCP_ON_SxI is None
    assert node().XCP.XCP_ON_TCP_IP is None
    assert node().XCP.XCP_ON_UDP_IP is None
    assert node().XCP.XCP_ON_USB is None


@pytest.mark.parametrize('a2ml_string', a2ml_strings)
@pytest.mark.parametrize('a2l_string', (pytest.param("""
        /begin IF_DATA XCP
            /begin XCP_ON_CAN
                1
                CAN_ID_BROADCAST 2
                CAN_ID_MASTER 3
                CAN_ID_SLAVE 4
                BAUDRATE 5
                SAMPLE_POINT 6
                SAMPLE_RATE SINGLE
                BTL_CYCLES 7
                SJW 8
                SYNC_EDGE SINGLE
                MAX_DLC_REQUIRED
                /begin DAQ_LIST_CAN_ID
                    9
                    VARIABLE
                    FIXED 10
                /end DAQ_LIST_CAN_ID
                /begin DAQ_LIST_CAN_ID
                    11
                    VARIABLE
                    FIXED 12
                /end DAQ_LIST_CAN_ID
            /end XCP_ON_CAN
        /end IF_DATA
        """, id='fully defined node'),))
def test_a2ml_xcp_on_can_node(a2ml_string, a2l_string):
    p = Parser(generate_a2l_string(a2ml_string=a2ml_string, if_data_string=a2l_string))

    def node(): return p.ast.project.module[0].if_data

    assert node().XCP.PROTOCOL_LAYER is None
    assert node().XCP.SEGMENT is None
    assert node().XCP.DAQ is None
    assert node().XCP.PAG is None
    assert node().XCP.PGM is None
    assert node().XCP.DAQ_EVENT is None
    assert node().XCP.XCP_ON_CAN[0] == 1
    assert node().XCP.XCP_ON_CAN.CAN_ID_BROADCAST == 2
    assert node().XCP.XCP_ON_CAN.CAN_ID_MASTER == 3
    assert node().XCP.XCP_ON_CAN.CAN_ID_SLAVE == 4
    assert node().XCP.XCP_ON_CAN.BAUDRATE == 5
    assert node().XCP.XCP_ON_CAN.SAMPLE_POINT == 6
    assert node().XCP.XCP_ON_CAN.SAMPLE_RATE == 'SINGLE'
    assert node().XCP.XCP_ON_CAN.BTL_CYCLES == 7
    assert node().XCP.XCP_ON_CAN.SJW == 8
    assert node().XCP.XCP_ON_CAN.SYNC_EDGE == 'SINGLE'
    assert node().XCP.XCP_ON_CAN.MAX_DLC_REQUIRED is True
    assert node().XCP.XCP_ON_CAN.DAQ_LIST_CAN_ID[0][0] == 9
    assert node().XCP.XCP_ON_CAN.DAQ_LIST_CAN_ID[0].VARIABLE is True
    assert node().XCP.XCP_ON_CAN.DAQ_LIST_CAN_ID[0].FIXED == 10
    assert node().XCP.XCP_ON_CAN.DAQ_LIST_CAN_ID[1][0] == 11
    assert node().XCP.XCP_ON_CAN.DAQ_LIST_CAN_ID[1].VARIABLE is True
    assert node().XCP.XCP_ON_CAN.DAQ_LIST_CAN_ID[1].FIXED == 12
    assert node().XCP.XCP_ON_SxI is None
    assert node().XCP.XCP_ON_TCP_IP is None
    assert node().XCP.XCP_ON_UDP_IP is None
    assert node().XCP.XCP_ON_USB is None


@pytest.mark.skip
@pytest.mark.parametrize('a2ml_string, a2l_string', (
        pytest.param(asap2_1_61, """
        /begin IF_DATA XCP
            /begin XCP_ON_SxI
            /end XCP_ON_SxI
        /end IF_DATA
        """, id='ASAP2 version 1.61'),
))
def test_a2ml_xcp_on_sxi_node(a2ml_string, a2l_string):
    p = Parser(generate_a2l_string(a2ml_string=a2ml_string, if_data_string=a2l_string))

    def node(): return p.ast.project.module[0].if_data

    assert node().XCP.PROTOCOL_LAYER is None
    assert node().XCP.SEGMENT is None
    assert node().XCP.DAQ is None
    assert node().XCP.PAG is None
    assert node().XCP.PGM is None
    assert node().XCP.DAQ_EVENT is None
    assert node().XCP.XCP_ON_CAN is None
    assert node().XCP.XCP_ON_SxI is None
    assert node().XCP.XCP_ON_TCP_IP is None
    assert node().XCP.XCP_ON_UDP_IP is None
    assert node().XCP.XCP_ON_USB is None


@pytest.mark.skip
@pytest.mark.parametrize('a2ml_string, a2l_string', (
        pytest.param(asap2_1_61, """
        /begin IF_DATA XCP
            /begin XCP_ON_TCP_IP
            /end XCP_ON_TCP_IP
        /end IF_DATA
        """, id='ASAP2 version 1.61'),
))
def test_a2ml_xcp_on_tcp_ip_node(a2ml_string, a2l_string):
    p = Parser(generate_a2l_string(a2ml_string=a2ml_string, if_data_string=a2l_string))

    def node(): return p.ast.project.module[0].if_data

    assert node().XCP.PROTOCOL_LAYER is None
    assert node().XCP.SEGMENT is None
    assert node().XCP.DAQ is None
    assert node().XCP.PAG is None
    assert node().XCP.PGM is None
    assert node().XCP.DAQ_EVENT is None
    assert node().XCP.XCP_ON_CAN is None
    assert node().XCP.XCP_ON_SxI is None
    assert node().XCP.XCP_ON_TCP_IP is None
    assert node().XCP.XCP_ON_UDP_IP is None
    assert node().XCP.XCP_ON_USB is None


@pytest.mark.skip
@pytest.mark.parametrize('a2ml_string, a2l_string', (
        pytest.param(asap2_1_61, """
        /begin IF_DATA XCP
            /begin XCP_ON_UDP_IP
            /end XCP_ON_UDP_IP
        /end IF_DATA
        """, id='ASAP2 version 1.61'),
))
def test_a2ml_xcp_on_udp_ip_node(a2ml_string, a2l_string):
    p = Parser(generate_a2l_string(a2ml_string=a2ml_string, if_data_string=a2l_string))

    def node(): return p.ast.project.module[0].if_data

    assert node().XCP.PROTOCOL_LAYER is None
    assert node().XCP.SEGMENT is None
    assert node().XCP.DAQ is None
    assert node().XCP.PAG is None
    assert node().XCP.PGM is None
    assert node().XCP.DAQ_EVENT is None
    assert node().XCP.XCP_ON_CAN is None
    assert node().XCP.XCP_ON_SxI is None
    assert node().XCP.XCP_ON_TCP_IP is None
    assert node().XCP.XCP_ON_UDP_IP is None
    assert node().XCP.XCP_ON_USB is None


@pytest.mark.skip
@pytest.mark.parametrize('a2ml_string, a2l_string', (
        pytest.param(asap2_1_61, """
        /begin IF_DATA XCP
            /begin XCP_ON_USB
            /end XCP_ON_USB
        /end IF_DATA
        """, id='ASAP2 version 1.61'),
))
def test_a2ml_xcp_on_usb_node(a2ml_string, a2l_string):
    p = Parser(generate_a2l_string(a2ml_string=a2ml_string, if_data_string=a2l_string))

    def node(): return p.ast.project.module[0].if_data

    assert node().XCP.PROTOCOL_LAYER is None
    assert node().XCP.SEGMENT is None
    assert node().XCP.DAQ is None
    assert node().XCP.PAG is None
    assert node().XCP.PGM is None
    assert node().XCP.DAQ_EVENT is None
    assert node().XCP.XCP_ON_CAN is None
    assert node().XCP.XCP_ON_SxI is None
    assert node().XCP.XCP_ON_TCP_IP is None
    assert node().XCP.XCP_ON_UDP_IP is None
    assert node().XCP.XCP_ON_USB is None
