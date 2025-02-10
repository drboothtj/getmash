'''
subparser for mash clustering
'''    

def get_arguments(subparser):
    subparser.add_argument(
        "mash_table",
        type=str,
        default=None,
        help="Path to an all vs. all mash table"
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