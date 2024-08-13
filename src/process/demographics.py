import sys
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
from .helpers import clean
from src import DATA_DEMOGRAPHICS_RAW, DATA_DEMOGRAPHICS_PROCESSED

def clean(
        data_file_raw=DATA_DEMOGRAPHICS_RAW, 
        data_file_processed=DATA_DEMOGRAPHICS_PROCESSED
):
    """
    Transforms Gender, Age and Income range columns to Age, Female and minimum Income 
    columns from WealthEngine output file. Renames AcctID column to ID and sets ID as 
    index. Drops all other columns. 

    Args:
        data_file_raw (str): path to raw Excel file to start with.
        data_file_processed (str): path to where to save final csv file output.               
    
    Returns:
        int: 0 to indicate success.    
    """
    
    df = pd.read_excel(data_file_raw)
    df = df[['AcctID', 'Age', 'Gender', 'Income']]
    df = df.rename(columns={'AcctID': 'ID'})
    df = df.set_index('ID')
    
    #transform Gender and Income columns  
    gender = {'M': 0, 'F': 1, np.nan: np.nan}
    df['Gender'] = df['Gender'].map(lambda x: gender[x])
    df = df.rename(columns={'Gender': 'Female'})
    
    income_levels = {'$1-$50K': 1,
                     '$50K-$100K': 50000,
                     '$100K-$250K': 100000,
                     '$250K-$500K': 250000,
                     '$500K+': 500000, 
                     'Unable to rate': np.nan}
    df['Income'] = df['Income'].map(lambda x: income_levels[x.strip()])
    
    print('\n', df.shape)
    print('\n', df.head())
    print('\nNAN COUNTS:')
    print(df.isna().sum())
    
    print('\nAVERAGES:')
    print('Age:', df['Age'].mean())
    print('Female:', df['Female'].mean())
    print('Min Income:', df['Income'].mean())
    
    
    #save prepped copy  
    df.to_csv(data_file_processed)
    return 0  
    
if __name__ == '__main__': 
    sys.exit(clean())
    