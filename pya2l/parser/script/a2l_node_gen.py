import os
import pystache

nodes = [
    {
        'args': [
            {
                'name': 'version_no',
                'type': 'Int'
            },
            {
                'name': 'upgrade_no',
                'type': 'Int'
            }
        ],
        'kwargs': [],
        'name': 'A2ML_VERSION'
    },
    {
        'args': [],
        'kwargs': [
            {
                'name': 'ANNOTATION_LABEL',
                'type': 'ANNOTATION_LABEL'
            },
            {
                'name': 'ANNOTATION_ORIGIN',
                'type': 'ANNOTATION_ORIGIN'
            },
            {
                'name': 'ANNOTATION_TEXT',
                'type': 'ANNOTATION_TEXT'
            }
        ],
        'name': 'ANNOTATION'
    },
    {
        'args': [
            {
                'name': 'label',
                'type': 'String'
            }
        ],
        'kwargs': [],
        'name': 'ANNOTATION_LABEL'
    },
    {
        'args': [
            {
                'name': 'origin',
                'type': 'String'
            }
        ],
        'kwargs': [],
        'name': 'ANNOTATION_ORIGIN'
    },
    {
        'args': [],
        'kwargs': [
            {
                'multiple': True,
                'name': 'text',
                'type': 'list'
            }
        ],
        'name': 'ANNOTATION_TEXT'
    },
    {
        'args': [
            {
                'name': 'version_no',
                'type': 'Int'
            },
            {
                'name': 'upgrade_no',
                'type': 'Int'
            }
        ],
        'kwargs': [],
        'name': 'ASAP2_VERSION'
    },
    {
        'args': [
            {
                'name': 'attribute',
                'type': 'enum_attribute'
            },
            {
                'name': 'input_quantity',
                'type': 'Ident'
            },
            {
                'name': 'conversion',
                'type': 'Ident'
            },
            {
                'name': 'max_axis_points',
                'type': 'Int'
            },
            {
                'name': 'lower_limit',
                'type': 'Float'
            },
            {
                'name': 'upper_limit',
                'type': 'Float'
            }
        ],
        'kwargs': [
            {
                'name': 'READ_ONLY',
                'type': 'READ_ONLY'
            },
            {
                'name': 'FORMAT',
                'type': 'FORMAT'
            },
            {
                'multiple': True,
                'name': 'ANNOTATION',
                'type': 'ANNOTATION'
            },
            {
                'name': 'AXIS_PTS_REF',
                'type': 'AXIS_PTS_REF'
            },
            {
                'name': 'MAX_GRAD',
                'type': 'MAX_GRAD'
            },
            {
                'name': 'MONOTONY',
                'type': 'MONOTONY'
            },
            {
                'name': 'BYTE_ORDER',
                'type': 'BYTE_ORDER'
            },
            {
                'name': 'EXTENDED_LIMITS',
                'type': 'EXTENDED_LIMITS'
            },
            {
                'name': 'FIX_AXIS_PAR',
                'type': 'FIX_AXIS_PAR'
            },
            {
                'name': 'FIX_AXIS_PAR_DIST',
                'type': 'FIX_AXIS_PAR_DIST'
            },
            {
                'name': 'FIX_AXIS_PAR_LIST',
                'type': 'FIX_AXIS_PAR_LIST'
            },
            {
                'name': 'DEPOSIT',
                'type': 'DEPOSIT'
            },
            {
                'name': 'CURVE_AXIS_REF',
                'type': 'CURVE_AXIS_REF'
            }
        ],
        'name': 'AXIS_DESCR'
    },
    {
        'args': [
            {
                'name': 'name',
                'type': 'Ident'
            },
            {
                'name': 'long_identifier',
                'type': 'String'
            },
            {
                'name': 'address',
                'type': 'Long'
            },
            {
                'name': 'input_quantity',
                'type': 'Ident'
            },
            {
                'name': 'deposit',
                'type': 'Ident'
            },
            {
                'name': 'max_diff',
                'type': 'Float'
            },
            {
                'name': 'conversion',
                'type': 'Ident'
            },
            {
                'name': 'max_axis_points',
                'type': 'Int'
            },
            {
                'name': 'lower_limit',
                'type': 'Float'
            },
            {
                'name': 'upper_limit',
                'type': 'Float'
            }
        ],
        'kwargs': [
            {
                'name': 'DISPLAY_IDENTIFIER',
                'type': 'DISPLAY_IDENTIFIER'
            },
            {
                'name': 'READ_ONLY',
                'type': 'READ_ONLY'
            },
            {
                'name': 'FORMAT',
                'type': 'FORMAT'
            },
            {
                'name': 'DEPOSIT',
                'type': 'DEPOSIT'
            },
            {
                'name': 'BYTE_ORDER',
                'type': 'BYTE_ORDER'
            },
            {
                'name': 'FUNCTION_LIST',
                'type': 'FUNCTION_LIST'
            },
            {
                'name': 'REF_MEMORY_SEGMENT',
                'type': 'REF_MEMORY_SEGMENT'
            },
            {
                'name': 'GUARD_RAILS',
                'type': 'GUARD_RAILS'
            },
            {
                'name': 'EXTENDED_LIMITS',
                'type': 'EXTENDED_LIMITS'
            },
            {
                'multiple': True,
                'name': 'ANNOTATION',
                'type': 'ANNOTATION'
            },
            {
                'multiple': True,
                'name': 'IF_DATA',
                'type': 'IF_DATA'
            },
            {
                'name': 'CALIBRATION_ACCESS',
                'type': 'CALIBRATION_ACCESS'
            },
            {
                'name': 'ECU_ADDRESS_EXTENSION',
                'type': 'ECU_ADDRESS_EXTENSION'
            }
        ],
        'name': 'AXIS_PTS'
    },
    {
        'args': [
            {
                'name': 'axis_points',
                'type': 'Ident'
            }
        ],
        'kwargs': [

        ],
        'name': 'AXIS_PTS_REF'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            },
            {
                'name': 'index_incr',
                'type': 'IndexOrder'
            },
            {
                'name': 'addressing',
                'type': 'AddrType'
            }
        ],
        'kwargs': [],
        'name': 'AXIS_PTS_X'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            },
            {
                'name': 'index_incr',
                'type': 'IndexOrder'
            },
            {
                'name': 'addressing',
                'type': 'AddrType'
            }
        ],
        'kwargs': [],
        'name': 'AXIS_PTS_Y'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            },
            {
                'name': 'index_incr',
                'type': 'IndexOrder'
            },
            {
                'name': 'addressing',
                'type': 'AddrType'
            }
        ],
        'kwargs': [],
        'name': 'AXIS_PTS_Z'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            },
            {
                'name': 'max_number_of_rescale_pairs',
                'type': 'Int'
            },
            {
                'name': 'index_incr',
                'type': 'IndexOrder'
            },
            {
                'name': 'addressing',
                'type': 'AddrType'
            }
        ],
        'kwargs': [],
        'name': 'AXIS_RESCALE_X'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            },
            {
                'name': 'max_number_of_rescale_pairs',
                'type': 'Int'
            },
            {
                'name': 'index_incr',
                'type': 'IndexOrder'
            },
            {
                'name': 'addressing',
                'type': 'AddrType'
            }
        ],
        'kwargs': [],
        'name': 'AXIS_RESCALE_Y'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            },
            {
                'name': 'max_number_of_rescale_pairs',
                'type': 'Int'
            },
            {
                'name': 'index_incr',
                'type': 'IndexOrder'
            },
            {
                'name': 'addressing',
                'type': 'AddrType'
            }
        ],
        'kwargs': [],
        'name': 'AXIS_RESCALE_Z'
    },
    {
        'args': [],
        'kwargs': [
            {
                'name': 'LEFT_SHIFT',
                'type': 'LEFT_SHIFT'
            },
            {
                'name': 'RIGHT_SHIFT',
                'type': 'RIGHT_SHIFT'
            },
            {
                'name': 'SIGN_EXTEND',
                'type': 'SIGN_EXTEND'
            }
        ],
        'name': 'BIT_OPERATION'
    },
    {
        'args': [
            {
                'name': 'byte_order',
                'type': 'ByteOrder'
            }
        ],
        'kwargs': [],
        'name': 'BYTE_ORDER'
    },
    {
        'args': [
            {
                'name': 'method',
                'type': 'String'
            },
            {
                'name': 'version',
                'type': 'Long'
            }
        ],
        'kwargs': [
            {
                'multiple': True,
                'name': 'CALIBRATION_HANDLE',
                'type': 'CALIBRATION_HANDLE'
            }
        ],
        'name': 'CALIBRATION_METHOD'
    },
    {
        'args': [
            {
                'name': 'name',
                'type': 'Ident'
            },
            {
                'name': 'long_identifier',
                'type': 'String'
            },
            {
                'name': 'type',
                'type': 'enum_type'
            },
            {
                'name': 'address',
                'type': 'Long'
            },
            {
                'name': 'deposit',
                'type': 'Ident'
            },
            {
                'name': 'max_diff',
                'type': 'Float'
            },
            {
                'name': 'conversion',
                'type': 'Ident'
            },
            {
                'name': 'lower_limit',
                'type': 'Float'
            },
            {
                'name': 'upper_limit',
                'type': 'Float'
            }
        ],
        'kwargs': [
            {
                'name': 'DISPLAY_IDENTIFIER',
                'type': 'DISPLAY_IDENTIFIER'
            },
            {
                'name': 'FORMAT',
                'type': 'FORMAT'
            },
            {
                'name': 'BYTE_ORDER',
                'type': 'BYTE_ORDER'
            },
            {
                'name': 'BIT_MASK',
                'type': 'BIT_MASK'
            },
            {
                'name': 'FUNCTION_LIST',
                'type': 'FUNCTION_LIST'
            },
            {
                'name': 'NUMBER',
                'type': 'NUMBER'
            },
            {
                'name': 'EXTENDED_LIMITS',
                'type': 'EXTENDED_LIMITS'
            },
            {
                'name': 'READ_ONLY',
                'type': 'READ_ONLY'
            },
            {
                'name': 'GUARD_RAILS',
                'type': 'GUARD_RAILS'
            },
            {
                'name': 'MAP_LIST',
                'type': 'MAP_LIST'
            },
            {
                'name': 'MAX_REFRESH',
                'type': 'MAX_REFRESH'
            },
            {
                'name': 'DEPENDENT_CHARACTERISTIC',
                'type': 'DEPENDENT_CHARACTERISTIC'
            },
            {
                'name': 'VIRTUAL_CHARACTERISTIC',
                'type': 'VIRTUAL_CHARACTERISTIC'
            },
            {
                'name': 'REF_MEMORY_SEGMENT',
                'type': 'REF_MEMORY_SEGMENT'
            },
            {
                'multiple': True,
                'name': 'ANNOTATION',
                'type': 'ANNOTATION'
            },
            {
                'name': 'COMPARISON_QUANTITY',
                'type': 'COMPARISON_QUANTITY'
            },
            {
                'multiple': True,
                'name': 'IF_DATA',
                'type': 'IF_DATA'
            },
            {
                'multiple': True,
                'name': 'AXIS_DESCR',
                'type': 'AXIS_DESCR'
            },
            {
                'name': 'CALIBRATION_ACCESS',
                'type': 'CALIBRATION_ACCESS'
            },
            {
                'name': 'MATRIX_DIM',
                'type': 'MATRIX_DIM'
            },
            {
                'name': 'ECU_ADDRESS_EXTENSION',
                'type': 'ECU_ADDRESS_EXTENSION'
            }
        ],
        'name': 'CHARACTERISTIC'
    },
    {
        'args': [
            {
                'name': 'a',
                'type': 'Float'
            },
            {
                'name': 'b',
                'type': 'Float'
            },
            {
                'name': 'c',
                'type': 'Float'
            },
            {
                'name': 'd',
                'type': 'Float'
            },
            {
                'name': 'e',
                'type': 'Float'
            },
            {
                'name': 'f',
                'type': 'Float'
            }
        ],
        'kwargs': [],
        'name': 'COEFFS'
    },
    {
        'args': [
            {
                'name': 'name',
                'type': 'Ident'
            },
            {
                'name': 'long_identifier',
                'type': 'String'
            },
            {
                'name': 'conversion_type',
                'type': 'enum_conversion_type'
            },
            {
                'name': 'format',
                'type': 'String'
            },
            {
                'name': 'unit',
                'type': 'String'
            }
        ],
        'kwargs': [
            {
                'name': 'FORMULA',
                'type': 'FORMULA'
            },
            {
                'name': 'COEFFS',
                'type': 'COEFFS'
            },
            {
                'name': 'COMPU_TAB_REF',
                'type': 'COMPU_TAB_REF'
            },
            {
                'name': 'REF_UNIT',
                'type': 'REF_UNIT'
            }
        ],
        'name': 'COMPU_METHOD'
    },
    {
        'args': [
            {
                'name': 'name',
                'type': 'Ident'
            },
            {
                'name': 'long_identifier',
                'type': 'String'
            },
            {
                'name': 'conversion_type',
                'type': 'enum_conversion_type'
            },
            {
                'name': 'number_value_pair',
                'type': 'Int'
            }
        ],
        'kwargs': [
            {
                'multiple': True,
                'name': 'in_val_out_val',
                'type': 'float_float',
                'remark': 'TODO: change in_val_out_val by value_pair...'
            },
            {
                'name': 'DEFAULT_VALUE',
                'type': 'DEFAULT_VALUE'
            }
        ],
        'name': 'COMPU_TAB'
    },
    {
        'args': [
            {
                'name': 'name',
                'type': 'Ident'
            },
            {
                'name': 'long_identifier',
                'type': 'String'
            },
            {
                'name': 'conversion_type',
                'type': 'enum_conversion_type'
            },
            {
                'name': 'number_value_pair',
                'type': 'Int'
            }
        ],
        'kwargs': [
            {
                'multiple': True,
                'name': 'compu_vtab_in_val_out_val',
                'type': 'float_string',
                'remark': 'TODO: change in_val_out_val by value_pair...'
            },
            {
                'name': 'DEFAULT_VALUE',
                'type': 'DEFAULT_VALUE'
            }
        ],
        'name': 'COMPU_VTAB'
    },
    {
        'args': [
            {
                'name': 'name',
                'type': 'Ident'
            },
            {
                'name': 'long_identifier',
                'type': 'String'
            },
            {
                'name': 'number_value_triple',
                'type': 'Int'
            }
        ],
        'kwargs': [
            {
                'multiple': True,
                'name': 'compu_vtab_range_in_val_out_val',
                'type': 'float_float_string',
                'remark': 'TODO: change in_val_out_val by value_pair...'
            },
            {
                'name': 'DEFAULT_VALUE',
                'type': 'DEFAULT_VALUE'
            }
        ],
        'name': 'COMPU_VTAB_RANGE'
    },
    {
        'args': [],
        'kwargs': [
            {
                'multiple': True,
                'name': 'identifier',
                'type': 'Ident'
            }
        ],
        'name': 'DEF_CHARACTERISTIC'
    },
    {
        'args': [
            {
                'name': 'formula',
                'type': 'String'
            }
        ],
        'kwargs': [
            {
                'multiple': True,
                'name': 'characteristic',
                'type': 'Ident',
                'remark': 'TODO: defined as (Characteristic)* in specification, one or more?'
            }
        ],
        'name': 'DEPENDENT_CHARACTERISTIC'
    },
    {
        'args': [
            {
                'name': 'mode',
                'type': 'enum_mode'
            }
        ],
        'kwargs': [],
        'name': 'DEPOSIT'
    },
    {
        'args': [
            {
                'name': 'display_name',
                'type': 'Ident'
            }
        ],
        'kwargs': [],
        'name': 'DISPLAY_IDENTIFIER'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            }
        ],
        'kwargs': [],
        'name': 'DIST_OP_X'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            }
        ],
        'kwargs': [],
        'name': 'DIST_OP_Y'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            }
        ],
        'kwargs': [],
        'name': 'DIST_OP_Z'
    },
    {
        'args': [
            {
                'name': 'offset',
                'type': 'Int'
            },
            {
                'name': 'shift',
                'type': 'Int'
            },
            {
                'name': 'numberapo',
                'type': 'Int'
            }],
        'kwargs': [],
        'name': 'FIX_AXIS_PAR'
    },
    {
        'args': [
            {
                'name': 'offset',
                'type': 'Int'
            },
            {
                'name': 'distance',
                'type': 'Int'
            },
            {
                'name': 'numberapo',
                'type': 'Int'
            }
        ],
        'kwargs': [],
        'name': 'FIX_AXIS_PAR_DIST'
    },
    {
        'args': [],
        'kwargs': [
            {
                'multiple': True,
                'name': 'axis_pts_value',
                'type': 'Float'
            }
        ],
        'name': 'FIX_AXIS_PAR_LIST'
    },
    {
        'args': [
            {
                'name': 'number_of_axis_points',
                'type': 'Int'
            }
        ],
        'kwargs': [],
        'name': 'FIX_NO_AXIS_PTS_X'
    },
    {
        'args': [
            {
                'name': 'number_of_axis_points',
                'type': 'Int'
            }
        ],
        'kwargs': [],
        'name': 'FIX_NO_AXIS_PTS_Y'
    },
    {
        'args': [
            {
                'name': 'number_of_axis_points',
                'type': 'Int'
            }
        ],
        'kwargs': [],
        'name': 'FIX_NO_AXIS_PTS_Z'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            },
            {
                'name': 'index_mode',
                'type': 'enum_index_mode'
            },
            {
                'name': 'addr_type',
                'type': 'AddrType'
            }
        ],
        'kwargs': [],
        'name': 'FNC_VALUES'
    },
    {
        'args': [
            {
                'name': 'f',
                'type': 'String'
            }
        ],
        'kwargs': [
            {
                'name': 'FORMULA_INV',
                'type': 'FORMULA_INV'
            }
        ],
        'name': 'FORMULA'
    },
    {
        'args': [
            {
                'name': 'name',
                'type': 'Ident'
            },
            {
                'name': 'long_identifier',
                'type': 'String'
            },
            {
                'name': 'scaling_unit',
                'type': 'Int'
            },
            {
                'name': 'rate',
                'type': 'Long'
            }
        ],
        'kwargs': [
            {
                'name': 'FRAME_MEASUREMENT',
                'type': 'FRAME_MEASUREMENT'
            },
            {
                'multiple': True,
                'name': 'IF_DATA',
                'type': 'IF_DATA'
            }
        ],
        'name': 'FRAME'
    },
    {
        'args': [],
        'kwargs': [
            {
                'multiple': True,
                'name': 'identifier',
                'type': 'Ident'
            }
        ],
        'name': 'FRAME_MEASUREMENT'
    },
    {
        'args': [
            {
                'name': 'name',
                'type': 'Ident'
            },
            {
                'name': 'long_identifier',
                'type': 'String'
            }
        ],
        'kwargs': [
            {
                'multiple': True,
                'name': 'ANNOTATION',
                'type': 'ANNOTATION'
            },
            {
                'name': 'DEF_CHARACTERISTIC',
                'type': 'DEF_CHARACTERISTIC'
            },
            {
                'name': 'REF_CHARACTERISTIC',
                'type': 'REF_CHARACTERISTIC'
            },
            {
                'name': 'IN_MEASUREMENT',
                'type': 'IN_MEASUREMENT'
            },
            {
                'name': 'OUT_MEASUREMENT',
                'type': 'OUT_MEASUREMENT'
            },
            {
                'name': 'LOC_MEASUREMENT',
                'type': 'LOC_MEASUREMENT'
            },
            {
                'name': 'SUB_FUNCTION',
                'type': 'SUB_FUNCTION'
            },
            {
                'name': 'FUNCTION_VERSION',
                'type': 'FUNCTION_VERSION'
            }
        ],
        'name': 'FUNCTION'
    },
    {
        'args': [],
        'kwargs': [
            {
                'multiple': True,
                'name': 'name',
                'type': 'Ident'
            }
        ],
        'name': 'FUNCTION_LIST'
    },
    {
        'args': [
            {
                'name': 'group_name',
                'type': 'Ident'
            },
            {
                'name': 'group_long_identifier',
                'type': 'String'
            }
        ],
        'kwargs': [
            {
                'multiple': True,
                'name': 'ANNOTATION',
                'type': 'ANNOTATION'
            },
            {
                'name': 'ROOT',
                'type': 'ROOT'
            },
            {
                'name': 'REF_CHARACTERISTIC',
                'type': 'REF_CHARACTERISTIC'
            },
            {
                'name': 'REF_MEASUREMENT',
                'type': 'REF_MEASUREMENT'
            },
            {
                'name': 'FUNCTION_LIST',
                'type': 'FUNCTION_LIST'
            },
            {
                'name': 'SUB_GROUP',
                'type': 'SUB_GROUP'
            }
        ],
        'name': 'GROUP'
    },
    {
        'args': [
            {
                'name': 'comment',
                'type': 'String'
            }
        ],
        'kwargs': [
            {
                'name': 'VERSION',
                'type': 'VERSION'
            },
            {
                'name': 'PROJECT_NO',
                'type': 'PROJECT_NO'
            }
        ],
        'name': 'HEADER'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            }
        ],
        'kwargs': [],
        'name': 'IDENTIFICATION'
    },
    {
        'args': [],
        'kwargs': [
            {
                'multiple': True,
                'name': 'identifier',
                'type': 'Ident'
            }
        ],
        'name': 'IN_MEASUREMENT'
    },
    {
        'args': [],
        'kwargs': [
            {
                'multiple': True,
                'name': 'identifier',
                'type': 'Ident'
            }
        ],
        'name': 'LOC_MEASUREMENT'
    },
    {
        'args': [
            {
                'name': 'max_gradient',
                'type': 'Float'
            }
        ],
        'kwargs': [],
        'name': 'MAX_GRAD'
    },
    {
        'args': [
            {
                'name': 'scaling_unit',
                'type': 'Int'
            },
            {
                'name': 'rate',
                'type': 'Long'
            }
        ],
        'kwargs': [],
        'name': 'MAX_REFRESH'
    },
    {
        'args': [
            {
                'name': 'name',
                'type': 'Ident'
            },
            {
                'name': 'long_identifier',
                'type': 'String'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            },
            {
                'name': 'conversion',
                'type': 'Ident'
            },
            {
                'name': 'resolution',
                'type': 'Int'
            },
            {
                'name': 'accuracy',
                'type': 'Float'
            },
            {
                'name': 'lower_limit',
                'type': 'Float'
            },
            {
                'name': 'upper_limit',
                'type': 'Float'
            }
        ],
        'kwargs': [
            {
                'name': 'DISPLAY_IDENTIFIER',
                'type': 'DISPLAY_IDENTIFIER'
            },
            {
                'name': 'READ_WRITE',
                'type': 'READ_WRITE'
            },
            {
                'name': 'FORMAT',
                'type': 'FORMAT'
            },
            {
                'name': 'ARRAY_SIZE',
                'type': 'ARRAY_SIZE'
            },
            {
                'name': 'BIT_MASK',
                'type': 'BIT_MASK'
            },
            {
                'name': 'BIT_OPERATION',
                'type': 'BIT_OPERATION'
            },
            {
                'name': 'BYTE_ORDER',
                'type': 'BYTE_ORDER'
            },
            {
                'name': 'MAX_REFRESH',
                'type': 'MAX_REFRESH'
            },
            {
                'name': 'VIRTUAL',
                'type': 'VIRTUAL'
            },
            {
                'name': 'FUNCTION_LIST',
                'type': 'FUNCTION_LIST'
            },
            {
                'name': 'ECU_ADDRESS',
                'type': 'ECU_ADDRESS'
            },
            {
                'name': 'ERROR_MASK',
                'type': 'ERROR_MASK'
            },
            {
                'name': 'REF_MEMORY_SEGMENT',
                'type': 'REF_MEMORY_SEGMENT'
            },
            {
                'multiple': True,
                'name': 'ANNOTATION',
                'type': 'ANNOTATION'
            },
            {
                'multiple': True,
                'name': 'IF_DATA',
                'type': 'IF_DATA'
            },
            {
                'name': 'MATRIX_DIM',
                'type': 'MATRIX_DIM'
            },
            {
                'name': 'ECU_ADDRESS_EXTENSION',
                'type': 'ECU_ADDRESS_EXTENSION'
            }
        ],
        'name': 'MEASUREMENT'
    },
    {
        'args': [
            {
                'name': 'prg_type',
                'type': 'enum_prg_type'
            },
            {
                'name': 'address',
                'type': 'Long'
            },
            {
                'name': 'size',
                'type': 'Long'
            },
            {
                'name': 'offset',
                'type': 'list'
            }
        ],
        'kwargs': [
            {
                'multiple': True,
                'name': 'IF_DATA',
                'type': 'IF_DATA'
            }
        ],
        'name': 'MEMORY_LAYOUT'
    },
    {
        'args': [
            {
                'name': 'name',
                'type': 'Ident'
            },
            {
                'name': 'long_identifier',
                'type': 'String'
            },
            {
                'name': 'prg_type',
                'type': 'enum_prg_type'
            },
            {
                'name': 'memory_type',
                'type': 'enum_memory_type'
            },
            {
                'name': 'attribute',
                'type': 'enum_attribute'
            },
            {
                'name': 'address',
                'type': 'Long'
            },
            {
                'name': 'size',
                'type': 'Long'
            },
            {
                'name': 'offset',
                'type': 'list'
            }
        ],
        'kwargs': [
            {
                'multiple': True,
                'name': 'IF_DATA',
                'type': 'IF_DATA'
            }
        ],
        'name': 'MEMORY_SEGMENT'
    },
    {
        'args': [
            {
                'name': 'name',
                'type': 'Ident'
            },
            {
                'name': 'long_identifier',
                'type': 'String'
            }
        ],
        'kwargs': [
            {
                'name': 'A2ML',
                'type': 'A2ML'
            },
            {
                'name': 'MOD_PAR',
                'type': 'MOD_PAR'
            },
            {
                'name': 'MOD_COMMON',
                'type': 'MOD_COMMON'
            },
            {
                'multiple': True,
                'name': 'IF_DATA',
                'type': 'IF_DATA'
            },
            {
                'multiple': True,
                'name': 'CHARACTERISTIC',
                'type': 'CHARACTERISTIC'
            },
            {
                'multiple': True,
                'name': 'AXIS_PTS',
                'type': 'AXIS_PTS'
            },
            {
                'multiple': True,
                'name': 'MEASUREMENT',
                'type': 'MEASUREMENT'
            },
            {
                'multiple': True,
                'name': 'COMPU_METHOD',
                'type': 'COMPU_METHOD'
            },
            {
                'multiple': True,
                'name': 'COMPU_TAB',
                'type': 'COMPU_TAB'
            },
            {
                'multiple': True,
                'name': 'COMPU_VTAB',
                'type': 'COMPU_VTAB'
            },
            {
                'multiple': True,
                'name': 'COMPU_VTAB_RANGE',
                'type': 'COMPU_VTAB_RANGE'
            },
            {
                'multiple': True,
                'name': 'FUNCTION',
                'type': 'FUNCTION'
            },
            {
                'multiple': True,
                'name': 'GROUP',
                'type': 'GROUP'
            },
            {
                'multiple': True,
                'name': 'RECORD_LAYOUT',
                'type': 'RECORD_LAYOUT'
            },
            {
                'name': 'VARIANT_CODING',
                'type': 'VARIANT_CODING'
            },
            {
                'name': 'FRAME',
                'type': 'FRAME'
            },
            {
                'multiple': True,
                'name': 'USER_RIGHTS',
                'type': 'USER_RIGHTS'
            },
            {
                'multiple': True,
                'name': 'UNIT',
                'type': 'UNIT'
            }
        ],
        'name': 'MODULE'
    },
    {
        'args': [
            {
                'name': 'comment',
                'type': 'String'
            }
        ],
        'kwargs': [
            {
                'name': 'S_REC_LAYOUT',
                'type': 'S_REC_LAYOUT'
            },
            {
                'name': 'DEPOSIT',
                'type': 'DEPOSIT'
            },
            {
                'name': 'BYTE_ORDER',
                'type': 'BYTE_ORDER'
            },
            {
                'name': 'DATA_SIZE',
                'type': 'DATA_SIZE'
            },
            {
                'name': 'ALIGNMENT_BYTE',
                'type': 'ALIGNMENT_BYTE'
            },
            {
                'name': 'ALIGNMENT_WORD',
                'type': 'ALIGNMENT_WORD'
            },
            {
                'name': 'ALIGNMENT_LONG',
                'type': 'ALIGNMENT_LONG'
            },
            {
                'name': 'ALIGNMENT_FLOAT32_IEEE',
                'type': 'ALIGNMENT_FLOAT32_IEEE'
            },
            {
                'name': 'ALIGNMENT_FLOAT64_IEEE',
                'type': 'ALIGNMENT_FLOAT64_IEEE'
            }
        ],
        'name': 'MOD_COMMON'
    },
    {
        'args': [
            {
                'name': 'comment',
                'type': 'String'
            }
        ],
        'kwargs': [
            {
                'name': 'VERSION',
                'type': 'VERSION'
            },
            {
                'multiple': True,
                'name': 'ADDR_EPK',
                'type': 'ADDR_EPK'
            },
            {
                'name': 'EPK',
                'type': 'EPK'
            },
            {
                'name': 'SUPPLIER',
                'type': 'SUPPLIER'
            },
            {
                'name': 'CUSTOMER',
                'type': 'CUSTOMER'
            },
            {
                'name': 'CUSTOMER_NO',
                'type': 'CUSTOMER_NO'
            },
            {
                'name': 'USER',
                'type': 'USER'
            },
            {
                'name': 'PHONE_NO',
                'type': 'PHONE_NO'
            },
            {
                'name': 'ECU',
                'type': 'ECU'
            },
            {
                'name': 'CPU_TYPE',
                'type': 'CPU_TYPE'
            },
            {
                'name': 'NO_OF_INTERFACES',
                'type': 'NO_OF_INTERFACES'
            },
            {
                'name': 'ECU_CALIBRATION_OFFSET',
                'type': 'ECU_CALIBRATION_OFFSET'
            },
            {
                'multiple': True,
                'name': 'CALIBRATION_METHOD',
                'type': 'CALIBRATION_METHOD'
            },
            {
                'multiple': True,
                'name': 'MEMORY_LAYOUT',
                'type': 'MEMORY_LAYOUT'
            },
            {
                'multiple': True,
                'name': 'MEMORY_SEGMENT',
                'type': 'MEMORY_SEGMENT'
            },
            {
                'multiple': True,
                'name': 'SYSTEM_CONSTANT',
                'type': 'SYSTEM_CONSTANT'
            }
        ],
        'name': 'MOD_PAR'
    },
    {
        'args': [
            {
                'name': 'monotony',
                'type': 'monotony_enum'
            }
        ],
        'kwargs': [],
        'name': 'MONOTONY'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            }
        ],
        'kwargs': [],
        'name': 'NO_AXIS_PTS_X'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            }
        ],
        'kwargs': [],
        'name': 'NO_AXIS_PTS_Y'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            }
        ],
        'kwargs': [],
        'name': 'NO_AXIS_PTS_Z'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            }
        ],
        'kwargs': [],
        'name': 'NO_RESCALE_X'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            }
        ],
        'kwargs': [],
        'name': 'NO_RESCALE_Y'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            }
        ],
        'kwargs': [],
        'name': 'NO_RESCALE_Z'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            }
        ],
        'kwargs': [],
        'name': 'OFFSET_X'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            }
        ],
        'kwargs': [],
        'name': 'OFFSET_Y'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            }
        ],
        'kwargs': [],
        'name': 'OFFSET_Z'
    },
    {
        'args': [],
        'kwargs': [
            {
                'multiple': True,
                'name': 'identifier',
                'type': 'Ident'
            }
        ],
        'name': 'OUT_MEASUREMENT'
    },
    {
        'args': [
            {
                'name': 'name',
                'type': 'Ident'
            },
            {
                'name': 'long_identifier',
                'type': 'String'
            }
        ],
        'kwargs': [
            {
                'name': 'HEADER',
                'type': 'HEADER'
            },
            {
                'multiple': True,
                'name': 'MODULE',
                'type': 'MODULE'
            }
        ],
        'name': 'PROJECT'
    },
    {
        'args': [
            {
                'name': 'name',
                'type': 'Ident'
            }
        ],
        'kwargs': [
            {
                'name': 'FNC_VALUES',
                'type': 'FNC_VALUES'
            },
            {
                'name': 'IDENTIFICATION',
                'type': 'IDENTIFICATION'
            },
            {
                'name': 'AXIS_PTS_X',
                'type': 'AXIS_PTS_X'
            },
            {
                'name': 'AXIS_PTS_Y',
                'type': 'AXIS_PTS_Y'
            },
            {
                'name': 'AXIS_PTS_Z',
                'type': 'AXIS_PTS_Z'
            },
            {
                'name': 'AXIS_RESCALE_X',
                'type': 'AXIS_RESCALE_X'
            },
            {
                'name': 'AXIS_RESCALE_Y',
                'type': 'AXIS_RESCALE_Y'
            },
            {
                'name': 'AXIS_RESCALE_Z',
                'type': 'AXIS_RESCALE_Z'
            },
            {
                'name': 'NO_AXIS_PTS_X',
                'type': 'NO_AXIS_PTS_X'
            },
            {
                'name': 'NO_AXIS_PTS_Y',
                'type': 'NO_AXIS_PTS_Y'
            },
            {
                'name': 'NO_AXIS_PTS_Z',
                'type': 'NO_AXIS_PTS_Z'
            },
            {
                'name': 'NO_RESCALE_X',
                'type': 'NO_RESCALE_X'
            },
            {
                'name': 'NO_RESCALE_Y',
                'type': 'NO_RESCALE_Y'
            },
            {
                'name': 'NO_RESCALE_Z',
                'type': 'NO_RESCALE_Z'
            },
            {
                'name': 'FIX_NO_AXIS_PTS_X',
                'type': 'FIX_NO_AXIS_PTS_X'
            },
            {
                'name': 'FIX_NO_AXIS_PTS_Y',
                'type': 'FIX_NO_AXIS_PTS_Y'
            },
            {
                'name': 'FIX_NO_AXIS_PTS_Z',
                'type': 'FIX_NO_AXIS_PTS_Z'
            },
            {
                'name': 'SRC_ADDR_X',
                'type': 'SRC_ADDR_X'
            },
            {
                'name': 'SRC_ADDR_Y',
                'type': 'SRC_ADDR_Y'
            },
            {
                'name': 'SRC_ADDR_Z',
                'type': 'SRC_ADDR_Z'
            },
            {
                'name': 'RIP_ADDR_X',
                'type': 'RIP_ADDR_X'
            },
            {
                'name': 'RIP_ADDR_Y',
                'type': 'RIP_ADDR_Y'
            },
            {
                'name': 'RIP_ADDR_Z',
                'type': 'RIP_ADDR_Z'
            },
            {
                'name': 'RIP_ADDR_W',
                'type': 'RIP_ADDR_W'
            },
            {
                'name': 'SHIFT_OP_X',
                'type': 'SHIFT_OP_X'
            },
            {
                'name': 'SHIFT_OP_Y',
                'type': 'SHIFT_OP_Y'
            },
            {
                'name': 'SHIFT_OP_Z',
                'type': 'SHIFT_OP_Z'
            },
            {
                'name': 'OFFSET_X',
                'type': 'OFFSET_X'
            },
            {
                'name': 'OFFSET_Y',
                'type': 'OFFSET_Y'
            },
            {
                'name': 'OFFSET_Z',
                'type': 'OFFSET_Z'
            },
            {
                'name': 'DIST_OP_X',
                'type': 'DIST_OP_X'
            },
            {
                'name': 'DIST_OP_Y',
                'type': 'DIST_OP_Y'
            },
            {
                'name': 'DIST_OP_Z',
                'type': 'DIST_OP_Z'
            },
            {
                'name': 'ALIGNMENT_BYTE',
                'type': 'ALIGNMENT_BYTE'
            },
            {
                'name': 'ALIGNMENT_WORD',
                'type': 'ALIGNMENT_WORD'
            },
            {
                'name': 'ALIGNMENT_LONG',
                'type': 'ALIGNMENT_LONG'
            },
            {
                'name': 'ALIGNMENT_FLOAT32_IEEE',
                'type': 'ALIGNMENT_FLOAT32_IEEE'
            },
            {
                'name': 'ALIGNMENT_FLOAT64_IEEE',
                'type': 'ALIGNMENT_FLOAT64_IEEE'
            },
            {
                'multiple': True,
                'name': 'RESERVED',
                'type': 'RESERVED'
            }
        ],
        'name': 'RECORD_LAYOUT'
    },
    {
        'args': [],
        'kwargs': [
            {
                'multiple': True,
                'name': 'identifier',
                'type': 'Ident'
            }
        ],
        'name': 'REF_CHARACTERISTIC'
    },
    {
        'args': [],
        'kwargs': [
            {
                'multiple': True,
                'name': 'identifier',
                'type': 'Ident'
            }
        ],
        'name': 'REF_GROUP'
    },
    {
        'args': [],
        'kwargs': [
            {
                'multiple': True,
                'name': 'identifier',
                'type': 'Ident'
            }
        ],
        'name': 'REF_MEASUREMENT'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_size',
                'type': 'DataSize'
            }
        ],
        'kwargs': [],
        'name': 'RESERVED'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            }
        ],
        'kwargs': [],
        'name': 'RIP_ADDR_W'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            }
        ],
        'kwargs': [],
        'name': 'RIP_ADDR_X'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            }
        ],
        'kwargs': [],
        'name': 'RIP_ADDR_Y'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            }
        ],
        'kwargs': [],
        'name': 'RIP_ADDR_Z'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            }
        ],
        'kwargs': [],
        'name': 'SHIFT_OP_X'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            }
        ],
        'kwargs': [],
        'name': 'SHIFT_OP_Y'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            }
        ],
        'kwargs': [],
        'name': 'SHIFT_OP_Z'
    },
    {
        'args': [
            {
                'name': 'length',
                'type': 'Int'
            },
            {
                'name': 'mass',
                'type': 'Int'
            },
            {
                'name': 'time',
                'type': 'Int'
            },
            {
                'name': 'electric_current',
                'type': 'Int'
            },
            {
                'name': 'temperature',
                'type': 'Int'
            },
            {
                'name': 'amount_of_substance',
                'type': 'Int'
            },
            {
                'name': 'luminous_intensity',
                'type': 'Int'
            }
        ],
        'kwargs': [],
        'name': 'SI_EXPONENTS'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            }
        ],
        'kwargs': [],
        'name': 'SRC_ADDR_X'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            }
        ],
        'kwargs': [],
        'name': 'SRC_ADDR_Y'
    },
    {
        'args': [
            {
                'name': 'position',
                'type': 'Int'
            },
            {
                'name': 'data_type',
                'type': 'DataType'
            }
        ],
        'kwargs': [],
        'name': 'SRC_ADDR_Z'
    },
    {
        'args': [],
        'kwargs': [
            {
                'multiple': True,
                'name': 'identifier',
                'type': 'Ident'
            }
        ],
        'name': 'SUB_FUNCTION'
    },
    {
        'args': [],
        'kwargs': [
            {
                'multiple': True,
                'name': 'identifier',
                'type': 'Ident'
            }
        ],
        'name': 'SUB_GROUP'
    },
    {
        'args': [
            {
                'name': 'name',
                'type': 'String'
            },
            {
                'name': 'value',
                'type': 'String'
            }
        ],
        'kwargs': [],
        'name': 'SYSTEM_CONSTANT'
    },
    {
        'args': [
            {
                'name': 'name',
                'type': 'Ident'
            },
            {
                'name': 'long_identifier',
                'type': 'String'
            },
            {
                'name': 'display',
                'type': 'String'
            },
            {
                'name': 'type',
                'type': 'enum_type'
            }
        ],
        'kwargs': [
            {
                'name': 'SI_EXPONENTS',
                'type': 'SI_EXPONENTS'
            },
            {
                'name': 'REF_UNIT',
                'type': 'REF_UNIT'
            },
            {
                'name': 'UNIT_CONVERSION',
                'type': 'UNIT_CONVERSION'
            }
        ],
        'name': 'UNIT'
    },
    {
        'args': [
            {
                'name': 'gradient',
                'type': 'Float'
            },
            {
                'name': 'offset',
                'type': 'Float'
            }
        ],
        'kwargs': [],
        'name': 'UNIT_CONVERSION'
    },
    {
        'args': [
            {
                'name': 'user_level_id',
                'type': 'Ident'
            }
        ],
        'kwargs': [
            {
                'multiple': True,
                'name': 'REF_GROUP',
                'type': 'REF_GROUP'
            },
            {
                'name': 'READ_ONLY',
                'type': 'READ_ONLY'
            }
        ],
        'name': 'USER_RIGHTS'
    },
    {
        'args': [],
        'kwargs': [
            {
                'name': 'VAR_SEPARATOR',
                'type': 'VAR_SEPARATOR'
            },
            {
                'name': 'VAR_NAMING',
                'type': 'VAR_NAMING'
            },
            {
                'multiple': True,
                'name': 'VAR_CRITERION',
                'type': 'VAR_CRITERION'
            },
            {
                'multiple': True,
                'name': 'VAR_FORBIDDEN_COMB',
                'type': 'VAR_FORBIDDEN_COMB'
            },
            {
                'multiple': True,
                'name': 'VAR_CHARACTERISTIC',
                'type': 'VAR_CHARACTERISTIC'
            }
        ],
        'name': 'VARIANT_CODING'
    },
    {
        'args': [],
        'kwargs': [
            {
                'multiple': True,
                'name': 'address',
                'type': 'Long'
            }
        ],
        'name': 'VAR_ADDRESS'
    },
    {
        'args': [
            {
                'name': 'name',
                'type': 'Ident'
            }
        ],
        'kwargs': [
            {
                'multiple': True,
                'name': 'criterion_name',
                'type': 'Ident'
            },
            {
                'name': 'VAR_ADDRESS',
                'type': 'VAR_ADDRESS'
            }
        ],
        'name': 'VAR_CHARACTERISTIC'
    },
    {
        'args': [
            {
                'name': 'name',
                'type': 'Ident'
            },
            {
                'name': 'long_identifier',
                'type': 'String'
            },
            {
                'name': 'value',
                'type': 'list'
            }
        ],
        'kwargs': [
            {
                'name': 'VAR_MEASUREMENT',
                'type': 'VAR_MEASUREMENT'
            },
            {
                'name': 'VAR_SELECTION_CHARACTERISTIC',
                'type': 'VAR_SELECTION_CHARACTERISTIC'
            }
        ],
        'name': 'VAR_CRITERION'
    },
    {
        'args': [],
        'kwargs': [
            {
                'multiple': True,
                'name': 'criterion',
                'type': 'ident_ident'
            }
        ],
        'name': 'VAR_FORBIDDEN_COMB'
    },
    {
        'args': [
            {
                'name': 'version_identifier',
                'type': 'String'
            }
        ],
        'kwargs': [],
        'name': 'VERSION'
    },
    {
        'args': [
            {
                'name': 'formula',
                'type': 'String'
            }
        ],
        'kwargs': [
            {
                'multiple': True,
                'name': 'characteristic',
                'type': 'indent'
            }
        ],
        'name': 'VIRTUAL_CHARACTERISTIC'
    },
    {
        'args': [
            {
                'name': 'bit_count',
                'type': 'Long'
            }
        ],
        'kwargs': [],
        'name': 'LEFT_SHIFT'
    },
    {
        'args': [
            {
                'name': 'bit_count',
                'type': 'Long'
            }
        ],
        'kwargs': [],
        'name': 'RIGHT_SHIFT'
    },
    {
        'args': [
            {
                'name': 'name',
                'type': 'Ident'
            }
        ],
        'kwargs': [],
        'name': 'REF_MEMORY_SEGMENT'
    },
    {
        'args': [
            {
                'name': 'lower_limit',
                'type': 'Float'
            },
            {
                'name': 'upper_limit',
                'type': 'Float'
            }
        ],
        'kwargs': [],
        'name': 'EXTENDED_LIMITS'
    },
    {
        'args': [
            {
                'name': 'type',
                'type': 'enum_type'
            }
        ],
        'kwargs': [],
        'name': 'CALIBRATION_ACCESS'
    },
    {
        'args': [
            {
                'name': 'curve_axis',
                'type': 'Ident'
            }
        ],
        'kwargs': [],
        'name': 'CURVE_AXIS_REF'
    },
    {
        'args': [
            {
                'name': 'extension',
                'type': 'Int'
            }
        ],
        'kwargs': [],
        'name': 'ECU_ADDRESS_EXTENSION'
    },
    {
        'args': [
            {
                'name': 'number',
                'type': 'Int'
            }
        ],
        'kwargs': [],
        'name': 'NUMBER'
    },
    {
        'args': [
            {
                'name': 'mask',
                'type': 'Long'
            }
        ],
        'kwargs': [],
        'name': 'BIT_MASK'
    },
    {
        'args': [
            {
                'name': 'unit',
                'type': 'Ident'
            }
        ],
        'kwargs': [],
        'name': 'REF_UNIT'
    },
    {
        'args': [
            {
                'name': 'conversion_table',
                'type': 'Ident'
            }
        ],
        'kwargs': [],
        'name': 'COMPU_TAB_REF'
    },
    {
        'args': [],
        'kwargs': [
            {
                'multiple': True,
                'name': 'name',
                'type': 'Ident'
            }
        ],
        'name': 'MAP_LIST'
    },
    {
        'args': [
            {
                'multiple': True,
                'name': 'display_string',
                'type': 'String'
            }
        ],
        'kwargs': [],
        'name': 'DEFAULT_VALUE'
    },
    {
        'args': [],
        'kwargs': [
            {
                'multiple': True,
                'name': 'handle',
                'type': 'Long'
            }
        ],
        'name': 'CALIBRATION_HANDLE'
    },
    {
        'args': [
            {
                'name': 'function',
                'type': 'String'
            }
        ],
        'kwargs': [],
        'name': 'FORMULA_INV'
    },
    {
        'args': [
            {
                'name': 'project_number',
                'type': 'Ident'
            }
        ],
        'kwargs': [],
        'name': 'PROJECT_NO'
    },
    {
        'args': [
            {
                'name': 'name',
                'type': 'Ident'
            }
        ],
        'kwargs': [],
        'name': 'S_REC_LAYOUT'
    },
    {
        'args': [
            {
                'name': 'separator',
                'type': 'String'
            }
        ],
        'kwargs': [],
        'name': 'VAR_SEPARATOR'
    },
    {
        'args': [
            {
                'name': 'tag',
                'type': 'enum_tag'
            }
        ],
        'kwargs': [],
        'name': 'VAR_NAMING'
    },
    {
        'args': [
            {
                'name': 'name',
                'type': 'Ident'
            }
        ],
        'kwargs': [],
        'name': 'VAR_MEASUREMENT'
    },
    {
        'args': [
            {
                'name': 'name',
                'type': 'Ident'
            }
        ],
        'kwargs': [],
        'name': 'VAR_SELECTION_CHARACTERISTIC'
    },
    {
        'args': [
            {
                'name': 'alignment_border',
                'type': 'Int'
            }
        ],
        'kwargs': [],
        'name': 'ALIGNMENT_BYTE'
    },
    {
        'args': [
            {
                'name': 'alignment_border',
                'type': 'Int'
            }
        ],
        'kwargs': [],
        'name': 'ALIGNMENT_WORD'
    },
    {
        'args': [
            {
                'name': 'alignment_border',
                'type': 'Int'
            }
        ],
        'kwargs': [],
        'name': 'ALIGNMENT_LONG'
    },
    {
        'args': [
            {
                'name': 'alignment_border',
                'type': 'Int'
            }
        ],
        'kwargs': [],
        'name': 'ALIGNMENT_FLOAT32_IEEE'
    },
    {
        'args': [
            {
                'name': 'alignment_border',
                'type': 'Int'
            }
        ],
        'kwargs': [],
        'name': 'ALIGNMENT_FLOAT64_IEEE'
    },
    {
        'args': [
            {
                'name': 'size',
                'type': 'Int'
            }
        ],
        'kwargs': [],
        'name': 'DATA_SIZE'
    },
    {
        'args': [
            {
                'name': 'address',
                'type': 'Long'
            }
        ],
        'kwargs': [],
        'name': 'ADDR_EPK'
    },
    {
        'args': [
            {
                'name': 'identifier',
                'type': 'String'
            }
        ],
        'kwargs': [],
        'name': 'EPK'
    },
    {
        'args': [
            {
                'name': 'manufacturer',
                'type': 'String'
            }
        ],
        'kwargs': [],
        'name': 'SUPPLIER'
    },
    {
        'args': [
            {
                'name': 'customer',
                'type': 'String'
            }
        ],
        'kwargs': [],
        'name': 'CUSTOMER'
    },
    {
        'args': [
            {
                'name': 'number',
                'type': 'String'
            }
        ],
        'kwargs': [],
        'name': 'CUSTOMER_NO'
    },
    {
        'args': [
            {
                'name': 'user_name',
                'type': 'String'
            }
        ],
        'kwargs': [],
        'name': 'USER'
    },
    {
        'args': [
            {
                'name': 'phone_number',
                'type': 'String'
            }
        ],
        'kwargs': [],
        'name': 'PHONE_NO'
    },
    {
        'args': [
            {
                'name': 'control_unit',
                'type': 'String'
            }
        ],
        'kwargs': [],
        'name': 'ECU'
    },
    {
        'args': [
            {
                'name': 'cpu_identifier',
                'type': 'String'
            }
        ],
        'kwargs': [],
        'name': 'CPU_TYPE'
    },
    {
        'args': [
            {
                'name': 'number_of_interfaces',
                'type': 'Int'
            }
        ],
        'kwargs': [],
        'name': 'NO_OF_INTERFACES'
    },
    {
        'args': [
            {
                'name': 'offset',
                'type': 'Long'
            }
        ],
        'kwargs': [],
        'name': 'ECU_CALIBRATION_OFFSET'
    },
    {
        'args': [
            {
                'name': 'version_identifier',
                'type': 'String'
            }
        ],
        'kwargs': [],
        'name': 'FUNCTION_VERSION'
    },
    {
        'args': [
            {
                'name': 'format_string',
                'type': 'String'
            }
        ],
        'kwargs': [],
        'name': 'FORMAT'
    }
]
keywords = ['FORMAT', 'READ_ONLY', 'SIGN_EXTEND', 'GUARD_RAILS', 'ROOT', 'READ_WRITE']
cls_template = """\"\"\"
@project: parser
@file: a2l_node.py
@author: Guillaume Sottas
@date: 05.04.2018
\"\"\"

from pya2l.parser.node import ASTNode, node_type
from pya2l.parser.type import *

enum_index_mode = Ident
enum_attribute = Ident
enum_type = Ident
enum_conversion_type = Ident
enum_prg_type = Ident
enum_memory_type = Ident
enum_mode = Ident
monotony_enum = Ident
enum_tag = Ident


class A2lNode(ASTNode):
    def __setattr__(self, key, value):
        if hasattr(self, key) and isinstance(getattr(self, key), String):
            value = String(value)
        return super(A2lNode, self).__setattr__(key, value)

    def dump(self, n=0):
        yield n, '/begin {node}'.format(node=self.node)
        for e in super(A2lNode, self).dump(n=n + 1):
            yield e
        yield n, '/end {node}'.format(node=self.node)


class A2lTagNode(A2lNode):
    def dump(self, n=0):
        yield n, '{node} {value}'.format(node=self.node, value=getattr(self, list(self.properties)[0]))


@node_type('a2l')
class A2lFile(A2lNode):
    __slots__ = 'asap2_version', 'a2ml_version', 'project'

    def __init__(self, args):
        self.asap2_version = None
        self.a2ml_version = None
        self.project = None
        super(A2lFile, self).__init__(*args)


@node_type('IF_DATA')
class IF_DATA(A2lNode):
    def __new__(cls, tag=None, value=None):
        cls.__slots__ = cls.__slots__ + tuple([tag])
        setattr(cls, tag, value)
        return super(IF_DATA, cls).__new__(cls)

    def __init__(self, tag=None, value=None):
        super(IF_DATA, self).__init__((tag, value))

    def dict(self):
        return dict((tag, getattr(self, tag).dict()) for tag in self.properties)

    def dump(self, n=0):
        for tag, value in ((t, getattr(self, t)) for t in self.properties):
            yield n, '/begin {node} {tag}'.format(node=self.node, tag=tag)
            for e in value.dump(n=n + 1):
                yield e
            yield n, '/end {node}'.format(node=self.node)


@node_type('A2ML')
class A2ML(A2lNode):
    def __new__(cls, a2ml):
        cls.__slots__ = tuple(['type_definition'] + list(b.tag for b in filter(lambda d: hasattr(d, 'tag'), a2ml)))
        setattr(cls, 'type_definition', list())
        for e in a2ml:
            if hasattr(e, 'tag'):
                setattr(cls, e.tag, e)
            # elif e not in getattr(cls, 'type_definition'):
            #     getattr(cls, 'type_definition').append(e)
        return super(A2ML, cls).__new__(cls)

    def __init__(self, a2ml):
        args = [('type_definition', d) for d in filter(lambda d: not hasattr(d, 'tag'), a2ml)]
        for block in filter(lambda d: hasattr(d, 'tag'), a2ml):
            args.append((block.tag, block))
        super(A2ML, self).__init__(*args)

    def dump(self, n=0):
        return (e for e in super(A2ML, self).dump(n=n))

{{#cls}}

@node_type('{{name}}')
{{^tagged}}
class {{name}}(A2lNode):
    __slots__ = {{#slots}}'{{name}}', {{/slots}}{{^slots}}tuple(){{/slots}}

    def __init__(self, {{#args}}{{name}}, {{/args}}{{#has_kwargs}}args{{/has_kwargs}}):
        {{#args}}
        self.{{name}} = {{type}}({{name}}){{#remark}}  # {{.}}{{/remark}}
        {{/args}}
        {{#kwargs}}
        {{#if_data}}
        self.{{name}} = dict()
        {{/if_data}}
        {{^if_data}}
        self.{{name}} = {{#multiple}}list(){{/multiple}}{{^multiple}}None{{/multiple}}{{#remark}}  # {{.}}{{/remark}}
        {{/if_data}}
        {{/kwargs}}
        super({{name}}, self).__init__({{#has_kwargs}}*args{{/has_kwargs}})
{{/tagged}}
{{#tagged}}
class {{name}}({{#args}}{{type}}{{/args}}):
    def __init__(self, {{#args}}{{name}}{{/args}}):
        super({{name}}, self).__init__(self, {{#args}}{{name}}{{/args}})

    @property
    def node(self):
        return self._node

    def __str__(self):
        return '{} {}'.format(self.node, super({{name}}, self).__str__())
{{/tagged}}

{{/cls}}"""

