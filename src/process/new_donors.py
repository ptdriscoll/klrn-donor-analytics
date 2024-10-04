import sys
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from .helpers import clean
from src import (
    DATA_DONORS_RAW, 
    DATA_DONORS_WORKING,
    DATA_DONORS_NEW_PROCESSED,
    DATA_START, 
    DATA_END, 
    YEAR_CUTOFF
)

def process_data(
    data_file_raw=DATA_DONORS_RAW,
    data_file_working=DATA_DONORS_WORKING,
    data_file_processed=DATA_DONORS_NEW_PROCESSED,
    date_start=DATA_START,
    date_end=DATA_END,
    year_cutoff=YEAR_CUTOFF
):
    """
    Gets member donation data file and then:
        -filters by date_start and date_end
        -filters by new donors up to a year before date_end, but includes all donations they made
         through date_end 
        -transforms variables to continuous values 
        -aggregate accounts with multiple pledges, on ['ID', 'Date'] 
        -saves csv file to data_file_processed        

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
    
    print('\n\nRUNNING src/process/new_donors.py process_data\n')

    # ===================================
    # get and clean member data
    # ===================================
   
    cols_new = ['ID', 'Status', 'Sustainer', 'Major', 'Passport', 'Date', 'Type', 'Gift', 'Page']
    cols_keep = ['Count', 'Paid to Date', 'Balance']
    df = clean(data_file_raw, data_file_working, cols_new, cols_keep)
    #print('\n', df.tail())    

    # ===================================
    # filter by date_start and date_end
    # ===================================
    
    print('\nDF SHAPE BEFORE FILTERS: ', df.shape)
    df = df[(df['Date'] >= date_start) & (df['Date'] <= date_end)]
    #print('\n', df.tail())

    # ==================================================
    # filter by new donors up to a year before date_end, but include all donations 
    # they made through date_end
    # ==================================================    

    ids_all = df['ID'].unique()
    print('\nALL DONORS:', len(ids_all))
    
    df1 = df[df['Type'] == 'NEW']
    print('TEST df1', len(df1))

    print('df1', df1['ID'].unique().size)   

    #get date_end_year_before as same date the year before date_end
    date_end_obj = datetime.strptime(date_end, '%Y-%m-%d')
    date_year_before_obj = date_end_obj - relativedelta(years=1)
    date_end_year_before = date_year_before_obj.strftime('%Y-%m-%d') 

    #keep new donors up to date_end_year_before, but all their activity through date_end
    df_new = df[(df['Type'].str.strip() == 'NEW')
                & (df['Date'] <= date_end_year_before)]
    ids_new = df_new['ID'].unique()
    df = df[df['ID'].isin(ids_new)] 

    print('\nNEW DONORS:', len(ids_new))
    #print('\nDF TAIL AFTER FILTERS:\n\n', df.tail)    

    
    # ====================================================
    # transform variables to continuous values
    # ====================================================

    #convert fields
    df['Status'] = df['Status'].map(lambda x: 1 if x.strip() == 'MEMB' else 0) 
    df['Passport'] = df['Passport'] - pd.offsets.DateOffset(years=1) #match 1-yr pledge window
    df['Passport'] = df.apply(lambda x: 1 if x['Passport'] < x['Date'] else 0, axis=1)
    df['Date'] = pd.to_datetime(df['Date']).dt.to_period(year_cutoff) #set to a year
    df['Gift'] = df['Gift'].map(lambda x: 1 if x.strip() == 'YES' else 0)

    #add new fields
    df['Payments'] = df['Paid to Date'] + df['Balance'] #add paid and balance  

    #keep select fields
    df = df[['ID', 'Status', 'Passport', 'Date', 'Gift', 'Payments']]

    print('\n', df.tail)

    # ====================================================
    # aggregate accounts with multiple pledges, on ['ID', 'Date']   
    # ====================================================
    
    print('BEFORE', len(df)) 

    aggreg = { 
        'Payments': 'sum',  
        'Status': 'max',
        'Passport': 'max',
        'Gift': 'max',    
    }

    df = df.groupby(['ID', 'Date']).agg(aggreg)
    df = df.reset_index()
    df = df.set_index('ID')
    df = df.rename(columns={'Payments':'Total_Payments', 'Date':'Years'})

    print('\n', df.tail)

    # ====================================================
    # save prepped copy  
    # ====================================================

    df.to_csv(data_file_processed)
    return 0

if __name__ == '__main__': 
    sys.exit(process_data())
