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
    #allow supplying files or mash result and convert to distance martix
    if args.module == "mash":
        #add a step to extract from genbank files if provided

        sketch_path = sketch.sketch(
            args.fnas,
            args.output_directory,
            args.kmer_size,
            args.sketch_size,
        )
        mash_table_path = dist.dist(sketch_path, args.kmer_size, args.sketch_size, args.fnas) #maybe this architecture is a bit clunky

    elif args.module == "cluster":
        print('running clustering')
        #take tdistance matrix as input
    elif args.module == "plot":
        print('running plotting')

    else:
        print('select a module or use -h')


# do clustering on mash data NOTE: split initial and silhoutting?

# plot stuff...
