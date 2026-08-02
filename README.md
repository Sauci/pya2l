# pya2l

|                         branch                         |                                                                                build                                                                                 |                                                                         coverage                                                                         |
|:------------------------------------------------------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------:|
|  [master](https://github.com/Sauci/pya2l/tree/master)  | [![Python package](https://github.com/Sauci/pya2l/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/Sauci/pya2l/actions/workflows/build.yml)  |  [![code coverage](https://codecov.io/gh/Sauci/pya2l/branch/master/graphs/badge.svg?token=Q5aceZRFXh)](https://codecov.io/gh/Sauci/pya2l?branch=master)  |
| [develop](https://github.com/Sauci/pya2l/tree/develop) | [![Python package](https://github.com/Sauci/pya2l/actions/workflows/build.yml/badge.svg?branch=develop)](https://github.com/Sauci/pya2l/actions/workflows/build.yml) | [![code coverage](https://codecov.io/gh/Sauci/pya2l/branch/develop/graphs/badge.svg?token=Q5aceZRFXh)](https://codecov.io/gh/Sauci/pya2l?branch=develop) |

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://raw.githubusercontent.com/Sauci/pya2l/master/LICENSE.md) [![Gitter](https://img.shields.io/gitter/room/Sauci/pya2l.svg)](https://gitter.im/pya2l/Lobby)

## Package description

The purpose of this package is to provide an easy way to access and navigate
an [A2L](https://www.asam.net/standards/detail/mcd-2-mc/)-formatted file.  
Once the file has been loaded, a tree of Python objects is generated, allowing the user to access nodes.

## Installation

### Using *pip*

Install the latest released version of the package by running the following command:
`pip install pya2l`

or install the most recent version of the package (master branch) by running the following command:
`pip install git+https://github.com/Sauci/pya2l.git@master`

## Supported platforms

The A2L document itself is processed by the [a2l-grpc](https://github.com/Sauci/a2l-grpc) backend, whose shared objects
are distributed with this package. The one matching the host is selected at runtime, which means that a 32-bit
interpreter running on a 64-bit machine loads the 32-bit shared object.

| operating system | architecture | shared object                 | tested in CI        |
|:-----------------|:-------------|:------------------------------|:--------------------|
| Linux            | x86-64       | `a2l_grpc_linux_amd64.so`     | Python 3.9 to 3.13  |
| Linux            | x86 (32-bit) | `a2l_grpc_linux_386.so`       | no runner available |
| Linux            | ARM64        | `a2l_grpc_linux_arm64.so`     | Python 3.9 to 3.13  |
| Linux            | ARM (32-bit) | `a2l_grpc_linux_arm.so`       | no runner available |
| Windows          | x86-64       | `a2l_grpc_windows_amd64.dll`  | Python 3.9 to 3.13  |
| Windows          | x86 (32-bit) | `a2l_grpc_windows_386.dll`    | Python 3.9 to 3.13  |
| Windows          | ARM64        | `a2l_grpc_windows_arm64.dll`  | no wheel available  |
| macOS            | x86-64       | `a2l_grpc_darwin_amd64.dylib` | Python 3.9 to 3.13  |
| macOS            | ARM64        | `a2l_grpc_darwin_arm64.dylib` | Python 3.9 to 3.13  |

The two Linux platforms which are not covered by the continuous integration are supported, but no GitHub-hosted runner
is available to test them.

On Windows ARM64, the `grpcio` dependency of this package provides no wheel for the ARM64 interpreter, and its build
from source currently fails on that platform (see [grpc#39064](https://github.com/grpc/grpc/issues/39064)). Until such
a wheel is published, this package can only be used with an x86-64 interpreter, which runs under emulation and
therefore loads the `a2l_grpc_windows_amd64.dll` shared object. This is what the continuous integration does on the
Windows ARM64 runner, which means that the `a2l_grpc_windows_arm64.dll` shared object is currently not covered by any
test.

## Example of usage

### Command line tool

Once the package is installed, the `pya2l` command is available. It provides several different commands:

- Convert an A2L file to JSON with `pya2l -v <source>.a2l to_json -o <output>.json -i 2`
- Convert an A2L file to A2L with `pya2l -v <source>.a2l to_a2l -o <output>.a2l -i 2`
- Convert a JSON-formatted A2L file to JSON with `pya2l -v <source>.json to_json -o <output>.json -i 2`
- Convert a JSON-formatted A2L file to A2L with `pya2l -v <source>.json to_a2l -o <output>.a2l -i 2`

Adding the `-c` option to any of the above commands rejects files which use keywords requiring a newer ASAP2 version
than the one declared by the file itself. Without this option, such keywords are reported as warnings, which are
displayed with the `-v` option.

### Python API

The code snippet below shows how the properties of a node in an A2L string can be retrieved with this package.

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

### Error handling and ASAP2 version check

When the backend is unable to convert a document, an `A2lError` exception is raised, containing the reason for the
failure.

Keywords requiring a more recent ASAP2 version than the one declared by the file are reported in the `warnings`
property of the parser. They can be treated as errors by setting the `enforce_version_check` argument.

```python
from pya2l.parser import A2lError, A2lParser as Parser

a2l_string = """ASAP2_VERSION 1 50
/begin PROJECT project_name "example project"
    /begin MODULE first_module "first module long identifier"
        /begin MOD_COMMON "example of mod common"
            ALIGNMENT_INT64 8
        /end MOD_COMMON
    /end MODULE
/end PROJECT
"""

with Parser() as p:
    # ALIGNMENT_INT64 requires ASAP2 version 1.60, it is only reported as a warning.
    ast = p.tree_from_a2l(a2l_string.encode())
    assert len(p.warnings) == 1
    assert 'ALIGNMENT_INT64' in p.warnings[0]

    # the same content is rejected when the version check is enforced.
    try:
        p.tree_from_a2l(a2l_string.encode(), enforce_version_check=True)
        raise AssertionError('the above call should have raised an A2lError exception')
    except A2lError as e:
        assert 'ALIGNMENT_INT64' in str(e)
```
