from json import dumps
from pya2l.parser import A2lParser as Parser

a2l_string = """
    /begin PROJECT project_name "example project"
        /begin MODULE first_module "first module long identifier"
            /include "example.aml"
            /begin IF_DATA XCP
                /begin PROTOCOL_LAYER
                    89
                /end PROTOCOL_LAYER
            /end IF_DATA
            /begin IF_DATA CUSTOM
                E1
            /end IF_DATA
            /begin CHARACTERISTIC
                example_of_characteristic
                "first characteristic long identifier"
                VALUE
                0
                DAMOS_SST
                0
                first_characteristic_conversion
                -4.5
                12.0
            /end CHARACTERISTIC
        /end MODULE
    /end PROJECT
"""

p = Parser(a2l_string)

# get a list of available properties for a specific node.
assert set(p.ast.project.properties) == set(['name', 'module', 'header', 'long_identifier'])

# access nodes explicitly.
assert p.ast.project.module[0].characteristic[0].name == 'example_of_characteristic'
assert p.ast.project.module[0].characteristic[0].lower_limit == -4.5
assert p.ast.project.module[0].characteristic[0].upper_limit == 12.0

# access nodes by type.
assert p.nodes('CHARACTERISTIC')[0].name == 'example_of_characteristic'

# convert node to dictionary (the a2ml description is removed for readability).
ast = p.ast.dict()
ast['project']['module'][0].pop('a2ml')
assert dumps(ast, sort_keys=True, indent=1) == """{
 "a2ml_version": null, 
 "asap2_version": null, 
 "node": "a2l", 
 "project": {
  "header": null, 
  "long_identifier": "example project", 
  "module": [
   {
    "axis_pts": [], 
    "characteristic": [
     {
      "address": 0, 
      "annotation": [], 
      "axis_descr": [], 
      "bit_mask": null, 
      "byte_order": null, 
      "calibration_access": null, 
      "comparison_quantity": null, 
      "conversion": "first_characteristic_conversion", 
      "dependent_characteristic": null, 
      "deposit": "DAMOS_SST", 
      "display_identifier": null, 
      "ecu_address_extension": null, 
      "extended_limits": null, 
      "format": null, 
      "function_list": null, 
      "guard_rails": null, 
      "if_data": {}, 
      "long_identifier": "first characteristic long identifier", 
      "lower_limit": -4.5, 
      "map_list": null, 
      "matrix_dim": null, 
      "max_diff": 0, 
      "max_refresh": null, 
      "name": "example_of_characteristic", 
      "node": "CHARACTERISTIC", 
      "number": null, 
      "read_only": null, 
      "ref_memory_segment": null, 
      "type": "VALUE", 
      "upper_limit": 12.0, 
      "virtual_characteristic": null
     }
    ], 
    "compu_method": [], 
    "compu_tab": [], 
    "compu_vtab": [], 
    "compu_vtab_range": [], 
    "frame": null, 
    "function": [], 
    "group": [], 
    "if_data": {
     "CUSTOM": {
      "0": "E1"
     }, 
     "XCP": {
      "PROTOCOL_LAYER": {
       "0": 89
      }
     }
    }, 
    "long_identifier": "first module long identifier", 
    "measurement": [], 
    "mod_common": null, 
    "mod_par": null, 
    "name": "first_module", 
    "node": "MODULE", 
    "record_layout": [], 
    "unit": [], 
    "user_rights": [], 
    "variant_coding": null
   }
  ], 
  "name": "project_name", 
  "node": "PROJECT"
 }
}"""

# modify and write sequence.
p.ast.project.long_identifier = 'modified example project'
assert p.dump(indent=1) == """/begin PROJECT
 project_name
 "modified example project"
 /begin MODULE
  first_module
  "first module long identifier"
  /begin A2ML
   taggedstruct protocol_layer {
    block "PROTOCOL_LAYER"
    struct {
     uint;
    };
   };
   enum custom_enum {
    "E1" = 0,
    "E2" = 2
   };
   block "IF_DATA"
   taggedunion {
    "XCP"
    struct {
     taggedstruct protocol_layer;
    };
    "CUSTOM"
    struct {
     enum custom_enum;
    };
   };
  /end A2ML
  /begin IF_DATA XCP
   /begin PROTOCOL_LAYER
    89
   /end PROTOCOL_LAYER
  /end IF_DATA
  /begin IF_DATA CUSTOM
   E1
  /end IF_DATA
  /begin CHARACTERISTIC
   example_of_characteristic
   "first characteristic long identifier"
   VALUE
   0
   DAMOS_SST
   0
   first_characteristic_conversion
   -4.5
   12.0
  /end CHARACTERISTIC
 /end MODULE
/end PROJECT"""
