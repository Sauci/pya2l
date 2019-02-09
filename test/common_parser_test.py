"""
@project: parser
@file: a2ml_parser_test.py
@author: Guillaume Sottas
@date: 28.12.2018
"""

import pytest

from pya2l.parser.grammar.common import ASTNode


def test_node_equality_operator():
    class A(ASTNode):
        __slots__ = 'a',

        def __init__(self, a):
            self.a = a
            super(A, self).__init__()

    class B(ASTNode):
        __slots__ = 'b',

        def __init__(self, b):
            self.b = b
            super(B, self).__init__()

    assert A(0) != B(0)

    class C(ASTNode):
        __slots__ = 'a',

        def __init__(self, a):
            self.a = a
            super(C, self).__init__()

    assert C(0) != C(1)
    assert C(0) == C(0)
    assert A(0) == C(0)


def test_invalid_slot_property_exception():
    class InvalidNode(ASTNode):
        __slots__ = 'property_value'

        def __init__(self, property_value):
            self.property_value = property_value
            super(InvalidNode, self).__init__(0, 0)

    with pytest.raises(ValueError, message='__slot__ attribute must be a list (maybe \',\' is missing at the end?).'):
        InvalidNode(1)


def test_get_json():
    class A(ASTNode):
        _node = 'A'
        __slots__ = 'prop', 'sub_node'

        def __init__(self, prop, sub_node):
            self.prop = prop
            self.sub_node = sub_node
            super(A, self).__init__()

    class B(ASTNode):
        _node = 'B'
        __slots__ = 'list_property',

        def __init__(self, list_property):
            self.list_property = list_property
            super(B, self).__init__()

    class C(ASTNode):
        _node = 'C'

        def __init__(self):
            super(C, self).__init__()

    assert A(1, A(2, B([3, C()]))).json == {
        'node': 'A',
        'prop': 1,
        'sub_node': {
            'node': 'A',
            'prop': 2,
            'sub_node': {
                'node': 'B',
                'list_property': [3, {
                    'node': 'C'
                }]
            }
        }}
