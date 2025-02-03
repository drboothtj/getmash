'''
subparser for running mash
'''

def get_arguments(subparser):
    '''
    add arguments to the mash subparser
    '''
    subparser.add_argument(
        "fnas",
        help="Search string for .fna input files"
        )
    subparser.add_argument(
        "output_directory", help="Directory to save the MASH data"
        )
    subparser.add_argument(
        "--kmer-size",
        "-k",
        type=int,
        default=15,
        help=(
        "K-mer size for mash sketch. " #add meaningful description /HINT)
        "(default: %(default)s)"
            )
        )
    subparser.add_argument(
        "--sketch-size",
        "-s",
        type=int,
        default=10000,
        help=(
        "Sketch size for mash. " #add meaningful description /HINT)
        "(default: %(default)s)"
            )
        )

def get_subparser(subparsers) -> None:
    '''
    add the mash subparser
        arguments:
            subparsers: the subparsers object for the main parser
        returns:
            None
    '''
    subparser = subparsers.add_parser('mash', help='run MASH on you input genomes') #for more parameters run mash independently and run getmash cluster on output
    subparser = get_arguments(subparser)
