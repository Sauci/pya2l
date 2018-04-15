"""
@project: parser
@file: node.py
@author: Guillaume Sottas
@date: 05.04.2018
"""


class A2lNode(object):
    def __init__(self, node, *args, **kwargs):
        self._parent = None
        self._children = list()
        for attribute, value in args:
            attr = getattr(self, attribute)
            if isinstance(attr, list):
                attr.append(value)
            elif attr is None:
                setattr(self, attribute, value)
            else:
                print attr
                raise ValueError
            if isinstance(value, A2lNode):
                value.set_parent(self)
                self.add_children(value)
        self._node = node

    def set_parent(self, a2l_node):
        self._parent = a2l_node

    def add_children(self, a2l_node):
        self._children.append(a2l_node)

    def get_properties(self):
        return [p for p in self.__dict__.keys() if not p.startswith('_')]


class Version(A2lNode):
    def __init__(self, node, version_no, upgrade_no):
        self.version_no = version_no
        self.upgrade_no = upgrade_no
        super(Version, self).__init__(node)


class A2lFile(A2lNode):
    def __init__(self, node, args):
        self.asap2_version = None
        self.a2ml_version = None
        self.project = None
        super(A2lFile, self).__init__(node, *args)


class A2MLVersion(Version):
    pass


class AddressMapping(A2lNode):
    def __init__(self, node, orig_address, mapping_address, length):
        self.orig_address = orig_address
        self.mapping_address = mapping_address
        self.length = length
        super(AddressMapping, self).__init__(node)


class Annotation(A2lNode):
    def __init__(self, node, args):
        self.annotation_label = None
        self.annotation_origin = None
        self.annotation_text = None
        super(Annotation, self).__init__(node, *args)


class AnnotationText(A2lNode):
    def __init__(self, node, args):
        self.annotation_text = list()
        super(AnnotationText, self).__init__(node, *args)


class ASAP2Version(Version):
    pass


class AxisDescr(A2lNode):
    def __init__(self, node, attribute, input_quantity, conversion, max_axis_points, lower_limit, upper_limit, args):
        self.attribute = attribute
        self.input_quantity = input_quantity
        self.conversion = conversion
        self.max_axis_points = max_axis_points
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.read_only = None
        self.format = None
        self.annotation = list()
        self.axis_pts_ref = None
        self.max_grad = None
        self.monotony = None
        self.byte_order = None
        self.extended_limits = None
        self.fix_axis_par = None
        self.fix_axis_par_dist = None
        self.fix_axis_par_list = None
        self.deposit = None
        self.curve_axis_ref = None
        super(AxisDescr, self).__init__(node, *args)


class AxisPts(A2lNode):
    def __init__(self, node, name, long_identifier, address, input_quantity, deposit, max_diff, conversion,
                 max_axis_points, lower_limit, upper_limit, args):
        self.name = name
        self.long_identifier = long_identifier
        self.address = address
        self.input_quantity = input_quantity
        self.deposit = deposit
        self.max_diff = max_diff
        self.conversion = conversion
        self.max_axis_points = max_axis_points
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.display_identifier = None
        self.read_only = None
        self.format = None
        self.deposit = None
        self.byte_order = None
        self.function_list = None
        self.ref_memory_segment = None
        self.guard_rails = None
        self.extended_limits = None
        self.annotation = list()
        self.if_data_axis_pts = list()
        self.calibration_access = None
        self.ecu_address_extension = None
        try:
            super(AxisPts, self).__init__(node, *args)
        except ValueError as e:
            print e
            raise e


class AxisPtsXYZ(A2lNode):
    def __init__(self, node, position, datatype, indexorder, addrtype):
        self.position = position
        self.datatype = datatype
        self.indexorder = indexorder
        self.addrtype = addrtype
        super(AxisPtsXYZ, self).__init__(node)


class AxisPtsX(AxisPtsXYZ):
    pass


class AxisPtsY(AxisPtsXYZ):
    pass


class AxisPtsZ(AxisPtsXYZ):
    pass


