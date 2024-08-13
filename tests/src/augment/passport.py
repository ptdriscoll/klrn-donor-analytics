import os
import sys
import shutil
from pathlib import Path
from tests.src.helpers import compare_spreadsheets 
from src import ROOT_DIR
from src.augment.passport import (
    parse_args, 
    get_passport_views_per_group 
)

def run_compare_spreadsheets(input_file, name):
    """
    Renames input_file path, creates expected file path and then runs compare_spreadsheets()
    to compare the new file with the expected results.

    Args:
        views (str): path to input file.
        name (str): name to replace input file name with. 

    Returns:
        None.    
    """
    views = input_file.replace('assignments', name)
    views_expected = views.replace('output', 'output_expected')
    compare_spreadsheets(views, views_expected) 

def main():
    arg = parse_args()
    input_file = os.path.join(ROOT_DIR, 'tests', 'output', arg, 'assignments.csv')

    if arg == 'cluster':
        input_file_dir_path = Path(os.path.dirname(input_file))
        if input_file_dir_path.is_dir():
            file_copy = input_file.replace('output', 'output_expected')
            shutil.copy(file_copy, input_file)

        else:    
            print('\nDirectory does not exist:\n', '  ', input_file_dir_path)    
    
    if os.path.isfile(input_file):
        get_passport_views_per_group(arg, input_file)

        #compare passport_only files 
        if arg == 'passport_only':
            run_compare_spreadsheets(input_file, 'views')

        #compare passport_gifts files or new_donors files
        if arg == 'passport_gifts' or arg == 'new_donors':
            for name in ['views_all', 'views_both', 'views_passport']: 
                run_compare_spreadsheets(input_file, name)  

        #compare cluster files 
        if arg == 'cluster': 
            for name in ['views_0','views_1', 'views_2', 'views_3', 'views_all']:  
                run_compare_spreadsheets(input_file, name)              

    else:    
        print('\nFile does not exist:\n', '  ', input_file) 

if __name__ == '__main__':
    sys.exit(main())
