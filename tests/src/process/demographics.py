import os
import sys
from src.process.demographics import clean
from tests.src.helpers import compare_spreadsheets 
from src import DATA_DEMOGRAPHICS_PROCESSED, DATA_EXPECTED_DEMOGRAPHICS_PROCESSED

def main():
    clean()

    #compare working files
    compare_spreadsheets(DATA_DEMOGRAPHICS_PROCESSED, DATA_EXPECTED_DEMOGRAPHICS_PROCESSED)

if __name__ == '__main__': 
    sys.exit(main())
