'''
run mash sketching
'''
from getmash.utils import console
import glob
import os

def sketch(fna, output, kmers, sketch_size):
    '''
    run mash sketch
    '''
    command = ['mash', 'sketch']
    command.extend(['-k', str(kmers)])
    command.extend(['-s', str(sketch_size)])
    command.extend(glob.glob(fna))
    command.extend (['-o', os.path.join(output, 'getmash.msh')])
    #print(command) #add command to log
    console.run_in_terminal(command)
    #catch mash when info is too bad (k or s too small)
    #automate selection
