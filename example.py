from pya2l.parser import A2lParser as Parser

a2l_string = """/begin PROJECT project_name "example project"
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

with Parser(a2l_string) as p:

    # get a list of available properties for a specific node.
    assert set(p.ast.PROJECT.properties) == {'Name', 'LongIdentifier', 'HEADER', 'MODULE'}

    # access nodes explicitly.
    assert p.ast.PROJECT.MODULE[0].CHARACTERISTIC[0].Name.Value == 'example_of_characteristic'
    assert p.ast.PROJECT.MODULE[0].CHARACTERISTIC[0].LowerLimit.Value == -4.5
    assert p.ast.PROJECT.MODULE[0].CHARACTERISTIC[0].UpperLimit.Value == 12.0

a2l_string = """/begin PROJECT project_name "example project"
    /begin MODULE first_module "first module long identifier"
    /end MODULE
/end PROJECT
"""

with Parser(a2l_string) as p:

    # convert node to json-formatted string.
    assert p.ast.json(indent=2, sort_keys=False) == """{
  "PROJECT": {
    "Name": {
      "Value": "project_name"
    },
    "LongIdentifier": {
      "Value": "example project"
    },
    "MODULE": [
      {
        "Name": {
          "Value": "first_module"
        },
        "LongIdentifier": {
          "Value": "first module long identifier"
        },
        "IF_DATA": [],
        "CHARACTERISTIC": [],
        "AXIS_PTS": [],
        "MEASUREMENT": [],
        "COMPU_METHOD": [],
        "COMPU_TAB": [],
        "COMPU_VTAB": [],
        "COMPU_VTAB_RANGE": [],
        "FUNCTION": [],
        "GROUP": [],
        "RECORD_LAYOUT": [],
        "USER_RIGHTS": [],
        "UNIT": []
      }
    ]
  }
}"""