"""
@project: parser
@file: parser_test.py
@author: Guillaume Sottas
@date: 06.04.2018
"""

import pytest

from pya2l.parser.grammar.parser import A2lFormatException
from pya2l.parser.grammar.parser import A2lParser as Parser
from pya2l.parser.grammar.node import A2lNode, ProtocolLayer, Segment, Daq, Pag, Pgm, DaqEvent


def test_invalid_node_property():
    class InvalidNode(A2lNode):
        __slots__ = 'invalid_property',

        def __init__(self):
            self.invalid_property = dict()
            super(InvalidNode, self).__init__(('invalid_property', None))

    with pytest.raises(AttributeError, message='invalid_property'):
        InvalidNode()


def test_invalid_node_slot_property():
    class InvalidNode(A2lNode):
        __slots__ = 'property_value'

        def __init__(self, property_value):
            self.property_value = property_value
            super(InvalidNode, self).__init__()

    with pytest.raises(ValueError, message='__slot__ attribute must be a list (maybe \',\' is missing at the end?).'):
        InvalidNode(1)


def test_node_equality_operator():
    class A(A2lNode):
        __slots__ = 'a',

    class B(A2lNode):
        __slots__ = 'b',

    assert A() != B()

    class C(A2lNode):
        __slots__ = 'a',

        def __init__(self, a):
            self.a = a

    assert C(0) != C(1)
    assert C(0) == C(0)


def test_string_empty():
    a2l_string = ''
    a2l = Parser(a2l_string)
    assert a2l.tree.a2ml_version is None
    assert a2l.tree.asap2_version is None
    assert a2l.tree.project is None


def test_string_c_comment():
    a2l_string = """
        /* comment */
    """
    Parser(a2l_string)


def test_string_cpp_comment():
    a2l_sting = """
        // comment
    """
    Parser(a2l_sting)


def test_a2ml_taggedunion():
    a2l_string = """
        /begin PROJECT project_name "project long indentifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin A2ML
                    taggedunion first_tagged_union_identifier;
                    taggedunion {};
                    taggedunion third_tagged_union_identifier {};
                /end A2ML
            /end MODULE
        /end PROJECT"""
    Parser(a2l_string)


def test_a2ml_taggedunion_member():
    a2l_string = """
        /begin PROJECT project_name "project long indentifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin A2ML
                    taggedunion {
                        "first_tag";
                        "second_tag" ulong;
                        block "third_tag" ulong;
                    };
                /end A2ML
            /end MODULE
        /end PROJECT"""
    Parser(a2l_string)


def test_a2ml_version():
    a2l_string = 'A2ML_VERSION 1'
    with pytest.raises(A2lFormatException):
        Parser(a2l_string)
    a2l_string = 'A2ML_VERSION 2 3'
    a2l = Parser(a2l_string)
    assert a2l.tree.a2ml_version.version_no == 2
    assert a2l.tree.a2ml_version.upgrade_no == 3


def test_lexer_numeric_token():
    a2l_string = 'A2ML_VERSION 2 3'
    a2l = Parser(a2l_string)
    assert a2l.tree.a2ml_version.version_no == 2
    assert a2l.tree.a2ml_version.upgrade_no == 3
    a2l_string = 'A2ML_VERSION 0x2 0x3'
    a2l = Parser(a2l_string)
    assert a2l.tree.a2ml_version.version_no == 2
    assert a2l.tree.a2ml_version.upgrade_no == 3
    a2l_string = 'A2ML_VERSION 2.0 3.0'
    a2l = Parser(a2l_string)
    assert a2l.tree.a2ml_version.version_no == 2
    assert a2l.tree.a2ml_version.upgrade_no == 3


def test_asap2_version():
    a2l_string = 'ASAP2_VERSION 1'
    with pytest.raises(A2lFormatException):
        Parser(a2l_string)
    a2l_string = 'ASAP2_VERSION 2 3'
    a2l = Parser(a2l_string)
    assert a2l.tree.asap2_version.version_no == 2
    assert a2l.tree.asap2_version.upgrade_no == 3


def test_project_empty():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.name == 'project_name'
    assert a2l.tree.project.long_identifier == 'project long identifier'


def test_project_header_without_version():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin HEADER "header comment"
                PROJECT_NO M4711Z1
            /end HEADER
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.header.project_no == 'M4711Z1'


def test_project_header_without_project_no():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin HEADER "header comment"
                VERSION "BG5.0815"
            /end HEADER
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.header.version == 'BG5.0815'


def test_project_header_node():
    a2l_string = """
        /begin PROJECT project_name "project long indentifier"
            /begin HEADER "header comment"
                PROJECT_NO M4711Z1
                VERSION "BG5.0815"
            /end HEADER
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.header.project_no == 'M4711Z1'
    assert a2l.tree.project.header.version == 'BG5.0815'


def test_project_with_single_module_node():
    a2l_string = """
        /begin PROJECT project_name "project long indentifier"
            /begin MODULE first_module_name "first module long identifier"
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].name == 'first_module_name'
    assert a2l.tree.project.module[0].long_identifier == 'first module long identifier'


def test_project_with_multiple_module_node():
    a2l_string = """
        /begin PROJECT project_name "project long indentifier"
            /begin MODULE first_module_name "first module long identifier"
            /end MODULE
            /begin MODULE second_module_name "second module long identifier"
            /end MODULE
            /begin MODULE third_module_name "third module long identifier"
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].name == 'first_module_name'
    assert a2l.tree.project.module[0].long_identifier == 'first module long identifier'
    assert a2l.tree.project.module[1].name == 'second_module_name'
    assert a2l.tree.project.module[1].long_identifier == 'second module long identifier'
    assert a2l.tree.project.module[2].name == 'third_module_name'
    assert a2l.tree.project.module[2].long_identifier == 'third module long identifier'


def test_module_a2ml_node():
    a2l_string = """
        /begin PROJECT project_name "project long indentifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin A2ML
                    struct first_struct;
                /end A2ML
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0], 'a2ml')


def test_module_mod_par_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_PAR "mod_par comment"
                /end MOD_PAR
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0], 'mod_par')
    assert a2l.tree.project.module[0].mod_par.comment == 'mod_par comment'


def test_module_mod_common_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_COMMON "mod_common comment"
                /end MOD_COMMON
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0], 'mod_common')


def test_module_if_data_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin IF_DATA first_if_data_name
                /end IF_DATA
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0],
                   'if_data_module')  # TODO: set attribute if_data instead of if_data_module.


def test_module_with_multiple_if_data_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin IF_DATA first_if_data_name
                /end IF_DATA
                /begin IF_DATA second_if_data_name
                /end IF_DATA
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert len(a2l.tree.project.module[0].if_data_module) == 2


def test_module_characteristic_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin CHARACTERISTIC 
                    first_characteristic_name 
                    "first characteristic long identifier" 
                    VALUE 
                    0 
                    DAMOS_SST 
                    0 
                    first_characteristic_conversion 
                    0 
                    0
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0], 'characteristic')


def test_module_with_multiple_characteristic_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin CHARACTERISTIC 
                    first_characteristic_name 
                    "first characteristic long identifier" 
                    VALUE 
                    0 
                    DAMOS_SST 
                    0 
                    first_characteristic_conversion 
                    0 
                    0
                /end CHARACTERISTIC
                /begin CHARACTERISTIC 
                    second_characteristic_name 
                    "second characteristic long identifier" 
                    VALUE 
                    0 
                    DAMOS_SST 
                    0 
                    second_characteristic_conversion 
                    0 
                    0
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].characteristic[0].name == 'first_characteristic_name'
    assert a2l.tree.project.module[0].characteristic[1].name == 'second_characteristic_name'


def test_module_axis_pts_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin AXIS_PTS 
                    first_axis_pts_name 
                    "first axis_pts long identifier" 
                    0 
                    first_axis_pts_input_quantity 
                    DAMOS_SST 
                    1 
                    first_axis_pts_conversion 
                    0 
                    0 
                    0
                /end AXIS_PTS
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0], 'axis_pts')


def test_module_with_multiple_axis_pts_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin AXIS_PTS 
                    first_axis_pts_name 
                    "first axis_pts long identifier" 
                    0 
                    first_axis_pts_input_quantity 
                    DAMOS_SST 
                    1 
                    first_axis_pts_conversion 
                    0 
                    0 
                    0
                /end AXIS_PTS
                /begin AXIS_PTS 
                    second_axis_pts_name 
                    "second axis_pts long identifier" 
                    0 
                    second_axis_pts_input_quantity 
                    DAMOS_SST 
                    1 
                    second_axis_pts_conversion 
                    0 
                    0 
                    0
                /end AXIS_PTS
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].axis_pts[0].name == 'first_axis_pts_name'
    assert a2l.tree.project.module[0].axis_pts[1].name == 'second_axis_pts_name'


def test_module_measurement_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT 
                    first_measurement_name 
                    "first measurement long identifier" 
                    UBYTE 
                    first_measurement_conversion 
                    0 
                    0 
                    0 
                    0
                /end MEASUREMENT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0], 'measurement')


def test_module_with_multiple_measurement_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT 
                    first_measurement_name 
                    "first measurement long identifier" 
                    UBYTE 
                    first_measurement_conversion 
                    0 
                    0 
                    0 
                    0
                /end MEASUREMENT
                /begin MEASUREMENT 
                    second_measurement_name 
                    "second measurement long identifier" 
                    UBYTE 
                    second_measurement_conversion 
                    0 
                    0 
                    0 
                    0
                /end MEASUREMENT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].measurement[0].name == 'first_measurement_name'
    assert a2l.tree.project.module[0].measurement[1].name == 'second_measurement_name'


def test_module_compu_method_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin COMPU_METHOD first_compu_method_name "first compu_method long identifier" TAB_INTP "%d" "-"
                /end COMPU_METHOD
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0], 'compu_method')


def test_module_with_multiple_compu_method_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin COMPU_METHOD first_compu_method_name "first compu_method long identifier" TAB_INTP "%d" "-"
                /end COMPU_METHOD
                /begin COMPU_METHOD second_compu_method_name "second compu_method long identifier" TAB_INTP "%d" "-"
                /end COMPU_METHOD
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].compu_method[0].name == 'first_compu_method_name'
    assert a2l.tree.project.module[0].compu_method[1].name == 'second_compu_method_name'


def test_module_compu_tab_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin COMPU_TAB first_compu_tab_name "first compu_tab long identifier" TAB_INTP 1 1 1
                /end COMPU_TAB
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0], 'compu_tab')


def test_module_with_multiple_compu_tab_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin COMPU_TAB first_compu_tab_name "first compu_tab long identifier" TAB_INTP 1 1 1
                /end COMPU_TAB
                /begin COMPU_TAB second_compu_tab_name "second compu_tab long identifier" TAB_INTP 1 1 1
                /end COMPU_TAB
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].compu_tab[0].name == 'first_compu_tab_name'
    assert a2l.tree.project.module[0].compu_tab[1].name == 'second_compu_tab_name'


def test_module_compu_vtab_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin COMPU_VTAB first_compu_vtab_name "first compu_vtab long identifier" TAB_VERB 1 0 "0"
                /end COMPU_VTAB
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0], 'compu_vtab')


def test_module_with_multiple_compu_vtab_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin COMPU_VTAB first_compu_vtab_name "first compu_vtab long identifier" TAB_VERB 1 0 "0"
                /end COMPU_VTAB
                /begin COMPU_VTAB second_compu_vtab_name "second compu_vtab long identifier" TAB_VERB 1 0 "0"
                /end COMPU_VTAB
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].compu_vtab[0].name == 'first_compu_vtab_name'
    assert a2l.tree.project.module[0].compu_vtab[1].name == 'second_compu_vtab_name'


def test_module_compu_vtab_range_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin COMPU_VTAB_RANGE first_compu_vtab_range_name "first compu_vtab_range long identifier" 1 0 0 "0"
                /end COMPU_VTAB_RANGE
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0], 'compu_vtab_range')


def test_module_with_multiple_compu_vtab_range_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin COMPU_VTAB_RANGE first_compu_vtab_range_name "first compu_vtab_range long identifier" 1 0 0 "0"
                /end COMPU_VTAB_RANGE
                /begin COMPU_VTAB_RANGE second_compu_vtab_range_name "second compu_vtab_range long identifier" 1 0 0 "0"
                /end COMPU_VTAB_RANGE
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].compu_vtab_range[0].name == 'first_compu_vtab_range_name'
    assert a2l.tree.project.module[0].compu_vtab_range[1].name == 'second_compu_vtab_range_name'


def test_module_function_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin FUNCTION first_function_name "first function long identifier"
                /end FUNCTION
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0], 'function')


def test_module_with_multiple_function_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin FUNCTION first_function_name "first function long identifier"
                /end FUNCTION
                /begin FUNCTION second_function_name "second function long identifier"
                /end FUNCTION
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].function[0].name == 'first_function_name'
    assert a2l.tree.project.module[0].function[1].name == 'second_function_name'


def test_module_group_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin GROUP first_group_name "first group long identifier"
                /end GROUP
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0], 'group')


def test_module_with_multiple_group_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin GROUP first_group_name "first group long identifier"
                /end GROUP
                /begin GROUP second_group_name "second group long identifier"
                /end GROUP
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].group[0].group_name == 'first_group_name'
    assert a2l.tree.project.module[0].group[1].group_name == 'second_group_name'


def test_module_record_layout_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT first_record_layout_name
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0], 'record_layout')


def test_module_with_multiple_record_layout_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT first_record_layout_name
                /end RECORD_LAYOUT
                /begin RECORD_LAYOUT second_record_layout_name
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].record_layout[0].name == 'first_record_layout_name'
    assert a2l.tree.project.module[0].record_layout[1].name == 'second_record_layout_name'


def test_module_variant_coding_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin VARIANT_CODING
                /end VARIANT_CODING
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0], 'variant_coding')


def test_module_frame_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin FRAME frame_name "frame long identifier" 0 0
                /end FRAME
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0], 'frame')
    assert a2l.tree.project.module[0].frame.name == 'frame_name'


def test_module_user_rights_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin USER_RIGHTS first_user_rights
                /end USER_RIGHTS
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0], 'user_rights')


def test_module_with_multiple_user_rights_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin USER_RIGHTS first_user_rights_user_level_id
                /end USER_RIGHTS
                /begin USER_RIGHTS second_user_rights_user_level_id
                /end USER_RIGHTS
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].user_rights[0].user_level_id == 'first_user_rights_user_level_id'
    assert a2l.tree.project.module[0].user_rights[1].user_level_id == 'second_user_rights_user_level_id'


def test_module_unit_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin UNIT first_unit "first unit long identifier" "-" DERIVED
                /end UNIT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0], 'unit')


def test_module_with_multiple_unit_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin UNIT first_unit_name "first unit long identifier" "-" DERIVED
                /end UNIT
                /begin UNIT second_unit_name "second unit long identifier" "-" DERIVED
                /end UNIT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].unit[0].name == 'first_unit_name'
    assert a2l.tree.project.module[0].unit[1].name == 'second_unit_name'


def test_module_if_data_source_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin IF_DATA if_data_module_name
                    /begin SOURCE first_source_name 0 0
                    /end SOURCE
                /end IF_DATA
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].if_data_module[0], 'source')
    assert a2l.tree.project.module[0].if_data_module[0].source[0].name == 'first_source_name'


def test_module_if_data_raster_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin IF_DATA if_data_module_name
                    /begin RASTER "raster name" "raster short name" 0 0 0
                    /end RASTER
                /end IF_DATA
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].if_data_module[0], 'raster')
    assert a2l.tree.project.module[0].if_data_module[0].raster[0].raster_name == 'raster name'


def test_module_if_data_event_group_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin IF_DATA if_data_module_name
                    /begin EVENT_GROUP "raster group name" "raster group short name" 0 1 2
                    /end EVENT_GROUP
                /end IF_DATA
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].if_data_module[0], 'event_group')
    assert a2l.tree.project.module[0].if_data_module[0].event_group[0].raster_grp_name == 'raster group name'


def test_module_if_data_seed_key_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin IF_DATA if_data_module_name
                    /begin SEED_KEY "cal_dll_name.dll" "daq_dll_name.dll" "pgm_dll_name.dll"
                    /end SEED_KEY
                /end IF_DATA
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].if_data_module[0], 'seed_key')
    assert a2l.tree.project.module[0].if_data_module[0].seed_key.cal_dll == 'cal_dll_name.dll'


