'''
main routine for getmash
    functions:
        !!!
'''
from getmash.parser import parser
from getmash.mash import dist, sketch #add extract
from getmash.cluster import clustering

def run_mash(args) -> str:
    '''
    function to run mash module
        arguments:
            args: arguments from argparse
        returns:
            mash_table_path: the path to the produced mash table
    '''
    #move to mash module?   
    #add a step to extract from genbank files if provided
    sketch_path = sketch.sketch(
        args.fnas,
        args.output_directory,
        args.kmer_size,
        args.sketch_size,
    )
    mash_table_path = dist.dist(sketch_path, args.sketch_size, args.fnas) #maybe this architecture is a bit clunky
    return mash_table_path

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
    #add a total work flow! module == full_workflow
    '''
    if args. module == "workflow":
        mash_table_path = run_mash(args)
        ...
    '''
    if args.module == "mash":
        _ = run_mash(args)

    elif args.module == "cluster":
        clustering.get_clusters(args.mash_table, args.output_directory) # IMPORTANT: ADD ABILITY TO ADD CUSTOM DISTANCE TABLE

    elif args.module == "plot":
        print('running plotting')

    else:
        print('select a module or use -h')


#TODO
#MASH:
#   -add automatic kmer size optimisation      [NV]
#   -check folders exist and make new folder   [NV]
#   -add parallelisation?                      [NV]

#CLUSTERING:
#   - write output to tables (all tables)      [  ]
#   - enable inputing a custom distance table  [NV]
#   - plot clusters on a graph                 [  ]

#PLOT:
#   - similarity heat map. W/ wo cluster colours
#   - scatter plot 
#   - produce file for ITOL?
#   - DO THESE IN CLUSTERING REMOVE PLOT MODULE

#WORKFLOW:
#   - add a module for the full workflow
#   - add layers to establish sub clusters

#ALL
# - change name
# - pypi v0.1.0
# - Add logging
# - Add unit tests
# - Code review
