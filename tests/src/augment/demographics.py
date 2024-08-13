import os
import sys
from tests.src.helpers import compare_spreadsheets 
from src import ROOT_DIR
from src.augment.demographics import (
    parse_args, 
    get_data, 
    get_category,
    merge 
)

def main():
    arg = parse_args()
    path = os.path.join(ROOT_DIR, 'tests', 'output', arg, 'assignments.csv')

    if os.path.isfile(path):
        #merge data
        category = get_category(arg)
        df_demog = get_data()
        merge(df_demog, path, category)

        #compare files
        output_file = path.replace('assignments', 'demographics')
        output_expected_file = output_file.replace('output', 'output_expected')
        demographics = os.path.join(output_file)
        demographics_expected = os.path.join(output_expected_file)
        compare_spreadsheets(demographics, demographics_expected)

    else:    
        print('\nFile does not exist:\n', '  ', path)    

if __name__ == '__main__': 
    sys.exit(main())
