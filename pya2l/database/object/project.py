from .base import BaseObject, base_object


@base_object()
class Project(BaseObject):
    def __init__(self, name, components=None):
        super(Project, self).__init__(name)
        self.name = name
        if components is not None:
            self.components = components
        else:
            self.components = list()
