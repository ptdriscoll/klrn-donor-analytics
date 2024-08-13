import os
import sys
import argparse
import pandas as pd
from src.process.demographics import clean
from src import ROOT_DIR, DATA_DEMOGRAPHICS_PROCESSED

def parse_args():
    """
    Parses command-line argument to add as file_data argument to merge function. Options include:
        -cluster
        -new_donors
        -passport_gifts
        -passport_only

    Examples:
        $ python -m augment.demographics cluster 
        $ python -m augment.demographics new_donors 
        $ python -m augment.demographics passport_gifts 
        $ python -m augment.demographics passport_only

    Returns:
        str: filename specified by the user.
    """
    parser = argparse.ArgumentParser(description='Run augment module')
    parser.add_argument(
        'filename',
        type=str,
        help=('''Specify name of file to merge data overlay into, e.g. 
              cluster, new_donors, passport_gifts or passport_only'''
        ) 
    )
    arg, unknown = parser.parse_known_args()
    return arg.filename

def get_data(data_file_processed=DATA_DEMOGRAPHICS_PROCESSED):
    """
    Gets data from data/processed/demographics.csv, running src.process.demographics.clean()
    first if it doesn't exist, and returning a pandas.DataFrame.

    Arg:
        data_file_processed (str): path to where csv demographics data file is or will be.               

    Returns:
        pandas.DataFrame.
    """

    #create processed demographics data if it doesn't exist
    if not os.path.isfile(data_file_processed):
        clean()

    df = pd.read_csv(data_file_processed) 
    return df 

def get_category(name):
    """
    Get associated category for file name, for use in merge().

    Arg:
        name (str): file name returned by parse_args().

    Returns:
        str 
    """
    category = {
        'cluster': 'Cluster',
        'new_donors': 'Category',
        'passport_gifts': 'Category',
        'passport_only': 'Passport'
    }    
    return category[name]

def merge(df_demog, data_file, category):
    """
    Merges dataframe of WealthEngine demographics data with dataframe from donor file
    on ID, then aggregates categories to means. Result is saved to demographics.csv.

    Args:
        df_demog (pandas.DataFrame): demographics data from WealthEngine.
        data_file (str): path to CSV file with donor data. 
        category (str): name of column in data_file to aggregate demographic data on.

    Returns:
        None.     
    """

    print('\nDEMOGRAPHICS:', df_demog.shape)
    print('\n', df_demog.head())
    
    df_seg = pd.read_csv(data_file)
    df_seg = df_seg[['ID', category]]    
    
    print('\nSEGMENTS:', df_seg.shape)
    print('\n', df_seg.head())
    
    df = pd.merge(df_seg, df_demog, on='ID', how='left')
    
    print('\nSEGMENTS MERGED', df.shape)
    print('\n', df.head())
    
    df = df[[category, 'Age', 'Female', 'Income']]
    groups = df.groupby(category).mean()
    groups['Frequencies'] = df.groupby(category).size() 
    print('\n', groups)

    file_output = data_file.replace('assignments', 'demographics')
    groups.to_csv(file_output)

def main():
    arg = parse_args()
    path = os.path.join(ROOT_DIR, 'output', arg, 'assignments.csv')

    if os.path.isfile(path):
        category = get_category(arg)
        df_demog = get_data()
        merge(df_demog, path, category)

    else:    
        print('\nFile does not exist:\n', '  ', path)

if __name__ == '__main__': 
    sys.exit(main())
