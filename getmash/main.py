'''
main routine for getmash
    functions:
        !!!
'''
from getmash.parser import parser

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
        print('running mash')

    if args.module == "cluster":
        print('running clustering')

    if args.module == "plot":
        print('running plotting')

    else:
        print('select a module or use -h')

# get parser and args

# run mash on provided genomes

# do clustering on mash data

# plot stuff...
