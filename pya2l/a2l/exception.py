"""
@project: pya2l
@file: exception.py
@author: Guillaume Sottas
@date: 04.01.2019
"""


class A2lFormatException(Exception):
    def __init__(self, message, position, string=None):
        self.value = str(message) + str(position)
        if string:
            delta = 120
            s = position - delta if position >= delta else 0
            e = position + delta if len(string) >= position + delta else -1
            substring = string[s:e].replace('\r', ' ').replace('\n', ' ')
            indicator = ' ' * (delta if position >= delta else position) + '^'
            self.value += '\r\n\t' + ('...' if s else '   ') + substring + '\r\n\t   ' + indicator

        super(A2lFormatException, self).__init__(self.value)


class A2lLexerException(Exception):
    def __init__(self, value, line, position):
        self.value = value
        self.message = u'invalid character \'{}\' at line {}, position {}'.format(value, line, position)
        super(A2lLexerException, self).__init__(self.value)
