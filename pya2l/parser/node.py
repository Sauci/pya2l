"""
@project: parser
@file: common.py
@author: Guillaume Sottas
@date: 31.12.2018
"""


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

    @property
    def json(self):
        tmp = dict(node=self.node)
        for p in self.properties:
            v = getattr(self, p)
            if isinstance(v, ASTNode):
                tmp[p] = v.json
            elif isinstance(v, list):
                tmp[p] = list()
                for e in v:
                    if isinstance(e, ASTNode):
                        tmp[p].append(e.json)
                    else:
                        tmp[p].append(e)
            else:
                tmp[p] = v
        return tmp

    @property
    def properties(self):
        return (p for p in self.__slots__ if not p.startswith('_'))
