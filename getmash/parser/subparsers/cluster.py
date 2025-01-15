'''
subparser for mash clustering
'''    

def get_arguments(subparser):
    subparser.add_argument(
        "--place-holder",
        "-ph",
        type=str,
        default=None,
        help="PLACEHOLDER" # add help info
        )
    return subparser

def get_subparser(subparsers) -> None:
    '''
    add the cluster subparser
        arguments:
            subparsers: the subparsers object for the main parser
        returns:
            None
    '''
    subparser = subparsers.add_parser('cluster', help='run MASH-clustering on MASH output')
    subparser = get_arguments(subparser)