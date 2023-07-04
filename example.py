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

with Parser() as p:
    # get the AST.
    ast = p.tree_from_a2l(a2l_string.encode())

    # get a list of available properties for a specific node.
    assert set(ast.PROJECT.properties) == {'Name', 'LongIdentifier', 'HEADER', 'MODULE'}

    # access nodes explicitly.
    assert ast.PROJECT.MODULE[0].CHARACTERISTIC[0].Name.Value == 'example_of_characteristic'
    assert ast.PROJECT.MODULE[0].CHARACTERISTIC[0].LowerLimit.Value == -4.5
    assert ast.PROJECT.MODULE[0].CHARACTERISTIC[0].UpperLimit.Value == 12.0

a2l_string = """/begin PROJECT project_name "example project"
    /begin MODULE first_module "first module long identifier"
    /end MODULE
/end PROJECT
"""

with Parser() as p:
    # get the AST.
    ast = p.tree_from_a2l(a2l_string.encode())

    # convert node to json-formatted string.
    assert p.json_from_tree(ast, indent=2).decode() == """{
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
        }
      }
    ]
  }
}"""