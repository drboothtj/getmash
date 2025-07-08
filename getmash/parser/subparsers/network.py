'''
subparser for generating mash network
'''
def get_arguments(subparser)-> None:
    '''
    add arguments to the parser
        arguments:
            subparser: the network subparser
        returns:
            None
    '''
    subparser.add_argument(
        "mash_table",
        type=str,
        default=None,
        help="Path to an all vs. all mash table "
        )
    subparser.add_argument(
        "output_directory",
        type=str,
        default=None,
        help="Directory to save the network data "
        )
    subparser.add_argument(
        "--threshold",
        "-t",
        type=int,
        default=0.05,
        help=(
        "The MASH score threshold for drawing edges expressed as a decimal" 
        "(default: %(default)s)"
            )
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
    subparser = subparsers.add_parser(
        'network', help='draw a MASH-network from MASH output'
        )
    subparser = get_arguments(subparser)