class AxisRescale(A2lNode):
    def __init__(self, node, position, datatype, max_number_of_rescale_pairs, index_incr, addressing):
        self.position = position
        self.datatype = datatype
        self.max_number_of_rescale_pairs = max_number_of_rescale_pairs
        self.index_incr = index_incr
        self.addressing = addressing
        super(AxisRescale, self).__init__(node)


class AxisRescaleX(AxisRescale):
    pass


class AxisRescaleY(AxisRescale):
    pass


class AxisRescaleZ(AxisRescale):
    pass


class BitOperation(A2lNode):
    def __init__(self, node, args):
        self.left_shift = None
        self.right_shift = None
        self.sign_extend = None
        super(BitOperation, self).__init__(node, *args)


class CalibrationMethod(A2lNode):
    def __init__(self, node, method, version, args):
        self.method = method
        self.version = version
        self.calibration_handle = list()
        super(CalibrationMethod, self).__init__(node, *args)


class Characteristic(A2lNode):
    def __init__(self, node, name, long_identifier, type, address, deposit, max_diff, conversion, lower_limit,
                 upper_limit, args):
        self.name = name
        self.long_identifier = long_identifier
        self.type = type
        self.address = address
        self.deposit = deposit
        self.max_diff = max_diff
        self.conversion = conversion
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.display_identifier = None
        self.format = None
        self.byte_order = None
        self.bit_mask = None
        self.function_list = None
        self.number = None
        self.extended_limits = None
        self.read_only = None
        self.guard_rails = None
        self.map_list = None
        self.max_refresh = None
        self.dependent_characteristic = None
        self.virtual_characteristic = None
        self.ref_memory_segment = None
        self.annotation = list()
        self.comparison_quantity = None
        self.if_data_characteristic = list()
        self.axis_descr = list()
        self.calibration_access = None
        self.matrix_dim = None
        self.ecu_address_extension = None
        super(Characteristic, self).__init__(node, *args)


class Checksum(A2lNode):
    def __init__(self, node, checksum_dll, max_block_size):
        self.checksum_dll = checksum_dll
        self.max_block_size = max_block_size
        super(Checksum, self).__init__(node)


class Coeffs(A2lNode):
    def __init__(self, node, a, b, c, d, e, f):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        super(Coeffs, self).__init__(node)


class CompuMethod(A2lNode):
    def __init__(self, node, name, long_identifier, conversion_type, format, unit, args):
        self.name = name
        self.long_identifier = long_identifier
        self.conversion_type = conversion_type
        self.format = format
        self.unit = unit
        self.formula = None
        self.coeffs = None
        self.coeffs_linear = None  # TODO: should be removed, according to 1.51.
        self.compu_tab_ref = None
        self.ref_unit = None
        super(CompuMethod, self).__init__(node, *args)


class CompuTab(A2lNode):
    def __init__(self, node, name, long_identifier, conversion_type, number_value_pairs, args):
        self.name = name
        self.long_identifier = long_identifier
        self.conversion_type = conversion_type
        self.number_value_pairs = number_value_pairs
        self.in_val_out_val = None
        self.default_value = None
        self.default_value_numeric = None  # TODO: should be removed, according to 1.51.
        super(CompuTab, self).__init__(node, *args)


class CompuVTab(A2lNode):
    def __init__(self, node, name, long_identifier, conversion_type, number_value_pairs, args):
        self.name = name
        self.long_identifier = long_identifier
        self.conversion_type = conversion_type
        self.number_value_pairs = number_value_pairs
        self.compu_vtab_in_val_out_val = None  # TODO: replace with in_val_out_val...
        self.default_value = None
        super(CompuVTab, self).__init__(node, *args)


class CompuVTabRange(A2lNode):
    def __init__(self, node, name, long_identifier, number_value_triples, args):
        self.name = name
        self.long_identifier = long_identifier
        self.number_value_triples = number_value_triples
        self.compu_vtab_range_in_val_out_val = None  # TODO: replace with in_val_min_in_val_max_out_val...
        self.default_value = None
        super(CompuVTabRange, self).__init__(node, *args)


class DefCharacteristic(A2lNode):
    def __init__(self, node, args):
        self.identifier = list()
        super(DefCharacteristic, self).__init__(node, *args)


