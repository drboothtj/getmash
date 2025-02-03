'''
main routine for getmash
    functions:
        !!!
'''
from getmash.parser import parser
from getmash.mash import dist, sketch #add extract

def main() -> None:
    '''
    main function for getmash
        arguments:
            None
        returns:
            None
    '''
    args = parser.parse_args()

    if args.module == "mash":
        #add a step to extract from genbank files if provided

        sketch.sketch(
            args.fnas,
            args.output_directory,
            args.kmer_size,
            args.sketch_size,
        )
        #dist()

    elif args.module == "cluster":
        print('running clustering')
    elif args.module == "plot":
        print('running plotting')

    else:
        print('select a module or use -h')


# do clustering on mash data NOTE: split initial and silhoutting?

# plot stuff...
