'''
take mash data and return clusters
'''
from typing import Dict
from scipy.spatial.distance import squareform, pdist
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.cluster import KMeans

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv


#from sklearn.metrics import silhouette_samples, silhouette_score





def kMeansRes(scaled_data, k, alpha_k=0.02):
    '''
    # Calculating clusters from https://medium.com/towards-data-science/an-approach-for-choosing-number-of-clusters-for-k-means-c28e614ecb2c
    Parameters
    ----------
    scaled_data: matrix
        scaled data. rows are samples and columns are features for clustering
    k: int
        current k for applying KMeans
    alpha_k: float
        manually tuned factor that gives penalty to the number of clusters
    Returns
    -------
    scaled_inertia: float
        scaled inertia value for current k
    '''

    inertia_o = np.square((scaled_data - scaled_data.mean(axis=0))).sum()
    # fit k-means
    kmeans = KMeans(n_clusters=k, random_state=0).fit(scaled_data)
    scaled_inertia = kmeans.inertia_ / inertia_o + alpha_k * k
    return scaled_inertia

def chooseBestKforKMeans(scaled_data, k_range=10): #ADD K RANGE AS VARIABLE
    '''
    '''
    ans = []
    for k in range(2, k_range):
        scaled_inertia = kMeansRes(scaled_data, k)
        ans.append((k, scaled_inertia))
    results = pd.DataFrame(ans, columns = ['k','Scaled Inertia']).set_index('k')
    best_k = results.idxmin()[0]
    return best_k, results

def do_clustering(df_mash):
    '''
    '''
    # convert to similarity
    df_similarity = 1 - df_mash
    distances = pdist(df_similarity, metric='correlation')
    print(type(distances))
    distances = squareform(distances)
    linkage_matrix = linkage(distances, method='ward')
    # reorder rows and columns of the distance matrix based on clustering
    #ordered_indices = dendrogram(linkage_matrix, no_plot=True)['leaves']
    #df_reordered = df_similarity.iloc[ordered_indices, ordered_indices]
    best_k, results = chooseBestKforKMeans(distances)
    print(f'The recommends {best_k} clusters as optimal. We highly recommend confirming this manually.')

    # plot the results 
    #ALSO PLOT DISTANCES - extract to utils
    plt.figure(figsize=(7,4))
    plt.plot(results,'o')
    plt.title('Adjusted Inertia for each K')
    plt.xlabel('K')
    plt.ylabel('Adjusted Inertia')
    plt.savefig("kmeans_plot.png")

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
    cluster_matrix = do_clustering(distance_matrix)
    print(cluster_matrix)