class DependentCharacteristic(A2lNode):
    def __init__(self, node, formula, args):
        self.formula = formula
        self.characteristic = list()
        super(DependentCharacteristic, self).__init__(node, *args)


class DistOp(A2lNode):
    def __init__(self, node, position, datatype):
        self.position = position
        self.datatype = datatype
        super(DistOp, self).__init__(node)


class DistOpX(DistOp):
    pass


class DistOpY(DistOp):
    pass


class DistOpZ(DistOp):
    pass


class EventGroup(A2lNode):
    def __init__(self, node, raster_grp_name, short_name, raster_id):
        self.raster_grp_name = raster_grp_name
        self.short_name = short_name
        self.raster_id = raster_id
        super(EventGroup, self).__init__(node)


class FixAxisPar(A2lNode):
    def __init__(self, node, offset, shift, numberapo):
        self.offset = offset
        self.shift = shift
        self.numberapo = numberapo
        super(FixAxisPar, self).__init__(node)


class FixAxisParList(FixAxisPar):
    pass


class FixNoAxisPts(A2lNode):
    def __init__(self, node, number_of_axis_points):
        self.number_of_axis_points = number_of_axis_points
        super(FixNoAxisPts, self).__init__(node)


class FixNoAxisPtsX(FixNoAxisPts):
    pass


class FixNoAxisPtsY(FixNoAxisPts):
    pass


class FixNoAxisPtsZ(FixNoAxisPts):
    pass


class Formula(A2lNode):
    def __init__(self, node, f, args):
        self.f = f
        self.formula_inv = None
        super(Formula, self).__init__(node, *args)


class Frame(A2lNode):
    def __init__(self, node, name, long_identifier, scaling_unit, rate, args):
        self.name = name
        self.long_identifier = long_identifier
        self.scaling_unit = scaling_unit
        self.rate = rate
        self.frame_measurement = None
        self.frame_if_data = list()
        super(Frame, self).__init__(node, *args)


class Function(A2lNode):
    def __init__(self, node, name, long_identifier, args):
        self.name = name
        self.long_identifier = long_identifier
        self.annotation = list()
        self.def_characteristic = None
        self.ref_characteristic = None
        self.in_measurement = None
        self.out_measurement = None
        self.loc_measurement = None
        self.sub_function = None
        self.function_version = None
        super(Function, self).__init__(node, *args)


class FunctionList(A2lNode):
    def __init__(self, node, args):
        self.name = list()
        super(FunctionList, self).__init__(node, *args)


class Group(A2lNode):
    def __init__(self, node, group_name, group_long_identifier, args):
        self.group_name = group_name
        self.group_long_identifier = group_long_identifier
        self.annotation = list()
        self.root = None
        self.ref_characteristic = None
        self.ref_measurement = None
        self.function_list = None
        self.sub_group = None
        super(Group, self).__init__(node, *args)


class Header(A2lNode):
    def __init__(self, node, comment, args):
        self.comment = comment
        self.version = None
        self.project_no = None
        super(Header, self).__init__(node, *args)


class Identification(A2lNode):
    def __init__(self, node, position, datatype):
        self.position = position
        self.datatype = datatype
        super(Identification, self).__init__(node)


class IfDataMemorySegment(A2lNode):
    def __init__(self, node, name, args):
        self.name = name
        self.address_mapping = list()
        self.segment = list()
        super(IfDataMemorySegment, self).__init__(node, *args)


class InMeasurement(A2lNode):
    def __init__(self, node, args):
        self.identifier = list()
        super(InMeasurement, self).__init__(node, *args)


class LocMeasurement(A2lNode):
    def __init__(self, node, args):
        self.identifier = list()
        super(LocMeasurement, self).__init__(node, *args)


class MaxRefresh(A2lNode):
    def __init__(self, node, scaling_unit, rate):
        self.scaling_unit = scaling_unit
        self.rate = rate
        super(MaxRefresh, self).__init__(node)


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


class MemoryLayout(A2lNode):
    def __init__(self, node, prg_type, address, size, offset, args):
        self.prg_type = prg_type
        self.address = address
        self.size = size
        self.offset = offset
        self.if_data_memory_layout = list()
        super(MemoryLayout, self).__init__(node, *args)


