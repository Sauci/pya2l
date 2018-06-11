from .base import BaseObject, base_object


@base_object()
class Declaration(BaseObject):
    def __init__(self, name, definition=None, conditions=None):
        super(Declaration, self).__init__(name)
        self.name = name
        if definition is not None:
            self.definition = definition
        else:
            self.definition = None
        if conditions is not None:
            self.conditions = conditions
        else:
            self.conditions = list()
