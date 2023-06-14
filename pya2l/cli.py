"""
@project: pya2l
@file: cli.py
@author: Guillaume Sottas
@date: 28.12.2018
"""

import argparse
import sys

from pya2l.parser import A2lParser as Parser

JSON_CMD = 'to_json'


def main():
    parser = argparse.ArgumentParser(prog='pya2l', description='python command line utility for a2l-formatted files.')
    parser.add_argument('input_file', nargs=1, help='full path to a2l input file')

    subparsers = parser.add_subparsers(dest='sub_command', help='supported commands')

    json = subparsers.add_parser(JSON_CMD, help='converts an a2l file to json')
    json.add_argument('-o', nargs=1, help='full path to json output file')

    args = parser.parse_args()

    with open(args.input_file[0], 'r') as fp:
        data = fp.read()

    a2l = Parser(data)

    if args.sub_command == JSON_CMD:
        if args.o:
            with open(args.o[0], 'wb') as fp:
                fp.write(a2l.ast.json(indent=4, sort_keys=True).encode())
        else:
            sys.stdout.write(a2l.ast.json(indent=4, sort_keys=True))


if __name__ == '__main__':
    main()
