import os
import sys

from src.timeline.helpers import parse_args, get_data, create_timeline
from src.helpers import get_output_dir
from tests.src.helpers import compare_spreadsheets

def main():
    arg = parse_args()
    df = get_data()    
    output_dir = get_output_dir('timeline') 
    output_file = os.path.join(output_dir, f'all_{arg}.csv') 
    output_file_expected = output_file.replace('output', 'output_expected')   
    create_timeline(df, output_file, arg, categories='all')

    #compare csv files
    compare_spreadsheets(output_file, output_file_expected)

if __name__ == '__main__':
    sys.exit(main())
