"""
@project: parser
@file: node.py
@author: Guillaume Sottas
@date: 05.04.2018
"""


class A2lNode(object):
    __slots__ = '_node', '_parent', '_children'

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
                raise AttributeError(attribute)
            if isinstance(value, A2lNode):
                value.set_parent(self)
                self.add_children(value)
        self._node = node

    def set_parent(self, a2l_node):
        self._parent = a2l_node

    def add_children(self, a2l_node):
        self._children.append(a2l_node)

    def get_properties(self):
        return [p for p in self.__slots__ if not p.startswith('_')]

    def node(self):
        return self._node

    def get_node(self, node_name):
        nodes = list()
        for node in self._children:
            if node._node == node_name:
                nodes.append(node)
            nodes += node.get_node(node_name)
        return nodes


class Version(A2lNode):
    __slots__ = 'version_no', 'upgrade_no'

    def __init__(self, node, version_no, upgrade_no):
        self.version_no = version_no
        self.upgrade_no = upgrade_no
        super(Version, self).__init__(node)


class A2lFile(A2lNode):
    __slots__ = 'asap2_version', 'a2ml_version', 'project'

    def __init__(self, node, args):
        self.asap2_version = None
        self.a2ml_version = None
        self.project = None
        super(A2lFile, self).__init__(node, *args)


class Sector(A2lNode):
    __slots__ = 'name', 'sector_number', 'address', 'length', 'erase_number', 'program_number', 'programming_method'

    def __init__(self, node, name, sector_number, address, length, erase_number, program_number, programming_method):
        self.name = name
        self.sector_number = sector_number
        self.address = address
        self.length = length
        self.erase_number = erase_number
        self.program_number = program_number
        self.programming_method = programming_method
        super(Sector, self).__init__(node)


class A2MLVersion(Version):
    pass


class AddressMapping(A2lNode):
    __slots__ = 'orig_address', 'mapping_address', 'length'

    def __init__(self, node, orig_address, mapping_address, length):
        self.orig_address = orig_address
        self.mapping_address = mapping_address
        self.length = length
        super(AddressMapping, self).__init__(node)


class Annotation(A2lNode):
    __slots__ = 'annotation_label', 'annotation_origin', 'annotation_text'

    def __init__(self, node, args):
        self.annotation_label = None
        self.annotation_origin = None
        self.annotation_text = None
        super(Annotation, self).__init__(node, *args)


class AnnotationText(A2lNode):
    __slots__ = 'annotation_text'

    def __init__(self, node, args):
        self.annotation_text = list()
        super(AnnotationText, self).__init__(node, *args)


class ASAP2Version(Version):
    pass


class AvailableEventList(A2lNode):
    __slots__ = 'event'

    def __init__(self, node, args):
        self.event = list()
        super(AvailableEventList, self).__init__(node, *args)


class AxisDescr(A2lNode):
    __slots__ = 'attribute', 'input_quantity', 'conversion', 'max_axis_points', 'lower_limit', 'upper_limit', \
                'read_only', 'format', 'annotation', 'axis_pts_ref', 'max_grad', 'monotony', 'byte_order', \
                'extended_limits', 'fix_axis_par', 'fix_axis_par_dist', 'fix_axis_par_list', 'deposit', 'curve_axis_ref'

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
    __slots__ = 'name', 'long_identifier', 'address', 'input_quantity', 'deposit', 'max_diff', 'conversion', \
                'max_axis_points', 'lower_limit', 'upper_limit', 'display_identifier', 'read_only', 'format', \
                'deposit', 'byte_order', 'function_list', 'ref_memory_segment', 'guard_rails', 'extended_limits', \
                'annotation', 'if_data_axis_pts', 'calibration_access', 'ecu_address_extension'

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
        super(AxisPts, self).__init__(node, *args)


class AxisPtsXYZ(A2lNode):
    __slots__ = 'position', 'data_type', 'index_incr', 'addressing'

    def __init__(self, node, position, data_type, index_incr, addressing):
        self.position = position
        self.data_type = data_type
        self.index_incr = index_incr
        self.addressing = addressing
        super(AxisPtsXYZ, self).__init__(node)


