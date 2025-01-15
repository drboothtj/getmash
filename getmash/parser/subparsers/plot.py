'''
subparser for mash cluster plotting
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
    add the plotting subparser
        arguments:
            subparsers: the subparsers object for the main parser
        returns:
            None
    '''
    subparser = subparsers.add_parser('plot', help='plot results from MASH-clustering')
    subparser = get_arguments(subparser)