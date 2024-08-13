import os

print()
print('RUNNING TEST:', os.getenv('TESTS', 'False'))

base_dir = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.normpath(os.path.join(base_dir, '..')) 
from .config import PASSPORT_APP

#not running a test
if not os.getenv('TESTS', False):
    from .config import (
        DATA_DONORS, 
        DATA_DEMOGRAPHICS, 
        DATA_START, 
        DATA_END, 
        YEAR_CUTOFF,
        PASSPORT_VIEWS_START_DATE,
        PASSPORT_VIEWS_END_DATE
    )   

    DATA_RAW_DIR = os.path.join(ROOT_DIR, 'data', 'raw') 
    DATA_PROCESSED_DIR = os.path.join(ROOT_DIR, 'data', 'processed') 

    DATA_DONORS_RAW = os.path.join(DATA_RAW_DIR, DATA_DONORS)
    DATA_DEMOGRAPHICS_RAW = os.path.join(DATA_RAW_DIR, DATA_DEMOGRAPHICS)

    DATA_DONORS_WORKING = os.path.join(DATA_PROCESSED_DIR, DATA_DONORS.split('.xlsx')[0] + '-working.xlsx')
    DATA_DONORS_PROCESSED = os.path.join(DATA_PROCESSED_DIR, DATA_DONORS.split('.xlsx')[0] + '.csv')
    DATA_DONORS_NEW_PROCESSED = os.path.join(DATA_PROCESSED_DIR, DATA_DONORS.split('.xlsx')[0] + '-new.csv')
    DATA_DEMOGRAPHICS_PROCESSED = os.path.join(DATA_PROCESSED_DIR, DATA_DEMOGRAPHICS.split('.xlsx')[0] + '.csv')

    PASSPORT_VIEWS_START = PASSPORT_VIEWS_START_DATE 
    PASSPORT_VIEWS_END = PASSPORT_VIEWS_END_DATE

#running a test
else:
    DATA_RAW_DIR = os.path.join(ROOT_DIR, 'tests', 'data', 'raw') 
    DATA_PROCESSED_DIR = os.path.join(ROOT_DIR, 'tests', 'data', 'processed') 
    DATA_EXPECTED_PROCESSED_DIR = os.path.join(ROOT_DIR, 'tests', 'data_expected', 'processed') 

    DATA_DONORS_RAW = os.path.join(DATA_RAW_DIR, 'donors.xlsx')
    DATA_DEMOGRAPHICS_RAW = os.path.join(DATA_RAW_DIR, 'demographics.xlsx')

    DATA_DONORS_WORKING = os.path.join(DATA_PROCESSED_DIR, 'donors-working.xlsx')
    DATA_DONORS_PROCESSED = os.path.join(DATA_PROCESSED_DIR, 'donors.csv')
    DATA_DONORS_NEW_PROCESSED = os.path.join(DATA_PROCESSED_DIR, 'donors-new.csv')
    DATA_DEMOGRAPHICS_PROCESSED = os.path.join(DATA_PROCESSED_DIR, 'demographics.csv')

    DATA_EXPECTED_DONORS_WORKING = os.path.join(DATA_EXPECTED_PROCESSED_DIR, 'donors-working.xlsx')
    DATA_EXPECTED_DONORS_PROCESSED = os.path.join(DATA_EXPECTED_PROCESSED_DIR, 'donors.csv')
    DATA_EXPECTED_DONORS_NEW_PROCESSED = os.path.join(DATA_EXPECTED_PROCESSED_DIR, 'donors-new.csv')
    DATA_EXPECTED_DEMOGRAPHICS_PROCESSED = os.path.join(DATA_EXPECTED_PROCESSED_DIR, 'demographics.csv')

    DATA_START = '2019-10-01' 
    DATA_END = '2022-09-30'

    # where to cutoff annual timeframe, which is inclusive 
    # references:
    #   -https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html
    #   -https://stackoverflow.com/questions/22205159/format-pandas-datatime-object-to-show-fiscal-years-from-feb-to-feb-and-be-format
    YEAR_CUTOFF = 'Y-SEP' #standard fiscal year

    # the date range to filter Passport views - both are inclusive
    PASSPORT_VIEWS_START = '2019-10-01' 
    PASSPORT_VIEWS_END = '2022-09-30'