class AxisPtsX(AxisPtsXYZ):
    pass


class AxisPtsY(AxisPtsXYZ):
    pass


class AxisPtsZ(AxisPtsXYZ):
    pass


class AxisRescale(A2lNode):
    __slots__ = 'position', 'data_type', 'max_number_of_rescale_pairs', 'index_incr', 'addressing'

    def __init__(self, node, position, data_type, max_number_of_rescale_pairs, index_incr, addressing):
        self.position = position
        self.data_type = data_type
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
    __slots__ = 'left_shift', 'right_shift', 'sign_extend'

    def __init__(self, node, args):
        self.left_shift = None
        self.right_shift = None
        self.sign_extend = None
        super(BitOperation, self).__init__(node, *args)


class CalibrationMethod(A2lNode):
    __slots__ = 'method', 'version', 'calibration_handle'

    def __init__(self, node, method, version, args):
        self.method = method
        self.version = version
        self.calibration_handle = list()
        super(CalibrationMethod, self).__init__(node, *args)


class Characteristic(A2lNode):
    __slots__ = 'name', 'long_identifier', 'type', 'address', 'deposit', 'max_diff', 'conversion', 'lower_limit', \
                'upper_limit', 'display_identifier', 'format', 'byte_order', 'bit_mask', 'function_list', 'number', \
                'extended_limits', 'read_only', 'guard_rails', 'map_list', 'max_refresh', 'dependent_characteristic', \
                'virtual_characteristic', 'ref_memory_segment', 'annotation', 'comparison_quantity', \
                'if_data_characteristic', 'axis_descr', 'calibration_access', 'matrix_dim', 'ecu_address_extension'

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
    __slots__ = 'checksum_dll', 'max_block_size'

    def __init__(self, node, checksum_dll, max_block_size):
        self.checksum_dll = checksum_dll
        self.max_block_size = max_block_size
        super(Checksum, self).__init__(node)


class Coeffs(A2lNode):
    __slots__ = 'a', 'b', 'c', 'd', 'e', 'f'

    def __init__(self, node, a, b, c, d, e, f):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        super(Coeffs, self).__init__(node)


class CompuMethod(A2lNode):
    __slots__ = 'name', 'long_identifier', 'conversion_type', 'format', 'unit', 'formula', 'coeffs', 'coeffs_linear', \
                'compu_tab_ref', 'ref_unit'

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
    __slots__ = 'name', 'long_identifier', 'conversion_type', 'number_value_pairs', 'in_val_out_val', 'default_value', \
                'default_value_numeric'

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
    __slots__ = 'name', 'long_identifier', 'conversion_type', 'number_value_pairs', 'compu_vtab_in_val_out_val', \
                'default_value'

    def __init__(self, node, name, long_identifier, conversion_type, number_value_pairs, args):
        self.name = name
        self.long_identifier = long_identifier
        self.conversion_type = conversion_type
        self.number_value_pairs = number_value_pairs
        self.compu_vtab_in_val_out_val = None  # TODO: replace with in_val_out_val...
        self.default_value = None
        super(CompuVTab, self).__init__(node, *args)


class CompuVTabRange(A2lNode):
    __slots__ = 'name', 'long_identifier', 'number_value_triples', 'compu_vtab_range_in_val_out_val', 'default_value'

    def __init__(self, node, name, long_identifier, number_value_triples, args):
        self.name = name
        self.long_identifier = long_identifier
        self.number_value_triples = number_value_triples
        self.compu_vtab_range_in_val_out_val = None  # TODO: replace with in_val_min_in_val_max_out_val...
        self.default_value = None
        super(CompuVTabRange, self).__init__(node, *args)


