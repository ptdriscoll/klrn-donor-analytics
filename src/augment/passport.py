import os
import sys
from .helpers import parse_args
import pandas as pd 
from src import (
    ROOT_DIR, 
    PASSPORT_APP, 
    PASSPORT_VIEWS_START, 
    PASSPORT_VIEWS_END
)

sys.path.insert(0, PASSPORT_APP)

from VPPA.app.queries import get_channel_views_genres_members as get_views
from VPPA.app.helpers_process import normalize_shows

def get_passport_views(date_start, date_end, ids):
    """
    Gets top Passport shows watched by members. 

    Args:
        date_start (str): format is '2022-09-01'.
        date_end (str): format is '2022-09-01' and is inclusive.
        ids (List[str]): list of ids for SQL query, with format '1,2,3'.
        
    Returns:
        pandas.Dataframe: with columns Show and Views, and index starting at 1.
    """
    
    df = get_views(date_start, date_end, ids)  
    df = normalize_shows(df, 'content_channel') #cleans text formatting
    df = df.drop('alleg_account_id', axis=1)
    df = df.rename({'content_channel': 'Show', 'total_count': 'Views', 'genre': 'Genre'}, axis=1)   
    
    #group by Show and sort by Views
    aggreg = {'Views': 'sum', 'Genre': lambda x: x.iloc[-1]}
    df = df.groupby(['Show']).agg(aggreg)
    df = df.sort_values('Views', ascending=False)
    df = df.reset_index()
    df.index += 1 #start index at 1     
   
    return df

def get_save_views(df, input_file, date_start, date_end, title_append):
    """
    Creates a list of ids from df, invokes get_passport_views(), and saves views to output_dir. 

    Args:
        df (pandas.DataFrame): data from output/<directory>/assignments.csv.  
        input_file (str): path to input file.
        date_start (str): format is '2022-09-01'.
        date_end (str): format is '2022-09-01' and is inclusive.
        title_append (str): gets appended to file name to make it unique, such as '_views_passport' 

    Returns:
        None.    
    """

    ids = ','.join(str(x) for x in df['ID'])
    df_views = get_passport_views(date_start, date_end, ids) 
    output_file = input_file.replace('assignments', title_append)
    df_views.to_csv(output_file)  

def get_passport_views_per_group(name, input_file, date_start=PASSPORT_VIEWS_START, date_end=PASSPORT_VIEWS_END):
    """
    Uses name to fetch data file, and uses get_save_views() to get and save Passport views for all
    Passport members, both globally and per each category or cluster if categories or clusters exist.

    Args:
        name (str): name of data directory in file, output/<name>/assignments.csv.  
        input_file (str): path to inputfile, output/<name>/assignments.csv. 
        date_start (str): format is '2022-09-01'.
        date_end (str): format is '2022-09-01' and is inclusive.  
    
    Returns:
        None.    
    """
    
    df = pd.read_csv(input_file)
    df = df[df['Passport'] == 1]
      
    title_append = 'views' if name == 'passport_only' else 'views_all'
    get_save_views(df, input_file, date_start, date_end, title_append)

    if name == 'passport_gifts' or name == 'new_donors':
        for category in ['Passport', 'Both']:
            df_category = df[df['Category'] == category] 
            title_append = 'views_' + category.lower()
            get_save_views(df_category, input_file, date_start, date_end, title_append)

    if name == 'cluster':
        for cluster in df['Cluster'].unique():
            df_cluster = df[df['Cluster'] == cluster] 
            title_append = 'views_' + str(cluster)
            get_save_views(df_cluster, input_file, date_start, date_end, title_append)

def main():
    arg = parse_args()
    input_file = os.path.join(ROOT_DIR, 'output', arg, 'assignments.csv')
    
    if os.path.isfile(input_file):
        get_passport_views_per_group(arg, input_file)

    else:    
        print('\nFile does not exist:\n', '  ', input_file)    

if __name__ == '__main__':
    sys.exit(main())
