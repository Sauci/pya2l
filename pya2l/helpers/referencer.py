from .module import Module


class Referencer(object):
    def __init__(self, module: Module) -> None:
        self._module = module
