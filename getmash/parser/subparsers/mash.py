'''
subparser for running mash
'''

def get_arguments(subparser):
    '''
    add arguments to the mash subparser
    '''
    subparser.add_argument(
        "gbks",
        help="Input .gbk files containing protein sequences"
        )
    subparser.add_argument(
        "output_directory", help="Directory to save the MASH data"
        )
    subparser.add_argument(
        "--insert-common-args",
        "-i",
        type=int,
        default=7500,
        help="Maximum sequence length to process, sequences longer than this will be chunked, and processed separately"
        )
    ## add most relevent!!
    subparser.add_argument(
        "--parameters",
        "-p",
        type=str,
        default=None,
        help="additional MASH parameters" # add help info
        )
    return subparser

def get_subparser(subparsers) -> None:
    '''
    add the mash subparser
        arguments:
            subparsers: the subparsers object for the main parser
        returns:
            None
    '''
    subparser = subparsers.add_parser('mash', help='run MASH on you input genomes')
    subparser = get_arguments(subparser)