for cls_config in nodes:
    cls_config['name_lower'] = cls_config['name'].lower()
    if len(cls_config['args']) == 1 and len(cls_config['kwargs']) == 0:
        cls_config['tagged'] = True
    for arg in cls_config['args']:
        arg['name'] = arg['name'].lower()
    for arg in cls_config['kwargs']:
        if arg['name'] == 'IF_DATA':
            arg['if_data'] = True
        arg['name'] = arg['name'].lower()
    cls_config['slots'] = cls_config['args'] + cls_config['kwargs']
    cls_config['has_kwargs'] = len(cls_config['kwargs']) != 0

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'a2l_node.py'), 'w') as fp:
    fp.write(pystache.render(cls_template, dict(cls=sorted(nodes, key=lambda e: e['name']))))

cls_test_template = """
\"\"\"{{=<< >>=}}
@project: parser
@file: a2l_node_test.py
@author: Guillaume Sottas
@date: 13.02.2019
\"\"\"

import pytest
from pya2l.parser.a2l_node import *
from pya2l.parser.type import *


<<#keywords>>
<<.>> = (
    pytest.param('<<.>>', id='keyword <<.>> defined'),
    pytest.param('', id='keyword <<.>> not defined')
)

<</keywords>>

<<#cls>>
<<name_lower>>_string = '/begin <<name>><<#args>> {<<name>>}<</args>><<#kwargs>> {<<name>>}<</kwargs>> /end <<name>>'
<</cls>>

<<#cls>>
<<name_lower>> = pytest.param(<<name_lower>>_string,
    [<<#args>>('<<name>>', <<type>>), <</args>>],
    [<<#kwargs>>('<<name>>', <<type>>), <</kwargs>>])
<<name_lower>>_string = '/begin <<name>><<#args>> {<<name>>}<</args>><<#kwargs>> {<<name>>}<</kwargs>> /end <<name>>'

<</cls>>
"""

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'test.py'), 'w') as fp:
    fp.write(pystache.render(cls_test_template, dict(cls=sorted(nodes, key=lambda e: e['name']),
                                                     keywords=keywords)))
