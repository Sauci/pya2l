"""
@project: pya2l
@file: cli.py
@author: Guillaume Sottas
@date: 28.12.2018
"""

import argparse
import typing

import dictdiffer
import json
import logging
import os
import sys
# import textwrap

from pya2l.parser import A2lParser as Parser, RootNodeType

TO_JSON_CMD = 'to_json'
TO_A2L_CMD = 'to_a2l'
DIFF_CMD = 'diff'


def parse_args(args):
    parser = argparse.ArgumentParser(prog='pya2l', description='Command line utility for A2L-formatted files.')
    parser.add_argument('input_file', type=argparse.FileType('rb'), help='full path to A2L/JSON input file')
    parser.add_argument('-v', dest='verbose', action='store_true', help='enable verbose')
    parser.add_argument('-p', dest='port', type=int, default=3333, nargs='?',
                        help='TCP port used to connect to the backend')

    subparsers = parser.add_subparsers(dest='sub_command', help='supported commands')

    json_subparser = subparsers.add_parser(TO_JSON_CMD, help='converts an A2L/JSON file to JSON')
    json_subparser.add_argument('-o', dest='output_file', type=argparse.FileType('wb'),
                                help='full path to JSON output file')
    json_subparser.add_argument('-i', dest='indent', type=int, default=None, nargs='?',
                                help='indentation level (in number of leading spaces)')
    json_subparser.add_argument('-e', dest='emit_unpopulated', type=bool, default=False,
                                help='emit unpopulated fields')
    json_subparser.add_argument('-p', dest='allow_partial', type=bool, default=False,
                                help='allow production of JSON output with missing required field(s)')

    a2l_subparser = subparsers.add_parser(TO_A2L_CMD, help='converts an A2L/JSON file to A2L')
    a2l_subparser.add_argument('-o', dest='output_file', type=argparse.FileType('wb'),
                               help='full path to A2L output file')
    a2l_subparser.add_argument('-s', dest='sorted', action='store_true', default=False,
                               help='sort elements based on their unique key within the document')
    a2l_subparser.add_argument('-i', dest='indent', type=int, default=None, nargs='?',
                               help='indentation level (in number of leading spaces)')
    a2l_subparser.add_argument('-p', dest='allow_partial', type=bool, default=False,
                                help='allow production of JSON output with missing required field(s)')

    diff_subparser = subparsers.add_parser(DIFF_CMD, help='shows differences between two A2L/JSON files')
    diff_subparser.add_argument('right_hand_side', type=argparse.FileType('rb'),
                                help='full path to A2L/JSON right hand side input file')
    diff_subparser.add_argument('-p', dest='allow_partial', type=bool, default=False,
                                help='allow production of JSON output with missing required field(s)')

    # parser.epilog = textwrap.dedent(
    #     f"""\
    #         commands usage:\n
    #         {json_subparser.format_usage()}
    #         {a2l_subparser.format_usage()}
    #         {diff_subparser.format_usage()}
    #         """
    # )

    return parser.parse_args(args)


def process_input_file(fp, parser: Parser, allow_partial: bool, encoding: str = None) -> RootNodeType:
    data = fp.read()
    if encoding is not None:
        data = data.decode(encoding).encode()
    if os.path.splitext(fp.name)[1].lower() == '.json':
        result = parser.tree_from_json(data, allow_partial=allow_partial)
    elif os.path.splitext(fp.name)[1].lower() == '.a2l':
        result = parser.tree_from_a2l(data)
    else:
        raise TypeError(f'unsupported file extension "{os.path.splitext(fp.name)[1]}"')
    return result


def main(args: typing.List[str] = tuple(sys.argv[1:])):
    args = parse_args(args)

    log = logging.getLogger('pya2l')
    log.setLevel(logging.DEBUG)

    if args.verbose:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(fmt='%(asctime)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
        log.addHandler(stream_handler)

    try:
        with Parser(port=args.port, logger=log) as parser:
            input_tree = process_input_file(args.input_file, parser, args.allow_partial)
            if args.sub_command == TO_JSON_CMD:
                if args.output_file:
                    log.info(f'start writing to file {os.path.abspath(args.output_file.name)}')
                    args.output_file.write(parser.json_from_tree(input_tree,
                                                                 indent=args.indent,
                                                                 allow_partial=args.allow_partial,
                                                                 emit_unpopulated=args.emit_unpopulated))
                    log.info(f'finished writing to file {os.path.abspath(args.output_file.name)}')
                else:
                    sys.stdout.write(parser.json_from_tree(input_tree,
                                                           indent=args.indent,
                                                           allow_partial=args.allow_partial,
                                                           emit_unpopulated=args.emit_unpopulated).decode())
            elif args.sub_command == TO_A2L_CMD:
                if args.output_file:
                    log.info(f'start writing to file {os.path.abspath(args.output_file.name)}')
                    args.output_file.write(parser.a2l_from_tree(input_tree, sorted=args.sorted, indent=args.indent))
                    log.info(f'finished writing to file {os.path.abspath(args.output_file.name)}')
                else:
                    sys.stdout.write(parser.json_from_tree(input_tree,
                                                           indent=args.indent,
                                                           allow_partial=args.allow_partial,
                                                           emit_unpopulated=args.emit_unpopulated).decode())
            elif args.sub_command == DIFF_CMD:
                lhs_tree = input_tree
                rhs_tree = process_input_file(args.right_hand_side, parser, args.allow_partial)

                lhs_string = parser.json_from_tree(lhs_tree)
                rhs_string = parser.json_from_tree(rhs_tree)
                diff = list(dictdiffer.diff(json.loads(lhs_string), json.loads(rhs_string)))
                sys.stdout.write('\n'.join(str(d) for d in diff))
    except Exception as e:
        log.error(str(e))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
