'''
get distance matrix from mash results for getmash
'''
import glob
import os
from getmash.utils import console

def dist(sketch_path:str, kmers: int, sketch_size: int, fna: str):
    '''
    get mash table from mash dist for getmash
    '''    
    mash_path = os.path.join(os.path.dirname(sketch_path), 'getmash.tbl')
    command = ['mash', 'dist']
    command.extend(['-k', str(kmers)])
    command.extend(['-s', str(sketch_size)])
    command.extend(glob.glob(fna))
    command.extend([sketch_path])
    print(command)
    console.run_in_terminal(command, mash_path)
    
    #return mash_path

#run distance

#convert to table

#write table

