"""
@project: a2l_parser
@file: parser.py
@author: Guillaume Sottas
@date: 20.03.2018
"""

import ply.yacc as yacc
import lexer


class A2lFormatException(Exception):
    def __init__(self, message, position, string=None):
        self.value = str(message) + str(position)
        if string:
            delta = 20
            s = position - delta if position >= delta else 0
            e = position + delta if len(string) >= position + delta else -1
            substring = string[s:e].replace('\r', ' ').replace('\n', ' ')
            indicator = ' ' * (delta if position >= delta else position) + '^'
            self.value += '\r\n\t' + ('...' if s else '   ') + substring + '\r\n\t   ' + indicator

        super(A2lFormatException, self).__init__(self.value)


class A2lParser(object):
    tokens = lexer.tokens

    def __init__(self, string):
        yacc.yacc(module=self)
        yacc.parse(string)

    @staticmethod
    def p_error(p):
        print A2lFormatException('invalid sequence at position ', p.lexpos, string=p.lexer.lexdata)
        p.lexer.skip(1)
        pass

    @staticmethod
    def p_root(p):
        """a2l : version_list project"""
        pass

    @staticmethod
    def p_a2ml_declaration(p):
        """a2ml_declaration : a2ml_type_definition SEMICOLON
                            | a2ml_block_definition SEMICOLON"""


    @staticmethod
    def p_a2ml_declaration_list(p):
        """a2ml_declaration_list : a2ml_declaration
                                 | a2ml_declaration a2ml_declaration_list"""


    @staticmethod
    def p_a2ml_type_definition(p):
        """a2ml_type_definition : a2ml_type_name"""

    # a2ml_predefined_type_name
    # | a2ml_struct_type_name
    # | a2ml_taggedstruct_type_name
    # | a2ml_taggedunion_type_name
    # | a2ml_enum_type_name
    @staticmethod
    def p_a2ml_type_name(p):
        """a2ml_type_name : a2ml_predefined_type_name
                          | a2ml_struct_type_name
                          | a2ml_enum_type_name
                          | a2ml_taggedstruct_type_name
                          | a2ml_taggedunion_type_name"""
        p[0] = p[1]

    @staticmethod
    def p_a2ml_predefined_type_name(p):
        """a2ml_predefined_type_name : char
                                     | int
                                     | long
                                     | uchar
                                     | uint
                                     | ulong
                                     | double
                                     | float"""

    @staticmethod
    def p_a2ml_block_definition(p):
        """a2ml_block_definition : block a2ml_tag a2ml_type_name"""

    @staticmethod
    def p_a2ml_enum_type_name(p):
        """a2ml_enum_type_name : enum a2ml_identifier_optional CURLY_OPEN a2ml_enumerator_list CURLY_CLOSE
                               | enum a2ml_identifier"""

    @staticmethod
    def p_a2ml_enumerator_list(p):
        """a2ml_enumerator_list : a2ml_enumerator
                                | a2ml_enumerator COMMA a2ml_enumerator_list"""
        try:
            p[0] = [p[1]] + p[3]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_a2ml_enumerator(p):
        """a2ml_enumerator : a2ml_keyword EQUAL a2ml_constant
                           | a2ml_keyword"""

    @staticmethod
    def p_a2ml_struct_type_name(p):
        """a2ml_struct_type_name : struct a2ml_identifier_optional CURLY_OPEN a2ml_struct_member_list_optional CURLY_CLOSE
                                 | struct a2ml_identifier"""

    @staticmethod
    def p_a2ml_struct_member_list_optional(p):
        """a2ml_struct_member_list_optional : empty
                                            | a2ml_struct_member_list"""

    @staticmethod
    def p_a2ml_struct_member_list(p):
        """a2ml_struct_member_list : a2ml_struct_member
                                   | a2ml_struct_member a2ml_struct_member_list"""

    @staticmethod
    def p_a2ml_struct_member(p):
        """a2ml_struct_member : a2ml_member SEMICOLON"""

    @staticmethod
    def p_a2ml_member(p):
        """a2ml_member : a2ml_type_name a2ml_array_specifier_optional"""

    @staticmethod
    def p_a2ml_member_optional(p):
        """a2ml_member_optional : empty
                                | a2ml_member"""

    @staticmethod
    def p_a2ml_array_specifier_optional(p):
        """a2ml_array_specifier_optional : empty
                                         | a2ml_array_specifier"""

    @staticmethod
    def p_a2ml_array_specifier(p):
        """a2ml_array_specifier : BRACE_OPEN a2ml_constant BRACE_CLOSE
                                | BRACE_OPEN a2ml_constant BRACE_CLOSE a2ml_array_specifier"""

    @staticmethod
    def p_a2ml_taggedstruct_type_name(p):
        """a2ml_taggedstruct_type_name : taggedstruct a2ml_identifier_optional CURLY_OPEN a2ml_taggedstruct_member_list_optional CURLY_CLOSE
                                       | taggedstruct a2ml_identifier"""

    @staticmethod
    def p_a2ml_taggedstruct_member_list_optional(p):
        """a2ml_taggedstruct_member_list_optional : empty
                                                  | a2ml_taggedstruct_member_list"""
    @staticmethod
    def p_a2ml_taggedstruct_member_list(p):
        """a2ml_taggedstruct_member_list : a2ml_taggedstruct_member
                                         | a2ml_taggedstruct_member a2ml_taggedstruct_member_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_a2ml_taggedstruct_member(p):
        """a2ml_taggedstruct_member : a2ml_taggedstruct_definition SEMICOLON
                                    | PARENTHESE_OPEN a2ml_taggedstruct_definition PARENTHESE_CLOSE ASTERISK SEMICOLON
                                    | a2ml_block_definition SEMICOLON
                                    | PARENTHESE_OPEN a2ml_block_definition PARENTHESE_CLOSE ASTERISK SEMICOLON"""

    @staticmethod
    def p_a2ml_taggedstruct_definition(p): # TODO: check if the optional member is really optional (seems to be optional in example).
        """a2ml_taggedstruct_definition : a2ml_tag a2ml_member_optional
                                        | a2ml_tag PARENTHESE_OPEN a2ml_member PARENTHESE_CLOSE ASTERISK SEMICOLON"""

    @staticmethod
    def p_a2ml_taggedunion_type_name(p):
        """a2ml_taggedunion_type_name : taggedunion a2ml_identifier_optional CURLY_OPEN a2ml_taggedunion_member_list CURLY_CLOSE
                                      | taggedunion a2ml_identifier"""

    @staticmethod
    def p_a2ml_taggedunion_member_list(p):
        """a2ml_taggedunion_member_list : a2ml_taggedunion_member
                                        | a2ml_taggedunion_member a2ml_taggedunion_member_list"""

    @staticmethod
    def p_a2ml_taggedunion_member(p):
        """a2ml_taggedunion_member : a2ml_tag a2ml_member SEMICOLON
                                   | a2ml_block_definition SEMICOLON"""

    @staticmethod
    def p_a2ml_tag(p):
        """a2ml_tag : STRING"""

    @staticmethod
    def p_a2ml_identifier(p):
        """a2ml_identifier : IDENT"""

    @staticmethod
    def p_a2ml_identifier_optional(p):
        """a2ml_identifier_optional : empty
                                    | a2ml_identifier"""

    @staticmethod
    def p_a2ml_keyword(p):
        """a2ml_keyword : STRING"""

    @staticmethod
    def p_a2ml_constant(p):
        """a2ml_constant : NUMERIC"""

    @staticmethod
    def p_datatype(p):
        """datatype : UBYTE
                    | SBYTE
                    | UWORD
                    | SWORD
                    | ULONG
                    | SLONG
                    | A_UINT64
                    | A_INT64
                    | FLOAT32_IEEE
                    | FLOAT64_IEEE"""
        p[0] = p[1]

    @staticmethod
    def p_datasize(p):
        """datasize : BYTE
                    | WORD
                    | LONG"""
        p[0] = p[1]

    @staticmethod
    def p_addrtype(p):
        """addrtype : PBYTE
                    | PWORD
                    | PLONG
                    | DIRECT"""
        p[0] = p[1]

    @staticmethod
    def p_indexorder(p):
        """indexorder : INDEX_INCR
                      | INDEX_DECR"""
        p[0] = p[1]

    @staticmethod
    def p_version_list(p):
        """version_list : version
                        | version version_list"""
        pass

    @staticmethod
    def p_version(p):
        """version : version_asap2_a2ml number_list"""
        pass

    @staticmethod
    def p_version_asap2_a2ml(p):
        """version_asap2_a2ml : ASAP2_VERSION
                              | A2ML_VERSION"""

    @staticmethod
    def p_number_list(p):
        """number_list : NUMERIC
                       | NUMERIC number_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_ident_list(p):
        """ident_list : IDENT
                      | IDENT ident_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_string_list(p):
        """string_list : STRING
                       | STRING string_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_project(p):
        """project : begin PROJECT IDENT STRING optional_header module_list end PROJECT"""
        pass

    @staticmethod
    def p_optional_header(p):
        """optional_header : empty
                           | header"""
        p[0] = p[1]

    @staticmethod
    def p_header(p):
        """header : begin HEADER STRING header_version header_project_no end HEADER"""
        pass

    @staticmethod
    def p_header_version(p):
        """header_version : empty
                          | VERSION STRING"""
        p[0] = p[1]

    @staticmethod
    def p_header_project_no(p):
        """header_project_no : empty
                             | PROJECT_NO IDENT"""

    @staticmethod
    def p_module(p):
        """module : begin MODULE IDENT STRING optional_a2ml optional_module_parameter_list end MODULE"""
        pass

    @staticmethod
    def p_module_list(p):
        """module_list : module
                       | module module_list"""
        pass

    @staticmethod
    def p_a2ml(p):
        """a2ml : begin A2ML a2ml_declaration_list end A2ML"""
        pass

    @staticmethod
    def p_optional_a2ml(p):
        """optional_a2ml : empty
                         | a2ml"""
        p[0] = p[1]

    @staticmethod
    def p_module_parameter(p):
        """module_parameter : mod_par
                            | mod_common
                            | if_data
                            | characteristic
                            | axis_pts
                            | measurement
                            | compu_method
                            | compu_tab
                            | compu_vtab
                            | compu_vtab_range
                            | function
                            | group
                            | record_layout
                            | variant_coding
                            | frame
                            | user_rights
                            | unit"""
        p[0] = p[1]

    @staticmethod
    def p_module_parameter_list(p):
        """module_parameter_list : module_parameter
                                 | module_parameter module_parameter_list"""
        pass

    @staticmethod
    def p_optional_module_parameter_list(p):
        """optional_module_parameter_list : empty
                                          | module_parameter_list"""
        pass

    @staticmethod
    def p_mod_par(p):
        """mod_par : begin MOD_PAR end MOD_PAR"""
        pass

    @staticmethod
    def p_mod_common(p):
        """mod_common : begin MOD_COMMON end MOD_COMMON"""
        pass

    @staticmethod
    def p_if_data(p):
        """if_data : begin IF_DATA IDENT end IF_DATA"""
        pass

    @staticmethod
    def p_characteristic(p):
        """characteristic : begin CHARACTERISTIC IDENT STRING characteristic_type NUMERIC IDENT NUMERIC IDENT NUMERIC NUMERIC characteristic_optional_list_optional end CHARACTERISTIC"""
        pass

    @staticmethod
    def p_characteristic_type(p):
        """characteristic_type : VALUE
                               | CURVE
                               | MAP
                               | CUBOID
                               | VAL_BLK
                               | ASCII"""
        p[0] = p[1]

    @staticmethod
    def p_display_identifier(p):
        """display_identifier : DISPLAY_IDENTIFIER IDENT"""
        p[0] = p[2]

    @staticmethod
    def p_format(p):
        """format : FORMAT STRING"""
        p[0] = p[2]

    @staticmethod
    def p_byte_order(p):
        """byte_order : BYTE_ORDER byte_order_type"""
        p[0] = p[2]

    @staticmethod
    def p_byte_order_type(p):
        """byte_order_type : MSB_FIRST
                           | MSB_LAST"""
        p[0] = p[1]

    @staticmethod
    def p_bit_mask(p):
        """bit_mask : BIT_MASK NUMERIC"""
        p[0] = p[2]

    @staticmethod
    def p_function_list(p):
        """function_list : begin FUNCTION_LIST ident_list end FUNCTION_LIST"""
        p[0] = p[3]

    @staticmethod
    def p_number(p):
        """number : NUMBER NUMERIC"""
        p[0] = p[2]

    @staticmethod
    def p_extended_limits(p):
        """extended_limits : EXTENDED_LIMITS NUMERIC NUMERIC"""
        p[0] = (p[2], p[3])

    @staticmethod
    def p_map_list(p):
        """map_list : begin MAP_LIST ident_list end MAP_LIST"""
        p[0] = p[3]

    @staticmethod
    def p_max_refresh(p):
        """max_refresh : MAX_REFRESH NUMERIC NUMERIC"""
        p[0] = (p[2], p[3])

    @staticmethod
    def p_dependent_characteristic(p):
        """dependent_characteristic : begin DEPENDENT_CHARACTERISTIC STRING ident_list end DEPENDENT_CHARACTERISTIC"""
        pass

    @staticmethod
    def p_virtual_characteristic(p):
        """virtual_characteristic : begin VIRTUAL_CHARACTERISTIC STRING ident_list end VIRTUAL_CHARACTERISTIC"""
        pass

    @staticmethod
    def p_ref_memory_segment(p):
        """ref_memory_segment : REF_MEMORY_SEGMENT IDENT"""
        p[0] = p[2]

    @staticmethod
    def p_annotation(p):
        """annotation : begin ANNOTATION annotation_optional_list_optional end ANNOTATION"""
        p[0] = p[3]

    @staticmethod
    def p_annotation_optional(p):
        """annotation_optional : annotation_label
                               | annotation_origin
                               | annotation_text"""
        p[0] = p[1]

    @staticmethod
    def p_annotation_label(p):
        """annotation_label : ANNOTATION_LABEL STRING"""
        p[0] = p[2]

    @staticmethod
    def p_annotation_origin(p):
        """annotation_origin : ANNOTATION_ORIGIN STRING"""
        p[0] = p[2]

    @staticmethod
    def p_annotation_text(p):
        """annotation_text : begin ANNOTATION_TEXT string_list end ANNOTATION_TEXT"""
        p[0] = p[3]

    @staticmethod
    def p_annotation_optional_list(p):
        """annotation_optional_list : annotation_optional
                                    | annotation_optional annotation_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_annotation_optional_list_optional(p):
        """annotation_optional_list_optional : empty
                                             | annotation_optional_list"""
        p[0] = p[1]

    @staticmethod
    def p_comparison_quantity(p):
        """comparison_quantity : COMPARISON_QUANTITY IDENT"""
        p[0] = p[2]

    @staticmethod
    def p_axis_descr(p):
        """axis_descr : begin AXIS_DESCR axis_descr_attribute IDENT IDENT NUMERIC NUMERIC NUMERIC end AXIS_DESCR"""
        p[0] = p[4]

    @staticmethod
    def p_axis_descr_attribute(p):
        """axis_descr_attribute : STD_AXIS
                                | FIX_AXIS
                                | COM_AXIS
                                | RES_AXIS
                                | CURVE_AXIS"""
        p[0] = p[1]

    @staticmethod
    def p_calibration_access(p):
        """calibration_access : CALIBRATION_ACCESS calibration_access_type"""
        p[0] = p[2]

    @staticmethod
    def p_calibration_access_type(p):
        """calibration_access_type : CALIBRATION
                                   | NO_CALIBRATION
                                   | NOT_IN_MCD_SYSTEM
                                   | OFFLINE_CALIBRATION"""
        p[0] = p[1]

    @staticmethod
    def p_matrix_dim(p):
        """matrix_dim : MATRIX_DIM NUMERIC NUMERIC NUMERIC"""
        p[0] = (p[2], p[3], p[4])

    @staticmethod
    def p_ecu_address_extension(p):
        """ecu_address_extension : ECU_ADDRESS_EXTENSION NUMERIC"""
        p[0] = p[2]

    @staticmethod
    def p_characteristic_optional(p):
        """characteristic_optional : display_identifier
                                   | format
                                   | byte_order
                                   | bit_mask
                                   | function_list
                                   | number
                                   | extended_limits
                                   | READ_ONLY
                                   | GUARD_RAILS
                                   | map_list
                                   | max_refresh
                                   | dependent_characteristic
                                   | virtual_characteristic
                                   | ref_memory_segment
                                   | annotation
                                   | comparison_quantity
                                   | if_data
                                   | axis_descr
                                   | calibration_access
                                   | matrix_dim
                                   | ecu_address_extension"""
        p[0] = p[1]

    @staticmethod
    def p_characteristic_optional_list(p):
        """characteristic_optional_list : characteristic_optional
                                        | characteristic_optional characteristic_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_characteristic_optional_list_optional(p):
        """characteristic_optional_list_optional : empty
                                                 | characteristic_optional_list"""
        p[0] = p[1]

    @staticmethod
    def p_axis_pts(p):
        """axis_pts : begin AXIS_PTS IDENT STRING NUMERIC IDENT IDENT NUMERIC IDENT NUMERIC NUMERIC NUMERIC axis_pts_optional_list_optional end AXIS_PTS"""
        pass

    @staticmethod
    def p_axis_pts_optional(p):
        """axis_pts_optional : display_identifier
                             | READ_ONLY
                             | format
                             | deposit
                             | byte_order
                             | function_list
                             | ref_memory_segment
                             | GUARD_RAILS
                             | extended_limits
                             | annotation
                             | if_data
                             | calibration_access
                             | ecu_address_extension"""
        pass

    @staticmethod
    def p_axis_pts_optional_list(p):
        """axis_pts_optional_list : axis_pts_optional
                                  | axis_pts_optional axis_pts_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_axis_pts_optional_list_optional(p):
        """axis_pts_optional_list_optional : empty
                                           | axis_pts_optional_list"""
        p[0] = p[1]

    @staticmethod
    def p_deposit(p):
        """deposit : DEPOSIT deposit_mode"""
        p[0] = p[2]

    @staticmethod
    def p_deposit_mode(p):
        """deposit_mode : ABSOLUTE
                        | DIFFERENCE"""

    @staticmethod
    def p_measurement(p):
        """measurement : begin MEASUREMENT IDENT STRING datatype IDENT NUMERIC NUMERIC NUMERIC NUMERIC measurement_optional_list_optional end MEASUREMENT"""
        pass

    @staticmethod
    def p_measurement_optional(p):
        """measurement_optional : display_identifier
                                | READ_WRITE
                                | format
                                | array_size
                                | bit_mask
                                | bit_operation
                                | byte_order
                                | max_refresh
                                | virtual
                                | function_list
                                | ecu_address
                                | error_mask
                                | ref_memory_segment
                                | annotation
                                | if_data
                                | matrix_dim
                                | ecu_address_extension"""
        p[0] = p[1]

    @staticmethod
    def p_measurement_optional_list(p):
        """measurement_optional_list : measurement_optional
                                     | measurement_optional measurement_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_measurement_optional_list_optional(p):
        """measurement_optional_list_optional : empty
                                              | measurement_optional_list"""
        p[0] = p[1]

    @staticmethod
    def p_array_size(p):
        """array_size : ARRAY_SIZE NUMERIC"""
        p[0] = p[2]

    @staticmethod
    def p_bit_operation(p):
        """bit_operation : begin BIT_OPERATION bit_operation_optional_list_optional end BIT_OPERATION"""

    @staticmethod
    def p_bit_operation_optional(p):
        """bit_operation_optional : left_shift
                                  | right_shift
                                  | SIGN_EXTEND"""
        p[0] = p[1]

    @staticmethod
    def p_left_shift(p):
        """left_shift : LEFT_SHIFT NUMERIC"""
        return p[2]

    @staticmethod
    def p_right_shift(p):
        """right_shift : RIGHT_SHIFT NUMERIC"""
        return p[2]

    @staticmethod
    def p_bit_operation_optional_list(p):
        """bit_operation_optional_list : bit_operation_optional
                                       | bit_operation_optional bit_operation_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_bit_operation_optional_list_optional(p):
        """bit_operation_optional_list_optional : empty
                                                | bit_operation_optional_list"""
        p[0] = p[1]

    @staticmethod
    def p_compu_method(p):
        """compu_method : begin COMPU_METHOD IDENT STRING compu_method_conversion_type STRING STRING compu_method_optional_list_optional end COMPU_METHOD"""
        pass

    @staticmethod
    def p_compu_method_conversion_type(p):
        """compu_method_conversion_type : TAB_INTP
                             | TAB_NOINTP
                             | TAB_VERB
                             | RAT_FUNC
                             | FORM
                             | IDENTICAL"""
        p[0] = p[1]

    @staticmethod
    def p_compu_method_optional(p):
        """compu_method_optional : formula
                                 | coeffs
                                 | compu_tab_ref
                                 | ref_unit"""
        p[0] = p[1]

    @staticmethod
    def p_formula(p):
        """formula : begin FORMULA STRING formula_optional end FORMULA"""
        pass

    @staticmethod
    def p_formula_optional(p):
        """formula_optional : empty
                            | formula_inv"""

    @staticmethod
    def p_formula_inv(p):
        """formula_inv : STRING"""
        p[0] = p[1]  # might be simplified...

    @staticmethod
    def p_coeffs(p):
        """coeffs : COEFFS NUMERIC NUMERIC NUMERIC NUMERIC NUMERIC NUMERIC"""
        p[0] = (p[2], p[3], p[4], p[5], p[6], p[7])

    @staticmethod
    def p_compu_tab_ref(p):
        """compu_tab_ref : COMPU_TAB_REF IDENT"""
        p[0] = p[2]

    @staticmethod
    def p_ref_unit(p):
        """ref_unit : REF_UNIT IDENT"""
        p[0] = p[2]

    @staticmethod
    def p_compu_method_optional_list(p):
        """compu_method_optional_list : compu_method_optional
                                      | compu_method_optional compu_method_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_compu_method_optional_list_optional(p):
        """compu_method_optional_list_optional : empty
                                               | compu_method_optional_list"""
        p[0] = p[1]

    @staticmethod
    def p_virtual(p):
        """virtual : begin VIRTUAL ident_list end VIRTUAL"""
        p[0] = p[4]

    @staticmethod
    def p_ecu_address(p):
        """ecu_address : ECU_ADDRESS NUMERIC"""
        p[0] = p[2]

    @staticmethod
    def p_error_mask(p):
        """error_mask : ERROR_MASK NUMERIC"""
        p[0] = p[2]

    @staticmethod
    def p_compu_tab(p):
        """compu_tab : begin COMPU_TAB IDENT STRING compu_tab_conversion_type NUMERIC number_list compu_tab_optional end COMPU_TAB"""
        pass

    @staticmethod
    def p_compu_tab_conversion_type(p):
        """compu_tab_conversion_type : TAB_INTP
                                     | TAB_NOINTP"""
        pass

    @staticmethod
    def p_compu_tab_optional(p):
        """compu_tab_optional : empty
                              | default_value"""
        p[0] = p[1]

    @staticmethod
    def p_default_value(p):
        """default_value : DEFAULT_VALUE STRING"""
        pass

    @staticmethod
    def p_compu_vtab(p):
        """compu_vtab : begin COMPU_VTAB IDENT STRING compu_vtab_conversion_type NUMERIC number_string_value_list compu_vtab_optional end COMPU_VTAB"""
        pass

    @staticmethod
    def p_compu_vtab_conversion_type(p):
        """compu_vtab_conversion_type : TAB_VERB"""
        p[0] = p[1]

    @staticmethod
    def p_number_string_value_list(p):
        """number_string_value_list : number_string_value
                                    | number_string_value number_string_value_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_number_string_value(p):
        """number_string_value : NUMERIC STRING"""
        p[0] = (p[1], p[2])

    @staticmethod
    def p_compu_vtab_optional(p):
        """compu_vtab_optional : empty
                               | default_value"""
        p[0] = p[1]

    @staticmethod
    def p_compu_vtab_range(p):
        """compu_vtab_range : begin COMPU_VTAB_RANGE IDENT STRING NUMERIC number_number_string_value_list compu_vtab_range_optional end COMPU_VTAB_RANGE"""
        pass

    @staticmethod
    def p_number_number_string_value_list(p):
        """number_number_string_value_list : number_number_string_value
                                           | number_number_string_value number_number_string_value_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_number_number_string_value(p):
        """number_number_string_value : NUMERIC NUMERIC STRING"""
        p[0] = (p[1], p[2], p[3])

    @staticmethod
    def p_compu_vtab_range_optional(p):
        """compu_vtab_range_optional : empty
                                     | default_value"""
        p[0] = p[1]

    @staticmethod
    def p_function(p):
        """function : begin FUNCTION IDENT STRING function_optional_list_optional end FUNCTION"""
        pass

    @staticmethod
    def p_function_optional(p):
        """function_optional : annotation
                             | def_characteristic
                             | ref_characteristic
                             | in_measurement
                             | out_measurement
                             | loc_measurement
                             | sub_function
                             | function_version"""
        p[0] = p[1]

    @staticmethod
    def p_function_optional_list(p):
        """function_optional_list : function_optional
                                  | function_optional function_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_function_optional_list_optional(p):
        """function_optional_list_optional : empty
                                           | function_optional_list"""

    @staticmethod
    def p_def_characteristic(p):
        """def_characteristic : begin DEF_CHARACTERISTIC ident_list end DEF_CHARACTERISTIC"""
        pass

    @staticmethod
    def p_ref_characteristic(p):
        """ref_characteristic : begin REF_CHARACTERISTIC ident_list end REF_CHARACTERISTIC"""
        pass

    @staticmethod
    def p_in_measurement(p):
        """in_measurement : begin IN_MEASUREMENT ident_list end IN_MEASUREMENT"""
        pass

    @staticmethod
    def p_out_measurement(p):
        """out_measurement : begin OUT_MEASUREMENT ident_list end OUT_MEASUREMENT"""
        pass

    @staticmethod
    def p_loc_measurement(p):
        """loc_measurement : begin LOC_MEASUREMENT ident_list end LOC_MEASUREMENT"""
        pass

    @staticmethod
    def p_sub_function(p):
        """sub_function : begin SUB_FUNCTION ident_list end SUB_FUNCTION"""
        pass

    @staticmethod
    def p_function_version(p):
        """function_version : FUNCTION_VERSION STRING"""

    @staticmethod
    def p_group(p):
        """group : begin GROUP IDENT STRING group_optional_list_optional end GROUP"""
        pass

    @staticmethod
    def p_group_optional(p):
        """group_optional : annotation
                          | ROOT
                          | ref_characteristic
                          | ref_measurement
                          | function_list
                          | sub_group"""
        p[0] = p[1]

    @staticmethod
    def p_group_optional_list(p):
        """group_optional_list : group_optional
                               | group_optional group_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_group_optional_list_optional(p):
        """group_optional_list_optional : empty
                                        | group_optional_list"""
        p[0] = p[1]

    @staticmethod
    def p_ref_measurement(p):
        """ref_measurement : begin REF_MEASUREMENT ident_list end REF_MEASUREMENT"""
        p[0] = p[3]

    @staticmethod
    def p_sub_group(p):
        """sub_group : begin SUB_GROUP ident_list end SUB_GROUP"""
        p[0] = p[3]

    @staticmethod
    def p_record_layout(p):
        """record_layout : begin RECORD_LAYOUT IDENT record_layout_optional_list_optional end RECORD_LAYOUT"""
        pass

    @staticmethod
    def p_record_layout_optional(p):
        """record_layout_optional : fnc_values
                                  | identification
                                  | axis_pts_x
                                  | axis_pts_y
                                  | axis_pts_z
                                  | axis_rescale_x
                                  | axis_rescale_y
                                  | axis_rescale_z
                                  | no_axis_pts_x
                                  | no_axis_pts_y
                                  | no_axis_pts_z
                                  | no_rescale_x
                                  | no_rescale_y
                                  | no_rescale_z
                                  | fix_no_axis_pts_x
                                  | fix_no_axis_pts_y
                                  | fix_no_axis_pts_z
                                  | src_addr_x
                                  | src_addr_y
                                  | src_addr_z
                                  | rip_addr_x
                                  | rip_addr_y
                                  | rip_addr_z
                                  | rip_addr_w
                                  | shift_op_x
                                  | shift_op_y
                                  | shift_op_z
                                  | offset_x
                                  | offset_y
                                  | offset_z
                                  | dist_op_x
                                  | dist_op_y
                                  | dist_op_z
                                  | alignment_byte
                                  | alignment_word
                                  | alignment_long
                                  | alignment_float32_ieee
                                  | alignment_float64_ieee
                                  | reserved"""
        p[0] = p[1]

    @staticmethod
    def p_record_layout_optional_list(p):
        """record_layout_optional_list : record_layout_optional
                                       | record_layout_optional record_layout_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_record_layout_optional_list_optional(p):
        """record_layout_optional_list_optional : empty
                                                | record_layout_optional_list"""
        p[0] = p[1]

    @staticmethod
    def p_fnc_values(p):
        """fnc_values : FNC_VALUES NUMERIC datatype fnc_values_index_mode addrtype"""
        pass

    @staticmethod
    def p_fnc_values_index_mode(p):
        """fnc_values_index_mode : COLUMN_DIR
                                 | ROW_DIR
                                 | ALTERNATE_WITH_X
                                 | ALTERNATE_WITH_Y
                                 | ALTERNATE_CURVES"""
        p[0] = p[1]

    @staticmethod
    def p_identification(p):
        """identification : IDENTIFICATION NUMERIC datatype"""

    @staticmethod
    def p_axis_pts_x(p):
        """axis_pts_x : AXIS_PTS_X NUMERIC datatype indexorder addrtype"""

    @staticmethod
    def p_axis_pts_y(p):
        """axis_pts_y : AXIS_PTS_Y NUMERIC datatype indexorder addrtype"""

    @staticmethod
    def p_axis_pts_z(p):
        """axis_pts_z : AXIS_PTS_Z NUMERIC datatype indexorder addrtype"""

    @staticmethod
    def p_axis_rescale_x(p):
        """axis_rescale_x : AXIS_RESCALE_X NUMERIC datatype NUMERIC indexorder addrtype"""

    @staticmethod
    def p_axis_rescale_y(p):
        """axis_rescale_y : AXIS_RESCALE_Y NUMERIC datatype NUMERIC indexorder addrtype"""

    @staticmethod
    def p_axis_rescale_z(p):
        """axis_rescale_z : AXIS_RESCALE_Z NUMERIC datatype NUMERIC indexorder addrtype"""

    @staticmethod
    def p_no_axis_pts_x(p):
        """no_axis_pts_x : NO_AXIS_PTS_X NUMERIC datatype"""

    @staticmethod
    def p_no_axis_pts_y(p):
        """no_axis_pts_y : NO_AXIS_PTS_Y NUMERIC datatype"""

    @staticmethod
    def p_no_axis_pts_z(p):
        """no_axis_pts_z : NO_AXIS_PTS_Z NUMERIC datatype"""

    @staticmethod
    def p_no_rescale_x(p):
        """no_rescale_x : NO_RESCALE_X NUMERIC datatype"""

    @staticmethod
    def p_no_rescale_y(p):
        """no_rescale_y : NO_RESCALE_Y NUMERIC datatype"""

    @staticmethod
    def p_no_rescale_z(p):
        """no_rescale_z : NO_RESCALE_Z NUMERIC datatype"""

    @staticmethod
    def p_fix_no_axis_pts_x(p):
        """fix_no_axis_pts_x : FIX_NO_AXIS_PTS_X NUMERIC"""

    @staticmethod
    def p_fix_no_axis_pts_y(p):
        """fix_no_axis_pts_y : FIX_NO_AXIS_PTS_Y NUMERIC"""

    @staticmethod
    def p_fix_no_axis_pts_z(p):
        """fix_no_axis_pts_z : FIX_NO_AXIS_PTS_Z NUMERIC"""

    @staticmethod
    def p_src_addr_x(p):
        """src_addr_x : SRC_ADDR_X NUMERIC src_addr_optional"""

    @staticmethod
    def p_src_addr_y(p):
        """src_addr_y : SRC_ADDR_Y NUMERIC src_addr_optional"""

    @staticmethod
    def p_src_addr_z(p):
        """src_addr_z : SRC_ADDR_Z NUMERIC src_addr_optional"""

    @staticmethod
    def p_src_addr_optional(p):
        """src_addr_optional : empty
                             | datatype"""

    @staticmethod
    def p_rip_addr_x(p):
        """rip_addr_x : RIP_ADDR_X NUMERIC datatype"""

    @staticmethod
    def p_rip_addr_y(p):
        """rip_addr_y : RIP_ADDR_Y NUMERIC datatype"""

    @staticmethod
    def p_rip_addr_z(p):
        """rip_addr_z : RIP_ADDR_Z NUMERIC datatype"""

    @staticmethod
    def p_rip_addr_w(p):
        """rip_addr_w : RIP_ADDR_W NUMERIC datatype"""

    @staticmethod
    def p_shift_op_x(p):
        """shift_op_x : SHIFT_OP_X NUMERIC datatype"""

    @staticmethod
    def p_shift_op_y(p):
        """shift_op_y : SHIFT_OP_Y NUMERIC datatype"""

    @staticmethod
    def p_shift_op_z(p):
        """shift_op_z : SHIFT_OP_Z NUMERIC datatype"""

    @staticmethod
    def p_offset_x(p):
        """offset_x : OFFSET_X NUMERIC datatype"""

    @staticmethod
    def p_offset_y(p):
        """offset_y : OFFSET_Y NUMERIC datatype"""

    @staticmethod
    def p_offset_z(p):
        """offset_z : OFFSET_Z NUMERIC datatype"""

    @staticmethod
    def p_dist_op_x(p):
        """dist_op_x : DIST_OP_X NUMERIC datatype"""

    @staticmethod
    def p_dist_op_y(p):
        """dist_op_y : DIST_OP_Y NUMERIC datatype"""

    @staticmethod
    def p_dist_op_z(p):
        """dist_op_z : DIST_OP_Z NUMERIC datatype"""

    @staticmethod
    def p_alignment_byte(p):
        """alignment_byte : ALIGNMENT_BYTE NUMERIC"""

    @staticmethod
    def p_alignment_word(p):
        """alignment_word : ALIGNMENT_WORD NUMERIC"""

    @staticmethod
    def p_alignment_long(p):
        """alignment_long : ALIGNMENT_LONG NUMERIC"""

    @staticmethod
    def p_alignment_float32_ieee(p):
        """alignment_float32_ieee : ALIGNMENT_FLOAT32_IEEE NUMERIC"""

    @staticmethod
    def p_alignment_float64_ieee(p):
        """alignment_float64_ieee : ALIGNMENT_FLOAT64_IEEE NUMERIC"""

    @staticmethod
    def p_variant_coding(p):
        """variant_coding : begin VARIANT_CODING variant_coding_optional_list_optional end VARIANT_CODING"""
        pass

    @staticmethod
    def p_variant_coding_optional(p):
        """variant_coding_optional : var_separator
                                   | var_naming
                                   | var_criterion
                                   | var_forbidden_comb
                                   | var_characteristic"""
        p[0] = p[1]

    @staticmethod
    def p_var_characteristic(p):
        """var_characteristic : begin VAR_CHARACTERISTIC IDENT ident_list var_characteristic_optional end VAR_CHARACTERISTIC"""

    @staticmethod
    def p_var_characteristic_optional(p):
        """var_characteristic_optional : var_address"""

    @staticmethod
    def p_var_address(p):
        """var_address : begin VAR_ADDRESS number_list end VAR_ADDRESS"""

    @staticmethod
    def p_var_separator(p):
        """var_separator : VAR_SEPARATOR STRING"""

    @staticmethod
    def p_var_naming(p):
        """var_naming : VAR_NAMING IDENT"""

    @staticmethod
    def p_var_forbidden_comb(p):
        """var_forbidden_comb : begin VAR_FORBIDDEN_COMB ident_ident_value_list end VAR_FORBIDDEN_COMB"""

    @staticmethod
    def p_ident_ident_value_list(p):
        """ident_ident_value_list : ident_ident_value
                                  | ident_ident_value ident_ident_value_list"""

    @staticmethod
    def p_ident_ident_value(p):
        """ident_ident_value : IDENT IDENT"""
        p[0] = (p[1], p[2])

    @staticmethod
    def p_var_criterion(p):
        """var_criterion : begin VAR_CRITERION IDENT STRING ident_list var_criterion_optional_list_optional end VAR_CRITERION"""

    @staticmethod
    def p_var_criterion_optional(p):
        """var_criterion_optional : var_measurement
                                  | var_selection_characteristic"""

    @staticmethod
    def p_var_criterion_optional_list(p):
        """var_criterion_optional_list : var_criterion_optional
                                       | var_criterion_optional var_criterion_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_var_criterion_optional_list_optional(p):
        """var_criterion_optional_list_optional : empty
                                                | var_criterion_optional_list"""
        p[0] = p[1]

    @staticmethod
    def p_var_measurement(p):
        """var_measurement : VAR_MEASUREMENT IDENT"""

    @staticmethod
    def p_var_selection_characteristic(p):
        """var_selection_characteristic : VAR_SELECTION_CHARACTERISTIC IDENT"""

    @staticmethod
    def p_variant_coding_optional_list(p):
        """variant_coding_optional_list : variant_coding_optional
                                        | variant_coding_optional variant_coding_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_variant_coding_optional_list_optional(p):
        """variant_coding_optional_list_optional : empty
                                                 | variant_coding_optional_list"""
        p[0] = p[1]

    @staticmethod
    def p_reserved(p):
        """reserved : RESERVED NUMERIC datasize"""

    @staticmethod
    def p_frame(p):
        """frame : begin FRAME IDENT STRING NUMERIC NUMERIC frame_optional_list_optional end FRAME"""
        pass

    @staticmethod
    def p_frame_optional(p):
        """frame_optional : frame_measurement
                          | if_data"""

    @staticmethod
    def p_frame_optional_list(p):
        """frame_optional_list : frame_optional
                               | frame_optional frame_optional_list"""

    @staticmethod
    def p_frame_optional_list_optional(p):
        """frame_optional_list_optional : empty
                                        | frame_optional_list"""

    @staticmethod
    def p_frame_measurement(p):
        """frame_measurement : FRAME_MEASUREMENT ident_list"""

    @staticmethod
    def p_user_rights(p):
        """user_rights : begin USER_RIGHTS IDENT user_rights_optional_list_optional end USER_RIGHTS"""
        pass

    @staticmethod
    def p_user_rights_optional(p):
        """user_rights_optional : ref_group
                                | READ_ONLY"""

    @staticmethod
    def p_user_rights_optional_list(p):
        """user_rights_optional_list : user_rights_optional
                                     | user_rights_optional user_rights_optional_list"""

    @staticmethod
    def p_user_rights_optional_list_optional(p):
        """user_rights_optional_list_optional : empty
                                              | user_rights_optional_list"""

    @staticmethod
    def p_ref_group(p):
        """ref_group : begin REF_GROUP ident_list end REF_GROUP"""

    @staticmethod
    def p_unit(p):
        """unit : begin UNIT IDENT STRING STRING unit_type unit_optional_list_optional end UNIT"""
        pass

    @staticmethod
    def p_unit_type(p):
        """unit_type : EXTENDED_SI
                     | DERIVED"""

    @staticmethod
    def p_unit_optional(p):
        """unit_optional : si_exponents
                         | ref_unit
                         | unit_conversion"""

    @staticmethod
    def p_unit_optional_list(p):
        """unit_optional_list : unit_optional
                              | unit_optional unit_optional_list"""

    @staticmethod
    def p_unit_optional_list_optional(p):
        """unit_optional_list_optional : empty
                                       | unit_optional_list"""

    @staticmethod
    def p_si_exponents(p):
        """si_exponents : SI_EXPONENTS NUMERIC NUMERIC NUMERIC NUMERIC NUMERIC NUMERIC NUMERIC"""

    @staticmethod
    def p_unit_conversion(p):
        """unit_conversion : UNIT_CONVERSION NUMERIC NUMERIC"""

    @staticmethod
    def p_empty(p):
        """empty :"""
        pass


if __name__ == '__main__':
    parser = A2lParser(r"""
    ASAP2_VERSION 1 61
    A2ML_VERSION 2 36
    /begin PROJECT ASAP2_Example ""
        /begin HEADER "ASAP2 Example File"
            VERSION "V1.61"
            PROJECT_NO MCD_P12_08
        /end HEADER
        /begin MODULE Example ""
            /begin A2ML
                block "IF_DATA" taggedunion if_data {


/*  ==============================================================================================  */
/*                                                                                                  */
/*  ASAM XCP AML                                                                                    */
/*                                                                                                  */
/*  ==============================================================================================  */

        "XCP" struct {
          taggedstruct {
            block "PROTOCOL_LAYER" struct {
              uint;
              uint;
              uint;
              uint;
              uint;
              uint;
              uint;
              uint;
              uchar;
              uint;
              enum {
                "BYTE_ORDER_MSB_LAST" = 0,
                "BYTE_ORDER_MSB_FIRST" = 1
              };
              enum {
                "ADDRESS_GRANULARITY_BYTE" = 1,
                "ADDRESS_GRANULARITY_WORD" = 2,
                "ADDRESS_GRANULARITY_DWORD" = 4
              };
              taggedstruct {
                ("OPTIONAL_CMD" enum {
                  "GET_COMM_MODE_INFO" = 251,
                  "GET_ID" = 250,
                  "SET_REQUEST" = 249,
                  "GET_SEED" = 248,
                  "UNLOCK" = 247,
                  "SET_MTA" = 246,
                  "UPLOAD" = 245,
                  "SHORT_UPLOAD" = 244,
                  "BUILD_CHECKSUM" = 243,
                  "TRANSPORT_LAYER_CMD" = 242,
                  "USER_CMD" = 241,
                  "DOWNLOAD" = 240,
                  "DOWNLOAD_NEXT" = 239,
                  "DOWNLOAD_MAX" = 238,
                  "SHORT_DOWNLOAD" = 237,
                  "MODIFY_BITS" = 236,
                  "SET_CAL_PAGE" = 235,
                  "GET_CAL_PAGE" = 234,
                  "GET_PAG_PROCESSOR_INFO" = 233,
                  "GET_SEGMENT_INFO" = 232,
                  "GET_PAGE_INFO" = 231,
                  "SET_SEGMENT_MODE" = 230,
                  "GET_SEGMENT_MODE" = 229,
                  "COPY_CAL_PAGE" = 228,
                  "CLEAR_DAQ_LIST" = 227,
                  "SET_DAQ_PTR" = 226,
                  "WRITE_DAQ" = 225,
                  "SET_DAQ_LIST_MODE" = 224,
                  "GET_DAQ_LIST_MODE" = 223,
                  "START_STOP_DAQ_LIST" = 222,
                  "START_STOP_SYNCH" = 221,
                  "GET_DAQ_CLOCK" = 220,
                  "READ_DAQ" = 219,
                  "GET_DAQ_PROCESSOR_INFO" = 218,
                  "GET_DAQ_RESOLUTION_INFO" = 217,
                  "GET_DAQ_LIST_INFO" = 216,
                  "GET_DAQ_EVENT_INFO" = 215,
                  "FREE_DAQ" = 214,
                  "ALLOC_DAQ" = 213,
                  "ALLOC_ODT" = 212,
                  "ALLOC_ODT_ENTRY" = 211,
                  "PROGRAM_START" = 210,
                  "PROGRAM_CLEAR" = 209,
                  "PROGRAM" = 208,
                  "PROGRAM_RESET" = 207,
                  "GET_PGM_PROCESSOR_INFO" = 206,
                  "GET_SECTOR_INFO" = 205,
                  "PROGRAM_PREPARE" = 204,
                  "PROGRAM_FORMAT" = 203,
                  "PROGRAM_NEXT" = 202,
                  "PROGRAM_MAX" = 201,
                  "PROGRAM_VERIFY" = 200
                })*;
                "COMMUNICATION_MODE_SUPPORTED" taggedunion {
                  "BLOCK" taggedstruct {
                    "MASTER" struct {
                      uchar;
                      uchar;
                    };
                  };
                  "INTERLEAVED" uchar;
                };
                "SEED_AND_KEY_EXTERNAL_FUNCTION" char[256];
              };
            };
            block "SEGMENT" struct {
              uchar;
              uchar;
              uchar;
              uchar;
              uchar;
              taggedstruct {
                block "CHECKSUM" struct {
                  enum {
                    "XCP_ADD_11" = 1,
                    "XCP_ADD_12" = 2,
                    "XCP_ADD_14" = 3,
                    "XCP_ADD_22" = 4,
                    "XCP_ADD_24" = 5,
                    "XCP_ADD_44" = 6,
                    "XCP_CRC_16" = 7,
                    "XCP_CRC_16_CITT" = 8,
                    "XCP_CRC_32" = 9,
                    "XCP_USER_DEFINED" = 255
                  };
                  taggedstruct {
                    "MAX_BLOCK_SIZE" ulong;
                    "EXTERNAL_FUNCTION" char[256];
                  };
                };
                (block "PAGE" struct {
                  uchar;
                  enum {
                    "ECU_ACCESS_NOT_ALLOWED" = 0,
                    "ECU_ACCESS_WITHOUT_XCP_ONLY" = 1,
                    "ECU_ACCESS_WITH_XCP_ONLY" = 2,
                    "ECU_ACCESS_DONT_CARE" = 3
                  };
                  enum {
                    "XCP_READ_ACCESS_NOT_ALLOWED" = 0,
                    "XCP_READ_ACCESS_WITHOUT_ECU_ONLY" = 1,
                    "XCP_READ_ACCESS_WITH_ECU_ONLY" = 2,
                    "XCP_READ_ACCESS_DONT_CARE" = 3
                  };
                  enum {
                    "XCP_WRITE_ACCESS_NOT_ALLOWED" = 0,
                    "XCP_WRITE_ACCESS_WITHOUT_ECU_ONLY" = 1,
                    "XCP_WRITE_ACCESS_WITH_ECU_ONLY" = 2,
                    "XCP_WRITE_ACCESS_DONT_CARE" = 3
                  };
                  taggedstruct {
                    "INIT_SEGMENT" uchar;
                  };
                })*;
                (block "ADDRESS_MAPPING" struct {
                  ulong;
                  ulong;
                  ulong;
                })*;
                "PGM_VERIFY" ulong;
              };
            };
            block "DAQ" struct {
              enum {
                "STATIC" = 0,
                "DYNAMIC" = 1
              };
              uint;
              uint;
              uchar;
              enum {
                "OPTIMISATION_TYPE_DEFAULT" = 0,
                "OPTIMISATION_TYPE_ODT_TYPE_16" = 1,
                "OPTIMISATION_TYPE_ODT_TYPE_32" = 2,
                "OPTIMISATION_TYPE_ODT_TYPE_64" = 3,
                "OPTIMISATION_TYPE_ODT_TYPE_ALIGNMENT" = 4,
                "OPTIMISATION_TYPE_MAX_ENTRY_SIZE" = 5
              };
              enum {
                "ADDRESS_EXTENSION_FREE" = 0,
                "ADDRESS_EXTENSION_ODT" = 1,
                "ADDRESS_EXTENSION_DAQ" = 3
              };
              enum {
                "IDENTIFICATION_FIELD_TYPE_ABSOLUTE" = 0,
                "IDENTIFICATION_FIELD_TYPE_RELATIVE_BYTE" = 1,
                "IDENTIFICATION_FIELD_TYPE_RELATIVE_WORD" = 2,
                "IDENTIFICATION_FIELD_TYPE_RELATIVE_WORD_ALIGNED" = 3
              };
              enum {
                "GRANULARITY_ODT_ENTRY_SIZE_DAQ_BYTE" = 1,
                "GRANULARITY_ODT_ENTRY_SIZE_DAQ_WORD" = 2,
                "GRANULARITY_ODT_ENTRY_SIZE_DAQ_DWORD" = 4,
                "GRANULARITY_ODT_ENTRY_SIZE_DAQ_DLONG" = 8
              };
              uchar;
              enum {
                "NO_OVERLOAD_INDICATION" = 0,
                "OVERLOAD_INDICATION_PID" = 1,
                "OVERLOAD_INDICATION_EVENT" = 2
              };
              taggedstruct {
                "PRESCALER_SUPPORTED" ;
                "RESUME_SUPPORTED" ;
                block "STIM" struct {
                  enum {
                    "GRANULARITY_ODT_ENTRY_SIZE_STIM_BYTE" = 1,
                    "GRANULARITY_ODT_ENTRY_SIZE_STIM_WORD" = 2,
                    "GRANULARITY_ODT_ENTRY_SIZE_STIM_DWORD" = 4,
                    "GRANULARITY_ODT_ENTRY_SIZE_STIM_DLONG" = 8
                  };
                  uchar;
                  taggedstruct {
                    "BIT_STIM_SUPPORTED" ;
                  };
                };
                block "TIMESTAMP_SUPPORTED" struct {
                  uint;
                  enum {
                    "NO_TIME_STAMP" = 0,
                    "SIZE_BYTE" = 1,
                    "SIZE_WORD" = 2,
                    "SIZE_DWORD" = 4
                  };
                  enum {
                    "UNIT_1NS" = 0,
                    "UNIT_10NS" = 1,
                    "UNIT_100NS" = 2,
                    "UNIT_1US" = 3,
                    "UNIT_10US" = 4,
                    "UNIT_100US" = 5,
                    "UNIT_1MS" = 6,
                    "UNIT_10MS" = 7,
                    "UNIT_100MS" = 8,
                    "UNIT_1S" = 9
                  };
                  taggedstruct {
                    "TIMESTAMP_FIXED" ;
                  };
                };
                "PID_OFF_SUPPORTED" ;
                (block "DAQ_LIST" struct {
                  uint;
                  taggedstruct {
                    "DAQ_LIST_TYPE" enum {
                      "DAQ" = 1,
                      "STIM" = 2,
                      "DAQ_STIM" = 3
                    };
                    "MAX_ODT" uchar;
                    "MAX_ODT_ENTRIES" uchar;
                    "FIRST_PID" uchar;
                    "EVENT_FIXED" uint;
                    block "PREDEFINED" taggedstruct {
                      (block "ODT" struct {
                        uchar;
                        taggedstruct {
                          ("ODT_ENTRY" struct {
                            uchar;
                            ulong;
                            uchar;
                            uchar;
                            uchar;
                          })*;
                        };
                      })*;
                    };
                  };
                })*;
                (block "EVENT" struct {
                  char[101];
                  char[9];
                  uint;
                  enum {
                    "DAQ" = 1,
                    "STIM" = 2,
                    "DAQ_STIM" = 3
                  };
                  uchar;
                  uchar;
                  uchar;
                  uchar;
                })*;
              };
            };
            block "PAG" struct {
              uchar;
              taggedstruct {
                "FREEZE_SUPPORTED" ;
              };
            };
            block "PGM" struct {
              enum {
                "PGM_MODE_ABSOLUTE" = 1,
                "PGM_MODE_FUNCTIONAL" = 2,
                "PGM_MODE_ABSOLUTE_AND_FUNCTIONAL" = 3
              };
              uchar;
              uchar;
              taggedstruct {
                (block "SECTOR" struct {
                  char[101];
                  uchar;
                  ulong;
                  ulong;
                  uchar;
                  uchar;
                  uchar;
                })*;
                "COMMUNICATION_MODE_SUPPORTED" taggedunion {
                  "BLOCK" taggedstruct {
                    "SLAVE" ;
                    "MASTER" struct {
                      uchar;
                      uchar;
                    };
                  };
                  "INTERLEAVED" uchar;
                };
              };
            };
            block "DAQ_EVENT" taggedunion {
              "FIXED_EVENT_LIST" taggedstruct {
                ("EVENT" uint)*;
              };
              "VARIABLE" taggedstruct {
                block "AVAILABLE_EVENT_LIST" taggedstruct {
                  ("EVENT" uint)*;
                };
                block "DEFAULT_EVENT_LIST" taggedstruct {
                  ("EVENT" uint)*;
                };
              };
            };
            block "XCP_ON_CAN" struct {
              uint;
              taggedstruct {
                "CAN_ID_BROADCAST" ulong;
                "CAN_ID_MASTER" ulong;
                "CAN_ID_SLAVE" ulong;
                "BAUDRATE" ulong;
                "SAMPLE_POINT" uchar;
                "SAMPLE_RATE" enum {
                  "SINGLE" = 1,
                  "TRIPLE" = 3
                };
                "BTL_CYCLES" uchar;
                "SJW" uchar;
                "SYNC_EDGE" enum {
                  "SINGLE" = 1,
                  "DUAL" = 2
                };
                "MAX_DLC_REQUIRED" ;
                (block "DAQ_LIST_CAN_ID" struct {
                  uint;
                  taggedstruct {
                    "VARIABLE" ;
                    "FIXED" ulong;
                  };
                })*;
                block "PROTOCOL_LAYER" struct {
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uchar;
                  uint;
                  enum {
                    "BYTE_ORDER_MSB_LAST" = 0,
                    "BYTE_ORDER_MSB_FIRST" = 1
                  };
                  enum {
                    "ADDRESS_GRANULARITY_BYTE" = 1,
                    "ADDRESS_GRANULARITY_WORD" = 2,
                    "ADDRESS_GRANULARITY_DWORD" = 4
                  };
                  taggedstruct {
                    ("OPTIONAL_CMD" enum {
                      "GET_COMM_MODE_INFO" = 251,
                      "GET_ID" = 250,
                      "SET_REQUEST" = 249,
                      "GET_SEED" = 248,
                      "UNLOCK" = 247,
                      "SET_MTA" = 246,
                      "UPLOAD" = 245,
                      "SHORT_UPLOAD" = 244,
                      "BUILD_CHECKSUM" = 243,
                      "TRANSPORT_LAYER_CMD" = 242,
                      "USER_CMD" = 241,
                      "DOWNLOAD" = 240,
                      "DOWNLOAD_NEXT" = 239,
                      "DOWNLOAD_MAX" = 238,
                      "SHORT_DOWNLOAD" = 237,
                      "MODIFY_BITS" = 236,
                      "SET_CAL_PAGE" = 235,
                      "GET_CAL_PAGE" = 234,
                      "GET_PAG_PROCESSOR_INFO" = 233,
                      "GET_SEGMENT_INFO" = 232,
                      "GET_PAGE_INFO" = 231,
                      "SET_SEGMENT_MODE" = 230,
                      "GET_SEGMENT_MODE" = 229,
                      "COPY_CAL_PAGE" = 228,
                      "CLEAR_DAQ_LIST" = 227,
                      "SET_DAQ_PTR" = 226,
                      "WRITE_DAQ" = 225,
                      "SET_DAQ_LIST_MODE" = 224,
                      "GET_DAQ_LIST_MODE" = 223,
                      "START_STOP_DAQ_LIST" = 222,
                      "START_STOP_SYNCH" = 221,
                      "GET_DAQ_CLOCK" = 220,
                      "READ_DAQ" = 219,
                      "GET_DAQ_PROCESSOR_INFO" = 218,
                      "GET_DAQ_RESOLUTION_INFO" = 217,
                      "GET_DAQ_LIST_INFO" = 216,
                      "GET_DAQ_EVENT_INFO" = 215,
                      "FREE_DAQ" = 214,
                      "ALLOC_DAQ" = 213,
                      "ALLOC_ODT" = 212,
                      "ALLOC_ODT_ENTRY" = 211,
                      "PROGRAM_START" = 210,
                      "PROGRAM_CLEAR" = 209,
                      "PROGRAM" = 208,
                      "PROGRAM_RESET" = 207,
                      "GET_PGM_PROCESSOR_INFO" = 206,
                      "GET_SECTOR_INFO" = 205,
                      "PROGRAM_PREPARE" = 204,
                      "PROGRAM_FORMAT" = 203,
                      "PROGRAM_NEXT" = 202,
                      "PROGRAM_MAX" = 201,
                      "PROGRAM_VERIFY" = 200
                    })*;
                    "COMMUNICATION_MODE_SUPPORTED" taggedunion {
                      "BLOCK" taggedstruct {
                        "SLAVE" ;
                        "MASTER" struct {
                          uchar;
                          uchar;
                        };
                      };
                      "INTERLEAVED" uchar;
                    };
                    "SEED_AND_KEY_EXTERNAL_FUNCTION" char[256];
                  };
                };
                block "SEGMENT" struct {
                  uchar;
                  uchar;
                  uchar;
                  uchar;
                  uchar;
                  taggedstruct {
                    block "CHECKSUM" struct {
                      enum {
                        "XCP_ADD_11" = 1,
                        "XCP_ADD_12" = 2,
                        "XCP_ADD_14" = 3,
                        "XCP_ADD_22" = 4,
                        "XCP_ADD_24" = 5,
                        "XCP_ADD_44" = 6,
                        "XCP_CRC_16" = 7,
                        "XCP_CRC_16_CITT" = 8,
                        "XCP_CRC_32" = 9,
                        "XCP_USER_DEFINED" = 255
                      };
                      taggedstruct {
                        "MAX_BLOCK_SIZE" ulong;
                        "EXTERNAL_FUNCTION" char[256];
                      };
                    };
                    (block "PAGE" struct {
                      uchar;
                      enum {
                        "ECU_ACCESS_NOT_ALLOWED" = 0,
                        "ECU_ACCESS_WITHOUT_XCP_ONLY" = 1,
                        "ECU_ACCESS_WITH_XCP_ONLY" = 2,
                        "ECU_ACCESS_DONT_CARE" = 3
                      };
                      enum {
                        "XCP_READ_ACCESS_NOT_ALLOWED" = 0,
                        "XCP_READ_ACCESS_WITHOUT_ECU_ONLY" = 1,
                        "XCP_READ_ACCESS_WITH_ECU_ONLY" = 2,
                        "XCP_READ_ACCESS_DONT_CARE" = 3
                      };
                      enum {
                        "XCP_WRITE_ACCESS_NOT_ALLOWED" = 0,
                        "XCP_WRITE_ACCESS_WITHOUT_ECU_ONLY" = 1,
                        "XCP_WRITE_ACCESS_WITH_ECU_ONLY" = 2,
                        "XCP_WRITE_ACCESS_DONT_CARE" = 3
                      };
                      taggedstruct {
                        "INIT_SEGMENT" uchar;
                      };
                    })*;
                    (block "ADDRESS_MAPPING" struct {
                      ulong;
                      ulong;
                      ulong;
                    })*;
                    "PGM_VERIFY" ulong;
                  };
                };
                block "DAQ" struct {
                  enum {
                    "STATIC" = 0,
                    "DYNAMIC" = 1
                  };
                  uint;
                  uint;
                  uchar;
                  enum {
                    "OPTIMISATION_TYPE_DEFAULT" = 0,
                    "OPTIMISATION_TYPE_ODT_TYPE_16" = 1,
                    "OPTIMISATION_TYPE_ODT_TYPE_32" = 2,
                    "OPTIMISATION_TYPE_ODT_TYPE_64" = 3,
                    "OPTIMISATION_TYPE_ODT_TYPE_ALIGNMENT" = 4,
                    "OPTIMISATION_TYPE_MAX_ENTRY_SIZE" = 5
                  };
                  enum {
                    "ADDRESS_EXTENSION_FREE" = 0,
                    "ADDRESS_EXTENSION_ODT" = 1,
                    "ADDRESS_EXTENSION_DAQ" = 3
                  };
                  enum {
                    "IDENTIFICATION_FIELD_TYPE_ABSOLUTE" = 0,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_BYTE" = 1,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_WORD" = 2,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_WORD_ALIGNED" = 3
                  };
                  enum {
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_BYTE" = 1,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_WORD" = 2,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_DWORD" = 4,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_DLONG" = 8
                  };
                  uchar;
                  enum {
                    "NO_OVERLOAD_INDICATION" = 0,
                    "OVERLOAD_INDICATION_PID" = 1,
                    "OVERLOAD_INDICATION_EVENT" = 2
                  };
                  taggedstruct {
                    "PRESCALER_SUPPORTED" ;
                    "RESUME_SUPPORTED" ;
                    block "STIM" struct {
                      enum {
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_BYTE" = 1,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_WORD" = 2,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_DWORD" = 4,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_DLONG" = 8
                      };
                      uchar;
                      taggedstruct {
                        "BIT_STIM_SUPPORTED" ;
                      };
                    };
                    block "TIMESTAMP_SUPPORTED" struct {
                      uint;
                      enum {
                        "NO_TIME_STAMP" = 0,
                        "SIZE_BYTE" = 1,
                        "SIZE_WORD" = 2,
                        "SIZE_DWORD" = 4
                      };
                      enum {
                        "UNIT_1NS" = 0,
                        "UNIT_10NS" = 1,
                        "UNIT_100NS" = 2,
                        "UNIT_1US" = 3,
                        "UNIT_10US" = 4,
                        "UNIT_100US" = 5,
                        "UNIT_1MS" = 6,
                        "UNIT_10MS" = 7,
                        "UNIT_100MS" = 8,
                        "UNIT_1S" = 9
                      };
                      taggedstruct {
                        "TIMESTAMP_FIXED" ;
                      };
                    };
                    "PID_OFF_SUPPORTED" ;
                    (block "DAQ_LIST" struct {
                      uint;
                      taggedstruct {
                        "DAQ_LIST_TYPE" enum {
                          "DAQ" = 1,
                          "STIM" = 2,
                          "DAQ_STIM" = 3
                        };
                        "MAX_ODT" uchar;
                        "MAX_ODT_ENTRIES" uchar;
                        "FIRST_PID" uchar;
                        "EVENT_FIXED" uint;
                        block "PREDEFINED" taggedstruct {
                          (block "ODT" struct {
                            uchar;
                            taggedstruct {
                              ("ODT_ENTRY" struct {
                                uchar;
                                ulong;
                                uchar;
                                uchar;
                                uchar;
                              })*;
                            };
                          })*;
                        };
                      };
                    })*;
                    (block "EVENT" struct {
                      char[101];
                      char[9];
                      uint;
                      enum {
                        "DAQ" = 1,
                        "STIM" = 2,
                        "DAQ_STIM" = 3
                      };
                      uchar;
                      uchar;
                      uchar;
                      uchar;
                    })*;
                  };
                };
                block "PAG" struct {
                  uchar;
                  taggedstruct {
                    "FREEZE_SUPPORTED" ;
                  };
                };
                block "PGM" struct {
                  enum {
                    "PGM_MODE_ABSOLUTE" = 1,
                    "PGM_MODE_FUNCTIONAL" = 2,
                    "PGM_MODE_ABSOLUTE_AND_FUNCTIONAL" = 3
                  };
                  uchar;
                  uchar;
                  taggedstruct {
                    (block "SECTOR" struct {
                      char[101];
                      uchar;
                      ulong;
                      ulong;
                      uchar;
                      uchar;
                      uchar;
                    })*;
                    "COMMUNICATION_MODE_SUPPORTED" taggedunion {
                      "BLOCK" taggedstruct {
                        "SLAVE" ;
                        "MASTER" struct {
                          uchar;
                          uchar;
                        };
                      };
                      "INTERLEAVED" uchar;
                    };
                  };
                };
                block "DAQ_EVENT" taggedunion {
                  "FIXED_EVENT_LIST" taggedstruct {
                    ("EVENT" uint)*;
                  };
                  "VARIABLE" taggedstruct {
                    block "AVAILABLE_EVENT_LIST" taggedstruct {
                      ("EVENT" uint)*;
                    };
                    block "DEFAULT_EVENT_LIST" taggedstruct {
                      ("EVENT" uint)*;
                    };
                  };
                };
              };
            };
            block "XCP_ON_SxI" struct {
              uint;
              ulong;
              taggedstruct {
                "ASYNCH_FULL_DUPLEX_MODE" struct {
                  enum {
                    "PARITY_NONE" = 0,
                    "PARITY_ODD" = 1,
                    "PARITY_EVEN" = 2
                  };
                  enum {
                    "ONE_STOP_BIT" = 1,
                    "TWO_STOP_BITS" = 2
                  };
                };
                "SYNCH_FULL_DUPLEX_MODE_BYTE" ;
                "SYNCH_FULL_DUPLEX_MODE_WORD" ;
                "SYNCH_FULL_DUPLEX_MODE_DWORD" ;
                "SYNCH_MASTER_SLAVE_MODE_BYTE" ;
                "SYNCH_MASTER_SLAVE_MODE_WORD" ;
                "SYNCH_MASTER_SLAVE_MODE_DWORD" ;
              };
              enum {
                "HEADER_LEN_BYTE" = 0,
                "HEADER_LEN_CTR_BYTE" = 1,
                "HEADER_LEN_WORD" = 2,
                "HEADER_LEN_CTR_WORD" = 3
              };
              enum {
                "NO_CHECKSUM" = 0,
                "CHECKSUM_BYTE" = 1,
                "CHECKSUM_WORD" = 2
              };
              taggedstruct {
                block "PROTOCOL_LAYER" struct {
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uchar;
                  uint;
                  enum {
                    "BYTE_ORDER_MSB_LAST" = 0,
                    "BYTE_ORDER_MSB_FIRST" = 1
                  };
                  enum {
                    "ADDRESS_GRANULARITY_BYTE" = 1,
                    "ADDRESS_GRANULARITY_WORD" = 2,
                    "ADDRESS_GRANULARITY_DWORD" = 4
                  };
                  taggedstruct {
                    ("OPTIONAL_CMD" enum {
                      "GET_COMM_MODE_INFO" = 251,
                      "GET_ID" = 250,
                      "SET_REQUEST" = 249,
                      "GET_SEED" = 248,
                      "UNLOCK" = 247,
                      "SET_MTA" = 246,
                      "UPLOAD" = 245,
                      "SHORT_UPLOAD" = 244,
                      "BUILD_CHECKSUM" = 243,
                      "TRANSPORT_LAYER_CMD" = 242,
                      "USER_CMD" = 241,
                      "DOWNLOAD" = 240,
                      "DOWNLOAD_NEXT" = 239,
                      "DOWNLOAD_MAX" = 238,
                      "SHORT_DOWNLOAD" = 237,
                      "MODIFY_BITS" = 236,
                      "SET_CAL_PAGE" = 235,
                      "GET_CAL_PAGE" = 234,
                      "GET_PAG_PROCESSOR_INFO" = 233,
                      "GET_SEGMENT_INFO" = 232,
                      "GET_PAGE_INFO" = 231,
                      "SET_SEGMENT_MODE" = 230,
                      "GET_SEGMENT_MODE" = 229,
                      "COPY_CAL_PAGE" = 228,
                      "CLEAR_DAQ_LIST" = 227,
                      "SET_DAQ_PTR" = 226,
                      "WRITE_DAQ" = 225,
                      "SET_DAQ_LIST_MODE" = 224,
                      "GET_DAQ_LIST_MODE" = 223,
                      "START_STOP_DAQ_LIST" = 222,
                      "START_STOP_SYNCH" = 221,
                      "GET_DAQ_CLOCK" = 220,
                      "READ_DAQ" = 219,
                      "GET_DAQ_PROCESSOR_INFO" = 218,
                      "GET_DAQ_RESOLUTION_INFO" = 217,
                      "GET_DAQ_LIST_INFO" = 216,
                      "GET_DAQ_EVENT_INFO" = 215,
                      "FREE_DAQ" = 214,
                      "ALLOC_DAQ" = 213,
                      "ALLOC_ODT" = 212,
                      "ALLOC_ODT_ENTRY" = 211,
                      "PROGRAM_START" = 210,
                      "PROGRAM_CLEAR" = 209,
                      "PROGRAM" = 208,
                      "PROGRAM_RESET" = 207,
                      "GET_PGM_PROCESSOR_INFO" = 206,
                      "GET_SECTOR_INFO" = 205,
                      "PROGRAM_PREPARE" = 204,
                      "PROGRAM_FORMAT" = 203,
                      "PROGRAM_NEXT" = 202,
                      "PROGRAM_MAX" = 201,
                      "PROGRAM_VERIFY" = 200
                    })*;
                    "COMMUNICATION_MODE_SUPPORTED" taggedunion {
                      "BLOCK" taggedstruct {
                        "SLAVE" ;
                        "MASTER" struct {
                          uchar;
                          uchar;
                        };
                      };
                      "INTERLEAVED" uchar;
                    };
                    "SEED_AND_KEY_EXTERNAL_FUNCTION" char[256];
                  };
                };
                block "SEGMENT" struct {
                  uchar;
                  uchar;
                  uchar;
                  uchar;
                  uchar;
                  taggedstruct {
                    block "CHECKSUM" struct {
                      enum {
                        "XCP_ADD_11" = 1,
                        "XCP_ADD_12" = 2,
                        "XCP_ADD_14" = 3,
                        "XCP_ADD_22" = 4,
                        "XCP_ADD_24" = 5,
                        "XCP_ADD_44" = 6,
                        "XCP_CRC_16" = 7,
                        "XCP_CRC_16_CITT" = 8,
                        "XCP_CRC_32" = 9,
                        "XCP_USER_DEFINED" = 255
                      };
                      taggedstruct {
                        "MAX_BLOCK_SIZE" ulong;
                        "EXTERNAL_FUNCTION" char[256];
                      };
                    };
                    (block "PAGE" struct {
                      uchar;
                      enum {
                        "ECU_ACCESS_NOT_ALLOWED" = 0,
                        "ECU_ACCESS_WITHOUT_XCP_ONLY" = 1,
                        "ECU_ACCESS_WITH_XCP_ONLY" = 2,
                        "ECU_ACCESS_DONT_CARE" = 3
                      };
                      enum {
                        "XCP_READ_ACCESS_NOT_ALLOWED" = 0,
                        "XCP_READ_ACCESS_WITHOUT_ECU_ONLY" = 1,
                        "XCP_READ_ACCESS_WITH_ECU_ONLY" = 2,
                        "XCP_READ_ACCESS_DONT_CARE" = 3
                      };
                      enum {
                        "XCP_WRITE_ACCESS_NOT_ALLOWED" = 0,
                        "XCP_WRITE_ACCESS_WITHOUT_ECU_ONLY" = 1,
                        "XCP_WRITE_ACCESS_WITH_ECU_ONLY" = 2,
                        "XCP_WRITE_ACCESS_DONT_CARE" = 3
                      };
                      taggedstruct {
                        "INIT_SEGMENT" uchar;
                      };
                    })*;
                    (block "ADDRESS_MAPPING" struct {
                      ulong;
                      ulong;
                      ulong;
                    })*;
                    "PGM_VERIFY" ulong;
                  };
                };
                block "DAQ" struct {
                  enum {
                    "STATIC" = 0,
                    "DYNAMIC" = 1
                  };
                  uint;
                  uint;
                  uchar;
                  enum {
                    "OPTIMISATION_TYPE_DEFAULT" = 0,
                    "OPTIMISATION_TYPE_ODT_TYPE_16" = 1,
                    "OPTIMISATION_TYPE_ODT_TYPE_32" = 2,
                    "OPTIMISATION_TYPE_ODT_TYPE_64" = 3,
                    "OPTIMISATION_TYPE_ODT_TYPE_ALIGNMENT" = 4,
                    "OPTIMISATION_TYPE_MAX_ENTRY_SIZE" = 5
                  };
                  enum {
                    "ADDRESS_EXTENSION_FREE" = 0,
                    "ADDRESS_EXTENSION_ODT" = 1,
                    "ADDRESS_EXTENSION_DAQ" = 3
                  };
                  enum {
                    "IDENTIFICATION_FIELD_TYPE_ABSOLUTE" = 0,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_BYTE" = 1,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_WORD" = 2,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_WORD_ALIGNED" = 3
                  };
                  enum {
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_BYTE" = 1,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_WORD" = 2,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_DWORD" = 4,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_DLONG" = 8
                  };
                  uchar;
                  enum {
                    "NO_OVERLOAD_INDICATION" = 0,
                    "OVERLOAD_INDICATION_PID" = 1,
                    "OVERLOAD_INDICATION_EVENT" = 2
                  };
                  taggedstruct {
                    "PRESCALER_SUPPORTED" ;
                    "RESUME_SUPPORTED" ;
                    block "STIM" struct {
                      enum {
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_BYTE" = 1,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_WORD" = 2,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_DWORD" = 4,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_DLONG" = 8
                      };
                      uchar;
                      taggedstruct {
                        "BIT_STIM_SUPPORTED" ;
                      };
                    };
                    block "TIMESTAMP_SUPPORTED" struct {
                      uint;
                      enum {
                        "NO_TIME_STAMP" = 0,
                        "SIZE_BYTE" = 1,
                        "SIZE_WORD" = 2,
                        "SIZE_DWORD" = 4
                      };
                      enum {
                        "UNIT_1NS" = 0,
                        "UNIT_10NS" = 1,
                        "UNIT_100NS" = 2,
                        "UNIT_1US" = 3,
                        "UNIT_10US" = 4,
                        "UNIT_100US" = 5,
                        "UNIT_1MS" = 6,
                        "UNIT_10MS" = 7,
                        "UNIT_100MS" = 8,
                        "UNIT_1S" = 9
                      };
                      taggedstruct {
                        "TIMESTAMP_FIXED" ;
                      };
                    };
                    "PID_OFF_SUPPORTED" ;
                    (block "DAQ_LIST" struct {
                      uint;
                      taggedstruct {
                        "DAQ_LIST_TYPE" enum {
                          "DAQ" = 1,
                          "STIM" = 2,
                          "DAQ_STIM" = 3
                        };
                        "MAX_ODT" uchar;
                        "MAX_ODT_ENTRIES" uchar;
                        "FIRST_PID" uchar;
                        "EVENT_FIXED" uint;
                        block "PREDEFINED" taggedstruct {
                          (block "ODT" struct {
                            uchar;
                            taggedstruct {
                              ("ODT_ENTRY" struct {
                                uchar;
                                ulong;
                                uchar;
                                uchar;
                                uchar;
                              })*;
                            };
                          })*;
                        };
                      };
                    })*;
                    (block "EVENT" struct {
                      char[101];
                      char[9];
                      uint;
                      enum {
                        "DAQ" = 1,
                        "STIM" = 2,
                        "DAQ_STIM" = 3
                      };
                      uchar;
                      uchar;
                      uchar;
                      uchar;
                    })*;
                  };
                };
                block "PAG" struct {
                  uchar;
                  taggedstruct {
                    "FREEZE_SUPPORTED" ;
                  };
                };
                block "PGM" struct {
                  enum {
                    "PGM_MODE_ABSOLUTE" = 1,
                    "PGM_MODE_FUNCTIONAL" = 2,
                    "PGM_MODE_ABSOLUTE_AND_FUNCTIONAL" = 3
                  };
                  uchar;
                  uchar;
                  taggedstruct {
                    (block "SECTOR" struct {
                      char[101];
                      uchar;
                      ulong;
                      ulong;
                      uchar;
                      uchar;
                      uchar;
                    })*;
                    "COMMUNICATION_MODE_SUPPORTED" taggedunion {
                      "BLOCK" taggedstruct {
                        "SLAVE" ;
                        "MASTER" struct {
                          uchar;
                          uchar;
                        };
                      };
                      "INTERLEAVED" uchar;
                    };
                  };
                };
                block "DAQ_EVENT" taggedunion {
                  "FIXED_EVENT_LIST" taggedstruct {
                    ("EVENT" uint)*;
                  };
                  "VARIABLE" taggedstruct {
                    block "AVAILABLE_EVENT_LIST" taggedstruct {
                      ("EVENT" uint)*;
                    };
                    block "DEFAULT_EVENT_LIST" taggedstruct {
                      ("EVENT" uint)*;
                    };
                  };
                };
              };
            };
            block "XCP_ON_TCP_IP" struct {
              uint;
              uint;
              taggedunion {
                "HOST_NAME" char[256];
                "ADDRESS" char[15];
              };
              taggedstruct {
                block "PROTOCOL_LAYER" struct {
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uchar;
                  uint;
                  enum {
                    "BYTE_ORDER_MSB_LAST" = 0,
                    "BYTE_ORDER_MSB_FIRST" = 1
                  };
                  enum {
                    "ADDRESS_GRANULARITY_BYTE" = 1,
                    "ADDRESS_GRANULARITY_WORD" = 2,
                    "ADDRESS_GRANULARITY_DWORD" = 4
                  };
                  taggedstruct {
                    ("OPTIONAL_CMD" enum {
                      "GET_COMM_MODE_INFO" = 251,
                      "GET_ID" = 250,
                      "SET_REQUEST" = 249,
                      "GET_SEED" = 248,
                      "UNLOCK" = 247,
                      "SET_MTA" = 246,
                      "UPLOAD" = 245,
                      "SHORT_UPLOAD" = 244,
                      "BUILD_CHECKSUM" = 243,
                      "TRANSPORT_LAYER_CMD" = 242,
                      "USER_CMD" = 241,
                      "DOWNLOAD" = 240,
                      "DOWNLOAD_NEXT" = 239,
                      "DOWNLOAD_MAX" = 238,
                      "SHORT_DOWNLOAD" = 237,
                      "MODIFY_BITS" = 236,
                      "SET_CAL_PAGE" = 235,
                      "GET_CAL_PAGE" = 234,
                      "GET_PAG_PROCESSOR_INFO" = 233,
                      "GET_SEGMENT_INFO" = 232,
                      "GET_PAGE_INFO" = 231,
                      "SET_SEGMENT_MODE" = 230,
                      "GET_SEGMENT_MODE" = 229,
                      "COPY_CAL_PAGE" = 228,
                      "CLEAR_DAQ_LIST" = 227,
                      "SET_DAQ_PTR" = 226,
                      "WRITE_DAQ" = 225,
                      "SET_DAQ_LIST_MODE" = 224,
                      "GET_DAQ_LIST_MODE" = 223,
                      "START_STOP_DAQ_LIST" = 222,
                      "START_STOP_SYNCH" = 221,
                      "GET_DAQ_CLOCK" = 220,
                      "READ_DAQ" = 219,
                      "GET_DAQ_PROCESSOR_INFO" = 218,
                      "GET_DAQ_RESOLUTION_INFO" = 217,
                      "GET_DAQ_LIST_INFO" = 216,
                      "GET_DAQ_EVENT_INFO" = 215,
                      "FREE_DAQ" = 214,
                      "ALLOC_DAQ" = 213,
                      "ALLOC_ODT" = 212,
                      "ALLOC_ODT_ENTRY" = 211,
                      "PROGRAM_START" = 210,
                      "PROGRAM_CLEAR" = 209,
                      "PROGRAM" = 208,
                      "PROGRAM_RESET" = 207,
                      "GET_PGM_PROCESSOR_INFO" = 206,
                      "GET_SECTOR_INFO" = 205,
                      "PROGRAM_PREPARE" = 204,
                      "PROGRAM_FORMAT" = 203,
                      "PROGRAM_NEXT" = 202,
                      "PROGRAM_MAX" = 201,
                      "PROGRAM_VERIFY" = 200
                    })*;
                    "COMMUNICATION_MODE_SUPPORTED" taggedunion {
                      "BLOCK" taggedstruct {
                        "SLAVE" ;
                        "MASTER" struct {
                          uchar;
                          uchar;
                        };
                      };
                      "INTERLEAVED" uchar;
                    };
                    "SEED_AND_KEY_EXTERNAL_FUNCTION" char[256];
                  };
                };
                block "SEGMENT" struct {
                  uchar;
                  uchar;
                  uchar;
                  uchar;
                  uchar;
                  taggedstruct {
                    block "CHECKSUM" struct {
                      enum {
                        "XCP_ADD_11" = 1,
                        "XCP_ADD_12" = 2,
                        "XCP_ADD_14" = 3,
                        "XCP_ADD_22" = 4,
                        "XCP_ADD_24" = 5,
                        "XCP_ADD_44" = 6,
                        "XCP_CRC_16" = 7,
                        "XCP_CRC_16_CITT" = 8,
                        "XCP_CRC_32" = 9,
                        "XCP_USER_DEFINED" = 255
                      };
                      taggedstruct {
                        "MAX_BLOCK_SIZE" ulong;
                        "EXTERNAL_FUNCTION" char[256];
                      };
                    };
                    (block "PAGE" struct {
                      uchar;
                      enum {
                        "ECU_ACCESS_NOT_ALLOWED" = 0,
                        "ECU_ACCESS_WITHOUT_XCP_ONLY" = 1,
                        "ECU_ACCESS_WITH_XCP_ONLY" = 2,
                        "ECU_ACCESS_DONT_CARE" = 3
                      };
                      enum {
                        "XCP_READ_ACCESS_NOT_ALLOWED" = 0,
                        "XCP_READ_ACCESS_WITHOUT_ECU_ONLY" = 1,
                        "XCP_READ_ACCESS_WITH_ECU_ONLY" = 2,
                        "XCP_READ_ACCESS_DONT_CARE" = 3
                      };
                      enum {
                        "XCP_WRITE_ACCESS_NOT_ALLOWED" = 0,
                        "XCP_WRITE_ACCESS_WITHOUT_ECU_ONLY" = 1,
                        "XCP_WRITE_ACCESS_WITH_ECU_ONLY" = 2,
                        "XCP_WRITE_ACCESS_DONT_CARE" = 3
                      };
                      taggedstruct {
                        "INIT_SEGMENT" uchar;
                      };
                    })*;
                    (block "ADDRESS_MAPPING" struct {
                      ulong;
                      ulong;
                      ulong;
                    })*;
                    "PGM_VERIFY" ulong;
                  };
                };
                block "DAQ" struct {
                  enum {
                    "STATIC" = 0,
                    "DYNAMIC" = 1
                  };
                  uint;
                  uint;
                  uchar;
                  enum {
                    "OPTIMISATION_TYPE_DEFAULT" = 0,
                    "OPTIMISATION_TYPE_ODT_TYPE_16" = 1,
                    "OPTIMISATION_TYPE_ODT_TYPE_32" = 2,
                    "OPTIMISATION_TYPE_ODT_TYPE_64" = 3,
                    "OPTIMISATION_TYPE_ODT_TYPE_ALIGNMENT" = 4,
                    "OPTIMISATION_TYPE_MAX_ENTRY_SIZE" = 5
                  };
                  enum {
                    "ADDRESS_EXTENSION_FREE" = 0,
                    "ADDRESS_EXTENSION_ODT" = 1,
                    "ADDRESS_EXTENSION_DAQ" = 3
                  };
                  enum {
                    "IDENTIFICATION_FIELD_TYPE_ABSOLUTE" = 0,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_BYTE" = 1,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_WORD" = 2,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_WORD_ALIGNED" = 3
                  };
                  enum {
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_BYTE" = 1,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_WORD" = 2,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_DWORD" = 4,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_DLONG" = 8
                  };
                  uchar;
                  enum {
                    "NO_OVERLOAD_INDICATION" = 0,
                    "OVERLOAD_INDICATION_PID" = 1,
                    "OVERLOAD_INDICATION_EVENT" = 2
                  };
                  taggedstruct {
                    "PRESCALER_SUPPORTED" ;
                    "RESUME_SUPPORTED" ;
                    block "STIM" struct {
                      enum {
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_BYTE" = 1,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_WORD" = 2,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_DWORD" = 4,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_DLONG" = 8
                      };
                      uchar;
                      taggedstruct {
                        "BIT_STIM_SUPPORTED" ;
                      };
                    };
                    block "TIMESTAMP_SUPPORTED" struct {
                      uint;
                      enum {
                        "NO_TIME_STAMP" = 0,
                        "SIZE_BYTE" = 1,
                        "SIZE_WORD" = 2,
                        "SIZE_DWORD" = 4
                      };
                      enum {
                        "UNIT_1NS" = 0,
                        "UNIT_10NS" = 1,
                        "UNIT_100NS" = 2,
                        "UNIT_1US" = 3,
                        "UNIT_10US" = 4,
                        "UNIT_100US" = 5,
                        "UNIT_1MS" = 6,
                        "UNIT_10MS" = 7,
                        "UNIT_100MS" = 8,
                        "UNIT_1S" = 9
                      };
                      taggedstruct {
                        "TIMESTAMP_FIXED" ;
                      };
                    };
                    "PID_OFF_SUPPORTED" ;
                    (block "DAQ_LIST" struct {
                      uint;
                      taggedstruct {
                        "DAQ_LIST_TYPE" enum {
                          "DAQ" = 1,
                          "STIM" = 2,
                          "DAQ_STIM" = 3
                        };
                        "MAX_ODT" uchar;
                        "MAX_ODT_ENTRIES" uchar;
                        "FIRST_PID" uchar;
                        "EVENT_FIXED" uint;
                        block "PREDEFINED" taggedstruct {
                          (block "ODT" struct {
                            uchar;
                            taggedstruct {
                              ("ODT_ENTRY" struct {
                                uchar;
                                ulong;
                                uchar;
                                uchar;
                                uchar;
                              })*;
                            };
                          })*;
                        };
                      };
                    })*;
                    (block "EVENT" struct {
                      char[101];
                      char[9];
                      uint;
                      enum {
                        "DAQ" = 1,
                        "STIM" = 2,
                        "DAQ_STIM" = 3
                      };
                      uchar;
                      uchar;
                      uchar;
                      uchar;
                    })*;
                  };
                };
                block "PAG" struct {
                  uchar;
                  taggedstruct {
                    "FREEZE_SUPPORTED" ;
                  };
                };
                block "PGM" struct {
                  enum {
                    "PGM_MODE_ABSOLUTE" = 1,
                    "PGM_MODE_FUNCTIONAL" = 2,
                    "PGM_MODE_ABSOLUTE_AND_FUNCTIONAL" = 3
                  };
                  uchar;
                  uchar;
                  taggedstruct {
                    (block "SECTOR" struct {
                      char[101];
                      uchar;
                      ulong;
                      ulong;
                      uchar;
                      uchar;
                      uchar;
                    })*;
                    "COMMUNICATION_MODE_SUPPORTED" taggedunion {
                      "BLOCK" taggedstruct {
                        "SLAVE" ;
                        "MASTER" struct {
                          uchar;
                          uchar;
                        };
                      };
                      "INTERLEAVED" uchar;
                    };
                  };
                };
                block "DAQ_EVENT" taggedunion {
                  "FIXED_EVENT_LIST" taggedstruct {
                    ("EVENT" uint)*;
                  };
                  "VARIABLE" taggedstruct {
                    block "AVAILABLE_EVENT_LIST" taggedstruct {
                      ("EVENT" uint)*;
                    };
                    block "DEFAULT_EVENT_LIST" taggedstruct {
                      ("EVENT" uint)*;
                    };
                  };
                };
              };
            };
            block "XCP_ON_UDP_IP" struct {
              uint;
              uint;
              taggedunion {
                "HOST_NAME" char[256];
                "ADDRESS" char[15];
              };
              taggedstruct {
                block "PROTOCOL_LAYER" struct {
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uchar;
                  uint;
                  enum {
                    "BYTE_ORDER_MSB_LAST" = 0,
                    "BYTE_ORDER_MSB_FIRST" = 1
                  };
                  enum {
                    "ADDRESS_GRANULARITY_BYTE" = 1,
                    "ADDRESS_GRANULARITY_WORD" = 2,
                    "ADDRESS_GRANULARITY_DWORD" = 4
                  };
                  taggedstruct {
                    ("OPTIONAL_CMD" enum {
                      "GET_COMM_MODE_INFO" = 251,
                      "GET_ID" = 250,
                      "SET_REQUEST" = 249,
                      "GET_SEED" = 248,
                      "UNLOCK" = 247,
                      "SET_MTA" = 246,
                      "UPLOAD" = 245,
                      "SHORT_UPLOAD" = 244,
                      "BUILD_CHECKSUM" = 243,
                      "TRANSPORT_LAYER_CMD" = 242,
                      "USER_CMD" = 241,
                      "DOWNLOAD" = 240,
                      "DOWNLOAD_NEXT" = 239,
                      "DOWNLOAD_MAX" = 238,
                      "SHORT_DOWNLOAD" = 237,
                      "MODIFY_BITS" = 236,
                      "SET_CAL_PAGE" = 235,
                      "GET_CAL_PAGE" = 234,
                      "GET_PAG_PROCESSOR_INFO" = 233,
                      "GET_SEGMENT_INFO" = 232,
                      "GET_PAGE_INFO" = 231,
                      "SET_SEGMENT_MODE" = 230,
                      "GET_SEGMENT_MODE" = 229,
                      "COPY_CAL_PAGE" = 228,
                      "CLEAR_DAQ_LIST" = 227,
                      "SET_DAQ_PTR" = 226,
                      "WRITE_DAQ" = 225,
                      "SET_DAQ_LIST_MODE" = 224,
                      "GET_DAQ_LIST_MODE" = 223,
                      "START_STOP_DAQ_LIST" = 222,
                      "START_STOP_SYNCH" = 221,
                      "GET_DAQ_CLOCK" = 220,
                      "READ_DAQ" = 219,
                      "GET_DAQ_PROCESSOR_INFO" = 218,
                      "GET_DAQ_RESOLUTION_INFO" = 217,
                      "GET_DAQ_LIST_INFO" = 216,
                      "GET_DAQ_EVENT_INFO" = 215,
                      "FREE_DAQ" = 214,
                      "ALLOC_DAQ" = 213,
                      "ALLOC_ODT" = 212,
                      "ALLOC_ODT_ENTRY" = 211,
                      "PROGRAM_START" = 210,
                      "PROGRAM_CLEAR" = 209,
                      "PROGRAM" = 208,
                      "PROGRAM_RESET" = 207,
                      "GET_PGM_PROCESSOR_INFO" = 206,
                      "GET_SECTOR_INFO" = 205,
                      "PROGRAM_PREPARE" = 204,
                      "PROGRAM_FORMAT" = 203,
                      "PROGRAM_NEXT" = 202,
                      "PROGRAM_MAX" = 201,
                      "PROGRAM_VERIFY" = 200
                    })*;
                    "COMMUNICATION_MODE_SUPPORTED" taggedunion {
                      "BLOCK" taggedstruct {
                        "SLAVE" ;
                        "MASTER" struct {
                          uchar;
                          uchar;
                        };
                      };
                      "INTERLEAVED" uchar;
                    };
                    "SEED_AND_KEY_EXTERNAL_FUNCTION" char[256];
                  };
                };
                block "SEGMENT" struct {
                  uchar;
                  uchar;
                  uchar;
                  uchar;
                  uchar;
                  taggedstruct {
                    block "CHECKSUM" struct {
                      enum {
                        "XCP_ADD_11" = 1,
                        "XCP_ADD_12" = 2,
                        "XCP_ADD_14" = 3,
                        "XCP_ADD_22" = 4,
                        "XCP_ADD_24" = 5,
                        "XCP_ADD_44" = 6,
                        "XCP_CRC_16" = 7,
                        "XCP_CRC_16_CITT" = 8,
                        "XCP_CRC_32" = 9,
                        "XCP_USER_DEFINED" = 255
                      };
                      taggedstruct {
                        "MAX_BLOCK_SIZE" ulong;
                        "EXTERNAL_FUNCTION" char[256];
                      };
                    };
                    (block "PAGE" struct {
                      uchar;
                      enum {
                        "ECU_ACCESS_NOT_ALLOWED" = 0,
                        "ECU_ACCESS_WITHOUT_XCP_ONLY" = 1,
                        "ECU_ACCESS_WITH_XCP_ONLY" = 2,
                        "ECU_ACCESS_DONT_CARE" = 3
                      };
                      enum {
                        "XCP_READ_ACCESS_NOT_ALLOWED" = 0,
                        "XCP_READ_ACCESS_WITHOUT_ECU_ONLY" = 1,
                        "XCP_READ_ACCESS_WITH_ECU_ONLY" = 2,
                        "XCP_READ_ACCESS_DONT_CARE" = 3
                      };
                      enum {
                        "XCP_WRITE_ACCESS_NOT_ALLOWED" = 0,
                        "XCP_WRITE_ACCESS_WITHOUT_ECU_ONLY" = 1,
                        "XCP_WRITE_ACCESS_WITH_ECU_ONLY" = 2,
                        "XCP_WRITE_ACCESS_DONT_CARE" = 3
                      };
                      taggedstruct {
                        "INIT_SEGMENT" uchar;
                      };
                    })*;
                    (block "ADDRESS_MAPPING" struct {
                      ulong;
                      ulong;
                      ulong;
                    })*;
                    "PGM_VERIFY" ulong;
                  };
                };
                block "DAQ" struct {
                  enum {
                    "STATIC" = 0,
                    "DYNAMIC" = 1
                  };
                  uint;
                  uint;
                  uchar;
                  enum {
                    "OPTIMISATION_TYPE_DEFAULT" = 0,
                    "OPTIMISATION_TYPE_ODT_TYPE_16" = 1,
                    "OPTIMISATION_TYPE_ODT_TYPE_32" = 2,
                    "OPTIMISATION_TYPE_ODT_TYPE_64" = 3,
                    "OPTIMISATION_TYPE_ODT_TYPE_ALIGNMENT" = 4,
                    "OPTIMISATION_TYPE_MAX_ENTRY_SIZE" = 5
                  };
                  enum {
                    "ADDRESS_EXTENSION_FREE" = 0,
                    "ADDRESS_EXTENSION_ODT" = 1,
                    "ADDRESS_EXTENSION_DAQ" = 3
                  };
                  enum {
                    "IDENTIFICATION_FIELD_TYPE_ABSOLUTE" = 0,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_BYTE" = 1,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_WORD" = 2,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_WORD_ALIGNED" = 3
                  };
                  enum {
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_BYTE" = 1,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_WORD" = 2,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_DWORD" = 4,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_DLONG" = 8
                  };
                  uchar;
                  enum {
                    "NO_OVERLOAD_INDICATION" = 0,
                    "OVERLOAD_INDICATION_PID" = 1,
                    "OVERLOAD_INDICATION_EVENT" = 2
                  };
                  taggedstruct {
                    "PRESCALER_SUPPORTED" ;
                    "RESUME_SUPPORTED" ;
                    block "STIM" struct {
                      enum {
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_BYTE" = 1,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_WORD" = 2,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_DWORD" = 4,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_DLONG" = 8
                      };
                      uchar;
                      taggedstruct {
                        "BIT_STIM_SUPPORTED" ;
                      };
                    };
                    block "TIMESTAMP_SUPPORTED" struct {
                      uint;
                      enum {
                        "NO_TIME_STAMP" = 0,
                        "SIZE_BYTE" = 1,
                        "SIZE_WORD" = 2,
                        "SIZE_DWORD" = 4
                      };
                      enum {
                        "UNIT_1NS" = 0,
                        "UNIT_10NS" = 1,
                        "UNIT_100NS" = 2,
                        "UNIT_1US" = 3,
                        "UNIT_10US" = 4,
                        "UNIT_100US" = 5,
                        "UNIT_1MS" = 6,
                        "UNIT_10MS" = 7,
                        "UNIT_100MS" = 8,
                        "UNIT_1S" = 9
                      };
                      taggedstruct {
                        "TIMESTAMP_FIXED" ;
                      };
                    };
                    "PID_OFF_SUPPORTED" ;
                    (block "DAQ_LIST" struct {
                      uint;
                      taggedstruct {
                        "DAQ_LIST_TYPE" enum {
                          "DAQ" = 1,
                          "STIM" = 2,
                          "DAQ_STIM" = 3
                        };
                        "MAX_ODT" uchar;
                        "MAX_ODT_ENTRIES" uchar;
                        "FIRST_PID" uchar;
                        "EVENT_FIXED" uint;
                        block "PREDEFINED" taggedstruct {
                          (block "ODT" struct {
                            uchar;
                            taggedstruct {
                              ("ODT_ENTRY" struct {
                                uchar;
                                ulong;
                                uchar;
                                uchar;
                                uchar;
                              })*;
                            };
                          })*;
                        };
                      };
                    })*;
                    (block "EVENT" struct {
                      char[101];
                      char[9];
                      uint;
                      enum {
                        "DAQ" = 1,
                        "STIM" = 2,
                        "DAQ_STIM" = 3
                      };
                      uchar;
                      uchar;
                      uchar;
                      uchar;
                    })*;
                  };
                };
                block "PAG" struct {
                  uchar;
                  taggedstruct {
                    "FREEZE_SUPPORTED" ;
                  };
                };
                block "PGM" struct {
                  enum {
                    "PGM_MODE_ABSOLUTE" = 1,
                    "PGM_MODE_FUNCTIONAL" = 2,
                    "PGM_MODE_ABSOLUTE_AND_FUNCTIONAL" = 3
                  };
                  uchar;
                  uchar;
                  taggedstruct {
                    (block "SECTOR" struct {
                      char[101];
                      uchar;
                      ulong;
                      ulong;
                      uchar;
                      uchar;
                      uchar;
                    })*;
                    "COMMUNICATION_MODE_SUPPORTED" taggedunion {
                      "BLOCK" taggedstruct {
                        "SLAVE" ;
                        "MASTER" struct {
                          uchar;
                          uchar;
                        };
                      };
                      "INTERLEAVED" uchar;
                    };
                  };
                };
                block "DAQ_EVENT" taggedunion {
                  "FIXED_EVENT_LIST" taggedstruct {
                    ("EVENT" uint)*;
                  };
                  "VARIABLE" taggedstruct {
                    block "AVAILABLE_EVENT_LIST" taggedstruct {
                      ("EVENT" uint)*;
                    };
                    block "DEFAULT_EVENT_LIST" taggedstruct {
                      ("EVENT" uint)*;
                    };
                  };
                };
              };
            };
            block "XCP_ON_USB" struct {
              uint;
              uint;
              uint;
              uchar;
              enum {
                "HEADER_LEN_BYTE" = 0,
                "HEADER_LEN_CTR_BYTE" = 1,
                "HEADER_LEN_FILL_BYTE" = 2,
                "HEADER_LEN_WORD" = 3,
                "HEADER_LEN_CTR_WORD" = 4,
                "HEADER_LEN_FILL_WORD" = 5
              };
              taggedunion {
                block "OUT_EP_CMD_STIM" struct {
                  uchar;
                  enum {
                    "BULK_TRANSFER" = 2,
                    "INTERRUPT_TRANSFER" = 3
                  };
                  uint;
                  uchar;
                  enum {
                    "MESSAGE_PACKING_SINGLE" = 0,
                    "MESSAGE_PACKING_MULTIPLE" = 1,
                    "MESSAGE_PACKING_STREAMING" = 2
                  };
                  enum {
                    "ALIGNMENT_8_BIT" = 0,
                    "ALIGNMENT_16_BIT" = 1,
                    "ALIGNMENT_32_BIT" = 2,
                    "ALIGNMENT_64_BIT" = 3
                  };
                  taggedstruct {
                    "RECOMMENDED_HOST_BUFSIZE" uint;
                  };
                };
              };
              taggedunion {
                block "IN_EP_RESERR_DAQ_EVSERV" struct {
                  uchar;
                  enum {
                    "BULK_TRANSFER" = 2,
                    "INTERRUPT_TRANSFER" = 3
                  };
                  uint;
                  uchar;
                  enum {
                    "MESSAGE_PACKING_SINGLE" = 0,
                    "MESSAGE_PACKING_MULTIPLE" = 1,
                    "MESSAGE_PACKING_STREAMING" = 2
                  };
                  enum {
                    "ALIGNMENT_8_BIT" = 0,
                    "ALIGNMENT_16_BIT" = 1,
                    "ALIGNMENT_32_BIT" = 2,
                    "ALIGNMENT_64_BIT" = 3
                  };
                  taggedstruct {
                    "RECOMMENDED_HOST_BUFSIZE" uint;
                  };
                };
              };
              taggedstruct {
                "ALTERNATE_SETTING_NO" uchar;
                "INTERFACE_STRING_DESCRIPTOR" char[101];
                (block "OUT_EP_ONLY_STIM" struct {
                  uchar;
                  enum {
                    "BULK_TRANSFER" = 2,
                    "INTERRUPT_TRANSFER" = 3
                  };
                  uint;
                  uchar;
                  enum {
                    "MESSAGE_PACKING_SINGLE" = 0,
                    "MESSAGE_PACKING_MULTIPLE" = 1,
                    "MESSAGE_PACKING_STREAMING" = 2
                  };
                  enum {
                    "ALIGNMENT_8_BIT" = 0,
                    "ALIGNMENT_16_BIT" = 1,
                    "ALIGNMENT_32_BIT" = 2,
                    "ALIGNMENT_64_BIT" = 3
                  };
                  taggedstruct {
                    "RECOMMENDED_HOST_BUFSIZE" uint;
                  };
                })*;
                (block "IN_EP_ONLY_DAQ" struct {
                  uchar;
                  enum {
                    "BULK_TRANSFER" = 2,
                    "INTERRUPT_TRANSFER" = 3
                  };
                  uint;
                  uchar;
                  enum {
                    "MESSAGE_PACKING_SINGLE" = 0,
                    "MESSAGE_PACKING_MULTIPLE" = 1,
                    "MESSAGE_PACKING_STREAMING" = 2
                  };
                  enum {
                    "ALIGNMENT_8_BIT" = 0,
                    "ALIGNMENT_16_BIT" = 1,
                    "ALIGNMENT_32_BIT" = 2,
                    "ALIGNMENT_64_BIT" = 3
                  };
                  taggedstruct {
                    "RECOMMENDED_HOST_BUFSIZE" uint;
                  };
                })*;
                block "IN_EP_ONLY_EVSERV" struct {
                  uchar;
                  enum {
                    "BULK_TRANSFER" = 2,
                    "INTERRUPT_TRANSFER" = 3
                  };
                  uint;
                  uchar;
                  enum {
                    "MESSAGE_PACKING_SINGLE" = 0,
                    "MESSAGE_PACKING_MULTIPLE" = 1,
                    "MESSAGE_PACKING_STREAMING" = 2
                  };
                  enum {
                    "ALIGNMENT_8_BIT" = 0,
                    "ALIGNMENT_16_BIT" = 1,
                    "ALIGNMENT_32_BIT" = 2,
                    "ALIGNMENT_64_BIT" = 3
                  };
                  taggedstruct {
                    "RECOMMENDED_HOST_BUFSIZE" uint;
                  };
                };
                (block "DAQ_LIST_USB_ENDPOINT" struct {
                  uint;
                  taggedstruct {
                    "FIXED_IN" uchar;
                    "FIXED_OUT" uchar;
                  };
                })*;
                block "PROTOCOL_LAYER" struct {
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uint;
                  uchar;
                  uint;
                  enum {
                    "BYTE_ORDER_MSB_LAST" = 0,
                    "BYTE_ORDER_MSB_FIRST" = 1
                  };
                  enum {
                    "ADDRESS_GRANULARITY_BYTE" = 1,
                    "ADDRESS_GRANULARITY_WORD" = 2,
                    "ADDRESS_GRANULARITY_DWORD" = 4
                  };
                  taggedstruct {
                    ("OPTIONAL_CMD" enum {
                      "GET_COMM_MODE_INFO" = 251,
                      "GET_ID" = 250,
                      "SET_REQUEST" = 249,
                      "GET_SEED" = 248,
                      "UNLOCK" = 247,
                      "SET_MTA" = 246,
                      "UPLOAD" = 245,
                      "SHORT_UPLOAD" = 244,
                      "BUILD_CHECKSUM" = 243,
                      "TRANSPORT_LAYER_CMD" = 242,
                      "USER_CMD" = 241,
                      "DOWNLOAD" = 240,
                      "DOWNLOAD_NEXT" = 239,
                      "DOWNLOAD_MAX" = 238,
                      "SHORT_DOWNLOAD" = 237,
                      "MODIFY_BITS" = 236,
                      "SET_CAL_PAGE" = 235,
                      "GET_CAL_PAGE" = 234,
                      "GET_PAG_PROCESSOR_INFO" = 233,
                      "GET_SEGMENT_INFO" = 232,
                      "GET_PAGE_INFO" = 231,
                      "SET_SEGMENT_MODE" = 230,
                      "GET_SEGMENT_MODE" = 229,
                      "COPY_CAL_PAGE" = 228,
                      "CLEAR_DAQ_LIST" = 227,
                      "SET_DAQ_PTR" = 226,
                      "WRITE_DAQ" = 225,
                      "SET_DAQ_LIST_MODE" = 224,
                      "GET_DAQ_LIST_MODE" = 223,
                      "START_STOP_DAQ_LIST" = 222,
                      "START_STOP_SYNCH" = 221,
                      "GET_DAQ_CLOCK" = 220,
                      "READ_DAQ" = 219,
                      "GET_DAQ_PROCESSOR_INFO" = 218,
                      "GET_DAQ_RESOLUTION_INFO" = 217,
                      "GET_DAQ_LIST_INFO" = 216,
                      "GET_DAQ_EVENT_INFO" = 215,
                      "FREE_DAQ" = 214,
                      "ALLOC_DAQ" = 213,
                      "ALLOC_ODT" = 212,
                      "ALLOC_ODT_ENTRY" = 211,
                      "PROGRAM_START" = 210,
                      "PROGRAM_CLEAR" = 209,
                      "PROGRAM" = 208,
                      "PROGRAM_RESET" = 207,
                      "GET_PGM_PROCESSOR_INFO" = 206,
                      "GET_SECTOR_INFO" = 205,
                      "PROGRAM_PREPARE" = 204,
                      "PROGRAM_FORMAT" = 203,
                      "PROGRAM_NEXT" = 202,
                      "PROGRAM_MAX" = 201,
                      "PROGRAM_VERIFY" = 200
                    })*;
                    "COMMUNICATION_MODE_SUPPORTED" taggedunion {
                      "BLOCK" taggedstruct {
                        "SLAVE" ;
                        "MASTER" struct {
                          uchar;
                          uchar;
                        };
                      };
                      "INTERLEAVED" uchar;
                    };
                    "SEED_AND_KEY_EXTERNAL_FUNCTION" char[256];
                  };
                };
                block "SEGMENT" struct {
                  uchar;
                  uchar;
                  uchar;
                  uchar;
                  uchar;
                  taggedstruct {
                    block "CHECKSUM" struct {
                      enum {
                        "XCP_ADD_11" = 1,
                        "XCP_ADD_12" = 2,
                        "XCP_ADD_14" = 3,
                        "XCP_ADD_22" = 4,
                        "XCP_ADD_24" = 5,
                        "XCP_ADD_44" = 6,
                        "XCP_CRC_16" = 7,
                        "XCP_CRC_16_CITT" = 8,
                        "XCP_CRC_32" = 9,
                        "XCP_USER_DEFINED" = 255
                      };
                      taggedstruct {
                        "MAX_BLOCK_SIZE" ulong;
                        "EXTERNAL_FUNCTION" char[256];
                      };
                    };
                    (block "PAGE" struct {
                      uchar;
                      enum {
                        "ECU_ACCESS_NOT_ALLOWED" = 0,
                        "ECU_ACCESS_WITHOUT_XCP_ONLY" = 1,
                        "ECU_ACCESS_WITH_XCP_ONLY" = 2,
                        "ECU_ACCESS_DONT_CARE" = 3
                      };
                      enum {
                        "XCP_READ_ACCESS_NOT_ALLOWED" = 0,
                        "XCP_READ_ACCESS_WITHOUT_ECU_ONLY" = 1,
                        "XCP_READ_ACCESS_WITH_ECU_ONLY" = 2,
                        "XCP_READ_ACCESS_DONT_CARE" = 3
                      };
                      enum {
                        "XCP_WRITE_ACCESS_NOT_ALLOWED" = 0,
                        "XCP_WRITE_ACCESS_WITHOUT_ECU_ONLY" = 1,
                        "XCP_WRITE_ACCESS_WITH_ECU_ONLY" = 2,
                        "XCP_WRITE_ACCESS_DONT_CARE" = 3
                      };
                      taggedstruct {
                        "INIT_SEGMENT" uchar;
                      };
                    })*;
                    (block "ADDRESS_MAPPING" struct {
                      ulong;
                      ulong;
                      ulong;
                    })*;
                    "PGM_VERIFY" ulong;
                  };
                };
                block "DAQ" struct {
                  enum {
                    "STATIC" = 0,
                    "DYNAMIC" = 1
                  };
                  uint;
                  uint;
                  uchar;
                  enum {
                    "OPTIMISATION_TYPE_DEFAULT" = 0,
                    "OPTIMISATION_TYPE_ODT_TYPE_16" = 1,
                    "OPTIMISATION_TYPE_ODT_TYPE_32" = 2,
                    "OPTIMISATION_TYPE_ODT_TYPE_64" = 3,
                    "OPTIMISATION_TYPE_ODT_TYPE_ALIGNMENT" = 4,
                    "OPTIMISATION_TYPE_MAX_ENTRY_SIZE" = 5
                  };
                  enum {
                    "ADDRESS_EXTENSION_FREE" = 0,
                    "ADDRESS_EXTENSION_ODT" = 1,
                    "ADDRESS_EXTENSION_DAQ" = 3
                  };
                  enum {
                    "IDENTIFICATION_FIELD_TYPE_ABSOLUTE" = 0,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_BYTE" = 1,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_WORD" = 2,
                    "IDENTIFICATION_FIELD_TYPE_RELATIVE_WORD_ALIGNED" = 3
                  };
                  enum {
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_BYTE" = 1,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_WORD" = 2,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_DWORD" = 4,
                    "GRANULARITY_ODT_ENTRY_SIZE_DAQ_DLONG" = 8
                  };
                  uchar;
                  enum {
                    "NO_OVERLOAD_INDICATION" = 0,
                    "OVERLOAD_INDICATION_PID" = 1,
                    "OVERLOAD_INDICATION_EVENT" = 2
                  };
                  taggedstruct {
                    "PRESCALER_SUPPORTED" ;
                    "RESUME_SUPPORTED" ;
                    block "STIM" struct {
                      enum {
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_BYTE" = 1,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_WORD" = 2,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_DWORD" = 4,
                        "GRANULARITY_ODT_ENTRY_SIZE_STIM_DLONG" = 8
                      };
                      uchar;
                      taggedstruct {
                        "BIT_STIM_SUPPORTED" ;
                      };
                    };
                    block "TIMESTAMP_SUPPORTED" struct {
                      uint;
                      enum {
                        "NO_TIME_STAMP" = 0,
                        "SIZE_BYTE" = 1,
                        "SIZE_WORD" = 2,
                        "SIZE_DWORD" = 4
                      };
                      enum {
                        "UNIT_1NS" = 0,
                        "UNIT_10NS" = 1,
                        "UNIT_100NS" = 2,
                        "UNIT_1US" = 3,
                        "UNIT_10US" = 4,
                        "UNIT_100US" = 5,
                        "UNIT_1MS" = 6,
                        "UNIT_10MS" = 7,
                        "UNIT_100MS" = 8,
                        "UNIT_1S" = 9
                      };
                      taggedstruct {
                        "TIMESTAMP_FIXED" ;
                      };
                    };
                    "PID_OFF_SUPPORTED" ;
                    (block "DAQ_LIST" struct {
                      uint;
                      taggedstruct {
                        "DAQ_LIST_TYPE" enum {
                          "DAQ" = 1,
                          "STIM" = 2,
                          "DAQ_STIM" = 3
                        };
                        "MAX_ODT" uchar;
                        "MAX_ODT_ENTRIES" uchar;
                        "FIRST_PID" uchar;
                        "EVENT_FIXED" uint;
                        block "PREDEFINED" taggedstruct {
                          (block "ODT" struct {
                            uchar;
                            taggedstruct {
                              ("ODT_ENTRY" struct {
                                uchar;
                                ulong;
                                uchar;
                                uchar;
                                uchar;
                              })*;
                            };
                          })*;
                        };
                      };
                    })*;
                    (block "EVENT" struct {
                      char[101];
                      char[9];
                      uint;
                      enum {
                        "DAQ" = 1,
                        "STIM" = 2,
                        "DAQ_STIM" = 3
                      };
                      uchar;
                      uchar;
                      uchar;
                      uchar;
                    })*;
                  };
                };
                block "PAG" struct {
                  uchar;
                  taggedstruct {
                    "FREEZE_SUPPORTED" ;
                  };
                };
                block "PGM" struct {
                  enum {
                    "PGM_MODE_ABSOLUTE" = 1,
                    "PGM_MODE_FUNCTIONAL" = 2,
                    "PGM_MODE_ABSOLUTE_AND_FUNCTIONAL" = 3
                  };
                  uchar;
                  uchar;
                  taggedstruct {
                    (block "SECTOR" struct {
                      char[101];
                      uchar;
                      ulong;
                      ulong;
                      uchar;
                      uchar;
                      uchar;
                    })*;
                    "COMMUNICATION_MODE_SUPPORTED" taggedunion {
                      "BLOCK" taggedstruct {
                        "SLAVE" ;
                        "MASTER" struct {
                          uchar;
                          uchar;
                        };
                      };
                      "INTERLEAVED" uchar;
                    };
                  };
                };
                block "DAQ_EVENT" taggedunion {
                  "FIXED_EVENT_LIST" taggedstruct {
                    ("EVENT" uint)*;
                  };
                  "VARIABLE" taggedstruct {
                    block "AVAILABLE_EVENT_LIST" taggedstruct {
                      ("EVENT" uint)*;
                    };
                    block "DEFAULT_EVENT_LIST" taggedstruct {
                      ("EVENT" uint)*;
                    };
                  };
                };
              };
            };
          };
        };


      };
            /end A2ML
            /begin MOD_PAR
            /end MOD_PAR
            /begin MOD_COMMON
            /end MOD_COMMON
            /begin AXIS_PTS 
            AirChrgrMdlHi_CmprSpdCorrd_MAPX 
            "Air Charger Model _ Compressor Speed Corrected _ Map X Axis"
      0x50002DF2 
      AirChrgrMdlHi_CmprPRat 
      _REC_A2AXS_60_LMB_s2 
      15.9997558594 
      Fryuynd_aryqffa_FmndnDc_n_aoo45 
      16 
      -8 
      7.99975585938
      
        DISPLAY_IDENTIFIER DI.ASAM.C.SCALAR.SBYTE.IDENTICAL 
        READ_ONLY
                BYTE_ORDER MSB_FIRST
      ECU_ADDRESS_EXTENSION 0x0
      EXTENDED_LIMITS -8 7.99975585938
      DEPOSIT ABSOLUTE
                /begin FUNCTION_LIST
                    FunctionVirtualMeasurements
                    FunctionVirtualMeasurements
                    FunctionVirtualMeasurements
                /end FUNCTION_LIST
                /begin ANNOTATION
                    ANNOTATION_LABEL "ASAM Workinggroup"
                    ANNOTATION_ORIGIN ""
                    /begin ANNOTATION_TEXT
                        "Test the A2L annotation 3 "
                        "Test the A2L annotation 4 "
                    /end ANNOTATION_TEXT
                /end ANNOTATION
                REF_MEMORY_SEGMENT CAL_asd
                GUARD_RAILS
      FORMAT "%6.3"
      EXTENDED_LIMITS -8 7.99975585938
            /begin IF_DATA asd
            /end IF_DATA
            CALIBRATION_ACCESS CALIBRATION
    /end AXIS_PTS
            /begin IF_DATA asd
            /end IF_DATA
            /begin CHARACTERISTIC AirChrgrCoorr_SpdRefForCmprHi_C "Air Charger Coordinator _ Speed Reference For Compressor High _ Calibration Value"
      VALUE 0x50002D3A _REC_S1VAL_60_LMB_s2 524280 lAagFra_pBustdb_cAsAEha_1nR_oa0 -262144 262136
      ECU_ADDRESS_EXTENSION 0x0
      EXTENDED_LIMITS -262144 262136
      FORMAT "%6.3"
    /end CHARACTERISTIC
    /begin CHARACTERISTIC AirChrgrMdl_TestSubOfCmprTOutl_C "Air Charger Model _ Test Substitute Of Compressor Temperature Outlet _ Calibration Value"
      VALUE 0x50002DF0 _REC_S1VAL_60_LMB_s2 1123.96875 fzyBCrc_bErjugb_Fgjzexb_qR0ao3e -100 1023.96875
      ECU_ADDRESS_EXTENSION 0x0
      EXTENDED_LIMITS -100 1023.96875
      FORMAT "%6.3"
    /end CHARACTERISTIC
            /begin CHARACTERISTIC ASAM.C.SCALAR.UBYTE.IDENTICAL
                "Scalar FW U16 and CDF20 as name"
                VALUE
                0x7140
                RL.FNC.SBYTE.ROW_DIR
                0
                CM.IDENTICAL
                10 200
                EXTENDED_LIMITS 0 256
                NUMBER 42
                READ_ONLY
                DISPLAY_IDENTIFIER DI.ASAM.C.SCALAR.SBYTE.IDENTICAL
                FORMAT "%6.1"
                REF_MEMORY_SEGMENT SEC_CONST.UNSPECIFIED
                /begin VIRTUAL_CHARACTERISTIC
                    "X1 - 9"
                    ASAM.C.SCALAR.SBYTE.IDENTICAL                     /* used as input X1 variable in teh dependent formula */
                /end VIRTUAL_CHARACTERISTIC
                BIT_MASK 0x0FF0
                /begin DEPENDENT_CHARACTERISTIC
                    "X1 + 5"
                    ASAM.C.SCALAR.SBYTE.IDENTICAL                     /* used as input X1 variable in teh dependent formula */
                /end DEPENDENT_CHARACTERISTIC
                BYTE_ORDER MSB_LAST
                CALIBRATION_ACCESS CALIBRATION
                /begin ANNOTATION
                    ANNOTATION_LABEL "ASAM Workinggroup"
                    ANNOTATION_ORIGIN ""
                    /begin ANNOTATION_TEXT
                        "Test the A2L annotation 1 "
                        "Test the A2L annotation 2 "
                    /end ANNOTATION_TEXT
                /end ANNOTATION
                /begin AXIS_DESCR /* description of X-axis points */
