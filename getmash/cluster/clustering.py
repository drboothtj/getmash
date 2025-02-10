'''
take mash data and return clusters
'''
from typing import Dict, List
from scipy.spatial.distance import squareform, pdist
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv

def drop_data(mash_data: Dict, points_to_drop: List):
    '''
    remove the specified points from the mash data
    '''
    new_sources = []
    new_hits = []
    new_values = []
    for source, hit, value in zip(mash_data['Source'], mash_data['Hit'], mash_data['Value']):
        if not (source in points_to_drop or hit in points_to_drop):
            new_sources.append(source)
            new_hits.append(hit)
            new_values.append(value)
    new_mash_data = {
        'Source': new_sources,
        'Hit': new_hits,
        'Value': new_values
    }
    return new_mash_data


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

def chooseBestKforKMeans(scaled_data, n_samples, k_range=10): #ADD K RANGE AS VARIABLE
    '''
    '''
    ans = []
    for k in range(2, min(n_samples, k_range)):
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
    distances = squareform(distances)
    linkage_matrix = linkage(distances, method='ward')
    n_samples = linkage_matrix.shape[0] + 1
    # reorder rows and columns of the distance matrix based on clustering
    #ordered_indices = dendrogram(linkage_matrix, no_plot=True)['leaves']
    #df_reordered = df_similarity.iloc[ordered_indices, ordered_indices]
    best_k, results = chooseBestKforKMeans(distances, n_samples)
    print(f'The recommends {best_k} clusters as optimal. We highly recommend confirming this manually.')

    # plot the results 
    #ALSO PLOT DISTANCES - extract to utils
    plt.figure(figsize=(7,4))
    plt.plot(results,'o')
    plt.title('Adjusted Inertia for each K')
    plt.xlabel('K')
    plt.ylabel('Adjusted Inertia')
    plt.savefig("kmeans_plot.png")

    '''
    WE DO NEED THIS but only for the selected number of clusters!
    # Variables to store the silhouette scores
    silhouette_scores = []

    # Iterate over different numbers of clusters
    for num_clusters in range(2, 10):
    '''

    # Use fcluster to assign cluster labels
    clusters = fcluster(linkage_matrix, t=best_k, criterion='maxclust') #best k OR user input!

    # Calculate the silhouette score
    s_score = silhouette_score(distances, clusters)
    ##############SEPERATE THIS WHOLE BIT OUT! SILHOUTTE MAKES LESS SENSE IN FINAL ITERATION

    ### get assignments
    n_clusters = best_k ####USER INPUT! ALSO NEEDED
    # Use fcluster to assign cluster labels
    clusters = fcluster(linkage_matrix, t=n_clusters, criterion='maxclust')

    # Create dataframe assigning genomes to clusters
    df_mash_clusters_kmeans = pd.DataFrame({'Cluster': clusters}, index=df_similarity.index)
    df_mash_clusters_kmeans.to_csv('clusters.csv')
    # Compute silhouette coefficient for each sample
    silhouette_values = silhouette_samples(distances, clusters)

    df_silhouette = pd.DataFrame({"Cluster": clusters, "Silhouette": silhouette_values}, index=df_similarity.index)
    df_silhouette.to_csv("df_silhouette_1.csv")

    points_to_drop = df_silhouette[df_silhouette["Silhouette"] < 0.4].index.tolist()

    return s_score, points_to_drop

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
    s_score = 0
    iteration = 1
    while s_score < 0.4 or iteration <= 2: #make both input parameters!!! and ask user if they want to do it at all!
        distance_matrix = dict_to_matrix(mash_data)
        s_score, points_to_drop = do_clustering(distance_matrix)
        print(f'ITERATION {iteration}: silhoutte score is {s_score}.') #change to logging
        print(f'Dropping {len(points_to_drop)} samples.')
        mash_data = drop_data(mash_data, points_to_drop)
        iteration += 1
    #final iteration outside of loop!
    distance_matrix = dict_to_matrix(mash_data)
    s_score, _ = do_clustering(distance_matrix)
    print(f'ITERATION {iteration}: silhoutte score is {s_score}.') #change to logging
