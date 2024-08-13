import os
import pandas as pd
import numpy as np

# ===================================
# landing page variables
# ===================================

pass_pages = ['WEBPASS', 'WEBPASC']
view_pages = ['VIEWER']

web_pages = [
    'WEBPASS',
    'WEBPASC',
    'FUNDPA',
    'PLGGEN',
    'PLGGENS',
    'PLGGENT',
    'WEBGNR',
    'PROSPGNR',
    'PROSPGNRS',
    'RENGNRD',
    'RENGNRE',
    'RENGNRES',
    'RENGNRM',    
    'ADDGNR',
    'LAPSEGNR',    
    'TEST',
    'PLGSUS',
    'PLGSUST',
    'WEBSUS',
    'PROSPSUS',
    'PROSPSUSS',
    'RENSUSD',
    'RENSUSE',
    'RENSUSES',
    'RENSUSM',
    'TESTSUS',    
    'ADDSUS',
    'LAPSESUS',    
    'ROSMRYWB',
    'CHEF',
    'BBQ',
    'ANTIQUES',
    'FIESTA',
    'GIVINGTUE' 
]

other_pages = [
    'AQ1TIME',
    'AQSUST',
    'OPR1TNOPLG',
    'OPRACD',
    'OPRSUNOPLG',
    'OTHER'
]


def split_each_column(file, cols_new=['Date', 'Page'], cols_keep=['Description', 'Count', 'Amount']):
    """
    Takes an Excel download from Allegiance, and splits the 'Each -' column into separate columns 

    Args:
        file (str): path to Excel spreadsheet to read data from. 
        cols_new (List[str]): columns that spreadsheet's 'Each--' column will be split into.
        cols_keep (List[str]): spreadsheet columns that will be kept.  

    Returns:
        pandas.DataFrame: with new and kept columns.       
    """
    
    print('\nSPLITTING "Each" COLUMN ...')
        
    df = pd.read_excel(file)    
    df = df.rename(columns = lambda x: x.strip()) 
    
    df_split = df['Each -'].str.split(' - ', expand=True)
    df_split.columns = cols_new    
    df_trim = df[cols_keep]
    df_donors = pd.concat([df_split, df_trim], axis=1)
    df_donors = df_donors[df_donors.iloc[:,0] != 'Total'] #remove 'Total' row
    
    #trim strings, and replace empty strings with nan
    df_donors = df_donors.apply(lambda x: x.str.strip().replace('', np.nan) if x.dtype=='object' else x)
    
    if 'Page' in df.columns: df_donors.Page = df_donors.Page.replace('', 'OTHER')     
    return df_donors   
 
def clean(file_raw,
          file_working, 
          cols_new = ['ID', 'Status', 'Passport', 'Date', 'Type', 'Page'],
          cols_keep = ['Count', 'Amount']):     
    """
    First checks whether file_working exists, and if so a dataframe is returned from that. If not:
        -file_raw is run through helpers.split_each_column() to create a dataframe   
        -any 'Passport' or 'Date' columns are converted to a pandas datetime column
        -a working Excel file, with '-working' appended to the name, is saved 
    
    Args:
        file_raw (str): path to Excel spreadsheet to read raw data from. 
        file_working (str): path to cached Excel spreadsheet, if data has been initially cleaned. 
        cols_new (List[str]): columns that spreadsheet's 'Each--' column will be split into.
        cols_keep (List[str]): spreadsheet columns that will be kept.  

    Returns:
        pandas.DataFrame: from either a cached working file or newly cleaned data. 
    """       
    
    print('\nGETTING CLEAN DATA ...')     
    
    #use working file if it exists    
    if os.path.isfile(file_working):         
        df = pd.read_excel(file_working) 
        print('\nUSING WORKING DF')        
    
    #else clean raw file and return df
    else:
        df = split_each_column(file_raw, cols_new, cols_keep)

        #set date columns to datetime
        if 'Passport' in cols_new: 
            df['Passport'] = df['Passport'].map(lambda x: pd.to_datetime(x, errors='coerce'))
            
        if 'Date'  in cols_new:
            df['Date'] = df['Date'].map(lambda x: pd.to_datetime(x))
        
        #save working file
        with pd.ExcelWriter(file_working, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False)

        print('\nUSING FRESH DF')

    return df    