COM_AXIS N /* common axis points, input quantity
*/
CONV_N 14 /* conversion, max. no. of axis p.*/
0.0 5800.0 /* lower limit, upper limit */
/end AXIS_DESCR
                /begin IF_DATA XCP
                /end IF_DATA
                MAX_REFRESH 3 15
                MATRIX_DIM 2 4 3
                /begin FUNCTION_LIST
                    FunctionVirtualMeasurements
                    FunctionVirtualMeasurements
                    FunctionVirtualMeasurements
                /end FUNCTION_LIST
                /begin ANNOTATION
                    ANNOTATION_LABEL "ASAM Workinggroup"
                    ANNOTATION_ORIGIN ""
                    /begin ANNOTATION_TEXT
                        "Test the A2L annotation 3 "
                        "Test the A2L annotation 4 "
                    /end ANNOTATION_TEXT
                /end ANNOTATION
                /begin MAP_LIST
                    FunctionVirtualMeasurements
                    FunctionVirtualMeasurements
                    FunctionVirtualMeasurements
                /end MAP_LIST
                COMPARISON_QUANTITY blah.blah.blah__
                ECU_ADDRESS_EXTENSION 1
            /end CHARACTERISTIC
            /begin IF_DATA asd
            /end IF_DATA
            /begin MEASUREMENT N /* name */
                "Engine speed" /* long identifier */
                UWORD /* datatype */
                R_SPEED_3 /* conversion */
                2 /* resolution */
                2.5 /* accuracy */
                120.0 /* lower limit */
                8400.0 /* upper limit */
                /begin BIT_OPERATION
                    RIGHT_SHIFT 4 /*4 positions*/
                    SIGN_EXTEND
                /end BIT_OPERATION
            /begin IF_DATA asd
            /end IF_DATA
                BIT_MASK 0x0FF0
                /begin ANNOTATION
                    ANNOTATION_LABEL "ASAM Workinggroup"
                    ANNOTATION_ORIGIN ""
                    /begin ANNOTATION_TEXT
                        "Test the A2L annotation 3 "
                        "Test the A2L annotation 4 "
                    /end ANNOTATION_TEXT
                /end ANNOTATION
                MAX_REFRESH 3 15
                BYTE_ORDER MSB_FIRST
                /begin FUNCTION_LIST
                    FunctionVirtualMeasurements
                    FunctionVirtualMeasurements
                    FunctionVirtualMeasurements
                /end FUNCTION_LIST
      FORMAT "%5.0"
      READ_WRITE
                DISPLAY_IDENTIFIER DI.ASAM.C.SCALAR.SBYTE.IDENTICAL
                /begin ANNOTATION
                    ANNOTATION_LABEL "ASAM Workinggroup"
                    ANNOTATION_ORIGIN ""
                    /begin ANNOTATION_TEXT
                        "Test the A2L annotation 3 "
                        "Test the A2L annotation 4 "
                    /end ANNOTATION_TEXT
                /end ANNOTATION
                ECU_ADDRESS 0x12FE
                ERROR_MASK 0x00000001
                ECU_ADDRESS_EXTENSION 0x0
                MATRIX_DIM 2 4 3
                REF_MEMORY_SEGMENT SEC_VAR.FAST
                /begin VIRTUAL PHI_BASIS PHI_CORR
