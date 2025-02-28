'''
take mash data and return clusters
'''
from typing import Dict, List, Union
from scipy.spatial.distance import squareform, pdist
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from getmash.utils.plotting import basic_dotplot, clustermap
import pandas as pd
import numpy as np
import csv
import os

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

def do_clustering(df_mash: pd.DataFrame, output_directory: str, iteration: int=0, output_flag: bool=True) -> Union[float, List, pd.DataFrame]: 
    '''
    perform kmeans clustering on a mash matrix
        arguments:
            df_mash: dataframe containing all the mash distances
            output_directory: directory to save files
            iteration: the loop iteration, used for labeling files
        returns:
            s_score: the silhoutte score of the current clusters
            points_to_drop: a list of points to be removed for the next round of analysis that fall below the silhoutte threshold
    '''
    df_similarity = 1 - df_mash # convert distances to similarity
    distances = pdist(df_similarity, metric='correlation')
    distances = squareform(distances)
    linkage_matrix = linkage(distances, method='ward')

    n_samples = linkage_matrix.shape[0] + 1
    best_k, results = chooseBestKforKMeans(distances, n_samples)
    print(f'Recommending {best_k} clusters as optimal. We highly recommend confirming this manually.')
    
    if output_flag:
        basic_dotplot(results, 'K', 'Adjusted Inertia', os.path.join(output_directory, f'kmeans_plot_iteration_{iteration}.png'))
    
    clusters = fcluster(linkage_matrix, t=best_k, criterion='maxclust') #best k OR user input!
    s_score = silhouette_score(distances, clusters)
    n_clusters = best_k 
    clusters = fcluster(linkage_matrix, t=n_clusters, criterion='maxclust')

    silhouette_values = silhouette_samples(distances, clusters)
    df_silhouette = pd.DataFrame({"Cluster": clusters, "Silhouette": silhouette_values}, index=df_similarity.index)
    if output_flag:
        df_silhouette.to_csv(os.path.join(output_directory, f"clusters_iteration_{iteration}.csv"))
    points_to_drop = df_silhouette[df_silhouette["Silhouette"] < 0.4].index.tolist()

    if output_flag:
        clustermap(df_similarity, df_silhouette, linkage_matrix, os.path.join(output_directory, f'clustermap_iteration_{iteration}.svg'))

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
                data['Value'].append(float(line[2])) 
            return data

def get_clusters(mash_table_path: str, output_directory: str, s_score_threshold: float, max_iterations: int, output_flag: bool) -> str:
    '''
    main routine for clustering
        arguments:
            mash_table_path: path to all vs. all mash results as string
             output_directory: path to the output directory
        returns:
            clusters_path: path to clusters file
    '''
    mash_data = get_mash_dict(mash_table_path)
    s_score = 0
    iteration = 1
    while s_score < s_score_threshold and iteration < max_iterations: #make both input parameters!!! and ask user if they want to do it at all!
        distance_matrix = dict_to_matrix(mash_data)
        s_score, points_to_drop = do_clustering(distance_matrix, output_directory, iteration, output_flag) #make plotting and writing false
        print(f'ITERATION {iteration}: silhoutte score is {s_score}.') #change to logging
        print(f'Dropping {len(points_to_drop)} samples.')
        mash_data = drop_data(mash_data, points_to_drop)
        iteration += 1
    s_score, _ = do_clustering(distance_matrix, output_directory, iteration)
    print(f'ITERATION {iteration -1}: the final silhoutte score is {s_score}.') #change to logging
