'''
main routine for getmash
    functions:
        !!!
'''
from getmash.parser import parser
from getmash.mash import dist, sketch #add extract
from getmash.cluster import clustering
from getmash.network import network

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
    mash_table_path = dist.dist(
        sketch_path, args.sketch_size, args.fnas
        ) #maybe this architecture is a bit clunky
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
    elif args. module == "workflow":
        mash_table_path = run_mash(args)
        ...
    '''
    if args.module == "mash":
        _ = run_mash(args)

    elif args.module == "cluster":
        s_score_threshold = args.s_score_threshold
        max_iterations = args.max_iterations
        output_flag = args.output_intermediate
        clustering.get_clusters(
            args.mash_table, args.output_directory, s_score_threshold, max_iterations, output_flag
            )
        # actually, it should just work if you point it to a different table... TEST!
    elif args.module == "network":
        network.draw_network(args)
    else:
        print('select a module or use -h')

#TODO
#MASH:
#   -add automatic kmer size optimisation      [NV]
#   -check folders exist and make new folder   [NV]
#   -add parallelisation?                      [NV]

#CLUSTERING:
#   - add back unclustered members                    [  ]
#   - comparison of sihoutte maxima?                  [NV]
#   - better clustermap colours                       [NV]
#   - produce file for ITOL?                          [  ]
#   - drop clusters below a certain size              [  ]
#   - save as png as well as svg (too big breaks!)    [  ]

#WORKFLOW:
#   - add a module for the full workflow              [  ]
#   - add layers to establish sub clusters            [NV]

#ALL
# - squash/fix warnings                               [  ]
# - change name                                       [  ]
# - pypi v0.1.0                                       [  ]
# - Add logging                                       [  ]
# - Test and add unit tests                           [NV]
# - Code review                                       [NV]
# - make a script to convert sim to dist              [  ]