def test_module_if_data_checksum_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin IF_DATA if_data_module_name
                    /begin CHECKSUM "checksum_dll_name.dll"
                    /end CHECKSUM
                /end IF_DATA
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].if_data_module[0], 'checksum')
    assert a2l.tree.project.module[0].if_data_module[0].checksum.checksum_dll == 'checksum_dll_name.dll'


def test_module_if_data_tp_blob_tp_data_node():
    pytest.skip('missing clear specification...')


def test_module_if_data_xcp():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin IF_DATA XCP
                /end IF_DATA
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0], 'if_data_xcp')


def test_module_if_data_xcp_protocol_layer_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin IF_DATA XCP
                    /begin PROTOCOL_LAYER
                        0x0100 /* XCP protocol layer 1.0 */
        
                        10 /* T1 [ms] */
                        20 /* T2 [ms] */
                        30 /* T3 [ms] */
                        40 /* T4 [ms] */
                        50 /* T5 [ms] */
                        60 /* T6 [ms] */
                        70 /* T7 [ms] */
                
                        8 /* max CTO */
                        9 /* max DTO */
                    /end PROTOCOL_LAYER
                /end IF_DATA
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].if_data_xcp, 'protocol_layer')
    assert a2l.tree.project.module[0].if_data_xcp.protocol_layer[0].xcp_protocol_layer_version == 0x100
    assert a2l.tree.project.module[0].if_data_xcp.protocol_layer[0].t1 == 10
    assert a2l.tree.project.module[0].if_data_xcp.protocol_layer[0].t2 == 20
    assert a2l.tree.project.module[0].if_data_xcp.protocol_layer[0].t3 == 30
    assert a2l.tree.project.module[0].if_data_xcp.protocol_layer[0].t4 == 40
    assert a2l.tree.project.module[0].if_data_xcp.protocol_layer[0].t5 == 50
    assert a2l.tree.project.module[0].if_data_xcp.protocol_layer[0].t6 == 60
    assert a2l.tree.project.module[0].if_data_xcp.protocol_layer[0].t7 == 70
    assert a2l.tree.project.module[0].if_data_xcp.protocol_layer[0].max_cto == 8
    assert a2l.tree.project.module[0].if_data_xcp.protocol_layer[0].max_dto == 9


def test_module_if_data_xcp_with_multiple_protocol_layer_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin IF_DATA XCP
                    /begin PROTOCOL_LAYER
                        0x0100 /* XCP protocol layer 1.0 */
        
                        1 /* T1 [ms] */
                        1 /* T2 [ms] */
                        1 /* T3 [ms] */
                        1 /* T4 [ms] */
                        1 /* T5 [ms] */
                        1 /* T6 [ms] */
                        1 /* T7 [ms] */
                
                        1 /* max CTO */
                        1 /* max DTO */
                    /end PROTOCOL_LAYER
                    /begin PROTOCOL_LAYER
                        0x0100 /* XCP protocol layer 1.0 */
        
                        2 /* T1 [ms] */
                        2 /* T2 [ms] */
                        2 /* T3 [ms] */
                        2 /* T4 [ms] */
                        2 /* T5 [ms] */
                        2 /* T6 [ms] */
                        2 /* T7 [ms] */
                
                        2 /* max CTO */
                        2 /* max DTO */
                    /end PROTOCOL_LAYER
                /end IF_DATA
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].if_data_xcp.protocol_layer[0].t1 == 1
    assert a2l.tree.project.module[0].if_data_xcp.protocol_layer[1].t1 == 2


def test_module_if_data_xcp_daq_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin IF_DATA XCP
                    /begin DAQ
                        STATIC /* DAQ configuration type */
                        1 /* max DAQ */
                        2 /* max event channel */
                        3 /* min DAQ */
                        OPTIMISATION_TYPE_DEFAULT
                        ADDRESS_EXTENSION_FREE
                        IDENTIFICATION_FIELD_TYPE_ABSOLUTE
                        GRANULARITY_ODT_ENTRY_SIZE_DAQ_BYTE
                        4
                        NO_OVERLOAD_INDICATION
                        PRESCALER_SUPPORTED
                        RESUME_SUPPORTED
                    /end DAQ
                /end IF_DATA
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].if_data_xcp, 'daq')
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].daq_config_type == 'STATIC'
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].max_daq == 1
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].max_event_channel == 2
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].min_daq == 3
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].optimisation_type == 'OPTIMISATION_TYPE_DEFAULT'
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].address_extension == 'ADDRESS_EXTENSION_FREE'
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].identification_field_type == 'IDENTIFICATION_FIELD_TYPE_ABSOLUTE'
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].granularity_odt_entry == 'GRANULARITY_ODT_ENTRY_SIZE_DAQ_BYTE'
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].max_odt_entry_size_daq == 4
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].overload_indication == 'NO_OVERLOAD_INDICATION'
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].prescaler_supported == 'PRESCALER_SUPPORTED'
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].resume_supported == 'RESUME_SUPPORTED'


def test_module_if_data_xcp_pag_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin IF_DATA XCP
                    /begin PAG
                        1
                        FREEZE_SUPPORTED
                    /end PAG
                /end IF_DATA
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].if_data_xcp, 'pag')
    assert a2l.tree.project.module[0].if_data_xcp.pag[0].max_segments == 1
    assert a2l.tree.project.module[0].if_data_xcp.pag[0].freeze_supported == 'FREEZE_SUPPORTED'


def test_module_if_data_xcp_pgm_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin IF_DATA XCP
                    /begin PGM
                        PGM_MODE_ABSOLUTE_AND_FUNCTIONAL
                        1
                        2
                    /end PGM
                /end IF_DATA
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].if_data_xcp, 'pgm')
    assert a2l.tree.project.module[0].if_data_xcp.pgm[0].mode == 'PGM_MODE_ABSOLUTE_AND_FUNCTIONAL'
    assert a2l.tree.project.module[0].if_data_xcp.pgm[0].max_sectors == 1
    assert a2l.tree.project.module[0].if_data_xcp.pgm[0].max_cto_pgm == 2


def test_module_if_data_xcp_pgm_sector_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin IF_DATA XCP
                    /begin PGM
                        PGM_MODE_ABSOLUTE_AND_FUNCTIONAL
                        1
                        2
                        /begin SECTOR
                            "first sector name"
                            1
                            2
                            3
                            4
                            5
                            6
                        /end SECTOR
                        /begin SECTOR
                            "second sector name"
                            7
                            8
                            9
                            10
                            11
                            12
                        /end SECTOR
                    /end PGM
                /end IF_DATA
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].if_data_xcp.pgm[0], 'sector')
    assert a2l.tree.project.module[0].if_data_xcp.pgm[0].sector[0].name == 'first sector name'
    assert a2l.tree.project.module[0].if_data_xcp.pgm[0].sector[0].sector_number == 1
    assert a2l.tree.project.module[0].if_data_xcp.pgm[0].sector[0].address == 2
    assert a2l.tree.project.module[0].if_data_xcp.pgm[0].sector[0].length == 3
    assert a2l.tree.project.module[0].if_data_xcp.pgm[0].sector[0].erase_number == 4
    assert a2l.tree.project.module[0].if_data_xcp.pgm[0].sector[0].program_number == 5
    assert a2l.tree.project.module[0].if_data_xcp.pgm[0].sector[0].programming_method == 6
    assert a2l.tree.project.module[0].if_data_xcp.pgm[0].sector[1].name == 'second sector name'
    assert a2l.tree.project.module[0].if_data_xcp.pgm[0].sector[1].sector_number == 7
    assert a2l.tree.project.module[0].if_data_xcp.pgm[0].sector[1].address == 8
    assert a2l.tree.project.module[0].if_data_xcp.pgm[0].sector[1].length == 9
    assert a2l.tree.project.module[0].if_data_xcp.pgm[0].sector[1].erase_number == 10
    assert a2l.tree.project.module[0].if_data_xcp.pgm[0].sector[1].program_number == 11
    assert a2l.tree.project.module[0].if_data_xcp.pgm[0].sector[1].programming_method == 12


def test_module_if_data_xcp_daq_daq_list_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin IF_DATA XCP
                    /begin DAQ
                        STATIC /* DAQ configuration type */
                        1 /* max DAQ */
                        2 /* max event channel */
                        3 /* min DAQ */
                        OPTIMISATION_TYPE_DEFAULT
                        ADDRESS_EXTENSION_FREE
                        IDENTIFICATION_FIELD_TYPE_ABSOLUTE
                        GRANULARITY_ODT_ENTRY_SIZE_DAQ_BYTE
                        4
                        NO_OVERLOAD_INDICATION
                        PRESCALER_SUPPORTED
                        RESUME_SUPPORTED
                        /begin DAQ_LIST
                            0x0
                        /end DAQ_LIST
                        /begin DAQ_LIST
                            0x1
                            DAQ_LIST_TYPE DAQ
                            MAX_ODT 2
                            MAX_ODT_ENTRIES 3
                            FIRST_PID 4
                            EVENT_FIXED 5
                        /end DAQ_LIST
                    /end DAQ
                /end IF_DATA
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].if_data_xcp.daq[0], 'daq_list')
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].daq_list[0].daq_list_number == 0
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].daq_list[0].daq_list_type is None
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].daq_list[0].max_odt is None
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].daq_list[0].max_odt_entries is None
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].daq_list[0].first_pid is None
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].daq_list[0].event_fixed is None
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].daq_list[1].daq_list_number == 1
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].daq_list[1].daq_list_type == 'DAQ'
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].daq_list[1].max_odt == 2
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].daq_list[1].max_odt_entries == 3
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].daq_list[1].first_pid == 4
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].daq_list[1].event_fixed == 5


def test_module_if_data_xcp_event_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin IF_DATA XCP
                    /begin DAQ
                        STATIC /* DAQ configuration type */
                        1 /* max DAQ */
                        2 /* max event channel */
                        3 /* min DAQ */
                        OPTIMISATION_TYPE_DEFAULT
                        ADDRESS_EXTENSION_FREE
                        IDENTIFICATION_FIELD_TYPE_ABSOLUTE
                        GRANULARITY_ODT_ENTRY_SIZE_DAQ_BYTE
                        4
                        NO_OVERLOAD_INDICATION
                        PRESCALER_SUPPORTED
                        RESUME_SUPPORTED
                        /begin EVENT
                            "event name"
                            "event short name"
                            0x0
                            DAQ_STIM
                            1
                            2
                            3
                            4
                        /end EVENT
                    /end DAQ
                /end IF_DATA
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].if_data_xcp.daq[0], 'event')
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].event[0].name == 'event name'
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].event[0].short_name == 'event short name'
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].event[0].event_channel_number == 0
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].event[0].daq_list_type == 'DAQ_STIM'
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].event[0].max_daq_list == 1
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].event[0].time_cycle == 2
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].event[0].time_unit == 3
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].event[0].priority == 4


def test_module_if_data_xcp_timestamp_supported_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin IF_DATA XCP
                    /begin DAQ
                        STATIC /* DAQ configuration type */
                        1 /* max DAQ */
                        2 /* max event channel */
                        3 /* min DAQ */
                        OPTIMISATION_TYPE_DEFAULT
                        ADDRESS_EXTENSION_FREE
                        IDENTIFICATION_FIELD_TYPE_ABSOLUTE
                        GRANULARITY_ODT_ENTRY_SIZE_DAQ_BYTE
                        4
                        NO_OVERLOAD_INDICATION
                        PRESCALER_SUPPORTED
                        RESUME_SUPPORTED
                        /begin TIMESTAMP_SUPPORTED
                            1
                            timestamp_supported_size
                            timestamp_supported_unit
                        /end TIMESTAMP_SUPPORTED
                        /begin TIMESTAMP_SUPPORTED
                            1
                            timestamp_supported_size
                            timestamp_supported_unit
                            TIMESTAMP_FIXED
                        /end TIMESTAMP_SUPPORTED
                    /end DAQ
                /end IF_DATA
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].if_data_xcp.daq[0], 'timestamp_supported')
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].timestamp_supported[0].timestamp_ticks == 1
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].timestamp_supported[0].size == 'timestamp_supported_size'
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].timestamp_supported[0].unit == 'timestamp_supported_unit'
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].timestamp_supported[0].timestamp_fixed is None
    assert a2l.tree.project.module[0].if_data_xcp.daq[0].timestamp_supported[1].timestamp_fixed == 'TIMESTAMP_FIXED'


def test_mod_par_version_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_PAR "mod_par comment"
                    VERSION "mod_par version"
                /end MOD_PAR
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].mod_par, 'version')
    assert a2l.tree.project.module[0].mod_par.version == 'mod_par version'


def test_mod_par_addr_epk_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_PAR "mod_par comment"
                    ADDR_EPK 0
                /end MOD_PAR
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].mod_par, 'addr_epk')
    assert a2l.tree.project.module[0].mod_par.addr_epk[0] == 0


def test_mod_par_with_multiple_addr_epk_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_PAR "mod_par comment"
                    ADDR_EPK 0
                    ADDR_EPK 1
                /end MOD_PAR
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].mod_par.addr_epk[0] == 0
    assert a2l.tree.project.module[0].mod_par.addr_epk[1] == 1


def test_mod_par_epk_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_PAR "mod_par comment"
                    EPK "epk identifier"
                /end MOD_PAR
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].mod_par, 'epk')
    assert a2l.tree.project.module[0].mod_par.epk == 'epk identifier'


def test_mod_par_supplier_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_PAR "mod_par comment"
                    SUPPLIER "supplier"
                /end MOD_PAR
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].mod_par, 'supplier')
    assert a2l.tree.project.module[0].mod_par.supplier == 'supplier'


def test_mod_par_customer_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_PAR "mod_par comment"
                    CUSTOMER "customer"
                /end MOD_PAR
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].mod_par, 'customer')
    assert a2l.tree.project.module[0].mod_par.customer == 'customer'


def test_mod_par_customer_no_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_PAR "mod_par comment"
                    CUSTOMER_NO "customer no"
                /end MOD_PAR
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].mod_par, 'customer_no')
    assert a2l.tree.project.module[0].mod_par.customer_no == 'customer no'


def test_mod_par_user_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_PAR "mod_par comment"
                    USER "user"
                /end MOD_PAR
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].mod_par, 'user')
    assert a2l.tree.project.module[0].mod_par.user == 'user'


def test_mod_par_phone_no_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_PAR "mod_par comment"
                    PHONE_NO "phone no"
                /end MOD_PAR
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].mod_par, 'phone_no')
    assert a2l.tree.project.module[0].mod_par.phone_no == 'phone no'


def test_mod_par_ecu_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_PAR "mod_par comment"
                    ECU "ecu"
                /end MOD_PAR
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].mod_par, 'ecu')
    assert a2l.tree.project.module[0].mod_par.ecu == 'ecu'


def test_mod_par_cpu_type_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_PAR "mod_par comment"
                    CPU_TYPE "cpu type"
                /end MOD_PAR
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].mod_par, 'cpu_type')
    assert a2l.tree.project.module[0].mod_par.cpu_type == 'cpu type'


def test_mod_par_no_of_interfaces_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_PAR "mod_par comment"
                    NO_OF_INTERFACES 0
                /end MOD_PAR
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].mod_par, 'no_of_interfaces')
    assert a2l.tree.project.module[0].mod_par.no_of_interfaces == 0


def test_mod_par_ecu_calibration_offset_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_PAR "mod_par comment"
                    ECU_CALIBRATION_OFFSET 0
                /end MOD_PAR
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].mod_par, 'ecu_calibration_offset')
    assert a2l.tree.project.module[0].mod_par.ecu_calibration_offset == 0


def test_mod_par_calibration_method_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_PAR "mod_par comment"
                    /begin CALIBRATION_METHOD "calibration_method_method" 0
                    /end CALIBRATION_METHOD
                /end MOD_PAR
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].mod_par, 'calibration_method')