class Daq(A2lNode):
    __slots__ = 'daq_config_type', 'max_daq', 'max_event_channel', 'min_daq', 'optimisation_type', \
                'address_extension', 'identification_field_type', 'granularity_odt_entry', 'max_odt_entry_size_daq', \
                'overload_indication', 'prescaler_supported', 'resume_supported', 'daq_list', 'timestamp_supported', \
                'event', 'EVENT', 'IDENT', 'NUMERIC'

    def __init__(self,
                 node,
                 daq_config_type,
                 max_daq,
                 max_event_channel,
                 min_daq,
                 optimisation_type,
                 address_extension,
                 identification_field_type,
                 granularity_odt_entry,
                 max_odt_entry_size_daq,
                 overload_indication,
                 args):
        self.daq_config_type = daq_config_type
        self.max_daq = max_daq
        self.max_event_channel = max_event_channel
        self.min_daq = min_daq
        self.optimisation_type = optimisation_type
        self.address_extension = address_extension
        self.identification_field_type = identification_field_type
        self.granularity_odt_entry = granularity_odt_entry
        self.max_odt_entry_size_daq = max_odt_entry_size_daq
        self.overload_indication = overload_indication
        self.prescaler_supported = None
        self.resume_supported = None
        self.daq_list = list()
        self.timestamp_supported = list()
        self.event = list()
        self.EVENT = list()
        self.IDENT = list()
        self.NUMERIC = list()
        super(Daq, self).__init__(node, *args)


class DaqEvent(A2lNode):
    __slots__ = 'name', 'available_event_list', 'default_event_list'

    def __init__(self, node, name, args):
        self.name = name
        self.available_event_list = list()
        self.default_event_list = list()
        super(DaqEvent, self).__init__(node, *args)


class DaqList(A2lNode):
    __slots__ = 'daq_list_number', 'daq_list_type', 'max_odt', 'max_odt_entries', 'first_pid', 'event_fixed', \
                'predefined'

    def __init__(self, node, daq_list_number, args):
        self.daq_list_number = daq_list_number
        self.daq_list_type = None
        self.max_odt = None
        self.max_odt_entries = None
        self.first_pid = None
        self.event_fixed = None
        self.predefined = list()
        super(DaqList, self).__init__(node, *args)


class DaqListCanId(A2lNode):
    __slots__ = 'identifier', 'daq_list_can_id_type_fixed', 'daq_list_can_id_type_variable'

    def __init__(self, node, identifier, args):
        self.identifier = identifier
        self.daq_list_can_id_type_fixed = None
        self.daq_list_can_id_type_variable = None
        super(DaqListCanId, self).__init__(node, *args)


class DefaultEventList(A2lNode):
    __slots__ = 'event'

    def __init__(self, node, args):
        self.event = list()
        super(DefaultEventList, self).__init__(node, *args)


class DefCharacteristic(A2lNode):
    __slots__ = 'identifier'

    def __init__(self, node, args):
        self.identifier = list()
        super(DefCharacteristic, self).__init__(node, *args)


class DependentCharacteristic(A2lNode):
    __slots__ = 'formula', 'characteristic'

    def __init__(self, node, formula, args):
        self.formula = formula
        self.characteristic = list()
        super(DependentCharacteristic, self).__init__(node, *args)


class DistOp(A2lNode):
    __slots__ = 'position', 'data_type'

    def __init__(self, node, position, data_type):
        self.position = position
        self.data_type = data_type
        super(DistOp, self).__init__(node)


class DistOpX(DistOp):
    pass


class DistOpY(DistOp):
    pass


class DistOpZ(DistOp):
    pass


class Event(A2lNode):
    __slots__ = 'name', 'short_name', 'event_channel_number', 'daq_list_type', 'max_daq_list', 'time_cycle', \
                'time_unit', 'priority'

    def __init__(self, node, name, short_name, event_channel_number, daq_list_type, max_daq_list, time_cycle, time_unit,
                 priority):
        self.name = name
        self.short_name = short_name
        self.event_channel_number = event_channel_number
        self.daq_list_type = daq_list_type
        self.max_daq_list = max_daq_list
        self.time_cycle = time_cycle
        self.time_unit = time_unit
        self.priority = priority
        super(Event, self).__init__(node)