class MemorySegment(A2lNode):
    def __init__(self, node, name, long_identifier, prg_type, memory_type, attribute, address, size, offset, args):
        self.name = name
        self.long_identifier = long_identifier
        self.prg_type = prg_type
        self.memory_type = memory_type
        self.attribute = attribute
        self.address = address
        self.size = size
        self.offset = offset
        self.if_data_memory_segment = list()
        super(MemorySegment, self).__init__(node, *args)


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


class ModCommon(A2lNode):
    def __init__(self, node, comment, args):
        self.comment = comment
        self.s_rec_layout = None
        self.deposit = None
        self.byte_order = None
        self.data_size = None
        self.alignment_byte = None
        self.alignment_word = None
        self.alignment_long = None
        self.alignment_float32_ieee = None
        self.alignment_float64_ieee = None
        super(ModCommon, self).__init__(node, *args)


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


class NoAxisPts(A2lNode):
    def __init__(self, node, position, datatype):
        self.position = position
        self.datatype = datatype
        super(NoAxisPts, self).__init__(node)


class NoAxisPtsX(NoAxisPts):
    pass


class NoAxisPtsY(NoAxisPts):
    pass


class NoAxisPtsZ(NoAxisPts):
    pass


class NoRescale(A2lNode):
    def __init__(self, node, position, datatype):
        self.position = position
        self.datatype = datatype
        super(NoRescale, self).__init__(node)


class NoRescaleX(NoRescale):
    pass


class NoRescaleY(NoRescale):
    pass


class NoRescaleZ(NoRescale):
    pass


class Offset(A2lNode):
    def __init__(self, node, position, datatype):
        self.position = position
        self.datatype = datatype
        super(Offset, self).__init__(node)


class OffsetX(Offset):
    pass


class OffsetY(Offset):
    pass


class OffsetZ(Offset):
    pass


class OutMeasurement(A2lNode):
    def __init__(self, node, args):
        self.identifier = list()
        super(OutMeasurement, self).__init__(node, *args)


class Project(A2lNode):
    def __init__(self, node, name, long_identifier, args):
        self.name = name
        self.long_identifier = long_identifier
        self.header = None
        self.module = list()
        super(Project, self).__init__(node, *args)


class Raster(A2lNode):
    def __init__(self, node, raster_name, short_name, raster_id, scaling_unit, rate):
        self.raster_name = raster_name
        self.short_name = short_name
        self.raster_id = raster_id
        self.scaling_unit = scaling_unit
        self.rate = rate
        super(Raster, self).__init__(node)


class RecordLayout(A2lNode):
    def __init__(self, node, name, args):
        self.name = name
        self.fnc_values = None
        self.identification = None
        self.axis_pts_x = None
        self.axis_pts_y = None
        self.axis_pts_z = None
        self.axis_rescale_x = None
        self.axis_rescale_y = None
        self.axis_rescale_z = None
        self.no_axis_pts_x = None
        self.no_axis_pts_y = None
        self.no_axis_pts_z = None
        self.no_rescale_x = None
        self.no_rescale_y = None
        self.no_rescale_z = None
        self.fix_no_axis_pts_x = None
        self.fix_no_axis_pts_y = None
        self.fix_no_axis_pts_z = None
        self.src_addr_x = None
        self.src_addr_y = None
        self.src_addr_z = None
        self.rip_addr_x = None
        self.rip_addr_y = None
        self.rip_addr_z = None
        self.rip_addr_w = None
        self.shift_op_x = None
        self.shift_op_y = None
        self.shift_op_z = None
        self.offset_x = None
        self.offset_y = None
        self.offset_z = None
        self.dist_op_x = None
        self.dist_op_y = None
        self.dist_op_z = None
        self.alignment_byte = None
        self.alignment_word = None
        self.alignment_long = None
        self.alignment_float32_ieee = None
        self.alignment_float64_ieee = None
        self.reserved = list()
        super(RecordLayout, self).__init__(node, *args)


