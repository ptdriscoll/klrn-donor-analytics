import os
import sys

from src.timeline.helpers import parse_args, get_data, create_timeline
from src.helpers import get_output_dir
from tests.src.helpers import compare_spreadsheets

def main():
    arg = parse_args()
    df = get_data() 
    output_dir = get_output_dir('timeline') 
    output_expected_dir = output_dir.replace('output', 'output_expected')
    output_file = os.path.join(output_dir, f'passport_gifts_{arg}.csv')

    create_timeline(df, output_file, arg, categories='passport_gifts')

    #compare csv files
    timeline = os.path.join(output_dir, output_file)
    timeline_expected = os.path.join(output_expected_dir, output_file)
    compare_spreadsheets(timeline, timeline_expected)

if __name__ == '__main__':
    sys.exit(main())
