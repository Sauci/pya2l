|                         branch                         |                                                                                build                                                                                 |                                                                         coverage                                                                         |
|:------------------------------------------------------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------:|
|  [master](https://github.com/Sauci/pya2l/tree/master)  | [![Python package](https://github.com/Sauci/pya2l/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/Sauci/pya2l/actions/workflows/build.yml)  |  [![code coverage](https://codecov.io/gh/Sauci/pya2l/branch/master/graphs/badge.svg?token=Q5aceZRFXh)](https://codecov.io/gh/Sauci/pya2l?branch=master)  |
| [develop](https://github.com/Sauci/pya2l/tree/develop) | [![Python package](https://github.com/Sauci/pya2l/actions/workflows/build.yml/badge.svg?branch=develop)](https://github.com/Sauci/pya2l/actions/workflows/build.yml) | [![code coverage](https://codecov.io/gh/Sauci/pya2l/branch/develop/graphs/badge.svg?token=Q5aceZRFXh)](https://codecov.io/gh/Sauci/pya2l?branch=develop) |

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://raw.githubusercontent.com/Sauci/pya2l/master/LICENSE.md) [![Gitter](https://img.shields.io/gitter/room/Sauci/pya2l.svg)](https://gitter.im/pya2l/Lobby)

## Package description

the purpose of this package is to provide an easy way to access and navigate
in [a2l](https://www.asam.net/standards/detail/mcd-2-mc/) formatted file.  
once the file has been loaded, a tree of Python objects is generated, allowing the user to access nodes.

## Installation

### Using *pip*

Install the last released version of the package by running the following command:
`pip install pya2l`

or install the most recent version of the package (master branch) by running the following command:
`pip install git+https://github.com/Sauci/pya2l.git@master`

## Example of usage

### Command line tool

Once the package installed, the `pya2l` command will be available. It provides several different commands:

- Convert an A2L file to JSON with `pya2l -v <source>.a2l to_json -o <output.json> -i 2`
- Convert an A2L file to A2L with `pya2l -v <source.a2l> to_a2l -o <output.a2l> -i 2`
- Convert a JSON-formatted A2L file to JSON with `pya2l -v <source>.json to_json -o <output.json> -i 2`
- Convert a JSON-formatted A2L file to A2L with `pya2l -v <source>.json to_a2l -o <output.a2l> -i 2`

### Python API

the bellow code snippet shows how properties of a node in an a2l string can be retrieved using this package.

```python
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
```