class EventGroup(A2lNode):
    __slots__ = 'raster_grp_name', 'short_name', 'raster_id'

    def __init__(self, node, raster_grp_name, short_name, raster_id):
        self.raster_grp_name = raster_grp_name
        self.short_name = short_name
        self.raster_id = raster_id
        super(EventGroup, self).__init__(node)


class FixAxisPar(A2lNode):
    __slots__ = 'offset', 'shift', 'numberapo'

    def __init__(self, node, offset, shift, numberapo):
        self.offset = offset
        self.shift = shift
        self.numberapo = numberapo
        super(FixAxisPar, self).__init__(node)


class FixAxisParList(FixAxisPar):
    __slots__ = 'offset', 'distance', 'numberapo'

    def __init__(self, node, offset, distance, numberapo):
        self.offset = offset
        self.distance = distance
        self.numberapo = numberapo
        super(FixAxisPar, self).__init__(node)


class FixNoAxisPts(A2lNode):
    __slots__ = 'number_of_axis_points'

    def __init__(self, node, number_of_axis_points):
        self.number_of_axis_points = number_of_axis_points
        super(FixNoAxisPts, self).__init__(node)


class FixNoAxisPtsX(FixNoAxisPts):
    pass


class FixNoAxisPtsY(FixNoAxisPts):
    pass


class FixNoAxisPtsZ(FixNoAxisPts):
    pass


class FncValues(A2lNode):
    __slots__ = 'position', 'data_type', 'index_mode', 'addresstype'

    def __init__(self, node, position, data_type, index_mode, addresstype):
        self.position = position
        self.data_type = data_type
        self.index_mode = index_mode
        self.addresstype = addresstype
        super(FncValues, self).__init__(node)


class Formula(A2lNode):
    __slots__ = 'f', 'formula_inv'

    def __init__(self, node, f, args):
        self.f = f
        self.formula_inv = None
        super(Formula, self).__init__(node, *args)


class Frame(A2lNode):
    __slots__ = 'name', 'long_identifier', 'scaling_unit', 'rate', 'frame_measurement', 'if_data_frame'

    def __init__(self, node, name, long_identifier, scaling_unit, rate, args):
        self.name = name
        self.long_identifier = long_identifier
        self.scaling_unit = scaling_unit
        self.rate = rate
        self.frame_measurement = None
        self.if_data_frame = list()
        super(Frame, self).__init__(node, *args)


class FrameMeasurement(A2lNode):
    __slots__ = 'identifier'

    def __init__(self, node, args):
        self.identifier = list()
        super(FrameMeasurement, self).__init__(node, *args)


class Function(A2lNode):
    __slots__ = 'name', 'long_identifier', 'annotation', 'def_characteristic', 'ref_characteristic', 'in_measurement', \
                'out_measurement', 'loc_measurement', 'sub_function', 'function_version'

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
    __slots__ = 'name'

    def __init__(self, node, args):
        self.name = list()
        super(FunctionList, self).__init__(node, *args)


class Group(A2lNode):
    __slots__ = 'group_name', 'group_long_identifier', 'annotation', 'root', 'ref_characteristic', 'ref_measurement', \
                'function_list', 'sub_group'

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
    __slots__ = 'comment', 'version', 'project_no'

    def __init__(self, node, comment, args):
        self.comment = comment
        self.version = None
        self.project_no = None
        super(Header, self).__init__(node, *args)


class Identification(A2lNode):
    __slots__ = 'position', 'data_type'

    def __init__(self, node, position, data_type):
        self.position = position
        self.data_type = data_type
        super(Identification, self).__init__(node)


class IfDataFrame(A2lNode):
    __slots__ = 'name'

    def __init__(self, node, name, args):
        self.name = name
        super(IfDataFrame, self).__init__(node, *args)


class IfDataMemorySegment(A2lNode):
    __slots__ = 'name', 'address_mapping', 'segment', 'generic_parameter'

    def __init__(self, node, name, args):
        self.name = name
        self.address_mapping = list()
        self.segment = list()
        self.generic_parameter = list()
        super(IfDataMemorySegment, self).__init__(node, *args)


