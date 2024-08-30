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
    output_dir,
    date_start=DATA_START,
    date_end=DATA_END,
    year_cutoff=YEAR_CUTOFF
):
    pass

def main():
    arg = parse_args()
    df = get_data() 
    output_dir = get_output_dir('timelines')   

    print('\nCHECKS:')
    print('ARG:', arg)
    print('DF HEAD:\n', df.head())
    print('\nOUTPUT_DIR:', output_dir)

if __name__ == '__main__':
    sys.exit(main())
