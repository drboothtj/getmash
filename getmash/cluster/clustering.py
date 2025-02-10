'''
take mash data and return clusters
'''
from typing import Dict
import pandas as pd
import csv

def dict_to_matrix(data: Dict) -> pd.DataFrame:
    '''
    converts the mash dictionary into a distance matrix
        arguments: 
            data: the dictionary from get_mash_dict()
        returns:
            matrix: the mash results as a distance matrix
    '''
    df = pd.DataFrame(data, columns=['Source', 'Hit', 'Value'])
    matrix = df.pivot(index='Source', columns='Hit', values='Value')
    matrix = matrix.fillna(0)
    return matrix

def get_mash_dict(path: str) -> Dict:
        '''
        extract the data from the mash table
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
                data['Value'].append(float(line[2]))  # Convert Value to float
            return data

def get_clusters(mash_table_path: str) -> str:
    '''
    main routine for clustering
        arguments:
            mash_table_path: path to all vs. all mash results as string
        returns:
            clusters_path: path to clusters file
    '''
    mash_data = get_mash_dict(mash_table_path)
    distance_matrix = dict_to_matrix(mash_data)
    print(distance_matrix)