class RefCharacteristic(A2lNode):
    def __init__(self, node, args):
        self.identifier = list()
        super(RefCharacteristic, self).__init__(node, *args)


class RefGroup(A2lNode):
    def __init__(self, node, identifier):
        self.identifier = identifier
        super(RefGroup, self).__init__(node)


class RefMeasurement(A2lNode):
    def __init__(self, node, args):
        self.identifier = list()
        super(RefMeasurement, self).__init__(node, *args)


class RipAddr(A2lNode):
    def __init__(self, node, position, datatype):
        self.position = position
        self.datatype = datatype
        super(RipAddr, self).__init__(node)


class RipAddrX(RipAddr):
    pass


class RipAddrY(RipAddr):
    pass


class RipAddrZ(RipAddr):
    pass


class RipAddrW(RipAddr):
    pass


class SeedKey(A2lNode):
    def __init__(self, node, cal_dll, daq_dll, pgm_dll):
        self.cal_dll = cal_dll
        self.daq_dll = daq_dll
        self.pgm_dll = pgm_dll
        super(SeedKey, self).__init__(node)


class ShiftOp(A2lNode):
    def __init__(self, node, position, datatype):
        self.position = position
        self.datatype = datatype
        super(ShiftOp, self).__init__(node)


class ShiftOpX(ShiftOp):
    pass


class ShiftOpY(ShiftOp):
    pass


class ShiftOpZ(ShiftOp):
    pass


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


class Source(A2lNode):
    def __init__(self, node, name, scaling_unit, rate, args):
        self.name = name
        self.scaling_unit = scaling_unit
        self.rate = rate
        self.display_identifier = None
        self.qp_blob = None
        self.qp_data = None
        super(Source, self).__init__(node, *args)


class SrcAddr(A2lNode):
    def __init__(self, node, position, datatype):
        self.position = position
        self.datatype = datatype
        super(SrcAddr, self).__init__(node)


class SrcAddrX(SrcAddr):
    pass


class SrcAddrY(SrcAddr):
    pass


class SrcAddrZ(SrcAddr):
    pass


class SubFunction(A2lNode):
    def __init__(self, node, args):
        self.identifier = list()
        super(SubFunction, self).__init__(node, *args)


class SubGroup(A2lNode):
    def __init__(self, node, args):
        self.identifier = list()
        super(SubGroup, self).__init__(node, *args)


class SystemConstant(A2lNode):
    def __init__(self, node, name, value):
        self.name = name
        self.value = value
        super(SystemConstant, self).__init__(node)


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


class UnitConversion(A2lNode):
    def __init__(self, node, gradient, offset):
        self.gradient = gradient
        self.offset = offset
        super(UnitConversion, self).__init__(node)


class UserRights(A2lNode):
    def __init__(self, node, user_level_id, args):
        self.user_level_id = user_level_id
        self.read_only = None
        self.ref_group = list()
        super(UserRights, self).__init__(node, *args)


class VariantCoding(A2lNode):
    def __init__(self, node, args):
        self.var_separator = None
        self.var_naming = None
        self.var_criterion = list()
        self.var_forbidden_comb = list()
        self.var_characteristic = list()
        super(VariantCoding, self).__init__(node, *args)


class VarCharacteristic(A2lNode):
    def __init__(self, node, name, criterion_name, args):
        self.name = name
        self.criterion_name = criterion_name
        self.var_address = None
        super(VarCharacteristic, self).__init__(node, args)


class VarCriterion(A2lNode):
    def __init__(self, node, name, long_identifier, value, args):
        self.name = name
        self.long_identifier = long_identifier
        self.value = value
        self.var_measurement = None
        self.var_selection_characteristic = None
        super(VarCriterion, self).__init__(node, *args)


class VarForbiddenComb(A2lNode):
    def __init__(self, node, *args):
        self.criterion_name = list()
        self.criterion_value = list()
        super(VarForbiddenComb, self).__init__(node, *args)


class VirtualCharacteristic(A2lNode):
    def __init__(self, node, formula, args):
        self.formula = formula
        self.characteristic = list()
        super(VirtualCharacteristic, self).__init__(node, *args)