/end VIRTUAL
             ARRAY_SIZE 16                                        /* Note: ARRAY_SIZE allows only 1 dimension. For more dimensions use MATRIX_DIM */
     /end MEASUREMENT
            /begin COMPU_METHOD CM.IDENTICAL
      "conversion that delivers always phys = int"
      IDENTICAL "%3.0" "hours"
      COEFFS -0 +1 -0.2 +0.4 123123.123 -1
      REF_UNIT kms_per_hour
      COMPU_TAB_REF TMPCON1
      
      /begin FORMULA "a * x + b" /end FORMULA
            /end COMPU_METHOD
            /begin COMPU_TAB
            TT /* name */
"conversion table for oil temperatures"
 TAB_NOINTP /* convers_type */
7 /* number_value_pairs */ 
1 4.3 2 4.7 3 5.8 4 14.2 
5 16.8 6 17.2 7 19.4
DEFAULT_VALUE "out of range..."
            /end COMPU_TAB
            /begin COMPU_VTAB
            TT /* name */ "engine status conversion"
TAB_VERB 4
0 "engine off"
1 "idling"
2 "partial load"
3 "full load"
DEFAULT_VALUE "i'm the default..."
            /end COMPU_VTAB
            /begin COMPU_VTAB_RANGE
            TT
            "engine conversion"
            5
            0 0 "ONE"
            1 2 "fist section"
            3 3 "THREE"
            4 5 "second section"
            6 500 "usual_case"
            DEFAULT_VALUE "value_out_of.range"
            /end COMPU_VTAB_RANGE
            
            
            
            
            /begin FUNCTION ID_ADJUSTM /* name */
                "function group idling adjustment"
                /begin DEF_CHARACTERISTIC
                    INJECTION_CURVE
                /end DEF_CHARACTERISTIC 
                /begin REF_CHARACTERISTIC 
                    FACTOR_1                    
                /end REF_CHARACTERISTIC 
                /begin IN_MEASUREMENT
                    WHEEL_REVOLUTIONS ENGINE_SPEED
                /end IN_MEASUREMENT 
                /begin OUT_MEASUREMENT 
                    OK_FLAG SENSOR_FLAG
                /end OUT_MEASUREMENT 
                /begin LOC_MEASUREMENT
                    LOOP_COUNTER TEMPORARY_1
                /end LOC_MEASUREMENT 
                /begin SUB_FUNCTION
                    ID_ADJUSTM_SUB
                /end SUB_FUNCTION 
            /end FUNCTION
            
            
            
            
            /begin GROUP SOFTWARE_COMPONENTS "assignment of the definitions to C files"
            /begin REF_CHARACTERISTIC INJECTION_CURVE /end REF_CHARACTERISTIC
