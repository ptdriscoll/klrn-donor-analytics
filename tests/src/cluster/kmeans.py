import sys
from src.helpers import get_data, get_output_dir
from src.cluster.helpers import prep_data
from src.cluster.kmeans import run_kmeans

def main():
    df = get_data()
    df_std = prep_data(df)
    output_dir = get_output_dir('cluster')
    ser_cluster_labels = run_kmeans(df_std, output_dir,  clusters_pca_scatterplots=range(4,5))

    #test that 4 clusters exist 
    expected_labels = [0, 1, 2, 3]
    labels = sorted(ser_cluster_labels.unique())   
    assert labels == expected_labels, f'TEST PASSED: {labels} != {expected_labels}'
    print(f'\nTEST PASSED: {labels} == {expected_labels}')    

if __name__ == '__main__':
    sys.exit(main())
