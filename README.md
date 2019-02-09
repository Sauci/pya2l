
| branch  | build  | coverage |
|:-------:|:------:| :-------:|
| [master](https://github.com/Sauci/pya2l/tree/master)   | [![tests status](https://travis-ci.org/Sauci/pya2l.svg?branch=master)](https://travis-ci.org/Sauci/pya2l) [![Build status](https://ci.appveyor.com/api/projects/status/wwq1r9y3ot0d6lea/branch/master?svg=true)](https://ci.appveyor.com/project/Sauci/pya2l/branch/develop) | [![code coverage](https://codecov.io/gh/Sauci/pya2l/branch/master/graph/badge.svg?token=Q5aceZRFXh)](https://codecov.io/gh/Sauci/pya2l)  |
| [develop](https://github.com/Sauci/pya2l/tree/develop) | [![tests status](https://travis-ci.org/Sauci/pya2l.svg?branch=develop)](https://travis-ci.org/Sauci/pya2l) [![Build status](https://ci.appveyor.com/api/projects/status/wwq1r9y3ot0d6lea/branch/develop?svg=true)](https://ci.appveyor.com/project/Sauci/pya2l/branch/develop) | [![code coverage](https://codecov.io/gh/Sauci/pya2l/branch/develop/graph/badge.svg?token=Q5aceZRFXh)](https://codecov.io/gh/Sauci/pya2l) |

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://raw.githubusercontent.com/Sauci/pya2l/master/LICENSE.md) [![Gitter](https://img.shields.io/gitter/room/Sauci/pya2l.svg)](https://gitter.im/pya2l/Lobby)

## package description
the purpose of this package is to provide an easy way to access and navigate in [a2l](https://www.asam.net/standards/detail/mcd-2-mc/) formatted file.  
once the file has been loaded, a tree of Python objects is generated, allowing the user to access nodes.  
  
## installation  
  
### using `pip`
install the most recent version of the package (master branch) by running the following command:
`pip install git+https://github.com/Sauci/pya2l.git@master`

or install the last released version of the package by running the following command:
`pip install pya2l`
  
### from source
this package uses [ply](https://pypi.python.org/pypi/ply) package. if it is not already installed, install it first.  
once the above prerequisite is installed:
- download the [pya2l](https://github.com/Sauci/pya2l/archive/master.zip) package  
- unzip it  
- move to the directory containing the setup.py file  
- run the command `python setup.py install`

**note:** the above command might require privileged access to succeed.
  
## example of usage  
the bellow code snippet shows how properties of a node in an a2l string can be retrieved using this package.  

```python
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
        /end MODULE
    /end PROJECT
    """)

assert python_object_to_json_string(p.ast.project.json, sort_keys=True, indent=4) == """{
    "header": null,
    "long_identifier": "example project",
    "module": [
        {
            "a2ml": null,
            "axis_pts": [],
            "characteristic": [],
            "compu_method": [],
            "compu_tab": [],
            "compu_vtab": [],
            "compu_vtab_range": [],
            "frame": null,
            "function": [],
            "group": [],
            "if_data": [],
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

```

## limitations
currently, the a2ml-formatted content is only described in the grammar, but the content of the node cannot be
accessed as described above.

[![HitCount](http://hits.dwyl.io/Sauci/pya2l.svg)](http://hits.dwyl.io/Sauci/pya2l)
