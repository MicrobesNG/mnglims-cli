#!/usr/bin/env python3

import argparse

from limsfm import *

if __name__ == '__main__':
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='LIMSfm API')
    subparsers = parser.add_subparsers()

    # create the parser for the "getplatemeta" command
    parser_getplatemeta = subparsers.add_parser('getplatemeta')
    parser_getplatemeta.add_argument(
        'ref',
        type=str,
        help='The plate reference for which you want meta-data')
    parser_getplatemeta.set_defaults(func=get_plate_meta)

    # create the parser for the "setsamplequeue" command
    parser_setsamplequeue = subparsers.add_parser('setsamplequeue')
    parser_setsamplequeue.add_argument(
        'refs',
        type=str,
        help='The sample references you wish to queue (comma delimited)')
    parser_setsamplequeue.add_argument(
        'queue',
        type=str,
        help='The name of the destination queue')
    parser_setsamplequeue.set_defaults(func=set_sample_queue)

    # create the parser for the "setprojectresultspath" command
    parser_setprojectresultspath = subparsers.add_parser('setprojectresultspath')
    parser_setprojectresultspath.add_argument(
        'project_ref',
        metavar='project-ref',
        type=str,
        help='The project reference you wish to update')
    parser_setprojectresultspath.add_argument(
        'results_path',
        metavar='results-path',
        type=str,
        help='The project results path')
    parser_setprojectresultspath.set_defaults(func=set_project_results_path)

    # parse the args and call whatever function was selected
    args = parser.parse_args()
    args.func(args)

