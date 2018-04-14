"""
@project: parser
@file: parser_test.py
@author: Guillaume Sottas
@date: 06.04.2018
"""

import pytest

from parser import A2lFormatException
from parser import A2lParser as Parser


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


def test_compu_tab_default_value_node():
    a2l_string = """
        /begin PROJECT project_name "project long identifier"
            /begin MODULE first_module_name "first module long identifier"
                /begin COMPU_TAB first_compu_tab_name "first compu_tab long identifier" TAB_INTP 1 1 1
                    DEFAULT_VALUE "default value"
                /end COMPU_TAB
            /end MODULE
        /end PROJECT"""
    a2l = Parser(a2l_string)
    assert hasattr(a2l.tree.project.module[0].compu_tab[0], 'default_value')
    assert a2l.tree.project.module[0].compu_tab[0].default_value == 'default value'

# TODO: implement tests for BIT_OPERATION.

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


def test_coeffs_node():
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
    assert a2l.tree.project.module[0].characteristic[0].function_list[0] == 'first_function'
    assert a2l.tree.project.module[0].characteristic[0].function_list[1] == 'second_function'


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
    assert a2l.tree.project.module[0].characteristic[0].axis_descr[0].fix_axis_par_dist.shift == 1
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