def test_mod_par_with_multiple_calibration_method_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_PAR "mod_par comment"
                    /begin CALIBRATION_METHOD "first_calibration_method_method" 0
                    /end CALIBRATION_METHOD
                    /begin CALIBRATION_METHOD "second_calibration_method_method" 0
                    /end CALIBRATION_METHOD
                /end MOD_PAR
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].mod_par.calibration_method[0].method == 'first_calibration_method_method'
    assert a2l.tree.project.module[0].mod_par.calibration_method[1].method == 'second_calibration_method_method'


def test_mod_par_memory_layout_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_PAR "mod_par comment"
                    /begin MEMORY_LAYOUT PRG_CODE 0 0 0 0 0 0 0
                    /end MEMORY_LAYOUT
                /end MOD_PAR
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].mod_par, 'memory_layout')


def test_mod_par_with_multiple_memory_layout_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_PAR "mod_par comment"
                    /begin MEMORY_LAYOUT PRG_CODE 0 0 0 0 0 0 0
                    /end MEMORY_LAYOUT
                    /begin MEMORY_LAYOUT PRG_DATA 0 0 0 0 0 0 0
                    /end MEMORY_LAYOUT
                /end MOD_PAR
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].mod_par.memory_layout[0].prg_type == 'PRG_CODE'
    assert a2l.tree.project.module[0].mod_par.memory_layout[1].prg_type == 'PRG_DATA'


def test_mod_par_memory_segment_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_PAR "mod_par comment"
                    /begin MEMORY_SEGMENT 
                        memory_segment_name 
                        "memory_segment long identifier" 
                        CODE 
                        RAM 
                        INTERN 
                        0 
                        0 
                        0 
                        0 
                        0 
                        0 
                        0
                    /end MEMORY_SEGMENT
                /end MOD_PAR
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].mod_par, 'memory_segment')


def test_mod_par_with_multiple_memory_segment_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_PAR "mod_par comment"
                    /begin MEMORY_SEGMENT 
                        first_memory_segment_name 
                        "first memory_segment long identifier" 
                        CODE 
                        RAM 
                        INTERN 
                        0 
                        0 
                        0 
                        0 
                        0 
                        0 
                        0
                    /end MEMORY_SEGMENT
                    /begin MEMORY_SEGMENT 
                        second_memory_segment_name 
                        "second memory_segment long identifier" 
                        CODE 
                        RAM 
                        INTERN 
                        0 
                        0 
                        0 
                        0 
                        0 
                        0 
                        0
                    /end MEMORY_SEGMENT
                /end MOD_PAR
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].mod_par.memory_segment[0].name == 'first_memory_segment_name'
    assert a2l.tree.project.module[0].mod_par.memory_segment[1].name == 'second_memory_segment_name'


def test_mod_par_system_constant_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_PAR "mod_par comment"
                    SYSTEM_CONSTANT "system_constant name" "system_constant value"
                /end MOD_PAR
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].mod_par, 'system_constant')


def test_mod_par_with_multiple_system_constant_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_PAR "mod_par comment"
                    SYSTEM_CONSTANT "first system_constant name" "first system_constant value"
                    SYSTEM_CONSTANT "second system_constant name" "second system_constant value"
                /end MOD_PAR
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].mod_par.system_constant[0].name == 'first system_constant name'
    assert a2l.tree.project.module[0].mod_par.system_constant[1].name == 'second system_constant name'


def test_mod_common_s_rec_layout_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_COMMON "mod_common comment"
                    S_REC_LAYOUT s_rec_layout
                /end MOD_COMMON
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].mod_common, 's_rec_layout')
    assert a2l.tree.project.module[0].mod_common.s_rec_layout == 's_rec_layout'


def test_mod_common_deposit_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_COMMON "mod_common comment"
                    DEPOSIT ABSOLUTE
                /end MOD_COMMON
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].mod_common, 'deposit')
    assert a2l.tree.project.module[0].mod_common.deposit == 'ABSOLUTE'


def test_mod_common_byte_order_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_COMMON "mod_common comment"
                    BYTE_ORDER MSB_LAST
                /end MOD_COMMON
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].mod_common, 'byte_order')
    assert a2l.tree.project.module[0].mod_common.byte_order == 'MSB_LAST'


def test_mod_common_data_size_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_COMMON "mod_common comment"
                    DATA_SIZE 0
                /end MOD_COMMON
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].mod_common, 'data_size')
    assert a2l.tree.project.module[0].mod_common.data_size == 0


def test_mod_common_alignment_byte_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_COMMON "mod_common comment"
                    ALIGNMENT_BYTE 0
                /end MOD_COMMON
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].mod_common, 'alignment_byte')
    assert a2l.tree.project.module[0].mod_common.alignment_byte == 0


def test_mod_common_alignment_word_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_COMMON "mod_common comment"
                    ALIGNMENT_WORD 0
                /end MOD_COMMON
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].mod_common, 'alignment_word')
    assert a2l.tree.project.module[0].mod_common.alignment_word == 0


def test_mod_common_alignment_long_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_COMMON "mod_common comment"
                    ALIGNMENT_LONG 0
                /end MOD_COMMON
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].mod_common, 'alignment_long')
    assert a2l.tree.project.module[0].mod_common.alignment_long == 0


def test_mod_common_alignment_float32_ieee_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_COMMON "mod_common comment"
                    ALIGNMENT_FLOAT32_IEEE 0
                /end MOD_COMMON
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].mod_common, 'alignment_float32_ieee')
    assert a2l.tree.project.module[0].mod_common.alignment_float32_ieee == 0


def test_mod_common_alignment_float64_ieee_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_COMMON "mod_common comment"
                    ALIGNMENT_FLOAT64_IEEE 0
                /end MOD_COMMON
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].mod_common, 'alignment_float64_ieee')
    assert a2l.tree.project.module[0].mod_common.alignment_float64_ieee == 0


# TODO: implement test for module if_data node.


def test_characteristic_display_identifier_node():
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
                    DISPLAY_IDENTIFIER display_identifier
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0], 'display_identifier')
    assert a2l.tree.project.module[0].characteristic[0].display_identifier == 'display_identifier'


def test_characteristic_format_node():
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
                    FORMAT "%d"
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0], 'format')
    assert a2l.tree.project.module[0].characteristic[0].format == '%d'


def test_characteristic_byte_order_node():
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
                    BYTE_ORDER MSB_LAST
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0], 'byte_order')
    assert a2l.tree.project.module[0].characteristic[0].byte_order == 'MSB_LAST'


def test_characteristic_bit_mask_node():
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
                    BIT_MASK 0
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0], 'bit_mask')
    assert a2l.tree.project.module[0].characteristic[0].bit_mask == 0


def test_characteristic_function_list_node():
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
                    /begin FUNCTION_LIST
                        first_function
                        second_function
                    /end FUNCTION_LIST
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0], 'function_list')


def test_characteristic_number_node():
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
                    NUMBER 0
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0], 'number')
    assert a2l.tree.project.module[0].characteristic[0].number == 0


def test_characteristic_extended_limits_node():
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
                    EXTENDED_LIMITS 0 1
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0], 'extended_limits')
    assert a2l.tree.project.module[0].characteristic[0].extended_limits[0] == 0
    assert a2l.tree.project.module[0].characteristic[0].extended_limits[1] == 1


def test_characteristic_read_only_node():
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
                    READ_ONLY
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0], 'read_only')
    assert a2l.tree.project.module[0].characteristic[0].read_only == 'READ_ONLY'


def test_characteristic_guard_rails_node():
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
                    GUARD_RAILS
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0], 'guard_rails')
    assert a2l.tree.project.module[0].characteristic[0].guard_rails == 'GUARD_RAILS'


def test_characteristic_map_list_node():
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
                    /begin MAP_LIST
                        first_map
                        second_map
                    /end MAP_LIST
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0], 'map_list')


def test_characteristic_max_refresh_node():
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
                    MAX_REFRESH 0 1
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0], 'max_refresh')
    assert a2l.tree.project.module[0].characteristic[0].max_refresh is not None


def test_characteristic_dependent_characteristic_node():
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
                    /begin DEPENDENT_CHARACTERISTIC
                        "X"
                        A
                    /end DEPENDENT_CHARACTERISTIC
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0], 'dependent_characteristic')


def test_characteristic_virtual_characteristic_node():
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
                    /begin VIRTUAL_CHARACTERISTIC
                        "X"
                        A
                    /end VIRTUAL_CHARACTERISTIC
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0], 'virtual_characteristic')


def test_characteristic_ref_memory_segment_node():
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
                    REF_MEMORY_SEGMENT ref_memory_segment
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0], 'ref_memory_segment')
    assert a2l.tree.project.module[0].characteristic[0].ref_memory_segment == 'ref_memory_segment'


def test_characteristic_annotation_node():
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
                    /begin ANNOTATION
                    /end ANNOTATION
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0], 'annotation')


def test_characteristic_with_multiple_annotation_node():
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
                    /begin ANNOTATION
                    /end ANNOTATION
                    /begin ANNOTATION
                    /end ANNOTATION
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert len(a2l.tree.project.module[0].characteristic[0].annotation) == 2


def test_characteristic_comparison_quantity_node():
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
                    COMPARISON_QUANTITY comparison_quantity
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0], 'comparison_quantity')
    assert a2l.tree.project.module[0].characteristic[0].comparison_quantity == 'comparison_quantity'


def test_characteristic_if_data_node():
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
                    /begin IF_DATA if_data
                    /end IF_DATA
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0], 'if_data_characteristic')


def test_characteristic_with_multiple_if_data_node():
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
                    /begin IF_DATA first_if_data
                    /end IF_DATA
                    /begin IF_DATA second_if_data
                    /end IF_DATA
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert len(a2l.tree.project.module[0].characteristic[0].if_data_characteristic) == 2


def test_characteristic_axis_desc_node():
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
                    /begin AXIS_DESCR STD_AXIS input_quantity conversion 0 0 0
                    /end AXIS_DESCR
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0], 'axis_descr')


def test_characteristic_with_multiple_axis_descr_node():
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
                    /begin AXIS_DESCR STD_AXIS first_input_quantity first_conversion 0 0 0
                    /end AXIS_DESCR
                    /begin AXIS_DESCR STD_AXIS second_input_quantity second_conversion 0 0 0
                    /end AXIS_DESCR
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert len(a2l.tree.project.module[0].characteristic[0].axis_descr) == 2


def test_characteristic_calibration_access_node():
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
                    CALIBRATION_ACCESS CALIBRATION
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0], 'calibration_access')
    assert a2l.tree.project.module[0].characteristic[0].calibration_access == 'CALIBRATION'


def test_characteristic_matrix_dim_node():
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
                    MATRIX_DIM 0 1 2
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0], 'matrix_dim')
    assert a2l.tree.project.module[0].characteristic[0].matrix_dim[0] == 0
    assert a2l.tree.project.module[0].characteristic[0].matrix_dim[1] == 1
    assert a2l.tree.project.module[0].characteristic[0].matrix_dim[2] == 2


def test_characteristic_ecu_address_extension_node():
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
                    ECU_ADDRESS_EXTENSION 0
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0], 'ecu_address_extension')
    assert a2l.tree.project.module[0].characteristic[0].ecu_address_extension == 0


def test_axis_pts_display_identifier_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin AXIS_PTS
                    axis_pts_name 
                    "axis_pts long identifier"  
                    0
                    input_quantity 
                    deposit 
                    0 
                    conversion
                    0
                    0
                    0
                    DISPLAY_IDENTIFIER display_identifier
                /end AXIS_PTS
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].axis_pts[0], 'display_identifier')
    assert a2l.tree.project.module[0].axis_pts[0].display_identifier == 'display_identifier'


def test_axis_pts_read_only_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin AXIS_PTS
                    axis_pts_name 
                    "axis_pts long identifier"  
                    0
                    input_quantity 
                    deposit 
                    0 
                    conversion
                    0
                    0
                    0
                    READ_ONLY
                /end AXIS_PTS
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].axis_pts[0], 'read_only')
    assert a2l.tree.project.module[0].axis_pts[0].read_only == 'READ_ONLY'


def test_axis_pts_format_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin AXIS_PTS
                    axis_pts_name 
                    "axis_pts long identifier"  
                    0
                    input_quantity 
                    deposit 
                    0 
                    conversion
                    0
                    0
                    0
                    FORMAT "%d"
                /end AXIS_PTS
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].axis_pts[0], 'format')
    assert a2l.tree.project.module[0].axis_pts[0].format == '%d'


def test_axis_pts_deposit_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin AXIS_PTS
                    axis_pts_name 
                    "axis_pts long identifier"  
                    0
                    input_quantity 
                    deposit 
                    0 
                    conversion
                    0
                    0
                    0
                    DEPOSIT ABSOLUTE
                /end AXIS_PTS
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].axis_pts[0], 'deposit')
    assert a2l.tree.project.module[0].axis_pts[0].deposit == 'ABSOLUTE'


def test_axis_pts_byte_order_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin AXIS_PTS
                    axis_pts_name 
                    "axis_pts long identifier"  
                    0
                    input_quantity 
                    deposit 
                    0 
                    conversion
                    0
                    0
                    0
                    BYTE_ORDER MSB_LAST
                /end AXIS_PTS
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].axis_pts[0], 'byte_order')
    assert a2l.tree.project.module[0].axis_pts[0].byte_order == 'MSB_LAST'


def test_axis_pts_function_list_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin AXIS_PTS
                    axis_pts_name 
                    "axis_pts long identifier"  
                    0
                    input_quantity 
                    deposit 
                    0 
                    conversion
                    0
                    0
                    0
                    /begin FUNCTION_LIST
                        first_function
                        second_function
                    /end FUNCTION_LIST
                /end AXIS_PTS
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].axis_pts[0], 'function_list')


def test_axis_pts_ref_memory_segment_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin AXIS_PTS
                    axis_pts_name 
                    "axis_pts long identifier"  
                    0
                    input_quantity 
                    deposit 
                    0 
                    conversion
                    0
                    0
                    0
                    REF_MEMORY_SEGMENT ref_memory_segment
                /end AXIS_PTS
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].axis_pts[0], 'ref_memory_segment')
    assert a2l.tree.project.module[0].axis_pts[0].ref_memory_segment == 'ref_memory_segment'


def test_axis_pts_guard_rails_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin AXIS_PTS
                    axis_pts_name 
                    "axis_pts long identifier"  
                    0
                    input_quantity 
                    deposit 
                    0 
                    conversion
                    0
                    0
                    0
                    GUARD_RAILS
                /end AXIS_PTS
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].axis_pts[0], 'guard_rails')
    assert a2l.tree.project.module[0].axis_pts[0].guard_rails == 'GUARD_RAILS'


def test_axis_pts_extended_limits_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin AXIS_PTS
                    axis_pts_name 
                    "axis_pts long identifier"  
                    0
                    input_quantity 
                    deposit 
                    0 
                    conversion
                    0
                    0
                    0
                    EXTENDED_LIMITS 0 1
                /end AXIS_PTS
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].axis_pts[0], 'extended_limits')
    assert a2l.tree.project.module[0].axis_pts[0].extended_limits[0] == 0
    assert a2l.tree.project.module[0].axis_pts[0].extended_limits[1] == 1


def test_axis_pts_annotation_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin AXIS_PTS
                    axis_pts_name 
                    "axis_pts long identifier"  
                    0
                    input_quantity 
                    deposit 
                    0 
                    conversion
                    0
                    0
                    0
                    /begin ANNOTATION
                    /end ANNOTATION
                /end AXIS_PTS
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].axis_pts[0], 'annotation')


def test_axis_pts_with_multiple_annotation_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin AXIS_PTS
                    axis_pts_name 
                    "axis_pts long identifier"  
                    0
                    input_quantity 
                    deposit 
                    0 
                    conversion
                    0
                    0
                    0
                    /begin ANNOTATION
                    /end ANNOTATION
                    /begin ANNOTATION
                    /end ANNOTATION
                /end AXIS_PTS
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert len(a2l.tree.project.module[0].axis_pts[0].annotation) == 2


def test_axis_pts_if_data_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin AXIS_PTS
                    axis_pts_name 
                    "axis_pts long identifier"  
                    0
                    input_quantity 
                    deposit 
                    0 
                    conversion
                    0
                    0
                    0
                    /begin IF_DATA if_data
                    /end IF_DATA
                /end AXIS_PTS
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].axis_pts[0], 'if_data_axis_pts')


