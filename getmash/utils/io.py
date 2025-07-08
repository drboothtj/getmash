'''
io utils for getmash
'''
from typing import Dict, List
import csv

def write_list_to_file(items: List, filename: str) -> None:
    '''
    write a list as a file
        arguments:
            items: a list of strings
            filename: file to write to
        returns:
            None
    '''
    with open(filename, "w") as f:
        for item in items:
            f.write(f"{item}\n")


def get_mash_dict(path: str) -> Dict:
    '''
    read mash data from .tbl
        arguments:
            path: path to mash data as string
        returns:
                data: dictionary containing hits and scores
    '''
    with open(path) as file:
        tsv_file = csv.reader(file, delimiter="\t")
        data = {
            'Source': [],
            'Hit': [],
            'Value': []
        }
        for line in tsv_file:
            data['Source'].append(line[0])
            data['Hit'].append(line[1])
            data['Value'].append(float(line[2]))
        return data
