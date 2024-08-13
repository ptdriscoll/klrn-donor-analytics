import os
import sys
from src.process.donors import process_data
from tests.src.helpers import compare_spreadsheets 
from src import (
    DATA_DONORS_WORKING,
    DATA_EXPECTED_DONORS_WORKING,
    DATA_DONORS_NEW_PROCESSED,
    DATA_EXPECTED_DONORS_NEW_PROCESSED,
)

def main():
    if True: #toggle whether to also generate and test working file
        if os.path.exists(DATA_DONORS_WORKING):
            os.remove(DATA_DONORS_WORKING)

    process_data()

    #compare working files
    compare_spreadsheets(DATA_DONORS_WORKING, DATA_EXPECTED_DONORS_WORKING)
    
    #compare processed files
    compare_spreadsheets(DATA_DONORS_NEW_PROCESSED, DATA_EXPECTED_DONORS_NEW_PROCESSED)

if __name__ == '__main__': 
    sys.exit(main())