def test_axis_pts_with_multiple_if_data_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin AXIS_PTS
                    axis_pts_name 
                    "axis_pts long identifier"  
                    0
                    input_quantity 
                    deposit 
                    0 
                    conversion
                    0
                    0
                    0
                    /begin IF_DATA first_if_data
                    /end IF_DATA
                    /begin IF_DATA second_if_data
                    /end IF_DATA
                /end AXIS_PTS
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert len(a2l.tree.project.module[0].axis_pts[0].if_data_axis_pts) == 2


def test_axis_pts_calibration_access_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin AXIS_PTS
                    axis_pts_name 
                    "axis_pts long identifier"  
                    0
                    input_quantity 
                    deposit 
                    0 
                    conversion
                    0
                    0
                    0
                    CALIBRATION_ACCESS CALIBRATION
                /end AXIS_PTS
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].axis_pts[0], 'calibration_access')
    assert a2l.tree.project.module[0].axis_pts[0].calibration_access == 'CALIBRATION'


def test_axis_pts_ecu_address_extension_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin AXIS_PTS
                    axis_pts_name 
                    "axis_pts long identifier"  
                    0
                    input_quantity 
                    deposit 
                    0 
                    conversion
                    0
                    0
                    0
                    ECU_ADDRESS_EXTENSION 0
                /end AXIS_PTS
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].axis_pts[0], 'ecu_address_extension')
    assert a2l.tree.project.module[0].axis_pts[0].ecu_address_extension == 0


def test_measurement_display_identifier_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT
                    measurement_name 
                    "measurement long identifier"  
                    UWORD
                    conversion 
                    0
                    0
                    0
                    0
                    DISPLAY_IDENTIFIER display_identifier
                /end MEASUREMENT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].measurement[0], 'display_identifier')
    assert a2l.tree.project.module[0].measurement[0].display_identifier == 'display_identifier'


def test_measurement_if_data_xcp_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT
                    measurement_name 
                    "measurement long identifier"  
                    UWORD
                    conversion 
                    0
                    0
                    0
                    0
                    /begin IF_DATA XCP
                        /begin DAQ_EVENT VARIABLE
                            /begin AVAILABLE_EVENT_LIST
                                EVENT 0001 EVENT 0002
                            /end AVAILABLE_EVENT_LIST
                            /begin DEFAULT_EVENT_LIST
                                EVENT 0001
                            /end DEFAULT_EVENT_LIST
                        /end DAQ_EVENT
                    /end IF_DATA 
                /end MEASUREMENT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].measurement[0], 'if_data_xcp')


def test_if_data_xcp_daq_event_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT
                    measurement_name 
                    "measurement long identifier"  
                    UWORD
                    conversion 
                    0
                    0
                    0
                    0
                    /begin IF_DATA XCP
                        /begin DAQ_EVENT VARIABLE
                        /end DAQ_EVENT
                    /end IF_DATA 
                /end MEASUREMENT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].measurement[0].if_data_xcp[0], 'daq_event')
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].daq_event[0].name == 'VARIABLE'


def test_if_data_xcp_xcp_on_can_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT
                    measurement_name 
                    "measurement long identifier"  
                    UWORD
                    conversion 
                    0
                    0
                    0
                    0
                    /begin IF_DATA XCP
                        /begin XCP_ON_CAN 0
                            CAN_ID_BROADCAST 1
                            CAN_ID_MASTER 2
                            CAN_ID_SLAVE 3
                            BAUDRATE 4
                            SAMPLE_POINT 5
                            SAMPLE_RATE SINGLE
                            BTL_CYCLES 6
                            SJW 7
                            SYNC_EDGE SINGLE
                        /end XCP_ON_CAN
                        /begin XCP_ON_CAN 0
                            SAMPLE_RATE TRIPLE
                            SYNC_EDGE DUAL
                        /end XCP_ON_CAN
                        /begin XCP_ON_CAN 0
                            /begin DAQ_LIST_CAN_ID 0
                            /end DAQ_LIST_CAN_ID
                            /begin DAQ_LIST_CAN_ID 1
                                VARIABLE
                            /end DAQ_LIST_CAN_ID
                            /begin DAQ_LIST_CAN_ID 2
                                FIXED 12
                            /end DAQ_LIST_CAN_ID
                        /end XCP_ON_CAN
                    /end IF_DATA 
                /end MEASUREMENT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].measurement[0].if_data_xcp[0], 'xcp_on_can')
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_can[0].identifier == 0
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_can[0].can_id_broadcast == 1
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_can[0].can_id_master == 2
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_can[0].can_id_slave == 3
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_can[0].baudrate == 4
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_can[0].sample_point == 5
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_can[0].sample_rate == 'SINGLE'
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_can[0].btl_cycles == 6
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_can[0].sjw == 7
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_can[0].sync_edge == 'SINGLE'
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_can[1].sample_rate == 'TRIPLE'
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_can[1].sync_edge == 'DUAL'
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_can[2].daq_list_can_id[0].identifier == 0
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_can[2].daq_list_can_id[0].daq_list_can_id_type_variable is None
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_can[2].daq_list_can_id[0].daq_list_can_id_type_fixed is None
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_can[2].daq_list_can_id[1].identifier == 1
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_can[2].daq_list_can_id[1].daq_list_can_id_type_variable == 'VARIABLE'
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_can[2].daq_list_can_id[1].daq_list_can_id_type_fixed is None
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_can[2].daq_list_can_id[2].identifier == 2
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_can[2].daq_list_can_id[2].daq_list_can_id_type_variable is None
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_can[2].daq_list_can_id[2].daq_list_can_id_type_fixed == 12


@pytest.mark.parametrize('xcp_on_tcp_ip, identifier, port, host_name, address, protocol_layer, segment, daq, pag, pgm, daq_event', (
    ("""0 10""",
     0, 10, None, None, [], [], [], [], [], []),
    ("""1 11 HOST_NAME "host name" """,
     1, 11, 'host name', None, [], [], [], [], [], []),
    ("""2 12 ADDRESS "address" """,
     2, 12, None, 'address', [], [], [], [], [], []),
    ("""3 13 /begin PROTOCOL_LAYER 0 0 0 0 0 0 0 0 0 0 /end PROTOCOL_LAYER """,
     3, 13, None, None, [ProtocolLayer(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)], [], [], [], [], []),
    ("""4 14 /begin SEGMENT 0 0 0 0 0 /end SEGMENT """,
     4, 14, None, None, [], [Segment(0, 0, 0, 0, 0, [])], [], [], [], []),
    ("""5 15 /begin DAQ STATIC 0 0 0 OPTIMISATION_TYPE_DEFAULT ADDRESS_EXTENSION_FREE IDENTIFICATION_FIELD_TYPE_ABSOLUTE GRANULARITY_ODT_ENTRY_SIZE_DAQ_BYTE 4 NO_OVERLOAD_INDICATION /end DAQ """,
     5, 15, None, None, [], [], [Daq('STATIC', 0, 0, 0, 'OPTIMISATION_TYPE_DEFAULT', 'ADDRESS_EXTENSION_FREE', 'IDENTIFICATION_FIELD_TYPE_ABSOLUTE', 'GRANULARITY_ODT_ENTRY_SIZE_DAQ_BYTE', 4, 'NO_OVERLOAD_INDICATION', [])], [], [], []),
    ("""6 16 /begin PAG 0 /end PAG """,
     6, 16, None, None, [], [], [], [Pag(0, [])], [], []),
    ("""7 17 /begin PGM PGM_MODE_ABSOLUTE_AND_FUNCTIONAL 0 0 /end PGM """,
     7, 17, None, None, [], [], [], [], [Pgm('PGM_MODE_ABSOLUTE_AND_FUNCTIONAL', 0, 0, [])], []),
    ("""8 18 /begin DAQ_EVENT VARIABLE /end DAQ_EVENT """,
     8, 18, None, None, [], [], [], [], [], [DaqEvent('VARIABLE', [])]),
))
def test_if_data_xcp_xcp_on_tcp_ip_node(xcp_on_tcp_ip, identifier, port, host_name, address, protocol_layer, segment, daq, pag, pgm, daq_event):
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT
                    measurement_name 
                    "measurement long identifier"  
                    UWORD
                    conversion 
                    0
                    0
                    0
                    0
                    /begin IF_DATA XCP
                        /begin XCP_ON_TCP_IP
                            {}
                        /end XCP_ON_TCP_IP
                    /end IF_DATA 
                /end MEASUREMENT
            /end MODULE
        /end PROJECT""".format(xcp_on_tcp_ip)
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_tcp_ip[0].identifier == identifier
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_tcp_ip[0].port == port
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_tcp_ip[0].host_name == host_name
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_tcp_ip[0].address == address
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_tcp_ip[0].protocol_layer == protocol_layer
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_tcp_ip[0].segment == segment
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_tcp_ip[0].daq == daq
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_tcp_ip[0].pag == pag
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_tcp_ip[0].pgm == pgm
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_tcp_ip[0].daq_event == daq_event


@pytest.mark.parametrize('xcp_on_udp_ip, identifier, port, host_name, address, protocol_layer, segment, daq, pag, pgm, daq_event', (
    ("""0 10""",
     0, 10, None, None, [], [], [], [], [], []),
    ("""1 11 HOST_NAME "host name" """,
     1, 11, 'host name', None, [], [], [], [], [], []),
    ("""2 12 ADDRESS "address" """,
     2, 12, None, 'address', [], [], [], [], [], []),
    ("""3 13 /begin PROTOCOL_LAYER 0 0 0 0 0 0 0 0 0 0 /end PROTOCOL_LAYER """,
     3, 13, None, None, [ProtocolLayer(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)], [], [], [], [], []),
    ("""4 14 /begin SEGMENT 0 0 0 0 0 /end SEGMENT """,
     4, 14, None, None, [], [Segment(0, 0, 0, 0, 0, [])], [], [], [], []),
    ("""5 15 /begin DAQ STATIC 0 0 0 OPTIMISATION_TYPE_DEFAULT ADDRESS_EXTENSION_FREE IDENTIFICATION_FIELD_TYPE_ABSOLUTE GRANULARITY_ODT_ENTRY_SIZE_DAQ_BYTE 4 NO_OVERLOAD_INDICATION /end DAQ """,
     5, 15, None, None, [], [], [Daq('STATIC', 0, 0, 0, 'OPTIMISATION_TYPE_DEFAULT', 'ADDRESS_EXTENSION_FREE', 'IDENTIFICATION_FIELD_TYPE_ABSOLUTE', 'GRANULARITY_ODT_ENTRY_SIZE_DAQ_BYTE', 4, 'NO_OVERLOAD_INDICATION', [])], [], [], []),
    ("""6 16 /begin PAG 0 /end PAG """,
     6, 16, None, None, [], [], [], [Pag(0, [])], [], []),
    ("""7 17 /begin PGM PGM_MODE_ABSOLUTE_AND_FUNCTIONAL 0 0 /end PGM """,
     7, 17, None, None, [], [], [], [], [Pgm('PGM_MODE_ABSOLUTE_AND_FUNCTIONAL', 0, 0, [])], []),
    ("""8 18 /begin DAQ_EVENT VARIABLE /end DAQ_EVENT """,
     8, 18, None, None, [], [], [], [], [], [DaqEvent('VARIABLE', [])]),
))
def test_if_data_xcp_xcp_on_udp_ip_node(xcp_on_udp_ip, identifier, port, host_name, address, protocol_layer, segment, daq, pag, pgm, daq_event):
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT
                    measurement_name 
                    "measurement long identifier"  
                    UWORD
                    conversion 
                    0
                    0
                    0
                    0
                    /begin IF_DATA XCP
                        /begin XCP_ON_UDP_IP
                            {}
                        /end XCP_ON_UDP_IP
                    /end IF_DATA 
                /end MEASUREMENT
            /end MODULE
        /end PROJECT""".format(xcp_on_udp_ip)
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_udp_ip[0].identifier == identifier
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_udp_ip[0].port == port
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_udp_ip[0].host_name == host_name
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_udp_ip[0].address == address
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_udp_ip[0].protocol_layer == protocol_layer
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_udp_ip[0].segment == segment
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_udp_ip[0].daq == daq
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_udp_ip[0].pag == pag
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_udp_ip[0].pgm == pgm
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].xcp_on_udp_ip[0].daq_event == daq_event


def test_if_data_xcp_segment_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT
                    measurement_name 
                    "measurement long identifier"  
                    UWORD
                    conversion 
                    0
                    0
                    0
                    0
                    /begin IF_DATA XCP
                        /begin SEGMENT
                            0x00
                            0x01
                            0x02
                            0x03
                            0x04
                        /end SEGMENT
                        /begin SEGMENT
                            0x05
                            0x06
                            0x07
                            0x08
                            0x09
                            /begin CHECKSUM
                                "checksum.dll"
                            /end CHECKSUM
                        /end SEGMENT
                    /end IF_DATA 
                /end MEASUREMENT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].measurement[0].if_data_xcp[0], 'segment')
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].segment[0].segment_logical_number == 0
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].segment[0].number_of_pages == 1
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].segment[0].address_extension == 2
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].segment[0].compression_method == 3
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].segment[0].encryption_method == 4
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].segment[0].checksum is None
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].segment[1].segment_logical_number == 5
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].segment[1].number_of_pages == 6
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].segment[1].address_extension == 7
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].segment[1].compression_method == 8
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].segment[1].encryption_method == 9
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].segment[1].checksum.checksum_dll == 'checksum.dll'


def test_if_data_xcp_daq_event_available_event_list_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT
                    measurement_name 
                    "measurement long identifier"  
                    UWORD
                    conversion 
                    0
                    0
                    0
                    0
                    /begin IF_DATA XCP
                        /begin DAQ_EVENT VARIABLE
                            /begin AVAILABLE_EVENT_LIST
                                EVENT 0001
                                EVENT 0002
                            /end AVAILABLE_EVENT_LIST
                        /end DAQ_EVENT
                    /end IF_DATA 
                /end MEASUREMENT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].measurement[0].if_data_xcp[0].daq_event[0], 'available_event_list')
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].daq_event[0].available_event_list[0].event[0] == 1
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].daq_event[0].available_event_list[0].event[1] == 2


def test_if_data_xcp_daq_event_default_event_list_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT
                    measurement_name 
                    "measurement long identifier"  
                    UWORD
                    conversion 
                    0
                    0
                    0
                    0
                    /begin IF_DATA XCP
                        /begin DAQ_EVENT VARIABLE
                            /begin DEFAULT_EVENT_LIST
                                EVENT 0001
                                EVENT 0002
                            /end DEFAULT_EVENT_LIST
                        /end DAQ_EVENT
                    /end IF_DATA 
                /end MEASUREMENT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].measurement[0].if_data_xcp[0].daq_event[0], 'default_event_list')
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].daq_event[0].default_event_list[0].event[0] == 1
    assert a2l.tree.project.module[0].measurement[0].if_data_xcp[0].daq_event[0].default_event_list[0].event[1] == 2


def test_if_data_memory_segment_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_PAR "mod_par comment"
                    /begin MEMORY_SEGMENT
                        Dst80100000
                        ""
                        DATA
                        FLASH
                        INTERN
                        0x80100000
                        0x7FAE0
                        -1
                        -1
                        -1
                        -1
                        -1
                        /begin IF_DATA ETK_XETK
                            /begin ETK_XETK_ACCESS
                                SERIAL_INTERFACE
                            /end ETK_XETK_ACCESS
                        /end IF_DATA
                        /begin IF_DATA XCPplus 0x0102
                            /begin SEGMENT
                                2       /* segment logical number */
                                0x02       /* number of pages */
                                0x00       /* address extension */
                                0x00       /* compression method */
                                0x00       /* encryption method */
                                /begin CHECKSUM
                                    XCP_CRC_32 /* checksum: add bytes to 16bit result */
                                    MAX_BLOCK_SIZE 0xFFFFFFFF
                                /end CHECKSUM
                                /begin PAGE
                                    0x00       /* page number */
                                    ECU_ACCESS_DONT_CARE
                                    XCP_READ_ACCESS_DONT_CARE
                                    XCP_WRITE_ACCESS_NOT_ALLOWED
                                /end PAGE
                                /begin PAGE
                                    0x01       /* page number */
                                    ECU_ACCESS_DONT_CARE
                                    XCP_READ_ACCESS_DONT_CARE
                                    XCP_WRITE_ACCESS_WITH_ECU_ONLY
                                /end PAGE
                            /end SEGMENT
                        /end IF_DATA
                    /end MEMORY_SEGMENT
                /end MOD_PAR
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].mod_par.memory_segment[0].if_data_memory_segment[0], 'generic_parameter')
    assert len(a2l.tree.project.module[0].mod_par.memory_segment[0].if_data_memory_segment[0].generic_parameter) != 0