class IfDataModule(A2lNode):
    __slots__ = 'name', 'source', 'raster', 'event_group', 'seed_key', 'checksum', 'tp_blob', 'tp_data'

    def __init__(self, node, name, args):
        self.name = name
        self.source = list()
        self.raster = list()
        self.event_group = list()
        self.seed_key = None
        self.checksum = None
        self.tp_blob = None
        self.tp_data = None
        super(IfDataModule, self).__init__(node, *args)


class IfDataXcp(A2lNode):
    __slots__ = 'protocol_layer', 'daq', 'pag', 'pgm', 'segment', 'daq_event', 'xcp_on_can', 'generic_parameter_list'

    def __init__(self, node, args):
        self.protocol_layer = list()
        self.daq = list()
        self.pag = list()
        self.pgm = list()
        self.segment = list()
        self.daq_event = list()
        self.xcp_on_can = list()
        self.generic_parameter_list = None
        super(IfDataXcp, self).__init__(node, *args)


class InMeasurement(A2lNode):
    __slots__ = 'identifier'

    def __init__(self, node, args):
        self.identifier = list()
        super(InMeasurement, self).__init__(node, *args)


class LocMeasurement(A2lNode):
    __slots__ = 'identifier'

    def __init__(self, node, args):
        self.identifier = list()
        super(LocMeasurement, self).__init__(node, *args)


class MaxRefresh(A2lNode):
    __slots__ = 'scaling_unit', 'rate'

    def __init__(self, node, scaling_unit, rate):
        self.scaling_unit = scaling_unit
        self.rate = rate
        super(MaxRefresh, self).__init__(node)


class Measurement(A2lNode):
    __slots__ = 'name', 'long_identifier', 'data_type', 'conversion', 'resolution', 'accuracy', 'lower_limit', \
                'upper_limit', 'display_identifier', 'read_write', 'format', 'array_size', 'bit_mask', \
                'bit_operation', 'byte_order', 'max_refresh', 'virtual', 'function_list', 'ecu_address', 'error_mask', \
                'ref_memory_segment', 'annotation', 'if_data_xcp', 'if_data_measurement', 'matrix_dim', \
                'ecu_address_extension'

    def __init__(self, node, name, long_identifier, data_type, conversion, resolution, accuracy, lower_limit,
                 upper_limit, args):
        self.name = name
        self.long_identifier = long_identifier
        self.data_type = data_type
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
        self.if_data_xcp = list()
        self.if_data_measurement = list()
        self.matrix_dim = None
        self.ecu_address_extension = None
        super(Measurement, self).__init__(node, *args)


class MemoryLayout(A2lNode):
    __slots__ = 'prg_type', 'address', 'size', 'offset', 'if_data_memory_layout'

    def __init__(self, node, prg_type, address, size, offset, args):
        self.prg_type = prg_type
        self.address = address
        self.size = size
        self.offset = offset
        self.if_data_memory_layout = list()
        super(MemoryLayout, self).__init__(node, *args)


class MemorySegment(A2lNode):
    __slots__ = 'name', 'long_identifier', 'prg_type', 'memory_type', 'attribute', 'address', 'size', 'offset', \
                'if_data_memory_segment', 'if_data_xcp'

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
        self.if_data_xcp = list()
        super(MemorySegment, self).__init__(node, *args)


