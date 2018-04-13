## package description
the purpose of this package is to provide an easy way to access and navigate in [a2l](https://www.asam.net/standards/detail/mcd-2-mc/) file content.  
once the file has been loaded, a tree of Python objects is generated, allowing the user to easily access nodes.  
  
## installation  
  
### using `pip`
install the package by running the following command:  
`pip install git+https://github.com/Sauci/pya2l.git@master`  
  
### from source
this package uses [ply](https://pypi.python.org/pypi/ply) package. if it is not already installed, install it first.  
once the above prerequisite is installed:
- download the [pya2l](https://github.com/Sauci/pya2l/archive/master.zip) package  
- unzip it  
- move to the directory containing the setup.py file  
- run the command `python setup.py install`

**note:** the above command might require privileged access to succeed.
  
## example of usage  
the bellow code snippet shows how an a2l-formatted string can be accessed using this package.  

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

a2l = Parser(a2l_string)
assert a2l.tree.project.module[0].characteristic[0].name == 'example_of_characteristic'
assert a2l.tree.project.module[0].characteristic[0].lower_limit == -4.5
assert a2l.tree.project.module[0].characteristic[0].upper_limit == 12.0
```