def test_if_data_memory_segment_segment_page_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_PAR "mod_par comment"
                    /begin MEMORY_SEGMENT
                        Dst80100000
                        ""
                        DATA
                        FLASH
                        INTERN
                        0x80100000
                        0x7FAE0
                        -1
                        -1
                        -1
                        -1
                        -1
                        /begin IF_DATA XCPplus 0x0102
                            /begin SEGMENT
                                2       /* segment logical number */
                                0x02       /* number of pages */
                                0x00       /* address extension */
                                0x00       /* compression method */
                                0x00       /* encryption method */
                                /begin PAGE
                                    0x00       /* page number */
                                    ECU_ACCESS_NOT_ALLOWED
                                    XCP_READ_ACCESS_NOT_ALLOWED
                                    XCP_WRITE_ACCESS_NOT_ALLOWED
                                /end PAGE
                                /begin PAGE
                                    0x01       /* page number */
                                    ECU_ACCESS_DONT_CARE
                                    XCP_READ_ACCESS_DONT_CARE
                                    XCP_WRITE_ACCESS_DONT_CARE
                                    INIT_SEGMENT 0xFE
                                /end PAGE
                            /end SEGMENT
                        /end IF_DATA
                    /end MEMORY_SEGMENT
                /end MOD_PAR
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].mod_par.memory_segment[0].if_data_memory_segment[0].segment[0].page[0].ecu_access == 'ECU_ACCESS_NOT_ALLOWED'
    assert a2l.tree.project.module[0].mod_par.memory_segment[0].if_data_memory_segment[0].segment[0].page[0].xcp_read_access == 'XCP_READ_ACCESS_NOT_ALLOWED'
    assert a2l.tree.project.module[0].mod_par.memory_segment[0].if_data_memory_segment[0].segment[0].page[0].xcp_write_access == 'XCP_WRITE_ACCESS_NOT_ALLOWED'
    assert a2l.tree.project.module[0].mod_par.memory_segment[0].if_data_memory_segment[0].segment[0].page[0].init_segment is None
    assert a2l.tree.project.module[0].mod_par.memory_segment[0].if_data_memory_segment[0].segment[0].page[1].ecu_access == 'ECU_ACCESS_DONT_CARE'
    assert a2l.tree.project.module[0].mod_par.memory_segment[0].if_data_memory_segment[0].segment[0].page[1].xcp_read_access == 'XCP_READ_ACCESS_DONT_CARE'
    assert a2l.tree.project.module[0].mod_par.memory_segment[0].if_data_memory_segment[0].segment[0].page[1].xcp_write_access == 'XCP_WRITE_ACCESS_DONT_CARE'
    assert a2l.tree.project.module[0].mod_par.memory_segment[0].if_data_memory_segment[0].segment[0].page[1].init_segment == 0xFE


def test_if_data_memory_segment_segment_address_mapping_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_PAR "mod_par comment"
                    /begin MEMORY_SEGMENT
                        Dst80100000
                        ""
                        DATA
                        FLASH
                        INTERN
                        0x80100000
                        0x7FAE0
                        -1
                        -1
                        -1
                        -1
                        -1
                        /begin IF_DATA XCPplus 0x0102
                            /begin SEGMENT
                                2       /* segment logical number */
                                0x02       /* number of pages */
                                0x00       /* address extension */
                                0x00       /* compression method */
                                0x00       /* encryption method */
                                /begin ADDRESS_MAPPING
                                    0xe0000
                                    0x40000400
                                    0x21c
                                /end ADDRESS_MAPPING
                            /end SEGMENT
                        /end IF_DATA
                    /end MEMORY_SEGMENT
                /end MOD_PAR
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].mod_par.memory_segment[0].if_data_memory_segment[0].segment[0].address_mapping[0].orig_address == 0xE0000
    assert a2l.tree.project.module[0].mod_par.memory_segment[0].if_data_memory_segment[0].segment[0].address_mapping[0].mapping_address == 0x40000400
    assert a2l.tree.project.module[0].mod_par.memory_segment[0].if_data_memory_segment[0].segment[0].address_mapping[0].length == 0x21C


def test_if_data_memory_segment_address_mapping_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MOD_PAR "mod_par comment"
                    /begin MEMORY_SEGMENT
                        Dst80100000
                        ""
                        DATA
                        FLASH
                        INTERN
                        0x80100000
                        0x7FAE0
                        -1
                        -1
                        -1
                        -1
                        -1
                        /begin IF_DATA ASAP1B_ETK
                            ADDRESS_MAPPING 0x4000 0x8000 0x0200
                        /end IF_DATA
                    /end MEMORY_SEGMENT
                /end MOD_PAR
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].mod_par.memory_segment[0].if_data_memory_segment[0], 'address_mapping')
    assert a2l.tree.project.module[0].mod_par.memory_segment[0].if_data_memory_segment[0].address_mapping[0].orig_address == 0x4000
    assert a2l.tree.project.module[0].mod_par.memory_segment[0].if_data_memory_segment[0].address_mapping[0].mapping_address == 0x8000
    assert a2l.tree.project.module[0].mod_par.memory_segment[0].if_data_memory_segment[0].address_mapping[0].length == 0x0200


def test_measurement_read_write_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT
                    measurement_name 
                    "measurement long identifier"  
                    UWORD
                    conversion 
                    0
                    0
                    0
                    0
                    READ_WRITE
                /end MEASUREMENT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].measurement[0], 'read_write')
    assert a2l.tree.project.module[0].measurement[0].read_write == 'READ_WRITE'


def test_measurement_format_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT
                    measurement_name 
                    "measurement long identifier"  
                    UWORD
                    conversion 
                    0
                    0
                    0
                    0
                    FORMAT "%d"
                /end MEASUREMENT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].measurement[0], 'format')
    assert a2l.tree.project.module[0].measurement[0].format == '%d'


def test_measurement_array_size_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT
                    measurement_name 
                    "measurement long identifier"  
                    UWORD
                    conversion 
                    0
                    0
                    0
                    0
                    ARRAY_SIZE 0
                /end MEASUREMENT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].measurement[0], 'array_size')
    assert a2l.tree.project.module[0].measurement[0].array_size == 0


def test_measurement_bit_mask_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT
                    measurement_name 
                    "measurement long identifier"  
                    UWORD
                    conversion 
                    0
                    0
                    0
                    0
                    BIT_MASK 0
                /end MEASUREMENT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].measurement[0], 'bit_mask')
    assert a2l.tree.project.module[0].measurement[0].bit_mask == 0


def test_measurement_bit_operation_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT
                    measurement_name 
                    "measurement long identifier"  
                    UWORD
                    conversion 
                    0
                    0
                    0
                    0
                    /begin BIT_OPERATION
                        LEFT_SHIFT 0
                    /end BIT_OPERATION
                /end MEASUREMENT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].measurement[0], 'bit_operation')
    assert a2l.tree.project.module[0].measurement[0].bit_operation is not None


def test_measurement_byte_order_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT
                    measurement_name 
                    "measurement long identifier"  
                    UWORD
                    conversion 
                    0
                    0
                    0
                    0
                    BYTE_ORDER MSB_FIRST
                /end MEASUREMENT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].measurement[0], 'byte_order')
    assert a2l.tree.project.module[0].measurement[0].byte_order == 'MSB_FIRST'


def test_measurement_max_refresh_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT
                    measurement_name 
                    "measurement long identifier"  
                    UWORD
                    conversion 
                    0
                    0
                    0
                    0
                    MAX_REFRESH 0 1
                /end MEASUREMENT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].measurement[0], 'max_refresh')
    assert a2l.tree.project.module[0].measurement[0].max_refresh is not None


def test_measurement_virtual_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT
                    measurement_name 
                    "measurement long identifier"  
                    UWORD
                    conversion 
                    0
                    0
                    0
                    0
                    /begin VIRTUAL
                        virtual
                    /end VIRTUAL
                /end MEASUREMENT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].measurement[0], 'virtual')
    assert a2l.tree.project.module[0].measurement[0].virtual is not None


def test_measurement_function_list_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT
                    measurement_name 
                    "measurement long identifier"  
                    UWORD
                    conversion 
                    0
                    0
                    0
                    0
                    /begin FUNCTION_LIST
                        first_function
                        second_function
                    /end FUNCTION_LIST
                /end MEASUREMENT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].measurement[0], 'function_list')
    assert a2l.tree.project.module[0].measurement[0].function_list is not None


def test_measurement_ecu_address_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT
                    measurement_name 
                    "measurement long identifier"  
                    UWORD
                    conversion 
                    0
                    0
                    0
                    0
                    ECU_ADDRESS 0
                /end MEASUREMENT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].measurement[0], 'ecu_address')
    assert a2l.tree.project.module[0].measurement[0].ecu_address == 0


def test_measurement_error_mask_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT
                    measurement_name 
                    "measurement long identifier"  
                    UWORD
                    conversion 
                    0
                    0
                    0
                    0
                    ERROR_MASK 0
                /end MEASUREMENT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].measurement[0], 'error_mask')
    assert a2l.tree.project.module[0].measurement[0].error_mask == 0


def test_measurement_ref_memory_segment_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT
                    measurement_name 
                    "measurement long identifier"  
                    UWORD
                    conversion 
                    0
                    0
                    0
                    0
                    REF_MEMORY_SEGMENT ref_memory_segment
                /end MEASUREMENT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].measurement[0], 'ref_memory_segment')
    assert a2l.tree.project.module[0].measurement[0].ref_memory_segment == 'ref_memory_segment'


def test_measurement_annotation_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT
                    measurement_name 
                    "measurement long identifier"  
                    UWORD
                    conversion 
                    0
                    0
                    0
                    0
                    /begin ANNOTATION
                    /end ANNOTATION
                /end MEASUREMENT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].measurement[0], 'annotation')
    assert a2l.tree.project.module[0].measurement[0].annotation is not None


def test_measurement_with_multiple_annotation_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT
                    measurement_name 
                    "measurement long identifier"  
                    UWORD
                    conversion 
                    0
                    0
                    0
                    0
                    /begin ANNOTATION
                    /end ANNOTATION
                    /begin ANNOTATION
                    /end ANNOTATION
                /end MEASUREMENT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert len(a2l.tree.project.module[0].measurement[0].annotation) == 2


def test_measurement_if_data_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT
                    measurement_name 
                    "measurement long identifier"  
                    UWORD
                    conversion 
                    0
                    0
                    0
                    0
                    /begin IF_DATA if_data
                    /end IF_DATA
                /end MEASUREMENT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].measurement[0], 'if_data_measurement')
    assert a2l.tree.project.module[0].measurement[0].if_data_measurement is not None


def test_measurement_with_multiple_if_data_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT
                    measurement_name 
                    "measurement long identifier"  
                    UWORD
                    conversion 
                    0
                    0
                    0
                    0
                    /begin IF_DATA first_if_data
                    /end IF_DATA
                    /begin IF_DATA second_if_data
                    /end IF_DATA
                /end MEASUREMENT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert len(a2l.tree.project.module[0].measurement[0].if_data_measurement) == 2


def test_measurement_matrix_dim_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT
                    measurement_name 
                    "measurement long identifier"  
                    UWORD
                    conversion 
                    0
                    0
                    0
                    0
                    MATRIX_DIM 0 1 2
                /end MEASUREMENT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].measurement[0], 'matrix_dim')
    assert a2l.tree.project.module[0].measurement[0].matrix_dim[0] == 0
    assert a2l.tree.project.module[0].measurement[0].matrix_dim[1] == 1
    assert a2l.tree.project.module[0].measurement[0].matrix_dim[2] == 2


def test_measurement_ecu_address_extension_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT
                    measurement_name 
                    "measurement long identifier"  
                    UWORD
                    conversion 
                    0
                    0
                    0
                    0
                    ECU_ADDRESS_EXTENSION 0
                /end MEASUREMENT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].measurement[0], 'ecu_address_extension')
    assert a2l.tree.project.module[0].measurement[0].ecu_address_extension == 0


def test_compu_method_formula_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin COMPU_METHOD compu_method_name "compu_method long identifier" TAB_INTP "%d" "-"
                    /begin FORMULA
                        "formula"
                    /end FORMULA
                /end COMPU_METHOD
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].compu_method[0], 'formula')
    assert a2l.tree.project.module[0].compu_method[0].formula.f == 'formula'


def test_compu_method_coeffs_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin COMPU_METHOD compu_method_name "compu_method long identifier" TAB_INTP "%d" "-"
                    COEFFS 0 1 2 3 4 5
                /end COMPU_METHOD
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].compu_method[0], 'coeffs')
    assert a2l.tree.project.module[0].compu_method[0].coeffs is not None


def test_compu_method_compu_tab_ref_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin COMPU_METHOD compu_method_name "compu_method long identifier" TAB_INTP "%d" "-"
                    COMPU_TAB_REF compu_tab_ref
                /end COMPU_METHOD
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].compu_method[0], 'compu_tab_ref')
    assert a2l.tree.project.module[0].compu_method[0].compu_tab_ref == 'compu_tab_ref'


def test_compu_method_ref_unit_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin COMPU_METHOD compu_method_name "compu_method long identifier" TAB_INTP "%d" "-"
                    REF_UNIT ref_unit
                /end COMPU_METHOD
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].compu_method[0], 'ref_unit')
    assert a2l.tree.project.module[0].compu_method[0].ref_unit == 'ref_unit'


def test_compu_tab():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin COMPU_TAB first_compu_tab_name "first compu_tab long identifier" TAB_INTP 1 2 3
                    DEFAULT_VALUE "default value"
                /end COMPU_TAB
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].compu_tab[0], 'default_value')
    assert a2l.tree.project.module[0].compu_tab[0].default_value == 'default value'
    assert a2l.tree.project.module[0].compu_tab[0].in_val_out_val[0] == 2
    assert a2l.tree.project.module[0].compu_tab[0].in_val_out_val[1] == 3


def test_compu_vtab():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin COMPU_VTAB 
                    compu_vtab_name 
                    "compu_vtab long identifier" 
                    TAB_VERB 
                    2 
                    0 "0"
                    1 "1"
                    DEFAULT_VALUE "default value"
                /end COMPU_VTAB
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].compu_vtab[0], 'default_value')
    assert a2l.tree.project.module[0].compu_vtab[0].default_value == 'default value'
    assert a2l.tree.project.module[0].compu_vtab[0].compu_vtab_in_val_out_val[0][0] == 0
    assert a2l.tree.project.module[0].compu_vtab[0].compu_vtab_in_val_out_val[0][1] == '0'
    assert a2l.tree.project.module[0].compu_vtab[0].compu_vtab_in_val_out_val[1][0] == 1
    assert a2l.tree.project.module[0].compu_vtab[0].compu_vtab_in_val_out_val[1][1] == '1'


def test_compu_vtab_range():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin COMPU_VTAB_RANGE
                    compu_tab_range_name 
                    "compu_tab_range long identifier"  
                    2 
                    0 1 "2"
                    3 4 "5"
                    DEFAULT_VALUE "default value"
                /end COMPU_VTAB_RANGE
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].compu_vtab_range[0], 'default_value')
    assert a2l.tree.project.module[0].compu_vtab_range[0].default_value == 'default value'
    assert a2l.tree.project.module[0].compu_vtab_range[0].compu_vtab_range_in_val_out_val[0][0] == 0
    assert a2l.tree.project.module[0].compu_vtab_range[0].compu_vtab_range_in_val_out_val[0][1] == 1
    assert a2l.tree.project.module[0].compu_vtab_range[0].compu_vtab_range_in_val_out_val[0][2] == '2'
    assert a2l.tree.project.module[0].compu_vtab_range[0].compu_vtab_range_in_val_out_val[1][0] == 3
    assert a2l.tree.project.module[0].compu_vtab_range[0].compu_vtab_range_in_val_out_val[1][1] == 4
    assert a2l.tree.project.module[0].compu_vtab_range[0].compu_vtab_range_in_val_out_val[1][2] == '5'