class Module(A2lNode):
    __slots__ = 'name', 'long_identifier', 'a2ml', 'mod_par', 'mod_common', 'if_data_xcp', 'if_data_module', \
                'characteristic', 'axis_pts', 'measurement', 'compu_method', 'compu_tab', 'compu_vtab', \
                'compu_vtab_range', 'function', 'group', 'record_layout', 'variant_coding', 'frame', 'user_rights', \
                'unit'

    def __init__(self, node, name, long_identifier, args):
        self.name = name
        self.long_identifier = long_identifier
        self.a2ml = None
        self.mod_par = None
        self.mod_common = None
        self.if_data_xcp = None
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
    __slots__ = 'comment', 's_rec_layout', 'deposit', 'byte_order', 'data_size', 'alignment_byte', 'alignment_word', \
                'alignment_long', 'alignment_float32_ieee', 'alignment_float64_ieee'

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
    __slots__ = 'comment', 'version', 'addr_epk', 'epk', 'supplier', 'customer', 'customer_no', 'user', 'phone_no', \
                'ecu', 'cpu_type', 'no_of_interfaces', 'ecu_calibration_offset', 'calibration_method', \
                'memory_layout', 'memory_segment', 'system_constant'

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
    __slots__ = 'position', 'data_type'

    def __init__(self, node, position, data_type):
        self.position = position
        self.data_type = data_type
        super(NoAxisPts, self).__init__(node)


class NoAxisPtsX(NoAxisPts):
    pass


class NoAxisPtsY(NoAxisPts):
    pass


class NoAxisPtsZ(NoAxisPts):
    pass


class NoRescale(A2lNode):
    __slots__ = 'position', 'data_type'

    def __init__(self, node, position, data_type):
        self.position = position
        self.data_type = data_type
        super(NoRescale, self).__init__(node)


class NoRescaleX(NoRescale):
    pass


class NoRescaleY(NoRescale):
    pass


class NoRescaleZ(NoRescale):
    pass


class Offset(A2lNode):
    __slots__ = 'position', 'data_type'

    def __init__(self, node, position, data_type):
        self.position = position
        self.data_type = data_type
        super(Offset, self).__init__(node)


class OffsetX(Offset):
    pass


class OffsetY(Offset):
    pass


class OffsetZ(Offset):
    pass


class OutMeasurement(A2lNode):
    __slots__ = 'identifier'

    def __init__(self, node, args):
        self.identifier = list()
        super(OutMeasurement, self).__init__(node, *args)


class Pag(A2lNode):
    __slots__ = 'max_segments', 'freeze_supported'

    def __init__(self, node, max_segments, args):
        self.max_segments = max_segments
        self.freeze_supported = None
        super(Pag, self).__init__(node, *args)


class Pgm(A2lNode):
    __slots__ = 'mode', 'max_sectors', 'max_cto_pgm', 'sector', 'generic_parameter_list'

    def __init__(self, node, mode, max_sectors, max_cto_pgm, args):
        self.mode = mode
        self.max_sectors = max_sectors
        self.max_cto_pgm = max_cto_pgm
        self.sector = list()
        self.generic_parameter_list = None
        super(Pgm, self).__init__(node, *args)


class Project(A2lNode):
    __slots__ = 'name', 'long_identifier', 'header', 'module'

    def __init__(self, node, name, long_identifier, args):
        self.name = name
        self.long_identifier = long_identifier
        self.header = None
        self.module = list()
        super(Project, self).__init__(node, *args)


class ProtocolLayer(A2lNode):
    __slots__ = 'xcp_protocol_layer_version', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 'max_cto', 'max_dto'

    def __init__(self, node, xcp_protocol_layer_version, t1, t2, t3, t4, t5, t6, t7, max_cto, max_dto):
        self.xcp_protocol_layer_version = xcp_protocol_layer_version
        self.t1 = t1
        self.t2 = t2
        self.t3 = t3
        self.t4 = t4
        self.t5 = t5
        self.t6 = t6
        self.t7 = t7
        self.max_cto = max_cto
        self.max_dto = max_dto
        super(ProtocolLayer, self).__init__(node)


class Raster(A2lNode):
    __slots__ = 'raster_name', 'short_name', 'raster_id', 'scaling_unit', 'rate'

    def __init__(self, node, raster_name, short_name, raster_id, scaling_unit, rate):
        self.raster_name = raster_name
        self.short_name = short_name
        self.raster_id = raster_id
        self.scaling_unit = scaling_unit
        self.rate = rate
        super(Raster, self).__init__(node)


