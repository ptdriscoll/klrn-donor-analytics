import os
import sys

from .helpers import parse_args, get_data
from src.helpers import get_output_dir
from src import DATA_START, DATA_END, YEAR_CUTOFF

from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

def create_timeline(
    df,
    output_file,
    date_start=DATA_START,
    date_end=DATA_END,
    year_cutoff=YEAR_CUTOFF
):
    """
    Gets member donation data file and then:
        -filters by needed fields, and date_start and date_end
        -creates time frequency column
        -aggregate donations on on ['time_frequency'] 
        -saves csv file as output_file        

    Args:
        df (pandas.DataFrame):  dataframe of donations from donors working data in data/processed/.
        output_file (str): path to where results are saved as a csv file.
        date_start (str): for date range filter, is inclusive, in format 2019-10-01.
        date_end (str): for date range filter, is inclusive, in format 2022-09-30.
        year_cutoff (str): where to cutoff year timeframe, is inclusive, defaults to fy.                    
    
    References for @year_cutoff:
      -https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html
      -https://stackoverflow.com/questions/22205159/format-pandas-datatime-object-to-show-fiscal-years-from-feb-to-feb-and-be-format    
    """  

    df = df[(df['Date'] >= date_start) & (df['Date'] <= date_end)] #filter by date range    
    df['Payments'] = df['Paid to Date'] + df['Balance'] #add paid and balance
    df['Date'] = pd.to_datetime(df['Date']).dt.to_period(year_cutoff) #set years
    df = df[['Date', 'Payments']] #keep only needed fields
    df = df.rename(columns={'Date': 'Year', 'Payments': 'Donations'})

    aggreg = {'Donations': 'sum'}
    df = df.groupby('Year').agg(aggreg)
    df.to_csv(output_file)

def main():
    arg = parse_args()
    df = get_data() 
    output_dir = get_output_dir('timelines') 
    output_file = os.path.join(output_dir, f'all_{arg}.csv')  
    create_timeline(df, output_file)

if __name__ == '__main__':
    sys.exit(main())
