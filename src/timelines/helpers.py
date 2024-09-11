import argparse
import pandas as pd
from src.process.helpers import clean
from src.segment.passport_gifts import set_categories
from src import (
    DATA_DONORS_RAW, 
    DATA_DONORS_WORKING, 
    YEAR_CUTOFF,
    DATA_START, 
    DATA_END
)

def parse_args():
    """
    Parses command-line argument that will be translated into an offset alias to be added
    to a pandas dt.to_period() method to set time period frequencies. Options include:
        -annual
        -monthly
        -weekly

    Examples:
        $ python -m src.timeline.passport_gifts annual
        $ python -m src.timeline.passport_gifts weekly

    Returns:
        str: time period specified by the user.
    """
    parser = argparse.ArgumentParser(description='Run timelines module')
    parser.add_argument(
        'frequency',
        type=str,
        nargs='?',
        default='annual',
        help=('Specify time period frequency to plot timeline, e.g. annual, monthly or weekly') 
    )
    arg, unknown = parser.parse_known_args()
    return arg.frequency

def get_data():
    """
    Gets dataframe from donors working data in data/processed/, creating 
    donors working data from donors raw data in data/raw/ if needed.

    Returns:
        pandas.DataFrame.
    """
    cols_new = ['ID', 'Status', 'Sustainer', 'Major', 'Passport', 'Date', 'Type', 'Gift', 'Page']
    cols_keep = ['Count', 'Paid to Date', 'Balance']
    df = clean(DATA_DONORS_RAW, DATA_DONORS_WORKING, cols_new, cols_keep)
    return df

def get_time_frequency(time_period):
    """
    Gets freq argument to be used in pd.to_datetime(df['Date']).dt.to_period('M'). 

    Args:
        time_period (str): Desired time period frequency for timeline.   

    Returns:
        str: freq argument to be used in pd.to_datetime().                
    
    Reference:
        https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html  
    """  
    freq = {
        'weekly': 'W-SUN',
        'monthly': 'M',
        'annual': YEAR_CUTOFF
    }

    return freq[time_period]

def add_category_column(df, categories):
    """
    Adds Category column to dataframe, so timeline can include segmented layers.

    Args:
        df (pandas.DataFrame):  dataframe of donations from donors working data in data/processed/.
        categories (str): Categories label to determine timeline segments: 'all', 'passport_gifts, 'new_other'. 

    Returns:
        pandas.DataFrame with added Category column.        
    """
    if categories == 'all':
        df['Category'] = 'Donations'

    if categories == 'passport_gifts':
        df['Passport'] = df['Passport'] - pd.offsets.DateOffset(years=1) #match 1-yr pledge window
        df['Passport'] = df.apply(lambda x: 1 if x['Passport'] < x['Date'] else 0, axis=1) 
        df['Gift'] = df['Gift'].map({'YES': 1, 'NO': 0})
        df = set_categories(df) 

    return df    

def create_timeline(
    df,
    output_file,
    time_period,
    categories,
    date_start=DATA_START,
    date_end=DATA_END
):
    """
    Gets member donation data file and then:
        -filters by date_start and date_end
        -creates Payments and Category columns
        -drops unneeded columns
        -turns Date column into time frequencies
        -creates pivot table with Date as index, categories as 
         columns, and Payments summed
        -saves csv file as output_file        

    Args:
        df (pandas.DataFrame):  dataframe of donations from donors working data in data/processed/.
        output_file (str): path to where results are saved as a csv file.
        time_period (str): Desired time period frequency for timeline. 
        categories (str): Categories label to determine timeline segments: 'all', 'passport_gifts, 'new_other'.
        date_start (str): for date range filter, is inclusive, in format 2019-10-01.
        date_end (str): for date range filter, is inclusive, in format 2022-09-30.
     """  

    df = df[(df['Date'] >= date_start) & (df['Date'] <= date_end)] #filter by date range    
    df['Payments'] = df['Paid to Date'] + df['Balance'] #add paid and 
    df = add_category_column(df, categories) #add segments (or all 'Donations')
    df = df[['Date', 'Payments', 'Category']] #keep only needed fields

    #create timeline frequencies
    freq_arg = get_time_frequency(time_period)
    df['Date'] = pd.to_datetime(df['Date']).dt.to_period(freq_arg) #set time period

    table = df.pivot_table(index='Date', 
                       columns='Category', 
                       values='Payments', 
                       aggfunc='sum', 
                       fill_value=0)

    table.index.name = None
    table.columns.name = None
    table.to_csv(output_file)
 