class RecordLayout(A2lNode):
    __slots__ = 'name', 'fnc_values', 'identification', 'axis_pts_x', 'axis_pts_y', 'axis_pts_z', 'axis_rescale_x', \
                'axis_rescale_y', 'axis_rescale_z', 'no_axis_pts_x', 'no_axis_pts_y', 'no_axis_pts_z', 'no_rescale_x', \
                'no_rescale_y', 'no_rescale_z', 'fix_no_axis_pts_x', 'fix_no_axis_pts_y', 'fix_no_axis_pts_z', \
                'src_addr_x', 'src_addr_y', 'src_addr_z', 'rip_addr_x', 'rip_addr_y', 'rip_addr_z', 'rip_addr_w', \
                'shift_op_x', 'shift_op_y', 'shift_op_z', 'offset_x', 'offset_y', 'offset_z', 'dist_op_x', \
                'dist_op_y', 'dist_op_z', 'alignment_byte', 'alignment_word', 'alignment_long', \
                'alignment_float32_ieee', 'alignment_float64_ieee', 'reserved'

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
    __slots__ = 'identifier'

    def __init__(self, node, args):
        self.identifier = list()
        super(RefCharacteristic, self).__init__(node, *args)


class RefGroup(A2lNode):
    __slots__ = 'identifier'

    def __init__(self, node, args):
        self.identifier = list()
        super(RefGroup, self).__init__(node, *args)


class RefMeasurement(A2lNode):
    __slots__ = 'identifier'

    def __init__(self, node, args):
        self.identifier = list()
        super(RefMeasurement, self).__init__(node, *args)


class Reserved(A2lNode):
    __slots__ = 'position', 'data_size'

    def __init__(self, node, position, data_size):
        self.position = position
        self.data_size = data_size
        super(Reserved, self).__init__(node)


class RipAddr(A2lNode):
    __slots__ = 'position', 'data_type'

    def __init__(self, node, position, data_type):
        self.position = position
        self.data_type = data_type
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
    __slots__ = 'cal_dll', 'daq_dll', 'pgm_dll'

    def __init__(self, node, cal_dll, daq_dll, pgm_dll):
        self.cal_dll = cal_dll
        self.daq_dll = daq_dll
        self.pgm_dll = pgm_dll
        super(SeedKey, self).__init__(node)


class Segment(A2lNode):
    __slots__ = 'segment_logical_number', 'number_of_pages', 'address_extension', 'compression_method', \
                'encryption_method', 'checksum', 'page'

    def __init__(self, node, segment_logical_number, number_of_pages, address_extension, compression_method,
                 encryption_method, args):
        self.segment_logical_number = segment_logical_number
        self.number_of_pages = number_of_pages
        self.address_extension = address_extension
        self.compression_method = compression_method
        self.encryption_method = encryption_method
        self.checksum = None
        self.page = None
        super(Segment, self).__init__(node, *args)


class ShiftOp(A2lNode):
    __slots__ = 'position', 'data_type'

    def __init__(self, node, position, data_type):
        self.position = position
        self.data_type = data_type
        super(ShiftOp, self).__init__(node)


class ShiftOpX(ShiftOp):
    pass


class ShiftOpY(ShiftOp):
    pass


class ShiftOpZ(ShiftOp):
    pass


class SiExponents(A2lNode):
    __slots__ = 'length', 'mass', 'time', 'electric_current', 'temperature', 'amount_of_substance', 'luminous_intensity'

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
    __slots__ = 'name', 'scaling_unit', 'rate', 'display_identifier', 'qp_blob', 'qp_data'

    def __init__(self, node, name, scaling_unit, rate, args):
        self.name = name
        self.scaling_unit = scaling_unit
        self.rate = rate
        self.display_identifier = None
        self.qp_blob = None
        self.qp_data = None
        super(Source, self).__init__(node, *args)


class SrcAddr(A2lNode):
    __slots__ = 'position', 'data_type'

    def __init__(self, node, position, data_type):
        self.position = position
        self.data_type = data_type
        super(SrcAddr, self).__init__(node)


class SrcAddrX(SrcAddr):
    pass


class SrcAddrY(SrcAddr):
    pass


class SrcAddrZ(SrcAddr):
    pass