def test_function_annotation_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin FUNCTION first_function_name "first function long identifier"
                    /begin ANNOTATION
                    /end ANNOTATION
                /end FUNCTION
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].function[0], 'annotation')
    assert a2l.tree.project.module[0].function[0].annotation[0] is not None


def test_function_with_multiple_annotation_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin FUNCTION first_function_name "first function long identifier"
                    /begin ANNOTATION
                    /end ANNOTATION
                    /begin ANNOTATION
                    /end ANNOTATION
                /end FUNCTION
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert len(a2l.tree.project.module[0].function[0].annotation) == 2


def test_function_def_characteristic_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin FUNCTION first_function_name "first function long identifier"
                    /begin DEF_CHARACTERISTIC
                        first_def_characteristic
                        second_def_characteristic
                    /end DEF_CHARACTERISTIC
                /end FUNCTION
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].function[0], 'def_characteristic')
    assert a2l.tree.project.module[0].function[0].def_characteristic is not None


def test_function_ref_characteristic_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin FUNCTION first_function_name "first function long identifier"
                    /begin REF_CHARACTERISTIC
                        first_ref_characteristic
                        second_ref_characteristic
                    /end REF_CHARACTERISTIC
                /end FUNCTION
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].function[0], 'ref_characteristic')
    assert a2l.tree.project.module[0].function[0].ref_characteristic is not None


def test_function_in_measurement_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin FUNCTION first_function_name "first function long identifier"
                    /begin IN_MEASUREMENT
                        first_in_measurement
                        second_in_measurement
                    /end IN_MEASUREMENT
                /end FUNCTION
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].function[0], 'in_measurement')
    assert a2l.tree.project.module[0].function[0].in_measurement is not None


def test_function_out_measurement_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin FUNCTION first_function_name "first function long identifier"
                    /begin OUT_MEASUREMENT
                        first_out_measurement
                        second_out_measurement
                    /end OUT_MEASUREMENT
                /end FUNCTION
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].function[0], 'out_measurement')
    assert a2l.tree.project.module[0].function[0].out_measurement is not None


def test_function_loc_measurement_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin FUNCTION first_function_name "first function long identifier"
                    /begin LOC_MEASUREMENT
                        first_loc_measurement
                        second_loc_measurement
                    /end LOC_MEASUREMENT
                /end FUNCTION
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].function[0], 'loc_measurement')
    assert a2l.tree.project.module[0].function[0].loc_measurement is not None


def test_function_sub_function_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin FUNCTION first_function_name "first function long identifier"
                    /begin SUB_FUNCTION
                        first_sub_function
                        second_sub_function
                    /end SUB_FUNCTION
                /end FUNCTION
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].function[0], 'sub_function')
    assert a2l.tree.project.module[0].function[0].sub_function is not None


def test_function_function_version_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin FUNCTION first_function_name "first function long identifier"
                    FUNCTION_VERSION "function version"
                /end FUNCTION
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].function[0], 'function_version')
    assert a2l.tree.project.module[0].function[0].function_version == 'function version'


def test_group_annotation_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin GROUP first_group_name "first group long identifier"
                    /begin ANNOTATION
                    /end ANNOTATION
                /end GROUP
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].group[0], 'annotation')
    assert a2l.tree.project.module[0].group[0].annotation is not None


def test_group_with_multiple_annotation_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin GROUP first_group_name "first group long identifier"
                    /begin ANNOTATION
                    /end ANNOTATION
                    /begin ANNOTATION
                    /end ANNOTATION
                /end GROUP
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert len(a2l.tree.project.module[0].group[0].annotation) == 2


def test_group_root_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin GROUP first_group_name "first group long identifier"
                    ROOT
                /end GROUP
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].group[0], 'root')
    assert a2l.tree.project.module[0].group[0].root == 'ROOT'


def test_group_ref_characteristic_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin GROUP first_group_name "first group long identifier"
                    /begin REF_CHARACTERISTIC
                    /end REF_CHARACTERISTIC
                /end GROUP
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].group[0], 'ref_characteristic')
    assert a2l.tree.project.module[0].group[0].ref_characteristic is not None


def test_group_ref_measurement_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin GROUP first_group_name "first group long identifier"
                    /begin REF_MEASUREMENT
                    /end REF_MEASUREMENT
                /end GROUP
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].group[0], 'ref_measurement')
    assert a2l.tree.project.module[0].group[0].ref_measurement is not None


def test_group_function_list_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin GROUP first_group_name "first group long identifier"
                    /begin FUNCTION_LIST
                    /end FUNCTION_LIST
                /end GROUP
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].group[0], 'function_list')
    assert a2l.tree.project.module[0].group[0].function_list is not None


def test_group_sub_group_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin GROUP first_group_name "first group long identifier"
                    /begin SUB_GROUP
                    /end SUB_GROUP
                /end GROUP
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].group[0], 'sub_group')
    assert a2l.tree.project.module[0].group[0].sub_group is not None


def test_record_layout_fnc_values_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    FNC_VALUES 0 SWORD COLUMN_DIR DIRECT
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'fnc_values')
    assert a2l.tree.project.module[0].record_layout[0].fnc_values.position == 0
    assert a2l.tree.project.module[0].record_layout[0].fnc_values.data_type == 'SWORD'
    assert a2l.tree.project.module[0].record_layout[0].fnc_values.index_mode == 'COLUMN_DIR'
    assert a2l.tree.project.module[0].record_layout[0].fnc_values.addresstype == 'DIRECT'


def test_record_layout_identification_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    IDENTIFICATION 0 UWORD
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'identification')
    assert a2l.tree.project.module[0].record_layout[0].identification.position == 0
    assert a2l.tree.project.module[0].record_layout[0].identification.data_type == 'UWORD'


def test_record_layout_axis_pts_x_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    AXIS_PTS_X 0 ULONG INDEX_INCR DIRECT
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'axis_pts_x')
    assert a2l.tree.project.module[0].record_layout[0].axis_pts_x.position == 0
    assert a2l.tree.project.module[0].record_layout[0].axis_pts_x.data_type == 'ULONG'
    assert a2l.tree.project.module[0].record_layout[0].axis_pts_x.index_incr == 'INDEX_INCR'
    assert a2l.tree.project.module[0].record_layout[0].axis_pts_x.addressing == 'DIRECT'


def test_record_layout_axis_pts_y_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    AXIS_PTS_Y 0 ULONG INDEX_INCR DIRECT
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'axis_pts_y')
    assert a2l.tree.project.module[0].record_layout[0].axis_pts_y.position == 0
    assert a2l.tree.project.module[0].record_layout[0].axis_pts_y.data_type == 'ULONG'
    assert a2l.tree.project.module[0].record_layout[0].axis_pts_y.index_incr == 'INDEX_INCR'
    assert a2l.tree.project.module[0].record_layout[0].axis_pts_y.addressing == 'DIRECT'


def test_record_layout_axis_pts_z_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    AXIS_PTS_Z 0 ULONG INDEX_INCR DIRECT
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'axis_pts_z')
    assert a2l.tree.project.module[0].record_layout[0].axis_pts_z.position == 0
    assert a2l.tree.project.module[0].record_layout[0].axis_pts_z.data_type == 'ULONG'
    assert a2l.tree.project.module[0].record_layout[0].axis_pts_z.index_incr == 'INDEX_INCR'
    assert a2l.tree.project.module[0].record_layout[0].axis_pts_z.addressing == 'DIRECT'


def test_record_layout_axis_rescale_x_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    AXIS_RESCALE_X 0 ULONG 1 INDEX_INCR DIRECT
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'axis_rescale_x')
    assert a2l.tree.project.module[0].record_layout[0].axis_rescale_x.position == 0
    assert a2l.tree.project.module[0].record_layout[0].axis_rescale_x.data_type == 'ULONG'
    assert a2l.tree.project.module[0].record_layout[0].axis_rescale_x.max_number_of_rescale_pairs == 1
    assert a2l.tree.project.module[0].record_layout[0].axis_rescale_x.index_incr == 'INDEX_INCR'
    assert a2l.tree.project.module[0].record_layout[0].axis_rescale_x.addressing == 'DIRECT'


def test_record_layout_axis_rescale_y_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    AXIS_RESCALE_Y 0 ULONG 1 INDEX_INCR DIRECT
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'axis_rescale_y')
    assert a2l.tree.project.module[0].record_layout[0].axis_rescale_y.position == 0
    assert a2l.tree.project.module[0].record_layout[0].axis_rescale_y.data_type == 'ULONG'
    assert a2l.tree.project.module[0].record_layout[0].axis_rescale_y.max_number_of_rescale_pairs == 1
    assert a2l.tree.project.module[0].record_layout[0].axis_rescale_y.index_incr == 'INDEX_INCR'
    assert a2l.tree.project.module[0].record_layout[0].axis_rescale_y.addressing == 'DIRECT'


def test_record_layout_axis_rescale_z_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    AXIS_RESCALE_Z 0 ULONG 1 INDEX_INCR DIRECT
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'axis_rescale_z')
    assert a2l.tree.project.module[0].record_layout[0].axis_rescale_z.position == 0
    assert a2l.tree.project.module[0].record_layout[0].axis_rescale_z.data_type == 'ULONG'
    assert a2l.tree.project.module[0].record_layout[0].axis_rescale_z.max_number_of_rescale_pairs == 1
    assert a2l.tree.project.module[0].record_layout[0].axis_rescale_z.index_incr == 'INDEX_INCR'
    assert a2l.tree.project.module[0].record_layout[0].axis_rescale_z.addressing == 'DIRECT'


def test_record_layout_no_axis_pts_x_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    NO_AXIS_PTS_X 0 ULONG
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'no_axis_pts_x')
    assert a2l.tree.project.module[0].record_layout[0].no_axis_pts_x.position == 0
    assert a2l.tree.project.module[0].record_layout[0].no_axis_pts_x.data_type == 'ULONG'


def test_record_layout_no_axis_pts_y_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    NO_AXIS_PTS_Y 0 ULONG
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'no_axis_pts_y')
    assert a2l.tree.project.module[0].record_layout[0].no_axis_pts_y.position == 0
    assert a2l.tree.project.module[0].record_layout[0].no_axis_pts_y.data_type == 'ULONG'


def test_record_layout_no_axis_pts_z_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    NO_AXIS_PTS_Z 0 ULONG
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'no_axis_pts_z')
    assert a2l.tree.project.module[0].record_layout[0].no_axis_pts_z.position == 0
    assert a2l.tree.project.module[0].record_layout[0].no_axis_pts_z.data_type == 'ULONG'


def test_record_layout_no_rescale_x_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    NO_RESCALE_X 0 ULONG
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'no_rescale_x')
    assert a2l.tree.project.module[0].record_layout[0].no_rescale_x.position == 0
    assert a2l.tree.project.module[0].record_layout[0].no_rescale_x.data_type == 'ULONG'


def test_record_layout_no_rescale_y_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    NO_RESCALE_Y 0 ULONG
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'no_rescale_y')
    assert a2l.tree.project.module[0].record_layout[0].no_rescale_y.position == 0
    assert a2l.tree.project.module[0].record_layout[0].no_rescale_y.data_type == 'ULONG'


def test_record_layout_no_rescale_z_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    NO_RESCALE_Z 0 ULONG
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'no_rescale_z')
    assert a2l.tree.project.module[0].record_layout[0].no_rescale_z.position == 0
    assert a2l.tree.project.module[0].record_layout[0].no_rescale_z.data_type == 'ULONG'


def test_record_layout_fix_no_axis_pts_x_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    FIX_NO_AXIS_PTS_X 0
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'fix_no_axis_pts_x')
    assert a2l.tree.project.module[0].record_layout[0].fix_no_axis_pts_x.number_of_axis_points == 0


def test_record_layout_fix_no_axis_pts_y_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    FIX_NO_AXIS_PTS_Y 0
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'fix_no_axis_pts_y')
    assert a2l.tree.project.module[0].record_layout[0].fix_no_axis_pts_y.number_of_axis_points == 0


def test_record_layout_fix_no_axis_pts_z_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    FIX_NO_AXIS_PTS_Z 0
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'fix_no_axis_pts_z')
    assert a2l.tree.project.module[0].record_layout[0].fix_no_axis_pts_z.number_of_axis_points == 0


def test_record_layout_src_addr_x_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    SRC_ADDR_X 0 ULONG
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'src_addr_x')
    assert a2l.tree.project.module[0].record_layout[0].src_addr_x.position == 0
    assert a2l.tree.project.module[0].record_layout[0].src_addr_x.data_type == 'ULONG'


def test_record_layout_src_addr_y_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    SRC_ADDR_Y 0 ULONG
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'src_addr_y')
    assert a2l.tree.project.module[0].record_layout[0].src_addr_y.position == 0
    assert a2l.tree.project.module[0].record_layout[0].src_addr_y.data_type == 'ULONG'


def test_record_layout_src_addr_z_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    SRC_ADDR_Z 0 ULONG
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'src_addr_z')
    assert a2l.tree.project.module[0].record_layout[0].src_addr_z.position == 0
    assert a2l.tree.project.module[0].record_layout[0].src_addr_z.data_type == 'ULONG'


def test_record_layout_rip_addr_x_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    RIP_ADDR_X 0 ULONG
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'rip_addr_x')
    assert a2l.tree.project.module[0].record_layout[0].rip_addr_x.position == 0
    assert a2l.tree.project.module[0].record_layout[0].rip_addr_x.data_type == 'ULONG'


def test_record_layout_rip_addr_y_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    RIP_ADDR_Y 0 ULONG
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'rip_addr_y')
    assert a2l.tree.project.module[0].record_layout[0].rip_addr_y.position == 0
    assert a2l.tree.project.module[0].record_layout[0].rip_addr_y.data_type == 'ULONG'


def test_record_layout_rip_addr_z_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    RIP_ADDR_Z 0 ULONG
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'rip_addr_z')
    assert a2l.tree.project.module[0].record_layout[0].rip_addr_z.position == 0
    assert a2l.tree.project.module[0].record_layout[0].rip_addr_z.data_type == 'ULONG'


def test_record_layout_rip_addr_w_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    RIP_ADDR_W 0 ULONG
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'rip_addr_w')
    assert a2l.tree.project.module[0].record_layout[0].rip_addr_w.position == 0
    assert a2l.tree.project.module[0].record_layout[0].rip_addr_w.data_type == 'ULONG'


def test_record_layout_shift_op_x_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    SHIFT_OP_X 0 ULONG
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'shift_op_x')
    assert a2l.tree.project.module[0].record_layout[0].shift_op_x.position == 0
    assert a2l.tree.project.module[0].record_layout[0].shift_op_x.data_type == 'ULONG'


def test_record_layout_shift_op_y_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    SHIFT_OP_Y 0 ULONG
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'shift_op_y')
    assert a2l.tree.project.module[0].record_layout[0].shift_op_y.position == 0
    assert a2l.tree.project.module[0].record_layout[0].shift_op_y.data_type == 'ULONG'


def test_record_layout_shift_op_z_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    SHIFT_OP_Z 0 ULONG
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'shift_op_z')
    assert a2l.tree.project.module[0].record_layout[0].shift_op_z.position == 0
    assert a2l.tree.project.module[0].record_layout[0].shift_op_z.data_type == 'ULONG'


def test_record_layout_offset_x_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    OFFSET_X 0 ULONG
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'offset_x')
    assert a2l.tree.project.module[0].record_layout[0].offset_x.position == 0
    assert a2l.tree.project.module[0].record_layout[0].offset_x.data_type == 'ULONG'


def test_record_layout_offset_y_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    OFFSET_Y 0 ULONG
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'offset_y')
    assert a2l.tree.project.module[0].record_layout[0].offset_y.position == 0
    assert a2l.tree.project.module[0].record_layout[0].offset_y.data_type == 'ULONG'


