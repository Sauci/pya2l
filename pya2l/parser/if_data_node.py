"""
@project: pya2l
@file: if_data_node.py
@author: Guillaume Sottas
@date: 12.02.2019
"""

from itertools import chain


class AmlDynNode(object):
    __slots__ = 'args', 'kwargs'

    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs

    def __repr__(self):
        return ' '.join(s.__repr__() for s in self.args) + \
               (' ' if len(self.kwargs) else '') + \
               ' '.join(str(k) + '=' + v.__repr__() for k, v in self.kwargs.items())

    def __eq__(self, other):
        if isinstance(other, (tuple, list)) and len(self.kwargs) == 0 and self.args == other:
            return True
        elif isinstance(other, dict) and len(self.args) == 0 and self.kwargs == other.kwargs:
            return True
        elif isinstance(other, AmlDynNode) and self.args == other.args and self.kwargs == other.kwargs:
            return True
        return False

    def __getitem__(self, item):
        return self.args[item]

    def __getattr__(self, item):
        return self.kwargs[item]

    @property
    def properties(self):
        return self.kwargs.keys()

    def positionals(self):
        for parameter in self.args:
            yield parameter

    def keywords(self):
        for parameter in self.kwargs:
            yield parameter, getattr(self, parameter)

    def dict(self):
        result = dict()
        for k, v in chain(enumerate(self.positionals()), self.keywords()):
            if isinstance(v, AmlDynNode):
                result[k] = v.dict()
            else:
                result[k] = v
        return result

    def dump(self, n=0):
        for v in self.positionals():
            if isinstance(v, AmlDynNode):
                for e in v.dump(n=n + 1):
                    yield e
            else:
                yield n, str(v)
        for k, v in self.keywords():
            if isinstance(v, AmlDynNode):
                yield n, '/begin {tag}'.format(tag=k)
                for e in v.dump(n=n + 1):
                    yield e
                yield n, '/end {tag}'.format(tag=k)
            else:
                yield n, '{tag} {v}'.format(tag=k, v=str(v))


class AmlDynStruct(AmlDynNode):
    pass