class SubFunction(A2lNode):
    __slots__ = 'identifier'

    def __init__(self, node, args):
        self.identifier = list()
        super(SubFunction, self).__init__(node, *args)


class SubGroup(A2lNode):
    __slots__ = 'identifier'

    def __init__(self, node, args):
        self.identifier = list()
        super(SubGroup, self).__init__(node, *args)


class SystemConstant(A2lNode):
    __slots__ = 'name', 'value'

    def __init__(self, node, name, value):
        self.name = name
        self.value = value
        super(SystemConstant, self).__init__(node)


class TimestampSupported(A2lNode):
    __slots__ = 'timestamp_ticks', 'size', 'unit'

    def __init__(self, node, timestamp_ticks, size, unit, args):
        self.timestamp_ticks = timestamp_ticks
        self.size = size
        self.unit = unit
        super(TimestampSupported, self).__init__(node)


class Unit(A2lNode):
    __slots__ = 'name', 'long_identifier', 'display', 'type', 'si_exponents', 'ref_unit', 'unit_conversion'

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
    __slots__ = 'gradient', 'offset'

    def __init__(self, node, gradient, offset):
        self.gradient = gradient
        self.offset = offset
        super(UnitConversion, self).__init__(node)


class UserRights(A2lNode):
    __slots__ = 'user_level_id', 'read_only', 'ref_group'

    def __init__(self, node, user_level_id, args):
        self.user_level_id = user_level_id
        self.read_only = None
        self.ref_group = list()
        super(UserRights, self).__init__(node, *args)


class VariantCoding(A2lNode):
    __slots__ = 'var_separator', 'var_naming', 'var_criterion', 'var_forbidden_comb', 'var_characteristic'

    def __init__(self, node, args):
        self.var_separator = None
        self.var_naming = None
        self.var_criterion = list()
        self.var_forbidden_comb = list()
        self.var_characteristic = list()
        super(VariantCoding, self).__init__(node, *args)


class VarAddress(A2lNode):
    __slots__ = 'address'

    def __init__(self, node, args):
        self.address = list()
        super(VarAddress, self).__init__(node, *args)


class VarCharacteristic(A2lNode):
    __slots__ = 'name', 'criterion_name', 'var_address'

    def __init__(self, node, name, criterion_name, args):
        self.name = name
        self.criterion_name = criterion_name
        self.var_address = None
        super(VarCharacteristic, self).__init__(node, args)


class VarCriterion(A2lNode):
    __slots__ = 'name', 'long_identifier', 'value', 'var_measurement', 'var_selection_characteristic'

    def __init__(self, node, name, long_identifier, value, args):
        self.name = name
        self.long_identifier = long_identifier
        self.value = value
        self.var_measurement = None
        self.var_selection_characteristic = None
        super(VarCriterion, self).__init__(node, *args)


class VarForbiddenComb(A2lNode):
    __slots__ = 'criterion_name', 'criterion_value'

    def __init__(self, node, *args):
        self.criterion_name = list()
        self.criterion_value = list()
        super(VarForbiddenComb, self).__init__(node, *args)


class VirtualCharacteristic(A2lNode):
    __slots__ = 'formula', 'characteristic'

    def __init__(self, node, formula, args):
        self.formula = formula
        self.characteristic = list()
        super(VirtualCharacteristic, self).__init__(node, *args)


class XcpOnCan(A2lNode):
    __slots__ = 'identifier', 'can_id_broadcast', 'can_id_master', 'can_id_slave', 'baudrate', 'sample_point', \
                'sample_rate', 'btl_cycles', 'sjw', 'sync_edge', 'daq_list_can_id'

    def __init__(self, node, identifier, args):
        self.identifier = identifier
        self.can_id_broadcast = None
        self.can_id_master = None
        self.can_id_slave = None
        self.baudrate = None
        self.sample_point = None
        self.sample_rate = None
        self.btl_cycles = None
        self.sjw = None
        self.sync_edge = None
        self.daq_list_can_id = list()
        super(XcpOnCan, self).__init__(node, *args)
