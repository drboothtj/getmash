'''
subparser for mash clustering
'''    

def get_arguments(subparser):
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
        help="Directory to save the cluster data "
        )
    subparser.add_argument(
        "--max-iterations",
        "-m",
        type=int,
        default=5,
        help=(
        "Maximum number of iterations for silhouette filtering " 
        "(default: %(default)s)"
            )
        )
    subparser.add_argument(
        "--s-score-threshold",
        "-s",
        type=float,
        default=0.4,
        help=(
        "The silhouette score threshold for for silhouette filtering " 
        "(default: %(default)s)"
            )
        )
    subparser.add_argument(
        "--output-intermediate",
        "-o",
        action='store_true',
        help=(
        "Write tables and plots for all filtering iterations " 
        "(default: %(default)s)"
            )
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