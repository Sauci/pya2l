from .base import BaseObject, base_object


@base_object()
class Component(BaseObject):
    def __init__(self, name, declarations=None):
        super(Component, self).__init__(name)
        self.name = name
        if declarations:
            self.declarations = declarations
        else:
            self.declarations = list()