/begin REF_MEASUREMENT LOOP_COUNTER TEMPORARY_1 /end REF_MEASUREMENT
ROOT
/begin SUB_GROUP INJE C6TD
/end SUB_GROUP /end GROUP
            /begin RECORD_LAYOUT DAMOS_KF
FNC_VALUES 7 SWORD COLUMN_DIR DIRECT
AXIS_PTS_X 3 SWORD INDEX_INCR DIRECT
AXIS_PTS_Y 6 UBYTE INDEX_INCR DIRECT
NO_AXIS_PTS_X 2 UBYTE
NO_AXIS_PTS_Y 5 UBYTE
SRC_ADDR_X 1
SRC_ADDR_Y 4
ALIGNMENT_BYTE 2
/end RECORD_LAYOUT
            /begin VARIANT_CODING
VAR_SEPARATOR "." /* PUMKF.1 */
VAR_NAMING NUMERIC 
/* variant criterion "Car body" with three variants */
/begin VAR_CRITERION Car "Car body" Limousine Kombi Cabrio
/end VAR_CRITERION
/* variant criterion "Type of gear box" with two variants */
/begin VAR_CRITERION Gear "Type of gear box" Manual Automatic
/end VAR_CRITERION
/begin VAR_FORBIDDEN_COMB /* forbidden: Limousine - Manual */
Car Limousine
Gear Manual
/end VAR_FORBIDDEN_COMB
/begin VAR_FORBIDDEN_COMB /* forbidden: Cabrio - Automatic */
Car Cabrio
Gear Automatic
/end VAR_FORBIDDEN_COMB
/begin VAR_CHARACTERISTIC PUMKF /* define PUMKF as variant coded */
Gear /* Gear box variants */
/begin VAR_ADDRESS
0x7140 0x7168
/end VAR_ADDRESS
/end VAR_CHARACTERISTIC
/begin VAR_CHARACTERISTIC NLLM /* define NLLM as variant coded */
Gear Car /* car body and gear box variants */
/begin VAR_ADDRESS
0x8840 0x8858 0x8870 0x8888
/end VAR_ADDRESS
/end VAR_CHARACTERISTIC
/* forbidden variant combination (doesn't exist in control unit software): */
/begin VAR_FORBIDDEN_COMB
Car Limousine /* variant value 'Limousine' of criterion 'Car' */
Gear Manual /* variant value 'Manual' of criterion 'Gear' */
/end VAR_FORBIDDEN_COMB
/* variant criterion "Car body" with three variants */
/begin VAR_CRITERION Car "Car body"
/* Enumeration of criterion values */
Limousine Kombi Cabrio
VAR_MEASUREMENT S_CAR
VAR_SELECTION_CHARACTERISTIC V_CAR
/end VAR_CRITERION
VAR_SEPARATOR "." /* example: "PUMKF.1" */
/* three parts of variant coded adjustable objects name: */
/* 1.) Identifier of adjustable object: "PUMKF" */
/* 2.) Separator: "." (decimal point) */
/* 3.) Variants extension: "1" */
VAR_NAMING NUMERIC
/end VARIANT_CODING
/begin FRAME ABS_ADJUSTM
"function group ABS adjustment"
3
2 /* 2 msec. */
FRAME_MEASUREMENT LOOP_COUNTER TEMPORARY_1
/end FRAME


/begin USER_RIGHTS application_engineers
/begin REF_GROUP group_1 /end REF_GROUP
/end USER_RIGHTS
/begin USER_RIGHTS measurement_engineers
/begin REF_GROUP group_1 group_2 /end REF_GROUP
READ_ONLY
/end USER_RIGHTS
/begin UNIT
metres_per_second
"extended SI unit for velocity"
            "[m/s]"
EXTENDED_SI
SI_EXPONENTS 1 0 -1 0 0 0 0 /* [m] * [s]-1 */
/end UNIT
/begin UNIT
kms_per_hour
"derived unit for velocity: kilometres per hour"
"[km/h]"
EXTENDED_SI
SI_EXPONENTS 0 0 0 0 1 0 0
REF_UNIT metres_per_second
UNIT_CONVERSION 3.6 0.0 /* y [km/h] = (60*60/1000) * x [m/s] + 0.0
*/
/end UNIT
/begin UNIT
miles_per_hour
"derived unit for velocity: miles per hour"
"[mph]"
DERIVED
REF_UNIT metres_per_second
UNIT_CONVERSION 2.237 0.0 /* y [mph] = (60*60/1609) * x [m/s] + 0.0
*/
/end UNIT
        /end MODULE
    /end PROJECT""")
