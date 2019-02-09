from pya2l.parser import A2lParser as Parser

a2l_string = """
    /begin PROJECT project_name "example project"
        /begin MODULE first_module "first module long identifier"
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
assert p.get_node('CHARACTERISTIC')[0].name == 'example_of_characteristic'

# instantiate custom class for specified node.
from pya2l.parser.grammar.a2l_node import Characteristic


class CustomCharacteristic(Characteristic):
    def node(self):
        return 'my custom ' + super(CustomCharacteristic, self).node


p = Parser(a2l_string, CHARACTERISTIC=CustomCharacteristic)

assert isinstance(p.ast.project.module[0].characteristic[0], CustomCharacteristic)
assert p.ast.project.module[0].characteristic[0].node() == 'my custom CHARACTERISTIC'

# convert node to json-formatted string.
from json import dumps as python_object_to_json_string

p = Parser("""
    /begin PROJECT project_name "example project"
        /begin MODULE first_module "first module long identifier"
            /include "example.aml"
            /begin IF_DATA XCP
                /begin PROTOCOL_LAYER
                    89
                /end PROTOCOL_LAYER
            /end IF_DATA
        /end MODULE
    /end PROJECT
    """)

assert python_object_to_json_string(p.ast.project.json, sort_keys=True, indent=1) == """{
 "header": null, 
 "long_identifier": "example project", 
 "module": [
  {
   "a2ml": [
    {
     "definition": {
      "node": "block", 
      "tag": "IF_DATA", 
      "type_name": {
       "member": [
        {
         "member": {
          "array_specifier": null, 
          "node": "a2ml_member", 
          "type_name": {
           "member": [
            {
             "member": {
              "array_specifier": null, 
              "node": "a2ml_member", 
              "type_name": {
               "member": [
                {
                 "multiple": false, 
                 "node": "a2ml_taggedstruct_member", 
                 "type_name": {
                  "node": "block", 
                  "tag": "PROTOCOL_LAYER", 
                  "type_name": {
                   "member": [
                    {
                     "member": {
                      "array_specifier": null, 
                      "node": "a2ml_member", 
                      "type_name": {
                       "node": "int", 
                       "type_name": "uint"
                      }
                     }, 
                     "node": "a2ml_struct_member"
                    }
                   ], 
                   "node": "a2ml_struct_type_name"
                  }
                 }
                }
               ], 
               "node": "a2ml_taggedstruct_type_name"
              }
             }, 
             "node": "a2ml_struct_member"
            }
           ], 
           "node": "a2ml_struct_type_name"
          }
         }, 
         "node": "a2ml_taggedunion_member", 
         "tag": "XCP"
        }
       ], 
       "node": "a2ml_taggedunion_type_name"
      }
     }, 
     "node": "a2ml_declaration"
    }
   ], 
   "axis_pts": [], 
   "characteristic": [], 
   "compu_method": [], 
   "compu_tab": [], 
   "compu_vtab": [], 
   "compu_vtab_range": [], 
   "frame": null, 
   "function": [], 
   "group": [], 
   "if_data": {
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
}"""
