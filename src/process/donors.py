import sys
import pandas as pd
from .helpers import clean, pass_pages, web_pages
from src import (
    DATA_DONORS_RAW, 
    DATA_DONORS_WORKING,
    DATA_DONORS_PROCESSED,
    DATA_START, 
    DATA_END, 
    YEAR_CUTOFF,
)

def process_data(
    data_file_raw=DATA_DONORS_RAW,
    data_file_working=DATA_DONORS_WORKING,
    data_file_processed=DATA_DONORS_PROCESSED,
    date_start=DATA_START,
    date_end=DATA_END,
    year_cutoff=YEAR_CUTOFF
):

    """
    Processes data for use in donor_profiles and/or segment analyses such as passport_donors:
        -filters by start and end dates
        -transform variables to continuous values, creating new columns where needed
        -aggregates rows (where each is a donor pledge) to lifetime values (where each row is a donor)
        -saves a prepped csv file by appending '-prepped' to file name

    Args:
        data_file_raw (str): path to raw Excel file to start with.
        data_file_working (str): path to working Excel file if raw file has been initially cleaned.
        data_file_processed (str): path to where to save final csv file output.
        date_start (str): for date range filter, is inclusive, in format 2019-10-01.
        date_end (str): for date range filter, is inclusive, in format 2022-09-30.
        year_cutoff (str): where to cutoff year timeframe, is inclusive, defaults to fy.                    
    
    Returns:
        int: 0 to indicate success.
    
    References for @year_cutoff:
      -https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html
      -https://stackoverflow.com/questions/22205159/format-pandas-datatime-object-to-show-fiscal-years-from-feb-to-feb-and-be-format
    
    """

    # ===================================
    # get and clean member data
    # ===================================
   
    cols_new = ['ID', 'Status', 'Sustainer', 'Major', 'Passport', 'Date', 'Type', 'Gift', 'Page']
    cols_keep = ['Count', 'Paid to Date', 'Balance']
    df = clean(data_file_raw, data_file_working, cols_new, cols_keep)    
    #print('\n', df.tail())

    # ===================================
    # filter by date range
    # ===================================
    
    df = df[(df['Date'] >= date_start) & (df['Date'] <= date_end)]
    #print('\n', df.tail())

    # ==================================================
    # transform variables to continuous values
    # ==================================================  
    
    #convert fields
    df['Status'] = df['Status'].map(lambda x: 1 if x.strip() == 'MEMB' else 0) 
    df['Sustainer'] = df['Sustainer'].map(lambda x: 1 if x.strip() == 'ACT' else 0)
    df['Major'] = df['Major'].map(lambda x: 1 if pd.notnull(x) else 0)
    df['Passport'] = df['Passport'] - pd.offsets.DateOffset(years=1) #match 1-yr pledge window
    df['Passport'] = df.apply(lambda x: 1 if x['Passport'] < x['Date'] else 0, axis=1)
    df['Date'] = pd.to_datetime(df['Date']).dt.to_period(year_cutoff) #set to a year
    df['Gift'] = df['Gift'].map(lambda x: 1 if x.strip() == 'YES' else 0)
    
    #add new fields
    df['Rejoin'] = df['Type'].map(lambda x: 1 if x.strip() == 'EXPR' else 0) 
    df['Renew'] = df['Type'].map(lambda x: 1 if x.strip() == 'RENL' else 0) 
    df['Add'] = df['Type'].map(lambda x: 1 if x.strip() == 'ADDG' else 0) 
    df['New'] = df['Type'].map(lambda x: 1 if x.strip() == 'NEW' else 0)  
    df['Payments'] = df['Paid to Date'] + df['Balance'] #add paid and balance   
    
    online_pages = pass_pages + web_pages
    df['Online'] = df['Page'].str.strip().isin(online_pages)
    df['Online'] = df['Online'].map(lambda x: 1 if x == True else 0)
    
    #delete old fields
    df = df.drop(['Type', 'Page', 'Paid to Date', 'Balance'], axis=1) 
    
    print('\n', df.tail())

    # ==================================================
    # aggregate accounts (on ID) with multiple pledges 
    #
    # then calculate annual averages of pledges and payments for cluster analysis
    #   (to normalize for varying active years among donors
    #
    # but preserve number of years along with total pledge counts and payment amounts 
    #   (to later recalucate cluster averages, without using averages to calculate more averages)  
    #
    # all others stay as lifetime averages, to focus on donor behaviors instead of pledges  
    # ==================================================
    
    aggreg = { 
        'Count': 'sum',
        'Payments': 'sum',  
        'Status': 'mean',
        'Sustainer': 'mean',
        'Major': 'mean',
        'Passport': 'mean',
        'Gift': 'mean',    
        'Rejoin': 'mean',
        'Renew': 'mean',
        'Add': 'mean',     
        'New': 'mean',
        'Online': 'mean',
        'Date': 'nunique'
    }
    
    df = df.groupby('ID').agg(aggreg)
    df = df.rename(columns={'Count':'Total_Count', 
                            'Payments':'Total_Payments', 
                            'Date':'Num_Years'})
    df['Annual_Payment'] = df['Total_Payments'] / df['Num_Years']
    df['Annual_Count'] = df['Total_Count'] / df['Num_Years']
    
    print('\n', df.tail())
    
    # ===================================
    # save processed copy 
    # ===================================    
   
    df.to_csv(data_file_processed)
    return 0

if __name__ == '__main__': 
    sys.exit(process_data())
