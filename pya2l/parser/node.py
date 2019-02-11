"""
@project: parser
@file: common.py
@author: Guillaume Sottas
@date: 31.12.2018
"""

from json import dumps as json_dump
from pya2l.parser.type import String


class ASTNode(object):
    __slots__ = '_node', '_parent', '_children'

    def __init__(self, *args, **kwargs):
        if not isinstance(self.__slots__, tuple):
            raise ValueError('__slot__ attribute must be a tuple (maybe \',\' is missing at the end?).')
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
        if len(set(self.__slots__) ^ set(other.__slots__)):
            return False
        for s in set(self.__slots__) - {'line'}:
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
        yield n, '/begin {node}'.format(node=self.node)
        for p, v in ((k, getattr(self, k)) for k in self.properties):
            if v in (None, list()) and not self.node == 'IF_DATA':
                continue
            if isinstance(v, ASTNode):
                try:
                    for e in v.dump(n=n + 1):
                        yield e
                except TypeError as e:
                    raise e
            elif isinstance(v, list):
                for e in v:
                    if isinstance(e, ASTNode):
                        for e in e.dump(n=n + 1):
                            yield e
                    else:
                        yield n + 1, '{q}{string}{q}'.format(string=v, q='"' if isinstance(v, String) else '')
            elif isinstance(v, dict):
                continue
            else:
                yield n + 1, '{q}{string}{q}'.format(string=v, q='"' if isinstance(v, String) else '')
        yield n, '/end {node}'.format(node=self.node)

    def __setattr__(self, key, value):
        if hasattr(self, key) and isinstance(getattr(self, key), String):
            value = String(value)
        return super(ASTNode, self).__setattr__(key, value)

    @property
    def properties(self):
        return (p for p in self.__slots__ if not p.startswith('_'))
