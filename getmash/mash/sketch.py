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
    sketch_path = os.path.join(output, 'getmash.msh')
    command = ['mash', 'sketch']
    command.extend(['-k', str(kmers)])
    command.extend(['-s', str(sketch_size)])
    command.extend(glob.glob(fna))
    command.extend (['-o', sketch_path])
    #print(command) #add command to log
    console.run_in_terminal(command)
    #catch mash when info is too bad (k or s too small)
    #automate selection or k value
    return sketch_path