def test_record_layout_offset_z_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    OFFSET_Z 0 ULONG
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'offset_z')
    assert a2l.tree.project.module[0].record_layout[0].offset_z.position == 0
    assert a2l.tree.project.module[0].record_layout[0].offset_z.data_type == 'ULONG'


def test_record_layout_dist_op_x_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    DIST_OP_X 0 ULONG
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'dist_op_x')
    assert a2l.tree.project.module[0].record_layout[0].dist_op_x.position == 0
    assert a2l.tree.project.module[0].record_layout[0].dist_op_x.data_type == 'ULONG'


def test_record_layout_dist_op_y_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    DIST_OP_Y 0 ULONG
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'dist_op_y')
    assert a2l.tree.project.module[0].record_layout[0].dist_op_y.position == 0
    assert a2l.tree.project.module[0].record_layout[0].dist_op_y.data_type == 'ULONG'


def test_record_layout_dist_op_z_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    DIST_OP_Z 0 ULONG
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'dist_op_z')
    assert a2l.tree.project.module[0].record_layout[0].dist_op_z.position == 0
    assert a2l.tree.project.module[0].record_layout[0].dist_op_z.data_type == 'ULONG'


def test_record_layout_alignment_byte_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    ALIGNMENT_BYTE 0
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'alignment_byte')
    assert a2l.tree.project.module[0].record_layout[0].alignment_byte == 0


def test_record_layout_alignment_word_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    ALIGNMENT_WORD 0
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'alignment_word')
    assert a2l.tree.project.module[0].record_layout[0].alignment_word == 0


def test_record_layout_alignment_long_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    ALIGNMENT_LONG 0
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'alignment_long')
    assert a2l.tree.project.module[0].record_layout[0].alignment_long == 0


def test_record_layout_alignment_float32_ieee_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    ALIGNMENT_FLOAT32_IEEE 0
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'alignment_float32_ieee')
    assert a2l.tree.project.module[0].record_layout[0].alignment_float32_ieee == 0


def test_record_layout_alignment_float64_ieee_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    ALIGNMENT_FLOAT64_IEEE 0
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'alignment_float64_ieee')
    assert a2l.tree.project.module[0].record_layout[0].alignment_float64_ieee == 0


def test_record_layout_reserved_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    RESERVED 0 LONG
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].record_layout[0], 'reserved')
    assert a2l.tree.project.module[0].record_layout[0].reserved[0].position == 0
    assert a2l.tree.project.module[0].record_layout[0].reserved[0].data_size == 'LONG'


def test_record_layout_with_multiple_reserverd_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin RECORD_LAYOUT record_layout_name
                    RESERVED 0 LONG
                    RESERVED 0 LONG
                /end RECORD_LAYOUT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert len(a2l.tree.project.module[0].record_layout[0].reserved) == 2


def test_variant_coding_var_separator_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin VARIANT_CODING
                    VAR_SEPARATOR "var separator"
                /end VARIANT_CODING
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].variant_coding, 'var_separator')
    assert a2l.tree.project.module[0].variant_coding.var_separator == 'var separator'


def test_variant_coding_var_naming_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin VARIANT_CODING
                    VAR_NAMING var_naming
                /end VARIANT_CODING
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].variant_coding, 'var_naming')
    assert a2l.tree.project.module[0].variant_coding.var_naming == 'var_naming'


def test_variant_coding_var_criterion_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin VARIANT_CODING
                    /begin VAR_CRITERION
                        var_criterion_name "var_criterion long identifier"
                            first_var_criterion
                            second_var_criterion
                    /end VAR_CRITERION
                /end VARIANT_CODING
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].variant_coding, 'var_criterion')
    assert a2l.tree.project.module[0].variant_coding.var_criterion[0].name == 'var_criterion_name'


def test_variant_coding_with_multiple_var_criterion_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin VARIANT_CODING
                    /begin VAR_CRITERION
                        first_var_criterion_name "first var_criterion long identifier"
                            first_var_criterion
                            second_var_criterion
                    /end VAR_CRITERION
                    /begin VAR_CRITERION
                        second_var_criterion_name "second var_criterion long identifier"
                            first_var_criterion
                            second_var_criterion
                    /end VAR_CRITERION
                /end VARIANT_CODING
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert len(a2l.tree.project.module[0].variant_coding.var_criterion) == 2


def test_variant_coding_var_forbidden_comb_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin VARIANT_CODING
                    /begin VAR_FORBIDDEN_COMB
                        var_forbidden_comb_name var_forbidden_comb_value
                    /end VAR_FORBIDDEN_COMB
                /end VARIANT_CODING
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].variant_coding, 'var_forbidden_comb')
    assert a2l.tree.project.module[0].variant_coding.var_forbidden_comb is not None


def test_variant_coding_with_multiple_var_forbidden_comb_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin VARIANT_CODING
                    /begin VAR_FORBIDDEN_COMB
                        var_forbidden_comb_name var_forbidden_comb_value
                    /end VAR_FORBIDDEN_COMB
                    /begin VAR_FORBIDDEN_COMB
                        var_forbidden_comb_name var_forbidden_comb_value
                    /end VAR_FORBIDDEN_COMB
                /end VARIANT_CODING
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert len(a2l.tree.project.module[0].variant_coding.var_forbidden_comb) == 2


def test_variant_coding_var_characteristic_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin VARIANT_CODING
                    /begin VAR_CHARACTERISTIC
                        var_characteristic_name
                        first_var_characteristic_criterion_name
                        second_var_characteristic_criterion_name
                    /end VAR_CHARACTERISTIC
                /end VARIANT_CODING
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].variant_coding, 'var_characteristic')
    assert a2l.tree.project.module[0].variant_coding.var_characteristic is not None


def test_variant_coding_with_multiple_var_characteristic_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin VARIANT_CODING
                    /begin VAR_CHARACTERISTIC
                        first_var_characteristic_name
                        first_var_characteristic_criterion_name
                        second_var_characteristic_criterion_name
                    /end VAR_CHARACTERISTIC
                    /begin VAR_CHARACTERISTIC
                        second_var_characteristic_name
                        first_var_characteristic_criterion_name
                        second_var_characteristic_criterion_name
                    /end VAR_CHARACTERISTIC
                /end VARIANT_CODING
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert len(a2l.tree.project.module[0].variant_coding.var_characteristic) == 2


def test_frame_frame_measurement_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin FRAME frame_name "frame long identifier" 0 0
                    FRAME_MEASUREMENT first_identifier second_identifier
                /end FRAME
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].frame, 'frame_measurement')
    assert a2l.tree.project.module[0].frame is not None


def test_frame_if_data_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin FRAME frame_name "frame long identifier" 0 0
                    /begin IF_DATA if_data
                    /end IF_DATA
                /end FRAME
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].frame, 'if_data_frame')
    assert a2l.tree.project.module[0].frame.if_data_frame is not None


def test_frame_with_multiple_if_data_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin FRAME frame_name "frame long identifier" 0 0
                    /begin IF_DATA first_if_data
                    /end IF_DATA
                    /begin IF_DATA second_if_data
                    /end IF_DATA
                /end FRAME
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert len(a2l.tree.project.module[0].frame.if_data_frame) == 2


def test_user_rights_ref_group_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin USER_RIGHTS first_user_rights
                    /begin REF_GROUP
                    /end REF_GROUP
                /end USER_RIGHTS
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0], 'user_rights')
    assert a2l.tree.project.module[0].user_rights is not None


def test_user_rights_with_multiple_ref_group_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin USER_RIGHTS first_user_rights
                    /begin REF_GROUP
                    /end REF_GROUP
                    /begin REF_GROUP
                    /end REF_GROUP
                /end USER_RIGHTS
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert len(a2l.tree.project.module[0].user_rights[0].ref_group) == 2


def test_user_rights_read_only_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin USER_RIGHTS first_user_rights
                    READ_ONLY
                /end USER_RIGHTS
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].user_rights[0], 'read_only')
    assert a2l.tree.project.module[0].user_rights[0].read_only == 'READ_ONLY'


def test_unit_si_exponents_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin UNIT first_unit "first unit long identifier" "-" DERIVED
                    SI_EXPONENTS 0 -1 0 1 0 0 0
                /end UNIT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].unit[0], 'si_exponents')
    assert a2l.tree.project.module[0].unit[0].si_exponents is not None


def test_unit_ref_unit_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin UNIT first_unit "first unit long identifier" "-" DERIVED
                    REF_UNIT ref_unit
                /end UNIT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].unit[0], 'ref_unit')
    assert a2l.tree.project.module[0].unit[0].ref_unit is not None


def test_unit_unit_conversion_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin UNIT first_unit "first unit long identifier" "-" DERIVED
                    UNIT_CONVERSION 0 1
                /end UNIT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].unit[0], 'unit_conversion')
    assert a2l.tree.project.module[0].unit[0].unit_conversion is not None


# TODO: implement tests for BIT_OPERATION.


def test_unit_conversion_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin UNIT first_unit "first unit long identifier" "-" DERIVED
                    UNIT_CONVERSION 0 1
                /end UNIT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].unit[0].unit_conversion.gradient == 0
    assert a2l.tree.project.module[0].unit[0].unit_conversion.offset == 1


def test_ref_group():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin USER_RIGHTS first_user_rights
                    /begin REF_GROUP
                        first_identifier
                        second_identifier
                    /end REF_GROUP
                /end USER_RIGHTS
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].user_rights[0].ref_group[0].identifier[0] == 'first_identifier'
    assert a2l.tree.project.module[0].user_rights[0].ref_group[0].identifier[1] == 'second_identifier'


def test_frame_measurement():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin FRAME frame_name "frame long identifier" 0 0
                    FRAME_MEASUREMENT first_identifier second_identifier
                /end FRAME
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].frame.frame_measurement.identifier[0] == 'first_identifier'
    assert a2l.tree.project.module[0].frame.frame_measurement.identifier[1] == 'second_identifier'


def test_var_characteristic():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin VARIANT_CODING
                    /begin VAR_CHARACTERISTIC var_characteristic_name
                        first_var_characteristic_criterion_name
                        second_var_characteristic_criterion_name
                    /end VAR_CHARACTERISTIC
                /end VARIANT_CODING
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].variant_coding.var_characteristic[0].name == 'var_characteristic_name'
    assert a2l.tree.project.module[0].variant_coding.var_characteristic[0].criterion_name[
               0] == 'first_var_characteristic_criterion_name'
    assert a2l.tree.project.module[0].variant_coding.var_characteristic[0].criterion_name[
               1] == 'second_var_characteristic_criterion_name'


def test_var_characteristic_var_address_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin VARIANT_CODING
                    /begin VAR_CHARACTERISTIC var_characteristic_name
                        first_var_characteristic_criterion_name
                        second_var_characteristic_criterion_name
                        /begin VAR_ADDRESS
                            0
                        /end VAR_ADDRESS
                    /end VAR_CHARACTERISTIC
                /end VARIANT_CODING
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].variant_coding.var_characteristic[0], 'var_address')
    assert a2l.tree.project.module[0].variant_coding.var_characteristic[0].var_address is not None


def test_var_address():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin VARIANT_CODING
                    /begin VAR_CHARACTERISTIC var_characteristic_name
                        first_var_characteristic_criterion_name
                        second_var_characteristic_criterion_name
                        /begin VAR_ADDRESS
                            0
                            1
                        /end VAR_ADDRESS
                    /end VAR_CHARACTERISTIC
                /end VARIANT_CODING
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].variant_coding.var_characteristic[0].var_address.address[0] == 0
    assert a2l.tree.project.module[0].variant_coding.var_characteristic[0].var_address.address[1] == 1


def test_var_criterion():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin VARIANT_CODING
                    /begin VAR_CRITERION
                        var_criterion_name "var_criterion long identifier"
                            first_var_criterion
                            second_var_criterion
                    /end VAR_CRITERION
                /end VARIANT_CODING
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].variant_coding.var_criterion[0].value[0] == 'first_var_criterion'
    assert a2l.tree.project.module[0].variant_coding.var_criterion[0].value[1] == 'second_var_criterion'


def test_var_forbidden_comb():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin VARIANT_CODING
                    /begin VAR_FORBIDDEN_COMB
                        first_var_forbidden_comb_name first_var_forbidden_comb_value
                        second_var_forbidden_comb_name second_var_forbidden_comb_value
                    /end VAR_FORBIDDEN_COMB
                /end VARIANT_CODING
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].variant_coding.var_forbidden_comb[0].criterion_name[
               0] == 'first_var_forbidden_comb_name'
    assert a2l.tree.project.module[0].variant_coding.var_forbidden_comb[0].criterion_value[
               0] == 'first_var_forbidden_comb_value'
    assert a2l.tree.project.module[0].variant_coding.var_forbidden_comb[0].criterion_name[
               1] == 'second_var_forbidden_comb_name'
    assert a2l.tree.project.module[0].variant_coding.var_forbidden_comb[0].criterion_value[
               1] == 'second_var_forbidden_comb_value'


def test_var_criterion_var_measurement_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin VARIANT_CODING
                    /begin VAR_CRITERION
                        var_criterion_name "var_criterion long identifier"
                            first_var_criterion
                            second_var_criterion
                            VAR_MEASUREMENT var_measurement
                    /end VAR_CRITERION
                /end VARIANT_CODING
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].variant_coding.var_criterion[0], 'var_measurement')
    assert a2l.tree.project.module[0].variant_coding.var_criterion[0].var_measurement == 'var_measurement'


def test_var_criterion_var_selection_characteristic_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin VARIANT_CODING
                    /begin VAR_CRITERION
                        var_criterion_name "var_criterion long identifier"
                            first_var_criterion
                            second_var_criterion
                            VAR_SELECTION_CHARACTERISTIC var_selection_characteristic
                    /end VAR_CRITERION
                /end VARIANT_CODING
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].variant_coding.var_criterion[0], 'var_selection_characteristic')
    assert a2l.tree.project.module[0].variant_coding.var_criterion[
               0].var_selection_characteristic == 'var_selection_characteristic'


def test_formula_formula_inv_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin COMPU_METHOD compu_method_name "compu_method long identifier" TAB_INTP "%d" "-"
                    /begin FORMULA
                        "formula"
                        FORMULA_INV "formula inv"
                    /end FORMULA
                /end COMPU_METHOD
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].compu_method[0].formula.formula_inv == 'formula inv'


def test_def_characteristic():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin FUNCTION first_function_name "first function long identifier"
                    /begin DEF_CHARACTERISTIC
                        first_def_characteristic
                        second_def_characteristic
                    /end DEF_CHARACTERISTIC
                /end FUNCTION
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].function[0].def_characteristic.identifier[0] == 'first_def_characteristic'
    assert a2l.tree.project.module[0].function[0].def_characteristic.identifier[1] == 'second_def_characteristic'


def test_ref_characteristic():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin FUNCTION first_function_name "first function long identifier"
                    /begin REF_CHARACTERISTIC
                        first_ref_characteristic
                        second_ref_characteristic
                    /end REF_CHARACTERISTIC
                /end FUNCTION
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].function[0].ref_characteristic.identifier[0] == 'first_ref_characteristic'
    assert a2l.tree.project.module[0].function[0].ref_characteristic.identifier[1] == 'second_ref_characteristic'


def test_in_measurement():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin FUNCTION first_function_name "first function long identifier"
                    /begin IN_MEASUREMENT
                        first_in_measurement
                        second_in_measurement
                    /end IN_MEASUREMENT
                /end FUNCTION
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].function[0].in_measurement.identifier[0] == 'first_in_measurement'
    assert a2l.tree.project.module[0].function[0].in_measurement.identifier[1] == 'second_in_measurement'


def test_out_measurement():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin FUNCTION first_function_name "first function long identifier"
                    /begin OUT_MEASUREMENT
                        first_out_measurement
                        second_out_measurement
                    /end OUT_MEASUREMENT
                /end FUNCTION
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].function[0].out_measurement.identifier[0] == 'first_out_measurement'
    assert a2l.tree.project.module[0].function[0].out_measurement.identifier[1] == 'second_out_measurement'


def test_loc_measurement():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin FUNCTION first_function_name "first function long identifier"
                    /begin LOC_MEASUREMENT
                        first_loc_measurement
                        second_loc_measurement
                    /end LOC_MEASUREMENT
                /end FUNCTION
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].function[0].loc_measurement.identifier[0] == 'first_loc_measurement'
    assert a2l.tree.project.module[0].function[0].loc_measurement.identifier[1] == 'second_loc_measurement'


