import os
import sys

from src.helpers import get_data, get_output_dir
from .helpers import parse_args, prep_data

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist

def create_elbow_plot(df, output_dir, clusters_elbow_method=range(1,10)):
    """
    Runs iterations of model.predict(df) over a range of cluster=k to create an elbow plot of
    average distances from observations. Saves plot to output_dir. 
    
    Args:
        df (pandas.DataFrame): standardized data, transformed from data/processed/<NAME>-donors.csv.   
        output_dir (str): path to output directory. 
        clusters_elbow_method (range): range of number of clusters to iterate over.
        
    Returns:
        None.    
    """

    #k-means cluster analysis using Elbow Method
    mean_dist = []

    for k in clusters_elbow_method:
        model = KMeans(n_clusters=k)
        model.fit(df)
        assign = model.predict(df)
        mean_dist.append(
            sum(np.min(cdist(df, model.cluster_centers_, 
            'euclidean'), axis=1)) / df.shape[0]
            )

    #plot average distance from observations from the cluster centroid
    #to use the Elbow Method to identify number of clusters to choose
    plt.rcParams["figure.figsize"] = [9.0, 6.0]
    plt.plot(clusters_elbow_method, mean_dist)
    plt.xlabel('Number of Clusters')
    plt.ylabel('Average Distance')
    plt.title('Selecting K with the Elbow Method')    
    plt.savefig(os.path.join(output_dir, 'elbow.png'), dpi=72)
    plt.show()
    plt.clf()
    
def main():
    args = parse_args()
    range_end = args[0] + 1 if len(args) > 0 else 10

    df = get_data()
    df_std = prep_data(df)
    output_dir = get_output_dir('cluster')
    create_elbow_plot(df_std, output_dir, clusters_elbow_method=range(1,range_end))

if __name__ == '__main__':
    sys.exit(main())
