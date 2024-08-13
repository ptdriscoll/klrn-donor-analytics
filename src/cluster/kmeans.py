import os
import sys

from src.helpers import get_data, get_output_dir
from .helpers import (
    parse_args,
    merge_cluster_labels, 
    prep_data,
    plot_cluster_sizes
)

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA 

def run_kmeans(
        df,
        output_dir,
        clusters_pca_scatterplots=range(4,5),
        kmeans_n_init=30
    ):    
    """
    Runs a k-means cluster analysis on a pandas.DataFrame from data/processed/donors.csv, uses
    PCA scatterplot/s to interpret solution/s, and saves plot/s to output_dir. 
    
    Args:
        df (pandas.DataFrame): data from data/processed/<NAME>-donors.csv.   
        output_dir (str): path to output directory. 
        clusters_pca_scatterplots (range): range of number of clusters to interpret using PCA 
            scatterplots. Because of the color map, the max number of clusters is 7. 
        kmeans_n_init (int): how many times KMeans runs with different initial centroid seeds. 
        
    Returns:
        pandas.Series: column of numbered cluster assignments.    
    """

    #set color map for scatterplot/s
    #reference: https://stackoverflow.com/questions/36180477/assigning-custom-colors-to-clusters-using-numpy
    colors = {0:'r', 1:'b', 2:'g', 3:'y', 4:'m', 5:'c', 6:'k'}
    plt.xlabel('Canonical Variable 1')
    plt.ylabel('Canonical Variable 2')
        
    #interpret cluster solution using PCA scatterplots
    for x in clusters_pca_scatterplots:
        model = KMeans(n_clusters=x, n_init=kmeans_n_init)
        model.fit(df)
        model.predict(df)
        ser_cluster_labels = pd.Series(model.labels_)
        
        #plot clusters    
        pca_2 = PCA(2)
        plot_columns = pca_2.fit_transform(df)   
        plt.scatter(x=plot_columns[:,0], y=plot_columns[:,1], c=ser_cluster_labels.map(colors),
                    s=25, alpha=0.1, edgecolor='none')
        plt.title('Scatterplot of Canonical Variables for ' + str(x) + ' clusters')        
        plt.savefig(os.path.join(output_dir, 'model_' + str(x) + '.png'), dpi=72)
        plt.show()
        plt.clf()
        

    plt.Circle(( 0.5 , 0.5 ), 0.2 ) 
    plt.show()
    plt.clf()

    return ser_cluster_labels
    
def main():
    args = parse_args()
    range_start = args[0] if len(args) > 0 else 4
    range_end = range_start + 1

    df = get_data()
    df_std = prep_data(df)
    output_dir = get_output_dir('cluster')

    ser_cluster_labels = run_kmeans(df_std, 
                                    output_dir, 
                                    clusters_pca_scatterplots=range(range_start,range_end))
    
    df_groups = merge_cluster_labels(df, ser_cluster_labels, output_dir)
    plot_cluster_sizes(df_groups, output_dir)

if __name__ == '__main__':
    sys.exit(main())
