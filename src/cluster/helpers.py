import os
import argparse
import matplotlib.pyplot as plt
from sklearn import preprocessing

def parse_args():
    """
    Parses command-line arguments to add as arguments to cluster functions. Options include 
    one, two or no integers. 

    Returns:
        List[int]: list of 0 or more integers provided as command-line arguments. 

    Examples:
        Run with no values:
            $ python -m src.cluster.kmeans 

        Run with one value:
            $ python -m src.cluster.kmeans 4
            $ python -m src.cluster.elbow_plot 9

        Run with two values to set range, with each number inclusive: 
            $ python -m src.cluster.pca_plots 3 5 

    Returns:
        List[int]: list of integers specified by user, which can represent a range.          
    """
    parser = argparse.ArgumentParser(description='Run cluster module')
    parser.add_argument(
        'arg_values',
        nargs='*',
        type=int,
        help='Specify a range using one or two numbers, with each inclusive, e.g. 4 or 4 6'
    )
    args = parser.parse_args()
    return args.arg_values

def prep_data(
        df,
        cols_to_drop=['ID', 'Status', 'Total_Count', 'Total_Payments', 'Num_Years']
    ):
    """
    Drops unneeded columns, and standardizes predictors to mean=0 and std=1.

    Arg:
        df (pandas.DataFrame): data from data/processed/<NAME>-donors.csv.   
        cols_to_drop (List[str]): columns to drop from dataframe.             

    Returns:
        pandas.DataFrame.
    """
    #drop variables to leave out    
    df = df.drop(cols_to_drop, axis=1)

    print('\n', df.tail)

    #standardize predictors to mean=0 and std=1 
    for col in df.columns:
        df[col] = preprocessing.scale(df[col].astype('float64'))

    return df

def merge_cluster_labels(df, ser_cluster_labels, output_dir):
    """
    Adds column of cluster labels to dataframe, checks frequencies, aggregates clusters, 
    calculates cluster averages, and saves results to output_dir.

    Arg:
        df (pandas.DataFrame): data from data/processed/donors.csv.  
        ser_cluster_labels (pandas.Series): column of cluster label numbers to add to df. 
        output_dir (str): path to output directory.            

    Returns:
        pandas.DataFrame: cluster averages across columns.
    """ 

    #merge cluster assignments with data
    df['Cluster'] = ser_cluster_labels

    #print('\n', df)

    #check cluster frequencies
    print('\n\n\nCluster frequencies\n')
    print(df['Cluster'].value_counts())
    print('\nTotal frequencies:', df['Cluster'].count(), '\n')
    output = 'Cluster frequencies\n\n'
    output += str(df['Cluster'].value_counts())
    output += '\n\nTotal frequencies: ' + str(df['Cluster'].count())

    #aggregate on Cluster, then re-calculate annual average counts and payments
    aggreg = { 
        'Total_Count': 'sum',
        'Total_Payments': 'sum',
        'Num_Years': 'sum',
        'Sustainer': 'mean',
        'Major': 'mean',
        'Passport': 'mean',
        'Gift': 'mean',
        'Rejoin': 'mean',
        'Renew': 'mean',
        'Add': 'mean',
        'New': 'mean',
        'Online': 'mean'
    }
    groups = df.groupby('Cluster').agg(aggreg)
    groups['Annual_Payment'] = groups['Total_Payments'] / groups['Num_Years']
    groups['Annual_Count'] = groups['Total_Count'] / groups['Num_Years']
    groups['Frequencies'] = df.groupby('Cluster').size()
    groups = groups.drop(['Total_Count', 'Total_Payments', 'Num_Years'], axis=1) 

    print('\n\nClustering variable means by cluster\n')
    print(groups)
    output += '\n\n\nClustering variable means by cluster\n\n'
    output += str(groups)

    #transpose groups for value sorting in spreadsheet
    groups_T = groups.transpose()
    #print('\nGROUPS_T\n', groups_T, '\n')
        
    #add columns for sorting 
    groups_T['Total'] = groups_T.sum(axis=1)
    for col in groups_T.columns:
        if col == 'Total': break
        new_col_name =  'Group ' + str(col) + ' %'
        groups_T[new_col_name] = groups_T[col] / groups_T['Total'] * 100
        groups_T[new_col_name] = groups_T[new_col_name].round().astype('int')

    #print('\nGROUPS_T\n', groups_T, '\n')

    #save prepped data
    df.to_csv(os.path.join(output_dir, 'assignments.csv'), index=False)
    groups_T.to_csv(os.path.join(output_dir, 'groups.csv'))
    with open(os.path.join(output_dir, 'groups.txt'), 'w') as f: f.write(output) 

    return groups

def plot_cluster_sizes(df, output_dir):
    """
    Plots the "Frequencies" column in provided df, and saves png to output_dir.

    Args:
        df (pandas.DataFrame): data from data/processed/<NAME>-donors.csv.  
        output_dir (str): path to output directory.             

    Returns:
        None.
    """ 

    fig, ax = plt.subplots() 
    plt.axis("equal")
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    #group_frequencies = df['Cluster'].value_counts() #sorts by size 
    group_frequencies = df['Frequencies'] #keeps order of groups groupby
    total_frequencies = group_frequencies.sum()
    margin = total_frequencies * 0.05
    clusters_num = group_frequencies.count()

    lim = total_frequencies + (margin * (clusters_num + 1))
    ax.set_xlim((0, lim))
    ax.set_ylim((0, lim))

    #set color map for scatterplot/s
    #reference: https://stackoverflow.com/questions/36180477/assigning-custom-colors-to-clusters-using-numpy
    colors = {0:'r', 1:'b', 2:'g', 3:'y', 4:'m', 5:'c', 6:'k'}

    x_total = margin 
    y_mid = lim / 2
    color_idx = 0
    for freq in group_frequencies:
        radius = freq / 2
        x = radius + x_total
        y = y_mid
        color = colors[color_idx]
        ax.add_patch(plt.Circle((x, y), radius, color=color, alpha=0.9))
        
        x_total += freq + margin 
        color_idx += 1 
       
    plt.savefig(os.path.join(output_dir, 'frequencies_' + str(clusters_num) + '.png') , dpi=72)
