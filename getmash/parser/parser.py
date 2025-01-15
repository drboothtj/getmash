'''
this is the parser for getmash
    functions:
        get_parser()
        parse_args()
'''
import argparse
from argparse import RawTextHelpFormatter
from getmash.parser.subparsers import mash, cluster, plot

def get_parser():
    '''
    create a parser for bassbase
        arguments:
            None
        returns:
            parser: the getmash parser object
    '''
    parser = argparse.ArgumentParser(
        "getmash",
        description="",
        epilog="Written by T. J. Booth, 2025.",
        formatter_class=RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(title='Modules', dest='module')

    mash.get_subparser(subparsers)
    cluster.get_subparser(subparsers)
    plot.get_subparser(subparsers)
    #add full workflow option!
    return parser

def parse_args():
    '''get the arguments from the console via the parser'''
    arg_parser = get_parser()
    args = arg_parser.parse_args()
    return args

