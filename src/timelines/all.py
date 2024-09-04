import os
import sys

from .helpers import parse_args, get_data, get_time_frequency
from src.helpers import get_output_dir
from src import DATA_START, DATA_END

from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

def create_timeline(
    df,
    output_file,
    time_period,
    date_start=DATA_START,
    date_end=DATA_END
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
        time_period (str): Desired time period frequency for timeline. 
        date_start (str): for date range filter, is inclusive, in format 2019-10-01.
        date_end (str): for date range filter, is inclusive, in format 2022-09-30.
     """  

    df = df[(df['Date'] >= date_start) & (df['Date'] <= date_end)] #filter by date range    
    df['Payments'] = df['Paid to Date'] + df['Balance'] #add paid and balance
    df = df[['Date', 'Payments']] #keep only needed fields

    time_period_col, freq_arg = get_time_frequency(time_period)
    df = df.rename(columns={'Date': time_period_col, 'Payments': 'Donations'})
    df[time_period_col] = pd.to_datetime(df[time_period_col]).dt.to_period(freq_arg) #set time period

    aggreg = {'Donations': 'sum'}
    df = df.groupby(time_period_col).agg(aggreg)

    df.to_csv(output_file)

def main():
    arg = parse_args()
    df = get_data() 
    output_dir = get_output_dir('timelines') 
    output_file = os.path.join(output_dir, f'all_{arg}.csv')  
    create_timeline(df, output_file, arg)

if __name__ == '__main__':
    sys.exit(main())
