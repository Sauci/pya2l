"""
@project: parser
@file: common.py
@author: Guillaume Sottas
@date: 31.12.2018
"""

from pya2l.parser.type import String


class ASTNode(object):
    __slots__ = '_node', '_parent', '_children'

    def __init__(self, *args, **kwargs):
        self.parent = None
        self.children = list()
        for attribute, value in args:
            attr = getattr(self, attribute)
            if isinstance(attr, list):
                attr.append(value)
            else:
                setattr(self, attribute, value)
            if isinstance(value, ASTNode):
                value.parent = self
                self.add_children(value)

    def __eq__(self, other):
        if not isinstance(other, ASTNode):
            return False
        if len(set(self.properties) ^ set(other.properties)):
            return False
        for s in set(self.properties):
            if getattr(self, s) != getattr(other, s):
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def add_children(self, a2l_node):
        self._children.append(a2l_node)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, node):
        self._parent = node

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, value):
        self._children = value

    @property
    def node(self):
        return self._node

    def nodes(self, node_name):
        nodes = list()
        for node in self.children:
            if node.node == node_name:
                nodes.append(node)
            nodes += node.nodes(node_name)
        return nodes

    def dict(self):
        result = dict(node=self.node)
        for p in self.properties:
            v = getattr(self, p)
            if isinstance(v, ASTNode):
                result[p] = v.dict()
            elif isinstance(v, list):
                result[p] = list()
                for e in v:
                    if isinstance(e, ASTNode):
                        result[p].append(e.dict())
                    else:
                        result[p].append(e)
            else:
                result[p] = v
        return result

    def dump(self, n=0):
        for p, v in ((k, getattr(self, k)) for k in self.properties):
            if v in (None, list()):
                continue
            if isinstance(v, ASTNode):
                for e in v.dump(n=n):
                    yield e
            elif isinstance(v, list):
                for node in v:
                    if isinstance(node, ASTNode):
                        for e in node.dump(n=n):
                            yield e
                    else:
                        yield n, '{q}{string}{q}'.format(string=v, q='"' if isinstance(v, String) else '')
            elif isinstance(v, dict):
                continue
            else:
                yield n, '{q}{string}{q}'.format(string=v, q='"' if type(v) is String else '')

    @property
    def properties(self):
        return (p for p in self.__slots__ if not p.startswith('_'))


node_to_class = dict()


def node_type(node_type):
    def wrapper(cls):
        node_to_class[node_type] = cls
        cls._node = node_type
        return cls

    return wrapper


def node_factory(node_type, *args, **kwargs):
    return node_to_class[node_type](*args, **kwargs)
