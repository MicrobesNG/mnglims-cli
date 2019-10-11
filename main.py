#!/usr/bin/env python3

import argparse

from limsfm import *

if __name__ == '__main__':
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='LIMSfm API')
    subparsers = parser.add_subparsers()

    # subparser: "getplatemeta" command
    parser_getplatemeta = subparsers.add_parser('getplatemeta')
    parser_getplatemeta.add_argument(
        'ref',
        type=str,
        help='The plate reference for which you want meta-data')
    parser_getplatemeta.set_defaults(func=get_plate_meta)

    # subparser: "setsamplequeue" command
    parser_setsamplequeue = subparsers.add_parser('setsamplequeue')
    parser_setsamplequeue.add_argument(
        'queue_id',
        metavar='queue-id',
        type=int,
        help='The id of the destination queue')
    parser_setsamplequeue.add_argument(
        'ref',
        nargs='+',
        type=str,
        help='The sample references you wish to queue')
    parser_setsamplequeue.set_defaults(func=set_sample_queue)

    # subparser : "getprojectresultspath" command
    parser_getprojectresultspath = subparsers.add_parser('getprojectresultspath')
    parser_getprojectresultspath.add_argument(
    'ref',
    type=str,
    help='The project reference')
    parser_getprojectresultspath.set_defaults(func=get_project_results_path)

    # subparser: "setprojectresultspath" command
    parser_setprojectresultspath = subparsers.add_parser('setprojectresultspath')
    parser_setprojectresultspath.add_argument(
        'ref',
        type=str,
        help='The project reference')
    parser_setprojectresultspath.add_argument(
        'path',
        type=str,
        help='The results data path')
    parser_setprojectresultspath.set_defaults(func=set_project_results_path)

    # subparser: "getqueues" command
    parser_getqueues = subparsers.add_parser('getqueues')
    parser_getqueues.set_defaults(func=get_queues)

    # subparser: "updatesamples" command
    parser_updatesamples = subparsers.add_parser('updatesamples')
    parser_updatesamples.set_defaults(func=update_samples) 
    parser_updatesamples.register('type', 'bool', lambda x: x.lower() in ("yes", "true", "t", "1"))
    parser_updatesamples.add_argument(
        'ref',
        nargs='+',
        type=str,
        help='The sample reference(s) you wish to update'
    )
    parser_updatesamples.add_argument(
        '-c, --suspected-contamination',
        dest='suspected_contamination',
        type='bool',
        help='Suspected sample contamination (True/False)'
    )

    # subparser: "getemailtemplates" command
    #parser_getemailtemplates = subparsers.add_parser('getemailtemplates')
    #parser_getemailtemplates.set_defaults(func=get_email_templates)

    # parse the args and call whatever function was selected
    args = parser.parse_args()
    args.func(args)
