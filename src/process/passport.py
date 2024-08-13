import sys
sys.path.insert(0, 'T:\\Public Relations\\ONLINE\\Passport\\STATS')

from VPPA.app.queries import get_channel_views_members as get_views
from VPPA.app.helpers import normalize_shows

def get_passport_views(date_start, date_end, ids):
    """
    Gets top Passport shows watched by members 

    Args:
        date_start (str): format is '2022-09-01'
        date_end (str): format is '2022-09-01''
        ids (str): list of ids for SQL query, with format '1,2,3'
        
    Returns:
        pandas.DataFrame: with columns Show and Views, and index starting at 1
    """
    
    df = get_views(date_start, date_end, ids)         
    df = normalize_shows(df, 'content_channel') #cleans text formatting
    df = df.drop('alleg_account_id', axis=1)
    df = df.rename({'content_channel': 'Show', 'total_count': 'Views'}, axis=1)
   
    
    #group by Show and sort by Views
    df = df.groupby(['Show']).sum()
    df = df.sort_values('Views', ascending=False)
    df = df.reset_index()
    df.index += 1 #start index at 1      
   
    return df
