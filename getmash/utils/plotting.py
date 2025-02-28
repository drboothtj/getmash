'''
plotting utils for getmash
'''

import matplotlib.pyplot as plt
import seaborn as sns

def basic_dotplot(results, x_label, y_label, output_path) -> None:
    '''
    plot a very simplistic dotplot using matplotlib
        arguments:
            results: 2D matrix or dataframe
            x_label: the label for the x axis
            y_label: the label for the y axis
            output_path: the path to save the figure to
    '''
    plt.figure(figsize=(7,4))
    plt.plot(results,'o')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(output_path)

def clustermap(df_similarity, df_clusters, matrix, output_path: str) -> None:
    '''
    plot a cluster map based on the linkage matrix
    '''
    color_set_15 = [
        "#e6194b", "#3cb44b", "#ffe119", "#0082c8", "#f58231", "#911eb4", "#46f0f0", "#f032e6", "#d2f53c", "#fabebe", "#008080", "#e6beff", "#aa6e28", "#fffac8", "#800000"
        ] #onlh 15 colours find a better way and move to utils
    cluster_list = sorted(df_clusters.Cluster.unique())
    cluster_color_dict = dict(zip(cluster_list, color_set_15[:len(cluster_list)]))
    df_clusters["Cluster_Color"] = [cluster_color_dict[df_clusters.loc[genome_id, "Cluster"]] for genome_id in df_clusters.index]
    
    col_colors = df_clusters["Cluster_Color"]
    sns.set(font_scale=1.0)
    g = sns.clustermap(df_similarity, cmap='Blues', 
        row_linkage=matrix, col_linkage=matrix, 
        col_colors= col_colors,
        xticklabels=df_similarity.index,
        yticklabels=df_similarity.index)
    
    color_legend = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=cluster_color_dict[cluster],
        markersize=10) for cluster in sorted(cluster_list)]
    
    cluster_sizes = df_clusters.Cluster.value_counts()
    labels = [f"{cluster} (Members: {cluster_sizes[cluster]})" for cluster in sorted(cluster_list)]

    plt.legend(color_legend, labels, title='Cluster ID', bbox_to_anchor=(-1, 1))  
    plt.savefig(output_path, bbox_inches="tight")
