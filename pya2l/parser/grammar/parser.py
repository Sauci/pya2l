"""
@project: pya2l
@file: parser.py
@author: Guillaume Sottas
@date: 20.03.2018
"""

import os
import warnings
import ply.yacc as yacc

from pya2l.parser.exception import A2lFormatException
from pya2l.parser.grammar.lexer import tokens as lex_tokens, lexer, token_function
from pya2l.parser.node import node_factory
from pya2l.parser.a2l_node import *
from pya2l.parser.a2ml_node import *
from pya2l.parser.a2l_type import *


class A2lParser(object):
    tokens = lex_tokens

    def __init__(self, string):
        self.ast = None
        self.a2ml = A2ML()
        lexer.lineno = 1
        self._yacc = yacc.yacc(debug=True,
                               module=self,
                               optimize=False,
                               outputdir=os.path.dirname(os.path.realpath(__file__)))
        self._yacc.parse(string, tokenfunc=token_function)

    def nodes(self, node_name):
        if self.ast:
            return self.ast.nodes(node_name)
        else:
            return []

    def dump(self, indent=4, line_ending='\n', indent_char=' '):
        if self.ast and hasattr(self.ast, 'project'):
            result = list()
            for indentation_level, string in self.ast.project.dump():
                result.append(((indent_char * indent) * indentation_level) + string)
            return line_ending.join(result)
        else:
            return ''

    @staticmethod
    def p_error(p):
        if p:
            for _ in range(len(p.lexer.lexstatestack)):
                p.lexer.pop_state()
            raise A2lFormatException('invalid sequence at position ', p.lexpos, string=p.lexer.lexdata)
        else:
            raise A2lFormatException('invalid sequence in root node', 0, string='')

    def p_a2l(self, p):
        """a2l : a2l_optional_list_optional"""
        p[0] = node_factory(p.slice[0].type, p[1])
        self.ast = p[0]

    @staticmethod
    def p_a2l_optional(p):
        """a2l_optional : asap2_version
                        | a2ml_version
                        | project"""
        p[0] = p.slice[1].type, p[1]

    @staticmethod
    def p_a2l_optional_list(p):
        """a2l_optional_list : a2l_optional
                             | a2l_optional a2l_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_a2l_optional_list_optional(p):
        """a2l_optional_list_optional : empty
                                      | a2l_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_a2ml_declaration(p):
        """a2ml_declaration : a2ml_type_definition SC
                            | a2ml_block_definition SC"""
        p[0] = node_factory(p.slice[0].type, p[1])

    @staticmethod
    def p_a2ml_declaration_list(p):
        """a2ml_declaration_list : a2ml_declaration
                                 | a2ml_declaration a2ml_declaration_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_a2ml_type_definition(p):
        """a2ml_type_definition : a2ml_type_name"""
        p[0] = 'definition', node_factory(p.slice[0].type, p[1])

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
        p[0] = 'type_name', node_factory(p[1], ('type_name', p[1]))

    @staticmethod
    def p_a2ml_enum_type_name(p):
        """a2ml_enum_type_name : enum a2ml_identifier_optional CO a2ml_enumerator_list CC
                               | enum a2ml_identifier"""
        try:
            p[0] = 'type_name', node_factory(p.slice[0].type, p[2], p[4])
        except IndexError:
            p[0] = 'type_name', node_factory(p.slice[0].type, p[2])

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
        """a2ml_enumerator : a2ml_keyword EQ a2ml_constant
                           | a2ml_keyword"""
        try:
            p[0] = 'enumerator', node_factory(p.slice[0].type, p[1], p[3])
        except IndexError:
            p[0] = 'enumerator', node_factory(p.slice[0].type, p[1])

    @staticmethod
    def p_a2ml_struct_type_name(p):
        """a2ml_struct_type_name : struct a2ml_identifier_optional CO a2ml_struct_member_list_optional CC
                                 | struct a2ml_identifier"""
        try:
            p[0] = 'type_name', node_factory(p.slice[0].type, p[2], p[4])
        except IndexError:
            p[0] = 'type_name', node_factory(p.slice[0].type, p[2])

    @staticmethod
    def p_a2ml_struct_member_list_optional(p):
        """a2ml_struct_member_list_optional : empty
                                            | a2ml_struct_member_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_a2ml_struct_member_list(p):
        """a2ml_struct_member_list : a2ml_struct_member
                                   | a2ml_struct_member a2ml_struct_member_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_a2ml_struct_member(p):
        """a2ml_struct_member : a2ml_member SC"""
        p[0] = 'member', node_factory(p.slice[0].type, p[1])

    @staticmethod
    def p_a2ml_member(p):
        """a2ml_member : a2ml_type_name a2ml_array_specifier_optional"""
        p[0] = 'member', node_factory(p.slice[0].type, *p[1:3])

    @staticmethod
    def p_a2ml_member_optional(p):
        """a2ml_member_optional : empty
                                | a2ml_member"""
        if p[1]:
            p[0] = p[1]
        else:
            p[0] = 'member', p[1]

    @staticmethod
    def p_a2ml_array_specifier_optional(p):
        """a2ml_array_specifier_optional : empty
                                         | a2ml_array_specifier"""
        p[0] = 'array_specifier', p[1]

    @staticmethod
    def p_a2ml_array_specifier(p):
        """a2ml_array_specifier : BO a2ml_constant BC
                                | BO a2ml_constant BC a2ml_array_specifier"""
        try:
            p[0] = [p[2]] + p[4]
        except IndexError:
            p[0] = [p[2]]

    @staticmethod
    def p_a2ml_taggedstruct_type_name(p):
        """a2ml_taggedstruct_type_name : taggedstruct a2ml_identifier_optional CO a2ml_taggedstruct_member_list_optional CC
                                       | taggedstruct a2ml_identifier"""
        try:
            p[0] = 'type_name', node_factory(p.slice[0].type, p[2], p[4])
        except IndexError:
            p[0] = 'type_name', node_factory(p.slice[0].type, p[2])

    @staticmethod
    def p_a2ml_taggedstruct_member_list_optional(p):
        """a2ml_taggedstruct_member_list_optional : empty
                                                  | a2ml_taggedstruct_member_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_a2ml_taggedstruct_member_list(p):
        """a2ml_taggedstruct_member_list : a2ml_taggedstruct_member
                                         | a2ml_taggedstruct_member a2ml_taggedstruct_member_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_a2ml_semicolon_optional(p):
        """a2ml_semicolon_optional : SC
                                   | empty"""
        if p[1]:
            warnings.warn('non-standard format at position {}'.format(p.lexer.lexpos), SyntaxWarning)

    @staticmethod
    def p_a2ml_taggedstruct_member(p):
        # the bellow semicolon before parenthese close is not part of the specification. however, as described in
        # example http://www.msr-wg.de/medoc/download/msrsw/v222/msrsw-tr-intro/msrsw-tr-intro.pdf at page 55, the top
        # struct definition contains a semicolon at the end. as it does not alter the output, it is possible to support
        # it.
        """a2ml_taggedstruct_member : a2ml_taggedstruct_definition SC
                                    | PO a2ml_taggedstruct_definition a2ml_semicolon_optional PC ASTERISK SC
                                    | a2ml_block_definition SC
                                    | PO a2ml_block_definition a2ml_semicolon_optional PC ASTERISK SC"""
        if len(p) == 7:
            p[0] = 'member', node_factory(p.slice[0].type, ('type_name', p[2]), True)
        else:
            p[0] = 'member', node_factory(p.slice[0].type, ('type_name', p[1]), False)

    @staticmethod
    def p_a2ml_block_definition(p):
        """a2ml_block_definition : block a2ml_tag a2ml_type_name"""
        p[0] = 'definition', node_factory(p[1], *p[2:4])

    @staticmethod
    def p_a2ml_taggedstruct_definition(p):
        """a2ml_taggedstruct_definition : a2ml_tag a2ml_member_optional
                                        | a2ml_tag PO a2ml_member PC ASTERISK"""
        try:
            node = node_factory(p.slice[0].type, p[1], p[3], True)
        except IndexError:
            node = node_factory(p.slice[0].type, p[1], p[2], False)
        p[0] = 'definition', node

    @staticmethod
    def p_a2ml_taggedunion_type_name(p):
        """a2ml_taggedunion_type_name : taggedunion a2ml_identifier_optional CO a2ml_taggedunion_member_list_optional CC
                                      | taggedunion a2ml_identifier"""
        try:
            p[0] = 'type_name', node_factory(p.slice[0].type, p[2], p[4])
        except IndexError:
            p[0] = 'type_name', node_factory(p.slice[0].type, p[2])

    @staticmethod
    def p_a2ml_taggedunion_member_list(p):
        """a2ml_taggedunion_member_list : a2ml_taggedunion_member
                                        | a2ml_taggedunion_member a2ml_taggedunion_member_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_a2ml_taggedunion_member_list_optional(p):
        """a2ml_taggedunion_member_list_optional : empty
                                                 | a2ml_taggedunion_member_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_a2ml_taggedunion_member(p):
        """a2ml_taggedunion_member : a2ml_tag a2ml_member_optional SC
                                   | a2ml_block_definition SC"""
        if len(p) == 4:
            p[0] = 'member', node_factory(p.slice[0].type, p[1], p[2])
        else:
            p[0] = 'member', p[1][1]

    @staticmethod
    def p_a2ml_tag(p):
        """a2ml_tag : S"""
        p[0] = 'tag', p[1]

    @staticmethod
    def p_a2ml_identifier(p):
        """a2ml_identifier : I"""
        p[0] = 'identifier', p[1]

    @staticmethod
    def p_a2ml_identifier_optional(p):
        """a2ml_identifier_optional : empty
                                    | a2ml_identifier"""
        if p[1]:
            p[0] = p[1]
        else:
            p[0] = 'identifier', p[1]

    @staticmethod
    def p_a2ml_keyword(p):
        """a2ml_keyword : S"""
        p[0] = 'keyword', p[1]

    @staticmethod
    def p_a2ml_constant(p):
        """a2ml_constant : N"""
        p[0] = p[1]

    @staticmethod
    def p_datatype(p):
        """datatype : UBYTE
                    | SBYTE
                    | UWORD
                    | SWORD
                    | ULONG
                    | SLONG
                    | FLOAT32_IEEE
                    | FLOAT64_IEEE"""
        p[0] = DataType(p[1])

    @staticmethod
    def p_datasize(p):
        """datasize : BYTE
                    | WORD
                    | LONG"""
        p[0] = DataSize(p[1])

    @staticmethod
    def p_addrtype(p):
        """addrtype : PBYTE
                    | PWORD
                    | PLONG
                    | DIRECT"""
        p[0] = AddrType(p[1])

    @staticmethod
    def p_byte_order_type(p):
        """byte_order_type : MSB_FIRST
                           | MSB_LAST"""
        p[0] = ByteOrder(p[1])

    @staticmethod
    def p_indexorder(p):
        """indexorder : INDEX_INCR
                      | INDEX_DECR"""
        p[0] = IndexOrder(p[1])

    @staticmethod
    def p_asap2_version(p):
        """asap2_version : ASAP2_VERSION N N"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_a2ml_version(p):
        """a2ml_version : A2ML_VERSION N N"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_generic_parameter(p):
        """generic_parameter : I
                             | S
                             | N
                             | begin I generic_parameter_list_optional end I"""
        try:
            p[0] = [p[2]] + p[3]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_generic_parameter_list(p):
        """generic_parameter_list : generic_parameter
                                  | generic_parameter generic_parameter_list"""
        try:
            p[0] = p[1] + p[2]
        except IndexError:
            p[0] = p[1]

    @staticmethod
    def p_generic_parameter_list_optional(p):
        """generic_parameter_list_optional : empty
                                           | generic_parameter_list"""
        p[0] = list() if p[1] is None else p[1]

    @staticmethod
    def p_ident_list(p):
        """ident_list : I
                      | I ident_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_ident_list_optional(p):
        """ident_list_optional : empty
                               | ident_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_project(p):
        """project : begin PROJECT I S project_optional_list_optional end PROJECT"""
        p[0] = node_factory(*p[2:6])

    @staticmethod
    def p_project_optional(p):
        """project_optional : header
                            | module"""
        p[0] = p.slice[1].type, p[1]

    @staticmethod
    def p_project_optional_list(p):
        """project_optional_list : project_optional
                                 | project_optional project_optional_list """
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_project_optional_list_optional(p):
        """project_optional_list_optional : empty
                                          | project_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_header(p):
        """header : begin HEADER S header_optional_list_optional end HEADER"""
        p[0] = node_factory(*p[2:5])

    @staticmethod
    def p_header_optional(p):
        """header_optional : version
                           | project_no"""
        p[0] = p.slice[1].type, p[1]

    @staticmethod
    def p_header_optional_list(p):
        """header_optional_list : header_optional
                                | header_optional header_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_header_optional_list_optional(p):
        """header_optional_list_optional : empty
                                         | header_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_version(p):
        """version : VERSION S"""
        p[0] = p[2]

    @staticmethod
    def p_project_no(p):
        """project_no : PROJECT_NO I"""
        p[0] = node_factory(*p[1:3])

    def p_if_data(self, p):
        """if_data : begin IF_DATA I generic_parameter_list_optional end IF_DATA"""
        p[0] = node_factory(p[2], p[3], getattr(self.a2ml.get_class([p[2]] + [p[3]] + p[4]), p[3]))

    @staticmethod
    def p_module(p):
        """module : begin MODULE I S module_optional_list_optional end MODULE"""
        p[0] = node_factory(*p[2:6])

    @staticmethod
    def p_module_optional(p):
        """module_optional : a2ml
                           | mod_par
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
        p[0] = p.slice[1].type, p[1]

    @staticmethod
    def p_module_optional_list(p):
        """module_optional_list : module_optional
                                | module_optional module_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_module_optional_list_optional(p):
        """module_optional_list_optional : empty
                                         | module_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    def p_a2ml(self, p):
        """a2ml : begin A2ML a2ml_declaration_list end A2ML"""
        self.a2ml += p[3]
        p[0] = node_factory(*p[2:4])

    @staticmethod
    def p_mod_par(p):
        """mod_par : begin MOD_PAR S mod_par_optional_list_optional end MOD_PAR"""
        p[0] = node_factory(*p[2:5])

    @staticmethod
    def p_mod_par_optional(p):
        """mod_par_optional : version
                            | addr_epk
                            | epk
                            | supplier
                            | customer
                            | customer_no
                            | user
                            | phone_no
                            | ecu
                            | cpu_type
                            | no_of_interfaces
                            | ecu_calibration_offset
                            | calibration_method
                            | memory_layout
                            | memory_segment
                            | system_constant"""
        p[0] = p.slice[1].type, p[1]

    @staticmethod
    def p_mod_par_optional_list(p):
        """mod_par_optional_list : mod_par_optional
                                 | mod_par_optional mod_par_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_mod_par_optional_list_optional(p):
        """mod_par_optional_list_optional : empty
                                          | mod_par_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_addr_epk(p):
        """addr_epk : ADDR_EPK N"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_epk(p):
        """epk : EPK S"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_supplier(p):
        """supplier : SUPPLIER S"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_customer(p):
        """customer : CUSTOMER S"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_customer_no(p):
        """customer_no : CUSTOMER_NO S"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_user(p):
        """user : USER S"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_phone_no(p):
        """phone_no : PHONE_NO S"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_mod_common(p):
        """mod_common : begin MOD_COMMON S mod_common_optional_list_optional end MOD_COMMON"""
        p[0] = node_factory(*p[2:5])

    @staticmethod
    def p_mod_common_optional(p):
        """mod_common_optional : s_rec_layout
                               | deposit
                               | byte_order
                               | data_size
                               | alignment_byte
                               | alignment_word
                               | alignment_long
                               | alignment_float32_ieee
                               | alignment_float64_ieee"""
        p[0] = p.slice[1].type, p[1]

    @staticmethod
    def p_mod_common_optional_parameter_list(p):
        """mod_common_optional_list : mod_common_optional
                                    | mod_common_optional mod_common_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_mod_common_optional_parameter_list_optional(p):
        """mod_common_optional_list_optional : empty
                                             | mod_common_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_s_rec_layout(p):
        """s_rec_layout : S_REC_LAYOUT I"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_data_size(p):
        """data_size : DATA_SIZE N"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_ecu(p):
        """ecu : ECU S"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_cpu_type(p):
        """cpu_type : CPU_TYPE S"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_no_of_interfaces(p):
        """no_of_interfaces : NO_OF_INTERFACES N"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_ecu_calibration_offset(p):
        """ecu_calibration_offset : ECU_CALIBRATION_OFFSET N"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_calibration_method(p):
        """calibration_method : begin CALIBRATION_METHOD S N calibration_method_optional_list_optional end CALIBRATION_METHOD"""
        p[0] = node_factory(*p[2:6])

    @staticmethod
    def p_calibration_method_optional(p):
        """calibration_method_optional : calibration_handle"""
        p[0] = p.slice[1].type, p[1]

    @staticmethod
    def p_calibration_method_optional_list(p):
        """calibration_method_optional_list : calibration_method_optional
                                            | calibration_method_optional calibration_method_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_calibration_method_optional_list_optional(p):
        """calibration_method_optional_list_optional : empty
                                                     | calibration_method_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_calibration_handle(p):
        """calibration_handle : begin CALIBRATION_HANDLE calibration_handle_handle_list end CALIBRATION_HANDLE"""
        p[0] = node_factory(*p[2:4])

    @staticmethod
    def p_calibration_handle_handle_list(p):
        """calibration_handle_handle_list : N
                                          | N calibration_handle_handle_list"""
        n = 'handle', p[1]
        try:
            p[0] = [n] + p[2]
        except IndexError:
            p[0] = [n]

    @staticmethod
    def p_memory_layout(p):
        """memory_layout : begin MEMORY_LAYOUT memory_layout_prg_type N N offset memory_layout_optional_list_optional end MEMORY_LAYOUT"""
        p[0] = node_factory(*p[2:8])

    @staticmethod
    def p_memory_layout_prg_type(p):
        """memory_layout_prg_type : PRG_CODE
                                  | PRG_DATA
                                  | PRG_RESERVED"""
        p[0] = p[1]

    @staticmethod
    def p_offset(p):
        """offset : N N N N N"""
        p[0] = (p[1], p[2], p[3], p[4], p[5])

    @staticmethod
    def p_memory_layout_optional_list(p):
        """memory_layout_optional_list : if_data
                                       | if_data memory_layout_optional_list"""
        n = 'if_data', p[1]
        try:
            p[0] = [n] + p[2]
        except IndexError:
            p[0] = [n]

    @staticmethod
    def p_memory_layout_optional_list_optional(p):
        """memory_layout_optional_list_optional : empty
                                                | memory_layout_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_memory_segment(p):
        """memory_segment : begin MEMORY_SEGMENT I S memory_segment_prg_type memory_segment_memory_type memory_segment_attributes N N offset memory_segment_optional_list_optional end MEMORY_SEGMENT"""
        p[0] = node_factory(*p[2:12])

    @staticmethod
    def p_memory_segment_optional_list(p):
        """memory_segment_optional_list : if_data
                                        | if_data memory_segment_optional_list"""
        n = 'if_data', p[1]
        try:
            p[0] = [n] + p[2]
        except IndexError:
            p[0] = [n]

    @staticmethod
    def p_memory_segment_optional_list_optional(p):
        """memory_segment_optional_list_optional : empty
                                                 | memory_segment_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_memory_segment_prg_type(p):
        """memory_segment_prg_type : CODE
                                   | DATA
                                   | OFFLINE_DATA
                                   | VARIABLES
                                   | SERAM
                                   | RESERVED
                                   | CALIBRATION_VARIABLES
                                   | EXCLUDE_FROM_FLASH"""
        p[0] = p[1]

    @staticmethod
    def p_memory_segment_memory_type(p):
        """memory_segment_memory_type : RAM
                                      | EEPROM
                                      | EPROM
                                      | ROM
                                      | REGISTER
                                      | FLASH"""
        p[0] = p[1]

    @staticmethod
    def p_memory_segment_attributes(p):
        """memory_segment_attributes : INTERN
                                     | EXTERN"""
        p[0] = p[1]

    @staticmethod
    def p_system_constant(p):
        """system_constant : SYSTEM_CONSTANT S S"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_characteristic(p):
        """characteristic : begin CHARACTERISTIC I S characteristic_type N I N I N N characteristic_optional_list_optional end CHARACTERISTIC"""
        p[0] = node_factory(*p[2:13])

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
        """display_identifier : DISPLAY_IDENTIFIER I"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_format(p):
        """format : FORMAT S"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_byte_order(p):
        """byte_order : BYTE_ORDER byte_order_type"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_bit_mask(p):
        """bit_mask : BIT_MASK N"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_function_list(p):
        """function_list : begin FUNCTION_LIST function_list_optional_list end FUNCTION_LIST"""
        p[0] = node_factory(*p[2:4])

    @staticmethod
    def p_function_list_optional_list(p):
        """function_list_optional_list : I
                                       | I function_list_optional_list"""
        n = 'name', p[1]
        try:
            p[0] = [n] + p[2]
        except IndexError:
            p[0] = [n]

    @staticmethod
    def p_number(p):
        """number : NUMBER N"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_extended_limits(p):
        """extended_limits : EXTENDED_LIMITS N N"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_map_list(p):
        """map_list : begin MAP_LIST map_list_optional_list_optional end MAP_LIST"""
        p[0] = node_factory(*p[2:4])

    @staticmethod
    def p_map_list_optional_list(p):
        """map_list_optional_list : I
                                  | I map_list_optional_list"""
        n = ('name', p[1])
        try:
            p[0] = [n] + p[2]
        except IndexError:
            p[0] = [n]

    @staticmethod
    def p_map_list_optional_list_optional(p):
        """map_list_optional_list_optional : empty
                                           | map_list_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_max_refresh(p):
        """max_refresh : MAX_REFRESH N N"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_dependent_characteristic(p):
        """dependent_characteristic : begin DEPENDENT_CHARACTERISTIC S characteristic_list end DEPENDENT_CHARACTERISTIC"""
        p[0] = node_factory(*p[2:5])

    @staticmethod
    def p_characteristic_list(p):
        """characteristic_list : I
                               | I characteristic_list"""
        n = 'characteristic', p[1]
        try:
            p[0] = [n] + p[2]
        except IndexError:
            p[0] = [n]

    @staticmethod
    def p_virtual_characteristic(p):
        """virtual_characteristic : begin VIRTUAL_CHARACTERISTIC S characteristic_list end VIRTUAL_CHARACTERISTIC"""
        p[0] = node_factory(*p[2:5])

    @staticmethod
    def p_ref_memory_segment(p):
        """ref_memory_segment : REF_MEMORY_SEGMENT I"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_annotation(p):
        """annotation : begin ANNOTATION annotation_optional_list_optional end ANNOTATION"""
        p[0] = node_factory(*p[2:4])

    @staticmethod
    def p_annotation_optional(p):
        """annotation_optional : annotation_label
                               | annotation_origin
                               | annotation_text"""
        p[0] = p.slice[1].type, p[1]

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
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_annotation_label(p):
        """annotation_label : ANNOTATION_LABEL S"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_annotation_origin(p):
        """annotation_origin : ANNOTATION_ORIGIN S"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_annotation_text(p):
        """annotation_text : begin ANNOTATION_TEXT annotation_text_optional_list_optional end ANNOTATION_TEXT"""
        p[0] = node_factory(*p[2:4])

    @staticmethod
    def p_annotation_text_optional_list(p):
        """annotation_text_optional_list : S
                                         | S annotation_text_optional_list"""
        n = ('text', p[1])
        try:
            p[0] = [n] + p[2]
        except IndexError:
            p[0] = [n]

    @staticmethod
    def p_annotation_text_optional_list_optional(p):
        """annotation_text_optional_list_optional : empty
                                                  | annotation_text_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_comparison_quantity(p):
        """comparison_quantity : COMPARISON_QUANTITY I"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_axis_descr(p):
        """axis_descr : begin AXIS_DESCR axis_descr_attribute I I N N N axis_descr_optional_list_optional end AXIS_DESCR"""
        p[0] = node_factory(*p[2:10])

    @staticmethod
    def p_axis_descr_optional(p):
        """axis_descr_optional : read_only
                               | format
                               | annotation
                               | axis_pts_ref
                               | max_grad
                               | monotony
                               | byte_order
                               | extended_limits
                               | fix_axis_par
                               | fix_axis_par_dist
                               | fix_axis_par_list
                               | deposit
                               | curve_axis_ref"""
        p[0] = p.slice[1].type, p[1]

    @staticmethod
    def p_axis_descr_optional_list(p):
        """axis_descr_optional_list : axis_descr_optional
                                    | axis_descr_optional axis_descr_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_axis_descr_optional_list_optional(p):
        """axis_descr_optional_list_optional : empty
                                             | axis_descr_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_axis_pts_ref(p):
        """axis_pts_ref : AXIS_PTS_REF I"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_max_grad(p):
        """max_grad : MAX_GRAD N"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_monotony(p):
        """monotony : MONOTONY MON_INCREASE
                    | MONOTONY MON_DECREASE
                    | MONOTONY STRICT_INCREASE
                    | MONOTONY STRICT_DECREASE"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_fix_axis_par(p):
        """fix_axis_par : FIX_AXIS_PAR N N N"""
        p[0] = node_factory(*p[1:5])

    @staticmethod
    def p_fix_axis_par_dist(p):
        """fix_axis_par_dist : FIX_AXIS_PAR_DIST N N N"""
        p[0] = node_factory(*p[1:5])

    @staticmethod
    def p_fix_axis_par_list(p):
        """fix_axis_par_list : begin FIX_AXIS_PAR_LIST fix_axis_par_list_optional_list_optional end FIX_AXIS_PAR_LIST"""
        p[0] = node_factory(*p[2:4])

    @staticmethod
    def p_fix_axis_par_list_optional(p):
        """fix_axis_par_list_optional : axis_pts_value"""
        p[0] = p.slice[1].type, p[1]

    @staticmethod
    def p_fix_axis_par_list_optional_list(p):
        """fix_axis_par_list_optional_list : fix_axis_par_list_optional
                                           | fix_axis_par_list_optional fix_axis_par_list_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_fix_axis_par_list_optional_list_optional(p):
        """fix_axis_par_list_optional_list_optional : empty
                                                    | fix_axis_par_list_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_axis_pts_value(p):
        """axis_pts_value : N"""
        p[0] = p[1]

    @staticmethod
    def p_curve_axis_ref(p):
        """curve_axis_ref : CURVE_AXIS_REF I"""
        p[0] = node_factory(*p[1:3])

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
        """calibration_access : CALIBRATION_ACCESS CALIBRATION
                              |  CALIBRATION_ACCESS NO_CALIBRATION
                              |  CALIBRATION_ACCESS NOT_IN_MCD_SYSTEM
                              |  CALIBRATION_ACCESS OFFLINE_CALIBRATION"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_matrix_dim(p):
        """matrix_dim : MATRIX_DIM N N N"""
        p[0] = node_factory(*p[1:5])

    @staticmethod
    def p_ecu_address_extension(p):
        """ecu_address_extension : ECU_ADDRESS_EXTENSION N"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_characteristic_optional(p):
        """characteristic_optional : display_identifier
                                   | format
                                   | byte_order
                                   | bit_mask
                                   | function_list
                                   | number
                                   | extended_limits
                                   | read_only
                                   | guard_rails
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
        p[0] = p.slice[1].type, p[1]

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
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_axis_pts(p):
        """axis_pts : begin AXIS_PTS I S N I I N I N N N axis_pts_optional_list_optional end AXIS_PTS"""
        p[0] = node_factory(*p[2:14])

    @staticmethod
    def p_axis_pts_optional(p):
        """axis_pts_optional : display_identifier
                             | read_only
                             | format
                             | deposit
                             | byte_order
                             | function_list
                             | ref_memory_segment
                             | guard_rails
                             | extended_limits
                             | annotation
                             | if_data
                             | calibration_access
                             | ecu_address_extension"""
        p[0] = p.slice[1].type, p[1]

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
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_deposit(p):
        """deposit : DEPOSIT ABSOLUTE
                   | DEPOSIT DIFFERENCE"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_measurement(p):
        """measurement : begin MEASUREMENT I S datatype I N N N N measurement_optional_list_optional end MEASUREMENT"""
        p[0] = node_factory(*p[2:12])

    @staticmethod
    def p_measurement_optional(p):
        """measurement_optional : display_identifier
                                | read_write
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
        p[0] = p.slice[1].type, p[1]

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
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_read_write(p):
        """read_write : READ_WRITE"""
        p[0] = p[1]

    @staticmethod
    def p_array_size(p):
        """array_size : ARRAY_SIZE N"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_bit_operation(p):
        """bit_operation : begin BIT_OPERATION bit_operation_optional_list_optional end BIT_OPERATION"""
        p[0] = node_factory(*p[2:4])

    @staticmethod
    def p_bit_operation_optional(p):
        """bit_operation_optional : left_shift
                                  | right_shift
                                  | sign_extend"""
        p[0] = p.slice[1].type, p[1]

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
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_left_shift(p):
        """left_shift : LEFT_SHIFT N"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_right_shift(p):
        """right_shift : RIGHT_SHIFT N"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_sign_extend(p):
        """sign_extend : SIGN_EXTEND"""
        p[0] = p[1]

    @staticmethod
    def p_compu_method(p):
        """compu_method : begin COMPU_METHOD I S compu_method_conversion_type S S compu_method_optional_list_optional end COMPU_METHOD"""
        p[0] = node_factory(*p[2:9])

    @staticmethod
    def p_compu_method_optional(p):
        """compu_method_optional : formula
                                 | coeffs
                                 | compu_tab_ref
                                 | ref_unit"""
        p[0] = p.slice[1].type, p[1]

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
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_compu_method_conversion_type(p):
        """compu_method_conversion_type : TAB_INTP
                             | TAB_NOINTP
                             | TAB_VERB
                             | RAT_FUNC
                             | FORM
                             | I"""
        p[0] = p[1]

    @staticmethod
    def p_formula(p):
        """formula : begin FORMULA S formula_optional_list_optional end FORMULA"""
        p[0] = node_factory(*p[2:5])

    @staticmethod
    def p_formula_optional_list(p):
        """formula_optional_list : formula_inv
                                 | formula_inv formula_optional_list"""
        n = 'formula_inv', p[1]
        try:
            p[0] = [n] + p[2]
        except IndexError:
            p[0] = [n]

    @staticmethod
    def p_formula_optional_list_optional(p):
        """formula_optional_list_optional : empty
                                          | formula_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_formula_inv(p):
        """formula_inv : FORMULA_INV S"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_coeffs(p):
        """coeffs : COEFFS N N N N N N"""
        p[0] = node_factory(*p[1:8])

    @staticmethod
    def p_compu_tab_ref(p):
        """compu_tab_ref : COMPU_TAB_REF I"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_ref_unit(p):
        """ref_unit : REF_UNIT I"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_virtual(p):
        """virtual : begin VIRTUAL virtual_measuring_channel_list end VIRTUAL"""
        p[0] = node_factory(*p[2:4])

    @staticmethod
    def p_virtual_measuring_channel_list(p):
        """virtual_measuring_channel_list : I
                                 | I virtual_measuring_channel_list"""
        n = 'measuring_channel', p[1]
        try:
            p[0] = [n] + p[2]
        except IndexError:
            p[0] = [n]

    @staticmethod
    def p_ecu_address(p):
        """ecu_address : ECU_ADDRESS N"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_error_mask(p):
        """error_mask : ERROR_MASK N"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_compu_tab(p):
        """compu_tab : begin COMPU_TAB I S compu_tab_conversion_type N compu_tab_optional_list_optional end COMPU_TAB"""
        p[0] = node_factory(*p[2:8])

    @staticmethod
    def p_compu_tab_optional(p):
        """compu_tab_optional : in_val_out_val
                              | default_value"""
        p[0] = p.slice[1].type, p[1]

    @staticmethod
    def p_compu_tabl_optional_list(p):
        """compu_tab_optional_list : compu_tab_optional
                                   | compu_tab_optional compu_tab_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_compu_tab_optional_list_optional(p):
        """compu_tab_optional_list_optional : empty
                                            | compu_tab_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_in_val_out_val(p):
        """in_val_out_val : N N"""
        p[0] = (p[1], p[2])

    @staticmethod
    def p_compu_tab_conversion_type(p):
        """compu_tab_conversion_type : TAB_INTP
                                     | TAB_NOINTP"""
        p[0] = p[1]

    @staticmethod
    def p_default_value(p):
        """default_value : DEFAULT_VALUE S"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_compu_vtab(p):
        """compu_vtab : begin COMPU_VTAB I S compu_vtab_conversion_type N compu_vtab_optional_list_optional end COMPU_VTAB"""
        p[0] = node_factory(*p[2:8])

    @staticmethod
    def p_compu_vtab_optional(p):
        """compu_vtab_optional : default_value
                               | compu_vtab_in_val_out_val"""
        if type(p[1]) is tuple:
            p[0] = 'in_val_out_val', p[1]
        else:
            p[0] = p.slice[1].type, p[1]

    @staticmethod
    def p_compu_vtab_optional_list(p):
        """compu_vtab_optional_list : compu_vtab_optional
                                    | compu_vtab_optional compu_vtab_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_compu_vtab_optional_list_optional(p):
        """compu_vtab_optional_list_optional : empty
                                             | compu_vtab_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_compu_vtab_in_val_out_val(p):
        """compu_vtab_in_val_out_val : N S"""
        p[0] = (p[1], p[2])

    @staticmethod
    def p_compu_vtab_conversion_type(p):
        """compu_vtab_conversion_type : TAB_VERB"""
        p[0] = p[1]

    @staticmethod
    def p_compu_vtab_range(p):
        """compu_vtab_range : begin COMPU_VTAB_RANGE I S N compu_vtab_range_optional_list_optional end COMPU_VTAB_RANGE"""
        p[0] = node_factory(*p[2:7])

    @staticmethod
    def p_compu_vtab_range_optional(p):
        """compu_vtab_range_optional : compu_vtab_range_in_val_out_val
                                     | default_value"""
        if type(p[1]) is tuple:
            p[0] = 'in_val_out_val', p[1]
        else:
            p[0] = p.slice[1].type, p[1]

    @staticmethod
    def p_compu_vtab_range_optional_list(p):
        """compu_vtab_range_optional_list : compu_vtab_range_optional
                                          | compu_vtab_range_optional compu_vtab_range_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_compu_vtab_range_optional_list_optional(p):
        """compu_vtab_range_optional_list_optional : compu_vtab_range_optional_list
                                                   | empty"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_compu_vtab_range_in_val_out_val(p):
        """compu_vtab_range_in_val_out_val : N N S"""
        p[0] = (p[1], p[2], p[3])

    @staticmethod
    def p_function(p):
        """function : begin FUNCTION I S function_optional_list_optional end FUNCTION"""
        p[0] = node_factory(*p[2:6])

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
        p[0] = p.slice[1].type, p[1]

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
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_def_characteristic(p):
        """def_characteristic : begin DEF_CHARACTERISTIC def_characteristic_optional_list_optional end DEF_CHARACTERISTIC"""
        p[0] = node_factory(*p[2:4])

    @staticmethod
    def p_def_characteristic_optional(p):
        """def_characteristic_optional : identifier"""
        p[0] = p.slice[1].type, p[1]

    @staticmethod
    def p_def_characteristic_optional_list(p):
        """def_characteristic_optional_list : def_characteristic_optional
                                            | def_characteristic_optional def_characteristic_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_def_characteristic_optional_list_optional(p):
        """def_characteristic_optional_list_optional : empty
                                                     | def_characteristic_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_identifier(p):
        """identifier : I"""
        p[0] = p[1]

    @staticmethod
    def p_ref_characteristic(p):
        """ref_characteristic : begin REF_CHARACTERISTIC ref_characteristic_optional_list_optional end REF_CHARACTERISTIC"""
        p[0] = node_factory(*p[2:4])

    @staticmethod
    def p_ref_characteristic_optional(p):
        """ref_characteristic_optional : identifier"""
        p[0] = p.slice[1].type, p[1]

    @staticmethod
    def p_ref_characteristic_optional_list(p):
        """ref_characteristic_optional_list : ref_characteristic_optional
                                            | ref_characteristic_optional ref_characteristic_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_ref_characteristic_optional_list_optional(p):
        """ref_characteristic_optional_list_optional : empty
                                                     | ref_characteristic_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_in_measurement(p):
        """in_measurement : begin IN_MEASUREMENT in_measurement_optional_list_optional end IN_MEASUREMENT"""
        p[0] = node_factory(*p[2:4])

    @staticmethod
    def p_in_measurement_optional(p):
        """in_measurement_optional : identifier"""
        p[0] = p.slice[1].type, p[1]

    @staticmethod
    def p_in_measurement_optional_list(p):
        """in_measurement_optional_list : in_measurement_optional
                                        | in_measurement_optional in_measurement_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_in_measurment_optional_list_optional(p):
        """in_measurement_optional_list_optional : empty
                                                 | in_measurement_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_out_measurement(p):
        """out_measurement : begin OUT_MEASUREMENT out_measurement_optional_list_optional end OUT_MEASUREMENT"""
        p[0] = node_factory(*p[2:4])

    @staticmethod
    def p_out_measurement_optional(p):
        """out_measurement_optional : identifier"""
        p[0] = p.slice[1].type, p[1]

    @staticmethod
    def p_out_measurement_optional_list(p):
        """out_measurement_optional_list : out_measurement_optional
                                         | out_measurement_optional out_measurement_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_out_measurment_optional_list_optional(p):
        """out_measurement_optional_list_optional : empty
                                                  | out_measurement_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_loc_measurement(p):
        """loc_measurement : begin LOC_MEASUREMENT loc_measurement_optional_list_optional end LOC_MEASUREMENT"""
        p[0] = node_factory(*p[2:4])

    @staticmethod
    def p_loc_measurement_optional(p):
        """loc_measurement_optional : identifier"""
        p[0] = p.slice[1].type, p[1]

    @staticmethod
    def p_loc_measurement_optional_list(p):
        """loc_measurement_optional_list : loc_measurement_optional
                                         | loc_measurement_optional loc_measurement_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_loc_measurment_optional_list_optional(p):
        """loc_measurement_optional_list_optional : empty
                                                  | loc_measurement_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_sub_function(p):
        """sub_function : begin SUB_FUNCTION sub_function_optional_list_optional end SUB_FUNCTION"""
        p[0] = node_factory(*p[2:4])

    @staticmethod
    def p_sub_function_optional(p):
        """sub_function_optional : identifier"""
        p[0] = p.slice[1].type, p[1]

    @staticmethod
    def p_sub_function_optional_list(p):
        """sub_function_optional_list : sub_function_optional
                                      | sub_function_optional sub_function_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_sub_function_optional_list_optional(p):
        """sub_function_optional_list_optional : empty
                                               | sub_function_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_function_version(p):
        """function_version : FUNCTION_VERSION S"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_group(p):
        """group : begin GROUP I S group_optional_list_optional end GROUP"""
        p[0] = node_factory(*p[2:6])

    @staticmethod
    def p_group_optional(p):
        """group_optional : annotation
                          | root
                          | ref_characteristic
                          | ref_measurement
                          | function_list
                          | sub_group"""
        p[0] = p.slice[1].type, p[1]

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
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_root(p):
        """root : ROOT"""
        p[0] = p[1]

    @staticmethod
    def p_ref_measurement(p):
        """ref_measurement : begin REF_MEASUREMENT ref_measurement_optional_list_optional end REF_MEASUREMENT"""
        p[0] = node_factory(*p[2:4])

    @staticmethod
    def p_ref_measurement_optional(p):
        """ref_measurement_optional : identifier"""
        p[0] = p.slice[1].type, p[1]

    @staticmethod
    def p_ref_measurement_optional_list(p):
        """ref_measurement_optional_list : ref_measurement_optional
                                         | ref_measurement_optional ref_measurement_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_ref_measurement_optional_list_optional(p):
        """ref_measurement_optional_list_optional : empty
                                                  | ref_measurement_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_sub_group(p):
        """sub_group : begin SUB_GROUP sub_group_optional_list_optional end SUB_GROUP"""
        p[0] = node_factory(*p[2:4])

    @staticmethod
    def p_sub_group_optional(p):
        """sub_group_optional : identifier"""
        p[0] = p.slice[1].type, p[1]

    @staticmethod
    def p_sub_group_optional_list(p):
        """sub_group_optional_list : sub_group_optional
                                   | sub_group_optional sub_group_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_sub_group_optional_list_optional(p):
        """sub_group_optional_list_optional : empty
                                            | sub_group_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_record_layout(p):
        """record_layout : begin RECORD_LAYOUT I record_layout_optional_list_optional end RECORD_LAYOUT"""
        p[0] = node_factory(*p[2:5])

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
        p[0] = p.slice[1].type, p[1]

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
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_fnc_values(p):
        """fnc_values : FNC_VALUES N datatype fnc_values_index_mode addrtype"""
        p[0] = node_factory(*p[1:6])

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
        """identification : IDENTIFICATION N datatype"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_axis_pts_x(p):
        """axis_pts_x : AXIS_PTS_X N datatype indexorder addrtype"""
        p[0] = node_factory(*p[1:6])

    @staticmethod
    def p_axis_pts_y(p):
        """axis_pts_y : AXIS_PTS_Y N datatype indexorder addrtype"""
        p[0] = node_factory(*p[1:6])

    @staticmethod
    def p_axis_pts_z(p):
        """axis_pts_z : AXIS_PTS_Z N datatype indexorder addrtype"""
        p[0] = node_factory(*p[1:6])

    @staticmethod
    def p_axis_rescale_x(p):
        """axis_rescale_x : AXIS_RESCALE_X N datatype N indexorder addrtype"""
        p[0] = node_factory(*p[1:7])

    @staticmethod
    def p_axis_rescale_y(p):
        """axis_rescale_y : AXIS_RESCALE_Y N datatype N indexorder addrtype"""
        p[0] = node_factory(*p[1:7])

    @staticmethod
    def p_axis_rescale_z(p):
        """axis_rescale_z : AXIS_RESCALE_Z N datatype N indexorder addrtype"""
        p[0] = node_factory(*p[1:7])

    @staticmethod
    def p_no_axis_pts_x(p):
        """no_axis_pts_x : NO_AXIS_PTS_X N datatype"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_no_axis_pts_y(p):
        """no_axis_pts_y : NO_AXIS_PTS_Y N datatype"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_no_axis_pts_z(p):
        """no_axis_pts_z : NO_AXIS_PTS_Z N datatype"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_no_rescale_x(p):
        """no_rescale_x : NO_RESCALE_X N datatype"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_no_rescale_y(p):
        """no_rescale_y : NO_RESCALE_Y N datatype"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_no_rescale_z(p):
        """no_rescale_z : NO_RESCALE_Z N datatype"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_fix_no_axis_pts_x(p):
        """fix_no_axis_pts_x : FIX_NO_AXIS_PTS_X N"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_fix_no_axis_pts_y(p):
        """fix_no_axis_pts_y : FIX_NO_AXIS_PTS_Y N"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_fix_no_axis_pts_z(p):
        """fix_no_axis_pts_z : FIX_NO_AXIS_PTS_Z N"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_src_addr_x(p):
        """src_addr_x : SRC_ADDR_X N datatype"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_src_addr_y(p):
        """src_addr_y : SRC_ADDR_Y N datatype"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_src_addr_z(p):
        """src_addr_z : SRC_ADDR_Z N datatype"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_rip_addr_x(p):
        """rip_addr_x : RIP_ADDR_X N datatype"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_rip_addr_y(p):
        """rip_addr_y : RIP_ADDR_Y N datatype"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_rip_addr_z(p):
        """rip_addr_z : RIP_ADDR_Z N datatype"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_rip_addr_w(p):
        """rip_addr_w : RIP_ADDR_W N datatype"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_shift_op_x(p):
        """shift_op_x : SHIFT_OP_X N datatype"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_shift_op_y(p):
        """shift_op_y : SHIFT_OP_Y N datatype"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_shift_op_z(p):
        """shift_op_z : SHIFT_OP_Z N datatype"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_offset_x(p):
        """offset_x : OFFSET_X N datatype"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_offset_y(p):
        """offset_y : OFFSET_Y N datatype"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_offset_z(p):
        """offset_z : OFFSET_Z N datatype"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_dist_op_x(p):
        """dist_op_x : DIST_OP_X N datatype"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_dist_op_y(p):
        """dist_op_y : DIST_OP_Y N datatype"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_dist_op_z(p):
        """dist_op_z : DIST_OP_Z N datatype"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_alignment_byte(p):
        """alignment_byte : ALIGNMENT_BYTE N"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_alignment_word(p):
        """alignment_word : ALIGNMENT_WORD N"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_alignment_long(p):
        """alignment_long : ALIGNMENT_LONG N"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_alignment_float32_ieee(p):
        """alignment_float32_ieee : ALIGNMENT_FLOAT32_IEEE N"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_alignment_float64_ieee(p):
        """alignment_float64_ieee : ALIGNMENT_FLOAT64_IEEE N"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_variant_coding(p):
        """variant_coding : begin VARIANT_CODING variant_coding_optional_list_optional end VARIANT_CODING"""
        p[0] = node_factory(*p[2:4])

    @staticmethod
    def p_variant_coding_optional(p):
        """variant_coding_optional : var_separator
                                   | var_naming
                                   | var_criterion
                                   | var_forbidden_comb
                                   | var_characteristic"""
        p[0] = p.slice[1].type, p[1]

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
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_var_separator(p):
        """var_separator : VAR_SEPARATOR S"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_var_naming(p):
        """var_naming : VAR_NAMING I"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_var_criterion(p):
        """var_criterion : begin VAR_CRITERION I S ident_list_optional var_criterion_optional_list_optional end VAR_CRITERION"""
        p[0] = node_factory(*p[2:7])

    @staticmethod
    def p_var_characteristic(p):
        """var_characteristic : begin VAR_CHARACTERISTIC I var_characteristic_optional_optional end VAR_CHARACTERISTIC"""
        p[0] = node_factory(*p[2:5])

    @staticmethod
    def p_criterion_name(p):
        """criterion_name : I"""
        p[0] = p[1]

    @staticmethod
    def p_var_characteristic_optional(p):
        """var_characteristic_optional : var_address
                                       | criterion_name"""
        p[0] = p.slice[1].type, p[1]

    @staticmethod
    def p_var_characteristic_optional_list(p):
        """var_characteristic_optional_list : var_characteristic_optional
                                            | var_characteristic_optional var_characteristic_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_var_characteristic_optional_list_optional(p):
        """var_characteristic_optional_optional : empty
                                                | var_characteristic_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_var_address(p):
        """var_address : begin VAR_ADDRESS address_list_optional end VAR_ADDRESS"""
        p[0] = node_factory(*p[2:4])

    @staticmethod
    def p_address(p):
        """address : N"""
        p[0] = p.slice[0].type, p[1]

    @staticmethod
    def p_address_list(p):
        """address_list : address
                        | address address_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_address_list_optional(p):
        """address_list_optional : empty
                                 | address_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_var_forbidden_comb(p):
        """var_forbidden_comb : begin VAR_FORBIDDEN_COMB var_forbidden_comb_criterion_list_optional end VAR_FORBIDDEN_COMB"""
        p[0] = node_factory(*p[2:4])

    @staticmethod
    def p_var_forbidden_comb_criterion_list(p):
        """var_forbidden_comb_criterion_list : I I
                                             | I I var_forbidden_comb_criterion_list"""
        n = 'criterion', (p[1], p[2])
        try:
            p[0] = [n] + p[3]
        except IndexError:
            p[0] = [n]

    @staticmethod
    def p_var_forbidden_comb_criterion_list_optional(p):
        """var_forbidden_comb_criterion_list_optional : empty
                                                      | var_forbidden_comb_criterion_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_var_criterion_optional(p):
        """var_criterion_optional : var_measurement
                                  | var_selection_characteristic"""
        p[0] = p.slice[1].type, p[1]

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
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_var_measurement(p):
        """var_measurement : VAR_MEASUREMENT I"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_var_selection_characteristic(p):
        """var_selection_characteristic : VAR_SELECTION_CHARACTERISTIC I"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_reserved(p):
        """reserved : RESERVED N datasize"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_frame(p):
        """frame : begin FRAME I S N N frame_optional_list_optional end FRAME"""
        p[0] = node_factory(*p[2:8])

    @staticmethod
    def p_frame_optional(p):
        """frame_optional : frame_measurement
                          | if_data"""
        p[0] = p.slice[1].type, p[1]

    @staticmethod
    def p_frame_optional_list(p):
        """frame_optional_list : frame_optional
                               | frame_optional frame_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_frame_optional_list_optional(p):
        """frame_optional_list_optional : empty
                                        | frame_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_frame_measurement(p):
        """frame_measurement : FRAME_MEASUREMENT frame_measurement_optional_list_optional"""
        p[0] = node_factory(*p[1:3])

    @staticmethod
    def p_frame_measurement_optional(p):
        """frame_measurement_optional : identifier"""
        p[0] = p.slice[1].type, p[1]

    @staticmethod
    def p_frame_measurement_optional_list(p):
        """frame_measurement_optional_list : frame_measurement_optional
                                           | frame_measurement_optional frame_measurement_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_frame_measurement_optional_list_optional(p):
        """frame_measurement_optional_list_optional : empty
                                                    | frame_measurement_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_user_rights(p):
        """user_rights : begin USER_RIGHTS I user_rights_optional_list_optional end USER_RIGHTS"""
        p[0] = node_factory(*p[2:5])

    @staticmethod
    def p_user_rights_optional(p):
        """user_rights_optional : ref_group
                                | read_only"""
        p[0] = p.slice[1].type, p[1]

    @staticmethod
    def p_user_rights_optional_list(p):
        """user_rights_optional_list : user_rights_optional
                                     | user_rights_optional user_rights_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_user_rights_optional_list_optional(p):
        """user_rights_optional_list_optional : empty
                                              | user_rights_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_ref_group(p):
        """ref_group : begin REF_GROUP ref_group_optional_list_optional end REF_GROUP"""
        p[0] = node_factory(*p[2:4])

    @staticmethod
    def p_ref_group_optional(p):
        """ref_group_optional : identifier"""
        p[0] = p.slice[1].type, p[1]

    @staticmethod
    def p_ref_group_optional_list(p):
        """ref_group_optional_list : ref_group_optional
                                   | ref_group_optional ref_group_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_ref_group_optional_list_optional(p):
        """ref_group_optional_list_optional : empty
                                            | ref_group_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_read_only(p):
        """read_only : READ_ONLY"""
        p[0] = p[1]

    @staticmethod
    def p_guard_rails(p):
        """guard_rails : GUARD_RAILS"""
        p[0] = p[1]

    @staticmethod
    def p_unit(p):
        """unit : begin UNIT I S S unit_type unit_optional_list_optional end UNIT"""
        p[0] = node_factory(*p[2:8])

    @staticmethod
    def p_unit_optional(p):
        """unit_optional : si_exponents
                         | ref_unit
                         | unit_conversion"""
        p[0] = p.slice[1].type, p[1]

    @staticmethod
    def p_unit_optional_list(p):
        """unit_optional_list : unit_optional
                              | unit_optional unit_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_unit_optional_list_optional(p):
        """unit_optional_list_optional : empty
                                       | unit_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_unit_type(p):
        """unit_type : EXTENDED_SI
                     | DERIVED"""
        p[0] = p[1]

    @staticmethod
    def p_si_exponents(p):
        """si_exponents : SI_EXPONENTS N N N N N N N"""
        p[0] = node_factory(*p[1:9])

    @staticmethod
    def p_unit_conversion(p):
        """unit_conversion : UNIT_CONVERSION N N"""
        p[0] = node_factory(*p[1:4])

    @staticmethod
    def p_empty(p):
        """empty :"""
        p[0] = None