def test_sub_function():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin FUNCTION first_function_name "first function long identifier"
                    /begin SUB_FUNCTION
                        first_sub_function
                        second_sub_function
                    /end SUB_FUNCTION
                /end FUNCTION
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].function[0].sub_function.identifier[0] == 'first_sub_function'
    assert a2l.tree.project.module[0].function[0].sub_function.identifier[1] == 'second_sub_function'


def test_ref_measurement():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin GROUP first_group_name "first group long identifier"
                    /begin REF_MEASUREMENT
                        first_ref_measurement
                        second_ref_measurement
                    /end REF_MEASUREMENT
                /end GROUP
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].group[0].ref_measurement.identifier[0] == 'first_ref_measurement'
    assert a2l.tree.project.module[0].group[0].ref_measurement.identifier[1] == 'second_ref_measurement'


def test_sub_group():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin GROUP first_group_name "first group long identifier"
                    /begin SUB_GROUP
                        first_sub_group
                        second_sub_group
                    /end SUB_GROUP
                /end GROUP
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].group[0].sub_group.identifier[0] == 'first_sub_group'
    assert a2l.tree.project.module[0].group[0].sub_group.identifier[1] == 'second_sub_group'


def test_coeffs():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin COMPU_METHOD compu_method_name "compu_method long identifier" TAB_INTP "%d" "-"
                    COEFFS 0 1 2 3 4 5
                /end COMPU_METHOD
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].compu_method[0].coeffs.a == 0
    assert a2l.tree.project.module[0].compu_method[0].coeffs.b == 1
    assert a2l.tree.project.module[0].compu_method[0].coeffs.c == 2
    assert a2l.tree.project.module[0].compu_method[0].coeffs.d == 3
    assert a2l.tree.project.module[0].compu_method[0].coeffs.e == 4
    assert a2l.tree.project.module[0].compu_method[0].coeffs.f == 5


def test_max_refresh():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin MEASUREMENT
                    measurement_name 
                    "measurement long identifier"  
                    UWORD
                    conversion 
                    0
                    0
                    0
                    0
                    MAX_REFRESH 0 1
                /end MEASUREMENT
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].measurement[0].max_refresh.scaling_unit == 0
    assert a2l.tree.project.module[0].measurement[0].max_refresh.rate == 1


def test_function_list():
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
                    /begin FUNCTION_LIST
                        first_function
                        second_function
                    /end FUNCTION_LIST
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].characteristic[0].function_list.name[0] == 'first_function'
    assert a2l.tree.project.module[0].characteristic[0].function_list.name[1] == 'second_function'


def test_map_list():
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
                    /begin MAP_LIST
                        first_map
                        second_map
                    /end MAP_LIST
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].characteristic[0].map_list[0] == 'first_map'
    assert a2l.tree.project.module[0].characteristic[0].map_list[1] == 'second_map'


def test_dependent_characteristic():
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
                    /begin DEPENDENT_CHARACTERISTIC
                        "formula"
                        first_characteristic
                        second_characteristic
                    /end DEPENDENT_CHARACTERISTIC
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].characteristic[0].dependent_characteristic.formula == 'formula'
    assert a2l.tree.project.module[0].characteristic[0].dependent_characteristic.characteristic[
               0] == 'first_characteristic'
    assert a2l.tree.project.module[0].characteristic[0].dependent_characteristic.characteristic[
               1] == 'second_characteristic'


def test_virtual_characteristic():
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
                    /begin VIRTUAL_CHARACTERISTIC
                        "formula"
                        first_characteristic
                        second_characteristic
                    /end VIRTUAL_CHARACTERISTIC
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].characteristic[0].virtual_characteristic.formula == 'formula'
    assert a2l.tree.project.module[0].characteristic[0].virtual_characteristic.characteristic[
               0] == 'first_characteristic'
    assert a2l.tree.project.module[0].characteristic[0].virtual_characteristic.characteristic[
               1] == 'second_characteristic'


def test_annotation():
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
                    /begin ANNOTATION
                    /end ANNOTATION
                    /begin ANNOTATION
                        ANNOTATION_LABEL "annotation label"
                        ANNOTATION_ORIGIN "annotation origin"
                        /begin ANNOTATION_TEXT 
                            "first annotation text"
                            "second annotation text"
                        /end ANNOTATION_TEXT
                    /end ANNOTATION
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].characteristic[0].annotation[0].annotation_label == None
    assert a2l.tree.project.module[0].characteristic[0].annotation[0].annotation_origin == None
    assert a2l.tree.project.module[0].characteristic[0].annotation[0].annotation_text == None
    assert a2l.tree.project.module[0].characteristic[0].annotation[1].annotation_label == 'annotation label'
    assert a2l.tree.project.module[0].characteristic[0].annotation[1].annotation_origin == 'annotation origin'
    assert a2l.tree.project.module[0].characteristic[0].annotation[1].annotation_text is not None


def test_annotation_text():
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
                    /begin ANNOTATION
                        /begin ANNOTATION_TEXT 
                            "first annotation text"
                            "second annotation text"
                        /end ANNOTATION_TEXT
                    /end ANNOTATION
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].characteristic[0].annotation[0].annotation_text.annotation_text[
               0] == 'first annotation text'
    assert a2l.tree.project.module[0].characteristic[0].annotation[0].annotation_text.annotation_text[
               1] == 'second annotation text'


def test_axis_descr_read_only_node():
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
                    /begin AXIS_DESCR STD_AXIS input_quantity conversion 0 0 0
                        READ_ONLY
                    /end AXIS_DESCR
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0].axis_descr[0], 'read_only')
    assert a2l.tree.project.module[0].characteristic[0].axis_descr[0].read_only == 'READ_ONLY'


def test_axis_descr_format_node():
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
                    /begin AXIS_DESCR STD_AXIS input_quantity conversion 0 0 0
                        FORMAT "%d"
                    /end AXIS_DESCR
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0].axis_descr[0], 'format')
    assert a2l.tree.project.module[0].characteristic[0].axis_descr[0].format == '%d'


def test_axis_descr_annotation_node():
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
                    /begin AXIS_DESCR STD_AXIS input_quantity conversion 0 0 0
                        /begin ANNOTATION
                        /end ANNOTATION
                    /end AXIS_DESCR
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0].axis_descr[0], 'annotation')


def test_axis_descr_with_multiple_annotation_node():
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
                    /begin AXIS_DESCR STD_AXIS input_quantity conversion 0 0 0
                        /begin ANNOTATION
                        /end ANNOTATION
                        /begin ANNOTATION
                        /end ANNOTATION
                    /end AXIS_DESCR
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert len(a2l.tree.project.module[0].characteristic[0].axis_descr[0].annotation) == 2


def test_axis_descr_axis_pts_ref_node():
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
                    /begin AXIS_DESCR STD_AXIS input_quantity conversion 0 0 0
                        AXIS_PTS_REF axis_pts_ref
                    /end AXIS_DESCR
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0].axis_descr[0], 'axis_pts_ref')
    assert a2l.tree.project.module[0].characteristic[0].axis_descr[0].axis_pts_ref == 'axis_pts_ref'


def test_axis_descr_max_grad_node():
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
                    /begin AXIS_DESCR STD_AXIS input_quantity conversion 0 0 0
                        MAX_GRAD 0
                    /end AXIS_DESCR
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0].axis_descr[0], 'max_grad')
    assert a2l.tree.project.module[0].characteristic[0].axis_descr[0].max_grad == 0


def test_axis_descr_monotony_node():
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
                    /begin AXIS_DESCR STD_AXIS input_quantity conversion 0 0 0
                        MONOTONY MON_INCREASE
                    /end AXIS_DESCR
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0].axis_descr[0], 'monotony')
    assert a2l.tree.project.module[0].characteristic[0].axis_descr[0].monotony == 'MON_INCREASE'


def test_axis_descr_byte_order_node():
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
                    /begin AXIS_DESCR STD_AXIS input_quantity conversion 0 0 0
                        BYTE_ORDER MSB_LAST
                    /end AXIS_DESCR
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0].axis_descr[0], 'byte_order')
    assert a2l.tree.project.module[0].characteristic[0].axis_descr[0].byte_order == 'MSB_LAST'


def test_axis_descr_extended_limits_node():
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
                    /begin AXIS_DESCR STD_AXIS input_quantity conversion 0 0 0
                        EXTENDED_LIMITS 0 1
                    /end AXIS_DESCR
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0].axis_descr[0], 'extended_limits')
    assert a2l.tree.project.module[0].characteristic[0].axis_descr[0].extended_limits[0] == 0
    assert a2l.tree.project.module[0].characteristic[0].axis_descr[0].extended_limits[1] == 1


def test_axis_descr_fix_axis_par_node():
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
                    /begin AXIS_DESCR STD_AXIS input_quantity conversion 0 0 0
                        FIX_AXIS_PAR 0 1 2
                    /end AXIS_DESCR
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0].axis_descr[0], 'fix_axis_par')
    assert a2l.tree.project.module[0].characteristic[0].axis_descr[0].fix_axis_par is not None


def test_axis_descr_fix_axis_par_dist_node():
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
                    /begin AXIS_DESCR STD_AXIS input_quantity conversion 0 0 0
                        FIX_AXIS_PAR_DIST 0 1 2
                    /end AXIS_DESCR
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0].axis_descr[0], 'fix_axis_par_dist')
    assert a2l.tree.project.module[0].characteristic[0].axis_descr[0].fix_axis_par_dist is not None


def test_axis_descr_fix_axis_par_list_node():
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
                    /begin AXIS_DESCR STD_AXIS input_quantity conversion 0 0 0
                        /begin FIX_AXIS_PAR_LIST
                            0 1 2
                        /end FIX_AXIS_PAR_LIST
                    /end AXIS_DESCR
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0].axis_descr[0], 'fix_axis_par_list')
    assert a2l.tree.project.module[0].characteristic[0].axis_descr[0].fix_axis_par_list is not None


def test_axis_descr_deposit_node():
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
                    /begin AXIS_DESCR STD_AXIS input_quantity conversion 0 0 0
                        DEPOSIT ABSOLUTE
                    /end AXIS_DESCR
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0].axis_descr[0], 'deposit')
    assert a2l.tree.project.module[0].characteristic[0].axis_descr[0].deposit == 'ABSOLUTE'


def test_axis_descr_curve_axis_ref_node():
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
                    /begin AXIS_DESCR STD_AXIS input_quantity conversion 0 0 0
                        CURVE_AXIS_REF curve_axis_ref
                    /end AXIS_DESCR
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].characteristic[0].axis_descr[0], 'curve_axis_ref')
    assert a2l.tree.project.module[0].characteristic[0].axis_descr[0].curve_axis_ref == 'curve_axis_ref'


def test_fix_axis_par():
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
                    /begin AXIS_DESCR STD_AXIS input_quantity conversion 0 0 0
                        FIX_AXIS_PAR 0 1 2
                    /end AXIS_DESCR
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].characteristic[0].axis_descr[0].fix_axis_par.offset == 0
    assert a2l.tree.project.module[0].characteristic[0].axis_descr[0].fix_axis_par.shift == 1
    assert a2l.tree.project.module[0].characteristic[0].axis_descr[0].fix_axis_par.numberapo == 2


def test_fix_axis_par_dist():
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
                    /begin AXIS_DESCR STD_AXIS input_quantity conversion 0 0 0
                        FIX_AXIS_PAR_DIST 0 1 2
                    /end AXIS_DESCR
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].characteristic[0].axis_descr[0].fix_axis_par_dist.offset == 0
    assert a2l.tree.project.module[0].characteristic[0].axis_descr[0].fix_axis_par_dist.distance == 1
    assert a2l.tree.project.module[0].characteristic[0].axis_descr[0].fix_axis_par_dist.numberapo == 2


def test_fix_axis_par_list():
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
                    /begin AXIS_DESCR STD_AXIS input_quantity conversion 0 0 0
                        /begin FIX_AXIS_PAR_LIST
                            0 1 2
                        /end FIX_AXIS_PAR_LIST
                    /end AXIS_DESCR
                /end CHARACTERISTIC
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert a2l.tree.project.module[0].characteristic[0].axis_descr[0].fix_axis_par_list[0] == 0
    assert a2l.tree.project.module[0].characteristic[0].axis_descr[0].fix_axis_par_list[1] == 1
    assert a2l.tree.project.module[0].characteristic[0].axis_descr[0].fix_axis_par_list[2] == 2


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
    assert len(a2l.get_node('PROJECT')) == 1
    assert len(a2l.get_node('MODULE')) == 1
    assert len(a2l.get_node('CHARACTERISTIC')) == 2
    assert len(a2l.get_node('MEASUREMENT')) == 0


def test_get_properties():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert set(a2l.tree.project.properties) == set(['name', 'module', 'header', 'long_identifier'])


def test_get_json():
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
    assert a2l.tree.project.json == {
        'node': 'PROJECT',
        'header': None,
        'long_identifier': 'project long identifier',
        'module': [
            {
                'node': 'MODULE',
                'compu_tab': [],
                'record_layout': [],
                'long_identifier': 'first module long identifier',
                'unit': [],
                'compu_method': [],
                'function': [],
                'variant_coding': None,
                'characteristic': [
                    {
                        'node': 'CHARACTERISTIC',
                        'if_data_characteristic': [],
                        'long_identifier': 'characteristic long identifier',
                        'format': None,
                        'read_only': None,
                        'matrix_dim': None,
                        'extended_limits': None,
                        'dependent_characteristic': None,
                        'byte_order': None,
                        'virtual_characteristic': None,
                        'deposit': 'DAMOS_SST',
                        'ref_memory_segment': None,
                        'conversion': 'characteristic_conversion',
                        'type': 'VALUE',
                        'display_identifier': None,
                        'max_diff': 0,
                        'lower_limit': 0,
                        'address': 0,
                        'guard_rails': None,
                        'ecu_address_extension': None,
                        'annotation': [],
                        'name': 'characteristic_name',
                        'map_list': None,
                        'calibration_access': None,
                        'comparison_quantity': None,
                        'upper_limit': 0,
                        'bit_mask': None,
                        'max_refresh': None,
                        'function_list': None,
                        'number': None,
                        'axis_descr': []
                    },
                    {
                        'node': 'CHARACTERISTIC',
                        'if_data_characteristic': [],
                        'long_identifier': 'characteristic long identifier',
                        'format': None,
                        'read_only': None,
                        'matrix_dim': None,
                        'extended_limits': None,
                        'dependent_characteristic': None,
                        'byte_order': None,
                        'virtual_characteristic': None,
                        'deposit': 'DAMOS_SST',
                        'ref_memory_segment': None,
                        'conversion': 'characteristic_conversion',
                        'type': 'VALUE',
                        'display_identifier': None,
                        'max_diff': 0,
                        'lower_limit': 0,
                        'address': 0,
                        'guard_rails': None,
                        'ecu_address_extension': None,
                        'annotation': [],
                        'name': 'characteristic_name',
                        'map_list': None,
                        'calibration_access': None,
                        'comparison_quantity': None,
                        'upper_limit': 0,
                        'bit_mask': None,
                        'max_refresh': None,
                        'function_list': None,
                        'number': None,
                        'axis_descr': []
                    }],
                'group': [],
                'compu_vtab_range': [],
                'name': 'first_module_name',
                'frame': None,
                'a2ml': None,
                'user_rights': [],
                'compu_vtab': [],
                'measurement': [],
                'if_data_xcp': None,
                'axis_pts': [],
                'mod_par': None,
                'mod_common': None,
                'if_data_module': []
            }
        ],
        'name': 'project_name'
    }


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
    assert a2l.tree.project.module[0].characteristic[0].node() == 'CHARACTERISTIC'


def test_custom_class():
    from pya2l.parser.grammar.node import Project, A2lNode, a2l_node_type

    class CustomProject(Project):
        pass

    a2l_string = """
        /begin PROJECT project_name "project long identifier"
        /end PROJECT"""
    a2l = Parser(a2l_string, PROJECT=CustomProject)
    assert isinstance(a2l.tree.project, CustomProject)
