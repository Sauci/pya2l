"""
@project: pya2l
@file: pya2l.py
@author: Guillaume Sottas
@date: 20.03.2018
"""

from grammar import A2lParser, A2lFormatException


class PyA2l(A2lParser):
    def __init__(self, string):
        super(PyA2l, self).__init__(string)
