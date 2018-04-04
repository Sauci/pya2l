"""
@project: pya2l
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
            delta = 120
            s = position - delta if position >= delta else 0
            e = position + delta if len(string) >= position + delta else -1
            substring = string[s:e].replace('\r', ' ').replace('\n', ' ')
            indicator = ' ' * (delta if position >= delta else position) + '^'
            self.value += '\r\n\t' + ('...' if s else '   ') + substring + '\r\n\t   ' + indicator

        super(A2lFormatException, self).__init__(self.value)


def a2l_node_factory(node_type, *args, **kwargs):
    try:
        return {
            'A2ML_VERSION': A2MLVersion,
            'ADDRESS_MAPPING': AddressMapping,
            'ASAP2_VERSION': ASAP2Version,
            'CHECKSUM': Checksum,
            'EVENT_GROUP': EventGroup,
            'FRAME': Frame,
            'HEADER': Header,
            'IDENTIFICATION': Identification,
            'if_data_memory_segment': IfDataMemorySegment,
            'MEASUREMENT': Measurement,
            'MODULE': Module,
            'MOD_PAR': ModPar,
            'PROJECT': Project,
            'RASTER': Raster,
            'REF_GROUP': RefGroup,
            'ROOT': A2lFile,
            'SEED_KEY': SeedKey,
            'SI_EXPONENTS': SiExponents,
            'SYSTEM_CONSTANT': SystemConstant,
            'UNIT': Unit,
            'UNIT_CONVERSION': UnitConversion,
            'USER_RIGHTS': UserRights,
            'VAR_CRITERION': VarCriterion,
        }[node_type](node_type, *args, **kwargs)
    except KeyError:
        raise NotImplementedError(str(node_type))
    except:
        raise


class A2lNode(object):
    def __init__(self, node, *args, **kwargs):
        self._parent = None
        self._children = list()
        for attribute, value in args:
            try:
                attr = getattr(self, attribute)
                if isinstance(attr, list):
                    attr.append(value)
                elif attr is None:
                    setattr(self, attribute, value)
                else:
                    raise ValueError
                if isinstance(value, A2lNode):
                    value.set_parent(self)
                    self.add_children(value)
            except AttributeError as e:
                raise e
            except:
                raise
        self._node = node

    def set_parent(self, a2l_node):
        self._parent = a2l_node

    def add_children(self, a2l_node):
        self._children.append(a2l_node)


class Version(A2lNode):
    def __init__(self, node, major=None, minor=None, patch=None):
        self.major = major
        self.minor = minor
        self.patch = patch
        super(Version, self).__init__(node)
        print self


class A2lFile(A2lNode):
    def __init__(self, node, args):
        self.asap2_version = None
        self.a2ml_version = None
        self.project = None
        super(A2lFile, self).__init__(node, *args)
        print self


class A2MLVersion(Version): pass


class AddressMapping(A2lNode):
    def __init__(self, node, orig_address, mapping_address, length):
        self.orig_address = orig_address
        self.mapping_address = mapping_address
        self.length = length
        super(AddressMapping, self).__init__(node)
        print self


class ASAP2Version(Version): pass


class Checksum(A2lNode):
    def __init__(self, node, checksum_dll, max_block_size):
        self.checksum_dll = checksum_dll
        self.max_block_size = max_block_size
        super(Checksum, self).__init__(node)
        print self


class EventGroup(A2lNode):
    def __init__(self, node, raster_grp_name, short_name, raster_id):
        self.raster_grp_name = raster_grp_name
        self.short_name = short_name
        self.raster_id = raster_id
        super(EventGroup, self).__init__(node)
        print self


class Frame(A2lNode):
    def __init__(self, node, name, long_identifier, scaling_unit, rate, args):
        self.name = name
        self.long_identifier = long_identifier
        self.scaling_unit = scaling_unit
        self.rate = rate
        self.frame_measurement = None
        self.frame_if_data = list()
        super(Frame, self).__init__(node, *args)
        print self


class Header(A2lNode):
    def __init__(self, node, comment, version=None, project_no=None):
        self.comment = comment
        self.version = version
        self.project_no = project_no
        super(Header, self).__init__(node)
        print self


class Identification(A2lNode):
    def __init__(self, node, position, datatype):
        self.position = position
        self.datatype = datatype
        super(Identification, self).__init__(node)
        print self


class IfDataMemorySegment(A2lNode):
    def __init__(self, node, name, args):
        self.name = name
        self.address_mapping = list()
        self.segment = list()
        super(IfDataMemorySegment, self).__init__(node, *args)
        print self


class Measurement(A2lNode):
    def __init__(self, node, name, long_identifier, datatype, conversion, resolution, accuracy, lower_limit,
                 upper_limit, args):
        self.name = name
        self.long_identifier = long_identifier
        self.datatype = datatype
        self.conversion = conversion
        self.resolution = resolution
        self.accuracy = accuracy
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.display_identifier = None
        self.read_write = None
        self.format = None
        self.array_size = None
        self.bit_mask = None
        self.bit_operation = None
        self.byte_order = None
        self.max_refresh = None
        self.virtual = None
        self.function_list = None
        self.ecu_address = None
        self.error_mask = None
        self.ref_memory_segment = None
        self.annotation = list()
        self.if_data_measurement = list()
        self.matrix_dim = None
        self.ecu_address_extension = None
        super(Measurement, self).__init__(node, *args)
        print self


class Module(A2lNode):
    def __init__(self, node, name, long_identifier, args):
        self.name = name
        self.long_identifier = long_identifier
        self.a2ml = None
        self.mod_par = None
        self.mod_common = None
        self.if_data_module = list()
        self.characteristic = list()
        self.axis_pts = list()
        self.measurement = list()
        self.compu_method = list()
        self.compu_tab = list()
        self.compu_vtab = list()
        self.compu_vtab_range = list()
        self.function = list()
        self.group = list()
        self.record_layout = list()
        self.variant_coding = None
        self.frame = None
        self.user_rights = list()
        self.unit = list()
        super(Module, self).__init__(node, *args)
        print self


class ModPar(A2lNode):
    def __init__(self, node, comment, args):
        self.comment = comment
        self.version = None
        self.addr_epk = list()
        self.epk = None
        self.supplier = None
        self.customer = None
        self.customer_no = None
        self.user = None
        self.phone_no = None
        self.ecu = None
        self.cpu_type = None
        self.no_of_interfaces = None
        self.ecu_calibration_offset = None
        self.calibration_method = list()
        self.memory_layout = list()
        self.memory_segment = list()
        self.system_constant = list()
        super(ModPar, self).__init__(node, *args)
        print self


class Project(A2lNode):
    def __init__(self, node, name, long_identifier, args):
        self.name = name
        self.long_identifier = long_identifier
        self.header = None
        self.module = list()
        super(Project, self).__init__(node, *args)
        print self


class Raster(A2lNode):
    def __init__(self, node, raster_name, short_name, raster_id, scaling_unit, rate):
        self.raster_name = raster_name
        self.short_name = short_name
        self.raster_id = raster_id
        self.scaling_unit = scaling_unit
        self.rate = rate
        super(Raster, self).__init__(node)
        print self


class RefGroup(A2lNode):
    def __init__(self, node, identifier):
        self.identifier = identifier
        super(RefGroup, self).__init__(node)
        print self


class SeedKey(A2lNode):
    def __init__(self, node, cal_dll, daq_dll, pgm_dll):
        self.cal_dll = cal_dll
        self.daq_dll = daq_dll
        self.pgm_dll = pgm_dll
        super(SeedKey, self).__init__(node)
        print self


class SiExponents(A2lNode):
    def __init__(self, node, length, mass, time, electric_current, temperature, amount_of_substance,
                 luminous_intensity):
        self.length = length
        self.mass = mass
        self.time = time
        self.electric_current = electric_current
        self.temperature = temperature
        self.amount_of_substance = amount_of_substance
        self.luminous_intensity = luminous_intensity
        super(SiExponents, self).__init__(node)
        print self


class SystemConstant(A2lNode):
    def __init__(self, node, name, value):
        self.name = name
        self.value = value
        super(SystemConstant, self).__init__(node)
        print self


class Unit(A2lNode):
    def __init__(self, node, name, long_identifier, display, type, args):
        self.name = name
        self.long_identifier = long_identifier
        self.display = display
        self.type = type
        self.si_exponents = None
        self.ref_unit = None
        self.unit_conversion = None
        super(Unit, self).__init__(node, *args)
        print self


class UnitConversion(A2lNode):
    def __init__(self, node, gradient, offset):
        self.gradient = gradient
        self.offset = offset
        super(UnitConversion, self).__init__(node)
        print self


class UserRights(A2lNode):
    def __init__(self, node, user_level_id, args):
        self.user_level_id = user_level_id
        self.read_only = None
        self.ref_group = list()
        super(UserRights, self).__init__(node, *args)
        print self


class VarCriterion(A2lNode):
    def __init__(self, node, name, long_identifier, value, args):
        self.name = name
        self.long_identifier = long_identifier
        self.value = value
        self.var_measurement = None
        self.var_selection_characteristic = None
        super(VarCriterion, self).__init__(node, *args)
        print self


class A2lParser(A2lNode):
    tokens = lexer.tokens

    def __init__(self, string):
        self.ast = None
        self._yacc = yacc.yacc(module=self)
        self._yacc.parse(string)

    @staticmethod
    def p_error(p):
        raise A2lFormatException('invalid sequence at position ', p.lexpos, string=p.lexer.lexdata)

        try:
            skip_len = len(p.value)
            p.lexer.skip(skip_len)
        except Exception as e:
            p.lexer.skip(1)
        pass

    def p_a2l(self, p):
        """a2l : a2l_optional_list_optional"""
        p[0] = a2l_node_factory('ROOT', p[1])
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
        """a2ml_declaration : a2ml_type_definition SEMICOLON
                            | a2ml_block_definition SEMICOLON"""
        p[0] = p[1]

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
        p[0] = p[1]

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
        p[0] = p[1]

    @staticmethod
    def p_a2ml_block_definition(p):
        """a2ml_block_definition : block a2ml_tag a2ml_type_name"""

    @staticmethod
    def p_a2ml_enum_type_name(p):
        """a2ml_enum_type_name : enum a2ml_identifier_optional CURLY_OPEN a2ml_enumerator_list CURLY_CLOSE
                               | enum a2ml_identifier"""
        try:
            p[0] = [p[2]] + p[4]
        except IndexError:
            p[0] = [p[2]]

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
        p[0] = p[1]

    @staticmethod
    def p_a2ml_struct_type_name(p):
        """a2ml_struct_type_name : struct a2ml_identifier_optional CURLY_OPEN a2ml_struct_member_list_optional CURLY_CLOSE
                                 | struct a2ml_identifier"""
        p[0] = p[1]

    @staticmethod
    def p_a2ml_struct_member_list_optional(p):
        """a2ml_struct_member_list_optional : empty
                                            | a2ml_struct_member_list"""
        p[0] = p[1]

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
        """a2ml_struct_member : a2ml_member SEMICOLON"""
        p[0] = p[1]

    @staticmethod
    def p_a2ml_member(p):
        """a2ml_member : a2ml_type_name a2ml_array_specifier_optional"""
        p[0] = p[1]

    @staticmethod
    def p_a2ml_member_optional(p):
        """a2ml_member_optional : empty
                                | a2ml_member"""
        p[0] = p[1]

    @staticmethod
    def p_a2ml_array_specifier_optional(p):
        """a2ml_array_specifier_optional : empty
                                         | a2ml_array_specifier"""
        p[0] = p[1]

    @staticmethod
    def p_a2ml_array_specifier(p):
        """a2ml_array_specifier : BRACE_OPEN a2ml_constant BRACE_CLOSE
                                | BRACE_OPEN a2ml_constant BRACE_CLOSE a2ml_array_specifier"""
        p[0] = p[1]

    @staticmethod
    def p_a2ml_taggedstruct_type_name(p):
        """a2ml_taggedstruct_type_name : taggedstruct a2ml_identifier_optional CURLY_OPEN a2ml_taggedstruct_member_list_optional CURLY_CLOSE
                                       | taggedstruct a2ml_identifier"""
        p[0] = p[1]

    @staticmethod
    def p_a2ml_taggedstruct_member_list_optional(p):
        """a2ml_taggedstruct_member_list_optional : empty
                                                  | a2ml_taggedstruct_member_list"""
        p[0] = p[1]

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
    def p_a2ml_taggedstruct_definition(
            p):  # TODO: check if the optional member is really optional (seems to be optional in example).
        """a2ml_taggedstruct_definition : a2ml_tag a2ml_member_optional
                                        | a2ml_tag PARENTHESE_OPEN a2ml_member PARENTHESE_CLOSE ASTERISK"""

    @staticmethod
    def p_a2ml_taggedunion_type_name(p):
        """a2ml_taggedunion_type_name : taggedunion a2ml_identifier_optional CURLY_OPEN a2ml_taggedunion_member_list CURLY_CLOSE
                                      | taggedunion a2ml_identifier"""

    @staticmethod
    def p_a2ml_taggedunion_member_list(p):
        """a2ml_taggedunion_member_list : a2ml_taggedunion_member
                                        | a2ml_taggedunion_member a2ml_taggedunion_member_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

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
    def p_asap2_version(p):
        """asap2_version : ASAP2_VERSION number_list"""
        p[0] = a2l_node_factory(p[1], *p[2])

    @staticmethod
    def p_a2ml_version(p):
        """a2ml_version : A2ML_VERSION number_list"""
        p[0] = a2l_node_factory(p[1], *p[2])

    @staticmethod
    def p_generic_parameter(p):
        """generic_parameter : IDENT
                             | STRING
                             | NUMERIC
                             | begin IDENT generic_parameter_list_optional end IDENT"""

    @staticmethod
    def p_generic_parameter_list(p):
        """generic_parameter_list : generic_parameter
                                  | generic_parameter generic_parameter_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_generic_parameter_list_optional(p):
        """generic_parameter_list_optional : empty
                                           | generic_parameter_list"""

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
        """project : begin PROJECT IDENT STRING project_optional_list_optional end PROJECT"""
        p[0] = a2l_node_factory(*p[2:6])

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
        """header : begin HEADER STRING header_optional_list_optional end HEADER"""
        p[0] = a2l_node_factory(*p[2:5])

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
        """version : VERSION STRING"""
        p[0] = p[2]

    @staticmethod
    def p_project_no(p):
        """project_no : PROJECT_NO IDENT"""
        p[0] = p[2]

    @staticmethod
    def p_module(p):
        """module : begin MODULE IDENT STRING module_optional_list_optional end MODULE"""
        p[0] = a2l_node_factory(*p[2:6])

    @staticmethod
    def p_module_optional(p):
        """module_optional : a2ml
                           | mod_par
                           | mod_common
                           | if_data_module
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

    @staticmethod
    def p_a2ml(p):
        """a2ml : begin A2ML a2ml_declaration_list end A2ML"""
        p[0] = p[3]

    @staticmethod
    def p_if_data_module(p):
        """if_data_module : begin IF_DATA IDENT if_data_module_optional_list_optional end IF_DATA"""

    @staticmethod  # TODO: protocol_layer, daq and xcp_on_can are not available in rev.1.51...
    def p_if_data_module_optional(p):
        """if_data_module_optional : source
                                   | raster
                                   | event_group
                                   | seed_key
                                   | checksum
                                   | tp_blob tp_data
                                   | if_data_module_unsupported_element"""
        p[0] = p.slice[1].type, p[1]

    @staticmethod
    def p_if_data_module_optional_list(p):
        """if_data_module_optional_list : if_data_module_optional
                                        | if_data_module_optional if_data_module_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_if_data_module_optional_list_optional(p):
        """if_data_module_optional_list_optional : empty
                                                 | if_data_module_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_if_data_module_unsupported_element(p):
        """if_data_module_unsupported_element : generic_parameter_list"""

    @staticmethod
    def p_source(p):
        """source : begin SOURCE IDENT NUMERIC NUMERIC source_optional_list_optional end SOURCE"""
        p[0] = a2l_node_factory(*p[2:7])

    @staticmethod
    def p_raster(p):
        """raster : begin RASTER STRING STRING NUMERIC NUMERIC NUMERIC end RASTER"""
        p[0] = a2l_node_factory(*p[2:8])

    @staticmethod
    def p_event_group(p):
        """event_group : begin EVENT_GROUP STRING STRING number_list end EVENT_GROUP"""
        p[0] = a2l_node_factory(*p[2:6])

    @staticmethod
    def p_seed_key(p):
        """seed_key : begin SEED_KEY STRING STRING STRING end SEED_KEY"""
        p[0] = a2l_node_factory(*p[2:6])

    @staticmethod  # TODO: ident ident numeric pattern is not part of the specification, check...
    def p_checksum(p):
        """checksum : begin CHECKSUM STRING end CHECKSUM
                    | begin CHECKSUM IDENT max_block_size end CHECKSUM"""
        try:
            p[0] = a2l_node_factory(*p[2:3])  # TODO: add support for both descriptions.
        except TypeError:
            p[0] = a2l_node_factory(*p[2:5])

    @staticmethod
    def p_max_block_size(p):
        """max_block_size : MAX_BLOCK_SIZE NUMERIC"""
        p[0] = p[2]

    @staticmethod
    def p_tp_blob(p):
        """tp_blob : TP_BLOB"""
        p[0] = p[1]

    @staticmethod
    def p_tp_data(p):
        """tp_data : generic_parameter_list"""
        p[0] = p[1]

    @staticmethod
    def p_source_optional(p):
        """source_optional : display_identifier
                           | qp_blob"""

    @staticmethod
    def p_source_optional_list(p):
        """source_optional_list : source_optional
                                | source_optional source_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_source_optional_list_optional(p):
        """source_optional_list_optional : empty
                                         | source_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod
    def p_qp_blob(p):
        """qp_blob : QP_BLOB IDENT"""

    @staticmethod
    def p_mod_par(p):
        """mod_par : begin MOD_PAR STRING mod_par_optional_list_optional end MOD_PAR"""
        p[0] = a2l_node_factory(*p[2:5])

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
        """addr_epk : ADDR_EPK NUMERIC"""

    @staticmethod
    def p_epk(p):
        """epk : EPK STRING"""

    @staticmethod
    def p_supplier(p):
        """supplier : SUPPLIER STRING"""

    @staticmethod
    def p_customer(p):
        """customer : CUSTOMER STRING"""

    @staticmethod
    def p_customer_no(p):
        """customer_no : CUSTOMER_NO STRING"""

    @staticmethod
    def p_user(p):
        """user : USER STRING"""

    @staticmethod
    def p_phone_no(p):
        """phone_no : PHONE_NO STRING"""

    @staticmethod
    def p_mod_common(p):
        """mod_common : begin MOD_COMMON STRING mod_common_optional_parameter_list_optional end MOD_COMMON"""

    @staticmethod
    def p_mod_common_optional_parameter(p):
        """mod_common_optional_parameter : s_rec_layout
                                         | deposit
                                         | byte_order
                                         | data_size
                                         | alignment_byte
                                         | alignment_word
                                         | alignment_long
                                         | alignment_float32_ieee
                                         | alignment_float64_ieee"""

    @staticmethod
    def p_mod_common_optional_parameter_list(p):
        """mod_common_optional_parameter_list : mod_common_optional_parameter
                                              | mod_common_optional_parameter mod_common_optional_parameter_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_mod_common_optional_parameter_list_optional(p):
        """mod_common_optional_parameter_list_optional : empty
                                                       | mod_common_optional_parameter_list"""

    @staticmethod
    def p_s_rec_layout(p):
        """s_rec_layout : S_REC_LAYOUT IDENT"""
        p[0] = p[2]

    @staticmethod
    def p_data_size(p):
        """data_size : DATA_SIZE NUMERIC"""
        p[0] = p[2]

    @staticmethod
    def p_ecu(p):
        """ecu : ECU STRING"""
        p[0] = p[2]

    @staticmethod
    def p_cpu_type(p):
        """cpu_type : CPU_TYPE STRING"""
        p[0] = p[2]

    @staticmethod
    def p_no_of_interfaces(p):
        """no_of_interfaces : NO_OF_INTERFACES NUMERIC"""
        p[0] = p[2]

    @staticmethod
    def p_ecu_calibration_offset(p):
        """ecu_calibration_offset : ECU_CALIBRATION_OFFSET NUMERIC"""
        p[0] = p[2]

    @staticmethod
    def p_calibration_method(p):
        """calibration_method : begin CALIBRATION_METHOD STRING NUMERIC number_list end CALIBRATION_METHOD"""

    @staticmethod
    def p_memory_layout(p):
        """memory_layout : begin MEMORY_LAYOUT memory_layout_prg_type NUMERIC NUMERIC number_list memory_layout_parameter_optional end MEMORY_LAYOUT"""

    @staticmethod
    def p_memory_layout_prg_type(p):
        """memory_layout_prg_type : PRG_CODE
                                  | PRG_DATA
                                  | PRG_RESERVED"""

    @staticmethod
    def p_memory_layout_parameter_optional(p):
        """memory_layout_parameter_optional : empty
                                            | if_data_memory_layout"""

    @staticmethod
    def p_if_data_memory_layout(p):
        """if_data_memory_layout : begin IF_DATA IDENT if_data_memory_layout_optional_parameter_list_optional end IF_DATA"""

    @staticmethod
    def p_if_data_memory_layout_optional_parameter(p):
        """if_data_memory_layout_optional_parameter : dp_blob dp_data
                                                    | ba_blob pa_data"""

    @staticmethod
    def p_if_data_memory_layout_optional_parameter_list(p):
        """if_data_memory_layout_optional_parameter_list : if_data_memory_layout_optional_parameter
                                                         | if_data_memory_layout_optional_parameter if_data_memory_layout_optional_parameter_list"""

        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_if_data_memory_layout_optional_parameter_list_optional(p):
        """if_data_memory_layout_optional_parameter_list_optional : empty
                                                                  | if_data_memory_layout_optional_parameter_list"""

    @staticmethod
    def p_dp_blob(p):
        """dp_blob : DP_BLOB"""
        p[0] = p[1]

    @staticmethod
    def p_ba_blob(p):
        """ba_blob : BA_BLOB"""
        p[0] = p[1]

    @staticmethod
    def p_dp_data(p):
        """dp_data : generic_parameter_list"""
        p[0] = p[1]

    @staticmethod
    def p_pa_data(p):
        """pa_data : generic_parameter_list"""
        p[0] = p[1]

    @staticmethod
    def p_memory_segment(p):
        """memory_segment : begin MEMORY_SEGMENT IDENT STRING memory_segment_prg_type memory_segment_memory_type memory_segment_attributes NUMERIC NUMERIC NUMERIC NUMERIC NUMERIC NUMERIC NUMERIC memory_segment_optional_parameter_list_optional end MEMORY_SEGMENT"""
        p[0] = p[2]

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
    def p_memory_segment_optional_parameter_list_optional(p):
        """memory_segment_optional_parameter_list_optional : empty
                                                           | memory_segment_optional_parameter_list"""
        p[0] = p[1]

    @staticmethod
    def p_memory_segment_optional_list(p):
        """memory_segment_optional_parameter_list : memory_segment_optional
                                                  | memory_segment_optional memory_segment_optional_parameter_list"""

        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_memory_segment_optional(p):
        """memory_segment_optional : if_data_memory_segment"""

    @staticmethod
    def p_system_constant(p):
        """system_constant : SYSTEM_CONSTANT STRING STRING"""
        p[0] = a2l_node_factory(*p[1:4])

    @staticmethod
    def p_if_data_memory_segment(p):
        """if_data_memory_segment : begin IF_DATA IDENT if_data_memory_segment_optional_list_optional end IF_DATA"""
        p[0] = a2l_node_factory('if_data_memory_segment', *p[3:5])

    @staticmethod
    def p_if_data_memory_segment_optional(p):
        """if_data_memory_segment_optional : address_mapping
                                           | segment"""
        p[0] = p.slice[1].type, p[1]

    @staticmethod
    def p_if_data_memory_segment_optional_list(p):
        """if_data_memory_segment_optional_list : if_data_memory_segment_optional
                                                | if_data_memory_segment_optional if_data_memory_segment_optional_list"""

        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_if_data_memory_segment_optional_list_optional(p):
        """if_data_memory_segment_optional_list_optional : empty
                                                         | if_data_memory_segment_optional_list"""
        p[0] = tuple() if p[1] is None else p[1]

    @staticmethod  # TODO: segment is not defined in the specification, check...
    def p_segment(p):
        """segment : begin SEGMENT NUMERIC NUMERIC NUMERIC NUMERIC NUMERIC segment_optional_parameter_list_optional end SEGMENT"""

    @staticmethod
    def p_segment_optional_parameter(p):
        """segment_optional_parameter : page
                                      | checksum"""

    @staticmethod
    def p_segment_optional_parameter_list(p):
        """segment_optional_parameter_list : segment_optional_parameter
                                           | segment_optional_parameter segment_optional_parameter_list"""

        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_segment_optional_parameter_list_optional(p):
        """segment_optional_parameter_list_optional : empty
                                                    | segment_optional_parameter_list"""

    @staticmethod
    def p_page(p):
        """page : begin PAGE NUMERIC IDENT IDENT IDENT page_optional_parameter_list_optional end PAGE"""

    @staticmethod
    def p_page_optional_parameter(p):
        """page_optional_parameter : init_segment"""

    @staticmethod
    def p_page_optional_parameter_list(p):
        """page_optional_parameter_list : page_optional_parameter
                                        | page_optional_parameter page_optional_parameter_list"""

        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_page_optional_parameter_list_optional(p):
        """page_optional_parameter_list_optional : empty
                                                 | page_optional_parameter_list"""

    @staticmethod
    def p_init_segment(p):
        """init_segment : INIT_SEGMENT NUMERIC"""

    @staticmethod
    def p_address_mapping(p):
        """address_mapping : ADDRESS_MAPPING NUMERIC NUMERIC NUMERIC"""
        p[0] = a2l_node_factory(*p[1:5])

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
        """virtual_characteristic : begin VIRTUAL_CHARACTERISTIC STRING virtual_characteristic_optional_list_optional end VIRTUAL_CHARACTERISTIC"""
        pass

    @staticmethod
    def p_virtual_characteristic_optional(p):
        """virtual_characteristic_optional : IDENT"""

    @staticmethod
    def p_virtual_characteristic_optional_list(p):
        """virtual_characteristic_optional_list : virtual_characteristic_optional
                                                | virtual_characteristic_optional virtual_characteristic_optional_list"""

        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_virtual_characteristic_optional_list_optional(p):
        """virtual_characteristic_optional_list_optional : empty
                                                         | virtual_characteristic_optional_list"""

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
        """axis_descr : begin AXIS_DESCR axis_descr_attribute IDENT IDENT NUMERIC NUMERIC NUMERIC axis_descr_optional_list_optional end AXIS_DESCR"""
        p[0] = p[4]

    @staticmethod
    def p_axis_descr_optional(p):
        """axis_descr_optional : READ_ONLY
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

    @staticmethod
    def p_axis_pts_ref(p):
        """axis_pts_ref : AXIS_PTS_REF IDENT"""

    @staticmethod
    def p_max_grad(p):
        """max_grad : MAX_GRAD NUMERIC"""

    @staticmethod
    def p_monotony(p):
        """monotony : MONOTONY monotony_type"""

    @staticmethod
    def p_monotony_type(p):
        """monotony_type : MON_INCREASE
                         | MON_DECREASE
                         | STRICT_INCREASE
                         | STRICT_DECREASE"""

    @staticmethod
    def p_fix_axis_par(p):
        """fix_axis_par : FIX_AXIS_PAR NUMERIC NUMERIC NUMERIC"""

    @staticmethod
    def p_fix_axis_par_dist(p):
        """fix_axis_par_dist : FIX_AXIS_PAR_DIST NUMERIC NUMERIC NUMERIC"""

    @staticmethod
    def p_fix_axis_par_list(p):
        """fix_axis_par_list : begin FIX_AXIS_PAR_LIST number_list end FIX_AXIS_PAR_LIST"""

        p[0] = p[3]

    @staticmethod
    def p_curve_axis_ref(p):
        """curve_axis_ref : CURVE_AXIS_REF IDENT"""

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
                                   | if_data_characteristic
                                   | axis_descr
                                   | calibration_access
                                   | matrix_dim
                                   | ecu_address_extension"""
        p[0] = p[1]

    @staticmethod
    def p_if_data_characteristic(p):
        """if_data_characteristic : if_data_memory_layout"""

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
                             | if_data_axis_pts
                             | calibration_access
                             | ecu_address_extension"""
        p[0] = p[1]

    @staticmethod
    def p_if_data_axis_pts(p):
        """if_data_axis_pts : if_data_memory_layout"""
        p[0] = p[1]

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
        p[0] = p[1]

    @staticmethod
    def p_deposit_mode(p):
        """deposit_mode : ABSOLUTE
                        | DIFFERENCE"""
        p[0] = p[1]

    @staticmethod
    def p_measurement(p):
        """measurement : begin MEASUREMENT IDENT STRING datatype IDENT NUMERIC NUMERIC NUMERIC NUMERIC measurement_optional_list_optional end MEASUREMENT"""
        p[0] = a2l_node_factory(*p[2:12])

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
                                | if_data_measurement
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
    def p_if_data_measurement(p):
        """if_data_measurement : begin IF_DATA IDENT if_data_measurement_optional_parameter_list_optional end IF_DATA"""
        p[0] = p[1]

    @staticmethod
    def p_if_data_measurement_optional_parameter(p):
        """if_data_measurement_optional_parameter : kp_blob kp_data
                                                  | dp_blob dp_data
                                                  | pa_blob pa_data
                                                  | if_data_measurement_unsupported_element"""
        p[0] = p[1]

    @staticmethod
    def p_if_data_measurement_unsupported_element(p):
        """if_data_measurement_unsupported_element : begin IDENT generic_parameter_list end IDENT"""
        p[0] = p[1]

    @staticmethod
    def p_if_data_measurement_optional_parameter_list(p):
        """if_data_measurement_optional_parameter_list : if_data_measurement_optional_parameter
                                                       | if_data_measurement_optional_parameter if_data_measurement_optional_parameter_list"""

        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_if_data_measurement_optional_parameter_list_optional(p):
        """if_data_measurement_optional_parameter_list_optional : empty
                                                                | if_data_measurement_optional_parameter_list"""
        p[0] = p[1]

    @staticmethod
    def p_kp_blob(p):
        """kp_blob : KP_BLOB"""
        p[0] = p[1]

    @staticmethod
    def p_pa_blob(p):
        """pa_blob : PA_BLOB"""
        p[0] = p[1]

    @staticmethod
    def p_kp_data(p):
        """kp_data : kp_data_parameter_optional_list"""
        p[0] = p[1]

    @staticmethod
    def p_kp_data_parameter_optional(p):
        """kp_data_parameter_optional : NUMERIC
                                      | STRING
                                      | IDENT"""
        p[0] = p[1]

    @staticmethod
    def p_kp_data_parameter_optional_list(p):
        """kp_data_parameter_optional_list : kp_data_parameter_optional
                                           | kp_data_parameter_optional kp_data_parameter_optional_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]
        p[0] = p[1]

    @staticmethod
    def p_array_size(p):
        """array_size : ARRAY_SIZE NUMERIC"""
        p[0] = p[2]

    @staticmethod
    def p_bit_operation(p):
        """bit_operation : begin BIT_OPERATION bit_operation_optional_list_optional end BIT_OPERATION"""
        p[0] = p[1]

    @staticmethod
    def p_bit_operation_optional(p):
        """bit_operation_optional : left_shift
                                  | right_shift
                                  | SIGN_EXTEND"""
        p[0] = p[1]

    @staticmethod
    def p_left_shift(p):
        """left_shift : LEFT_SHIFT NUMERIC"""
        p[0] = p[1]

    @staticmethod
    def p_right_shift(p):
        """right_shift : RIGHT_SHIFT NUMERIC"""
        p[0] = p[1]

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
        p[0] = p[1]

    @staticmethod
    def p_compu_method_conversion_type(p):
        """compu_method_conversion_type : TAB_INTP
                             | TAB_NOINTP
                             | TAB_VERB
                             | RAT_FUNC
                             | FORM
                             | IDENTICAL
                             | LINEAR"""
        p[0] = p[1]

    @staticmethod
    def p_compu_method_optional(p):
        """compu_method_optional : formula
                                 | coeffs
                                 | coeffs_linear
                                 | compu_tab_ref
                                 | ref_unit"""
        p[0] = p[1]

    @staticmethod
    def p_formula(p):
        """formula : begin FORMULA STRING formula_optional end FORMULA"""
        p[0] = p[1]

    @staticmethod
    def p_formula_inv(p):
        """formula_inv : FORMULA_INV STRING"""
        p[0] = p[1]

    @staticmethod
    def p_formula_optional(p):
        """formula_optional : empty
                            | formula_inv"""
        p[0] = p[1]

    @staticmethod
    def p_coeffs(p):
        """coeffs : COEFFS NUMERIC NUMERIC NUMERIC NUMERIC NUMERIC NUMERIC"""
        p[0] = (p[2], p[3], p[4], p[5], p[6], p[7])

    @staticmethod
    def p_coeffs_linear(p):
        """coeffs_linear : COEFFS_LINEAR NUMERIC NUMERIC"""
        p[0] = p[1]

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
        p[0] = p[1]

    @staticmethod
    def p_compu_tab_conversion_type(p):
        """compu_tab_conversion_type : TAB_INTP
                                     | TAB_NOINTP"""
        p[0] = p[1]

    @staticmethod
    def p_compu_tab_optional(p):
        """compu_tab_optional : empty
                              | default_value
                              | default_value_numeric"""
        p[0] = p[1]

    @staticmethod
    def p_default_value(p):
        """default_value : DEFAULT_VALUE STRING"""
        p[0] = p[1]

    @staticmethod
    def p_default_value_numeric(p):
        """default_value_numeric : DEFAULT_VALUE_NUMERIC NUMERIC"""
        p[0] = p[1]

    @staticmethod
    def p_compu_vtab(p):
        """compu_vtab : begin COMPU_VTAB IDENT STRING compu_vtab_conversion_type NUMERIC number_string_value_list compu_vtab_optional end COMPU_VTAB"""
        p[0] = p[1]

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
        p[0] = p[1]

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
        p[0] = p[1]

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
        p[0] = p[1]

    @staticmethod
    def p_def_characteristic(p):
        """def_characteristic : begin DEF_CHARACTERISTIC ident_list end DEF_CHARACTERISTIC"""
        p[0] = p[1]

    @staticmethod
    def p_ref_characteristic(p):
        """ref_characteristic : begin REF_CHARACTERISTIC ref_characteristic_optional_list_optional end REF_CHARACTERISTIC"""
        p[0] = p[1]

    @staticmethod
    def p_ref_characteristic_optional(p):
        """ref_characteristic_optional : IDENT"""
        p[0] = p[1]

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
        p[0] = p[1]

    @staticmethod
    def p_in_measurement(p):
        """in_measurement : begin IN_MEASUREMENT ident_list end IN_MEASUREMENT"""
        p[0] = p[1]

    @staticmethod
    def p_out_measurement(p):
        """out_measurement : begin OUT_MEASUREMENT ident_list end OUT_MEASUREMENT"""
        p[0] = p[1]

    @staticmethod
    def p_loc_measurement(p):
        """loc_measurement : begin LOC_MEASUREMENT ident_list end LOC_MEASUREMENT"""
        p[0] = p[1]

    @staticmethod
    def p_sub_function(p):
        """sub_function : begin SUB_FUNCTION ident_list end SUB_FUNCTION"""
        p[0] = p[1]

    @staticmethod
    def p_function_version(p):
        """function_version : FUNCTION_VERSION STRING"""
        p[0] = p[1]

    @staticmethod
    def p_group(p):
        """group : begin GROUP IDENT STRING group_optional_list_optional end GROUP"""
        p[0] = p[1]

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
        """ref_measurement : begin REF_MEASUREMENT ref_measurement_optional_list_optional end REF_MEASUREMENT"""
        p[0] = p[3]

    @staticmethod
    def p_ref_measurement_optional(p):
        """ref_measurement_optional : IDENT"""
        p[0] = p[1]

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
        p[0] = p[1]

    @staticmethod
    def p_sub_group(p):
        """sub_group : begin SUB_GROUP ident_list end SUB_GROUP"""
        p[0] = p[3]

    @staticmethod
    def p_record_layout(p):
        """record_layout : begin RECORD_LAYOUT IDENT record_layout_optional_list_optional end RECORD_LAYOUT"""
        p[0] = p[1]

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
        p[0] = p[1]

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
        p[0] = a2l_node_factory(*p[1:4])

    @staticmethod
    def p_axis_pts_x(p):
        """axis_pts_x : AXIS_PTS_X NUMERIC datatype indexorder addrtype"""
        p[0] = p[1]

    @staticmethod
    def p_axis_pts_y(p):
        """axis_pts_y : AXIS_PTS_Y NUMERIC datatype indexorder addrtype"""
        p[0] = p[1]

    @staticmethod
    def p_axis_pts_z(p):
        """axis_pts_z : AXIS_PTS_Z NUMERIC datatype indexorder addrtype"""
        p[0] = p[1]

    @staticmethod
    def p_axis_rescale_x(p):
        """axis_rescale_x : AXIS_RESCALE_X NUMERIC datatype NUMERIC indexorder addrtype"""
        p[0] = p[1]

    @staticmethod
    def p_axis_rescale_y(p):
        """axis_rescale_y : AXIS_RESCALE_Y NUMERIC datatype NUMERIC indexorder addrtype"""
        p[0] = p[1]

    @staticmethod
    def p_axis_rescale_z(p):
        """axis_rescale_z : AXIS_RESCALE_Z NUMERIC datatype NUMERIC indexorder addrtype"""
        p[0] = p[1]

    @staticmethod
    def p_no_axis_pts_x(p):
        """no_axis_pts_x : NO_AXIS_PTS_X NUMERIC datatype"""
        p[0] = p[1]

    @staticmethod
    def p_no_axis_pts_y(p):
        """no_axis_pts_y : NO_AXIS_PTS_Y NUMERIC datatype"""
        p[0] = p[1]

    @staticmethod
    def p_no_axis_pts_z(p):
        """no_axis_pts_z : NO_AXIS_PTS_Z NUMERIC datatype"""
        p[0] = p[1]

    @staticmethod
    def p_no_rescale_x(p):
        """no_rescale_x : NO_RESCALE_X NUMERIC datatype"""
        p[0] = p[1]

    @staticmethod
    def p_no_rescale_y(p):
        """no_rescale_y : NO_RESCALE_Y NUMERIC datatype"""
        p[0] = p[1]

    @staticmethod
    def p_no_rescale_z(p):
        """no_rescale_z : NO_RESCALE_Z NUMERIC datatype"""
        p[0] = p[1]

    @staticmethod
    def p_fix_no_axis_pts_x(p):
        """fix_no_axis_pts_x : FIX_NO_AXIS_PTS_X NUMERIC"""
        p[0] = p[1]

    @staticmethod
    def p_fix_no_axis_pts_y(p):
        """fix_no_axis_pts_y : FIX_NO_AXIS_PTS_Y NUMERIC"""
        p[0] = p[1]

    @staticmethod
    def p_fix_no_axis_pts_z(p):
        """fix_no_axis_pts_z : FIX_NO_AXIS_PTS_Z NUMERIC"""
        p[0] = p[1]

    @staticmethod
    def p_src_addr_x(p):
        """src_addr_x : SRC_ADDR_X NUMERIC src_addr_optional"""
        p[0] = p[1]

    @staticmethod
    def p_src_addr_y(p):
        """src_addr_y : SRC_ADDR_Y NUMERIC src_addr_optional"""
        p[0] = p[1]

    @staticmethod
    def p_src_addr_z(p):
        """src_addr_z : SRC_ADDR_Z NUMERIC src_addr_optional"""
        p[0] = p[1]

    @staticmethod
    def p_src_addr_optional(p):
        """src_addr_optional : empty
                             | datatype"""
        p[0] = p[1]

    @staticmethod
    def p_rip_addr_x(p):
        """rip_addr_x : RIP_ADDR_X NUMERIC datatype"""
        p[0] = p[1]

    @staticmethod
    def p_rip_addr_y(p):
        """rip_addr_y : RIP_ADDR_Y NUMERIC datatype"""
        p[0] = p[1]

    @staticmethod
    def p_rip_addr_z(p):
        """rip_addr_z : RIP_ADDR_Z NUMERIC datatype"""
        p[0] = p[1]

    @staticmethod
    def p_rip_addr_w(p):
        """rip_addr_w : RIP_ADDR_W NUMERIC datatype"""
        p[0] = p[1]

    @staticmethod
    def p_shift_op_x(p):
        """shift_op_x : SHIFT_OP_X NUMERIC datatype"""
        p[0] = p[1]

    @staticmethod
    def p_shift_op_y(p):
        """shift_op_y : SHIFT_OP_Y NUMERIC datatype"""
        p[0] = p[1]

    @staticmethod
    def p_shift_op_z(p):
        """shift_op_z : SHIFT_OP_Z NUMERIC datatype"""
        p[0] = p[1]

    @staticmethod
    def p_offset_x(p):
        """offset_x : OFFSET_X NUMERIC datatype"""
        p[0] = p[1]

    @staticmethod
    def p_offset_y(p):
        """offset_y : OFFSET_Y NUMERIC datatype"""
        p[0] = p[1]

    @staticmethod
    def p_offset_z(p):
        """offset_z : OFFSET_Z NUMERIC datatype"""
        p[0] = p[1]

    @staticmethod
    def p_dist_op_x(p):
        """dist_op_x : DIST_OP_X NUMERIC datatype"""
        p[0] = p[1]

    @staticmethod
    def p_dist_op_y(p):
        """dist_op_y : DIST_OP_Y NUMERIC datatype"""
        p[0] = p[1]

    @staticmethod
    def p_dist_op_z(p):
        """dist_op_z : DIST_OP_Z NUMERIC datatype"""
        p[0] = p[1]

    @staticmethod
    def p_alignment_byte(p):
        """alignment_byte : ALIGNMENT_BYTE NUMERIC"""
        p[0] = p[1]

    @staticmethod
    def p_alignment_word(p):
        """alignment_word : ALIGNMENT_WORD NUMERIC"""
        p[0] = p[1]

    @staticmethod
    def p_alignment_long(p):
        """alignment_long : ALIGNMENT_LONG NUMERIC"""
        p[0] = p[1]

    @staticmethod
    def p_alignment_float32_ieee(p):
        """alignment_float32_ieee : ALIGNMENT_FLOAT32_IEEE NUMERIC"""
        p[0] = p[1]

    @staticmethod
    def p_alignment_float64_ieee(p):
        """alignment_float64_ieee : ALIGNMENT_FLOAT64_IEEE NUMERIC"""
        p[0] = p[1]

    @staticmethod
    def p_variant_coding(p):
        """variant_coding : begin VARIANT_CODING variant_coding_optional_list_optional end VARIANT_CODING"""
        p[0] = p[1]

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
        p[0] = p[1]

    @staticmethod
    def p_var_characteristic_optional(p):
        """var_characteristic_optional : var_address"""
        p[0] = p[1]

    @staticmethod
    def p_var_address(p):
        """var_address : begin VAR_ADDRESS number_list end VAR_ADDRESS"""
        p[0] = p[1]

    @staticmethod
    def p_var_separator(p):
        """var_separator : VAR_SEPARATOR STRING"""
        p[0] = p[1]

    @staticmethod
    def p_var_naming(p):
        """var_naming : VAR_NAMING IDENT"""
        p[0] = p[1]

    @staticmethod
    def p_var_forbidden_comb(p):
        """var_forbidden_comb : begin VAR_FORBIDDEN_COMB ident_ident_value_list end VAR_FORBIDDEN_COMB"""
        p[0] = p[1]

    @staticmethod
    def p_ident_ident_value_list(p):
        """ident_ident_value_list : ident_ident_value
                                  | ident_ident_value ident_ident_value_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_ident_ident_value(p):
        """ident_ident_value : IDENT IDENT"""
        p[0] = (p[1], p[2])

    @staticmethod
    def p_var_criterion(p):
        """var_criterion : begin VAR_CRITERION IDENT STRING ident_list var_criterion_optional_list_optional end VAR_CRITERION"""
        p[0] = a2l_node_factory(*p[2:7])

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
        """var_measurement : VAR_MEASUREMENT IDENT"""
        p[0] = p[1]

    @staticmethod
    def p_var_selection_characteristic(p):
        """var_selection_characteristic : VAR_SELECTION_CHARACTERISTIC IDENT"""
        p[0] = p[1]

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
        p[0] = p[1]

    @staticmethod
    def p_frame(p):
        """frame : begin FRAME IDENT STRING NUMERIC NUMERIC frame_optional_list_optional end FRAME"""
        p[0] = a2l_node_factory(*p[2:8])

    @staticmethod
    def p_frame_optional(p):
        """frame_optional : frame_measurement
                          | if_data_frame"""
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
    def p_if_data_frame(p):
        """if_data_frame : begin IF_DATA IDENT if_data_frame_parameter_optional_list_optional end IF_DATA"""
        p[0] = p[1]

    @staticmethod
    def p_if_data_frame_parameter_optional(p):
        """if_data_frame_parameter_optional : QP_BLOB qp_data"""
        p[0] = p[1]

    @staticmethod
    def p_if_data_frame_parameter_optional_list(p):
        """if_data_frame_parameter_optional_list : if_data_frame_parameter_optional
                                                 | if_data_frame_parameter_optional if_data_frame_parameter_optional_list"""

        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_if_data_frame_parameter_optional_list_optional(p):
        """if_data_frame_parameter_optional_list_optional : empty
                                                          | if_data_frame_parameter_optional_list"""
        p[0] = p[1]

    @staticmethod
    def p_qp_data(p):
        """qp_data : generic_parameter"""
        p[0] = p[1]

    @staticmethod
    def p_frame_measurement(p):
        """frame_measurement : FRAME_MEASUREMENT ident_list"""
        p[0] = p[1]

    @staticmethod
    def p_user_rights(p):
        """user_rights : begin USER_RIGHTS IDENT user_rights_optional_list_optional end USER_RIGHTS"""
        p[0] = a2l_node_factory(*p[2:5])

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
        """ref_group : begin REF_GROUP ref_group_ident_list end REF_GROUP"""
        p[0] = a2l_node_factory(*p[2:4])

    @staticmethod
    def p_ref_group_ident(p):
        """ref_group_ident : IDENT"""
        p[0] = p[1]

    @staticmethod
    def p_ref_group_ident_list(p):
        """ref_group_ident_list : ref_group_ident
                                | ref_group_ident ref_group_ident_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_read_only(p):
        """read_only : READ_ONLY"""
        p[0] = p[1]

    @staticmethod
    def p_unit(p):
        """unit : begin UNIT IDENT STRING STRING unit_type unit_optional_list_optional end UNIT"""
        p[0] = a2l_node_factory(*p[2:8])

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
        """si_exponents : SI_EXPONENTS NUMERIC NUMERIC NUMERIC NUMERIC NUMERIC NUMERIC NUMERIC"""
        p[0] = a2l_node_factory(*p[1:9])

    @staticmethod
    def p_unit_conversion(p):
        """unit_conversion : UNIT_CONVERSION NUMERIC NUMERIC"""
        p[0] = a2l_node_factory(*p[1:4])

    @staticmethod
    def p_empty(p):
        """empty :"""
        p[0] = None
