from .base import BaseObject, base_object


@base_object()
class Definition(BaseObject):
    def __init__(self, name='', bit_size=None, signed=None, array_size=tuple()):
        super(Definition, self).__init__(name)
        self.name = name
        self.bit_size = bit_size
        self.signed = signed
        self.array_size = array_size
