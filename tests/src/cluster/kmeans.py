import os
import sys
from src.helpers import get_data, get_output_dir
from src.cluster.helpers import prep_data, merge_cluster_labels
from src.cluster.kmeans import run_kmeans
from tests.src.helpers import compare_spreadsheets

def main():
    df = get_data()
    df_std = prep_data(df)
    output_dir = get_output_dir('cluster')
    output_expected_dir = output_dir.replace('output', 'output_expected')
    ser_cluster_labels = run_kmeans(df_std, output_dir,  clusters_pca_scatterplots=range(4,5), kmeans_random_state=42)
    merge_cluster_labels(df, ser_cluster_labels, output_dir)

    #test that 4 clusters exist 
    expected_labels = [0, 1, 2, 3]
    labels = sorted(ser_cluster_labels.unique())   
    assert labels == expected_labels, f'TEST PASSED: {labels} != {expected_labels}'
    print()
    print('='*50)
    print(f'\nTEST PASSED: {labels} == {expected_labels}')  

    #compare assignments.csv files
    assignments = os.path.join(output_dir, 'assignments.csv')
    assignments_expected = os.path.join(output_expected_dir, 'assignments.csv')
    compare_spreadsheets(assignments, assignments_expected)

    #compare groups.csv files
    groups = os.path.join(output_dir, 'groups.csv')
    groups_expected = os.path.join(output_expected_dir, 'groups.csv')
    compare_spreadsheets(groups, groups_expected)     

if __name__ == '__main__':
    sys.exit(main())
