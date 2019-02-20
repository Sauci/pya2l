"""
@project: pya2l
@file: parser.py
@author: Guillaume Sottas
@date: 19.02.2019
"""

from pya2l.parser.grammar import A2lParser


class Parser(A2lParser):
    def __init__(self, string, include_dir=tuple()):
        super(Parser, self).__init__(string, include_dir=include_dir)

    def nodes(self, node_name):
        if self.ast:
            return self.ast.nodes(node_name)
        else:
            return []

    def dump(self, indent=4, line_ending='\n', indent_char=' '):
        if self.ast and hasattr(self.ast, 'project'):
            result = list()
            for indentation_level, string in self.ast.project.dump():
                result.append(((indent_char * indent) * indentation_level) + string)
            return line_ending.join(result)
        else:
            return ''
