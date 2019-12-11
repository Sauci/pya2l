"""
@project: pya2l
@file: lexer.py
@author: Guillaume Sottas
@date: 20.03.2018
"""

import os
import ply.lex as lex

from pya2l.parser.exception import A2lLexerException
from pya2l.shared.type import String
from pya2l.a2l.token import tokens as a2l_tokens
from pya2l.a2ml.token import tokens as a2ml_tokens

a2l_keywords = dict((k, k) for k in a2l_tokens)

a2ml_keywords = dict((k, k) for k in a2ml_tokens)


class Lexer(object):
    tokens = tuple(set(list(a2l_keywords.values()) + list(a2ml_keywords.values()) +
                       [
                           r'N',
                           r'S',
                           r'I',
                           r'begin',
                           r'end',
                           r'include',
                           r'PO',
                           r'PC',
                           r'CO',
                           r'CC',
                           r'BO',
                           r'BC',
                           r'SC',
                           r'ASTERISK',
                           r'EQ',
                           r'COMMA'
                       ]))

    states = (('a2ml', 'exclusive'), ('ifdata', 'exclusive'))

    def __init__(self):
        self._lex = None
        self.lexer_stack = list()

    @property
    def instance(self):
        return self._lex

    def build(self, include_dir=tuple()):
        self._lex = lex.lex(debug=False,
                            optimize=True,
                            module=self,
                            outputdir=os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'),
                            lextab='lexer_tab')
        self._lex.lineno = 1
        self._lex.include_dir = include_dir
        return self

    def token_function(self):
        if len(self.lexer_stack):
            token = self.lexer_stack[-1].token()
        else:
            token = self._lex.token()
        if not token and len(self.lexer_stack):
            self.lexer_stack.pop()
            token = self.token_function()
        return token

    t_ANY_ignore = ' \t'

    @lex.TOKEN(r'(/\*(.|\n)*?\*/)')
    def t_ANY_ignore_C_COMMENT(self, token):
        token.lexer.lineno += len(token.value.splitlines())

    @staticmethod
    @lex.TOKEN(r'(\/{2}[^\r\n]+((\r\n)|(\r)|(\n)))')
    def t_ANY_ignore_CPP_COMMENT(token):
        token.lexer.lineno += len(token.value.splitlines())

    @staticmethod
    @lex.TOKEN(r'((\r\n)|(\r)|(\n))')
    def t_ANY_ignore_NEW_LINE(token):
        token.lexer.lineno += 1

    t_ANY_PO = r'\('
    t_ANY_PC = r'\)'
    t_ANY_CO = r'\{'
    t_ANY_CC = r'\}'
    t_ANY_BO = r'\['
    t_ANY_BC = r'\]'
    t_ANY_SC = r';'
    t_ANY_ASTERISK = r'\*'
    t_ANY_EQ = r'='
    t_ANY_COMMA = r','

    @staticmethod
    @lex.TOKEN(r'\/begin')
    def t_ANY_begin(token):
        return token

    @staticmethod
    @lex.TOKEN(r'\/end')
    def t_ANY_end(token):
        return token

    @staticmethod
    @lex.TOKEN(r'"(?:[^"\\]|\\.)*"')
    def t_ANY_S(token):
        token.value = String(token.value[1:-1])
        return token

    @staticmethod
    @lex.TOKEN(r'[+-]?(([0]{1}[Xx]{1}[A-Fa-f0-9]+)|(\d+(\.(\d*([eE][+-]?\d+)?)?|([eE][+-]?\d+)?)?))')
    def t_ANY_N(token):
        try:
            token.value = int(token.value, 10)
        except ValueError:
            try:
                token.value = int(token.value, 16)
            except ValueError:
                token.value = float(token.value)
        return token

    @staticmethod
    @lex.TOKEN(r'[A-Za-z_][A-Za-z0-9_\.\[\]]*')
    def t_INITIAL_I(token):
        if token.value == 'IF_DATA':
            token.type = token.value
            token.lexer.push_state('ifdata')
        elif token.value == 'A2ML':
            token.type = token.value
            token.lexer.push_state('a2ml')
        else:
            try:
                token.type = a2l_keywords[token.value.split('[')[0]]
            except KeyError:
                pass
        return token

    @staticmethod
    @lex.TOKEN(r'[A-Za-z_][A-Za-z0-9_]{0,}')
    def t_a2ml_I(token):
        if token.value == 'A2ML':
            token.type = token.value
            token.lexer.pop_state()
        else:
            try:
                token.type = a2ml_keywords[token.value]
            except KeyError:
                pass
        return token

    @staticmethod
    @lex.TOKEN(r'[A-Za-z_][A-Za-z0-9_\.\[\]]*')
    def t_ifdata_I(token):
        if token.value == 'IF_DATA':
            token.type = token.value
            token.lexer.pop_state()
        return token

    @lex.TOKEN(r'\/include\s*?(("[^"]+")|([^ ]+))')
    def t_ANY_ignore_include(self, token):
        filename = token.value.replace('/include', '').strip(' "')
        new_lexer = token.lexer.clone()
        new_lexer.lineno, new_lexer.lexpos = 1, 0
        string = None
        for directory in type(new_lexer.include_dir)(['']) + new_lexer.include_dir:
            try:
                with open(os.path.join(directory, filename), 'r') as fp:
                    string = fp.read()
            except IOError:
                continue
            else:
                break
        if string is None:
            raise IOError('unable to find included file "{}"'.format(str(filename)))
        new_lexer.input(string)
        self.lexer_stack.append(new_lexer)
        return new_lexer.token()

    @staticmethod
    def t_ANY_error(token):
        raise A2lLexerException(token.value[0], token.lineno, token.lexpos)
