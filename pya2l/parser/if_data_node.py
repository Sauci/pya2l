"""
@project: parser
@file: if_data_node.py
@author: Guillaume Sottas
@date: 12.02.2019
"""

from itertools import chain


class A2MLTaggedNode(object):
    def __new__(cls, args=tuple(), kwargs=dict()):
        for item in kwargs.items():
            setattr(cls, *item)
        cls.__slots__ = tuple(kwargs.keys())
        cls.__index__ = tuple(args)
        return super(A2MLTaggedNode, cls).__new__(cls)

    def keywords(self):
        for parameter in self.__slots__:
            yield parameter, getattr(self, parameter)

    def positionals(self):
        for parameter in self.__index__:
            yield parameter

    def dict(self):
        result = dict()
        for k, v in chain(enumerate(self.positionals()), self.keywords()):
            if isinstance(v, A2MLTaggedNode):
                result[k] = v.dict()
            else:
                result[k] = v
        return result

    def dump(self, n=0):
        result = ''
        for k, v in enumerate(self.positionals()):
            if isinstance(v, A2MLTaggedNode):
                result += v.dump(indent, lt, n=n + 1)
            else:
                result += str(v)
        for k, v in self.keywords():
            try:
                result += v.dump(indent, lt, n=n + 1)
            except AttributeError:
                result += str(v)
        return result


class Struct(A2MLTaggedNode):
    def dump(self, n=0):
        for v in self.positionals():
            if isinstance(v, A2MLTaggedNode):
                for e in v.dump(n=n + 1):
                    yield e
            else:
                yield n, str(v)
        for k, v in self.keywords():
            if isinstance(v, A2MLTaggedNode):
                yield n, '/begin {tag}'.format(tag=k)
                for e in v.dump(n=n + 1):
                    yield e
                yield n, '/end {tag}'.format(tag=k)
            else:
                yield n, '{tag} {v}'.format(tag=k, v=str(v))


class TaggedStruct(A2MLTaggedNode):
    def dump(self, n=0):
        raise Exception(self.__class__.__name__)
        return ''


class TaggedUnion(A2MLTaggedNode):
    def dump(self, n=0):
        raise Exception(self.__class__.__name__)
        return ''

    def dict(self):
        raise Exception(self.__class__.__name__)
        return ''


class Member(A2MLTaggedNode):
    def dump(self, n=0):
        raise Exception(self.__class__.__name__)
        return ''
