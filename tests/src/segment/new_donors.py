import os
import sys
from src.helpers import get_output_dir
from src.segment.new_donors import get_data, segment
from tests.src.helpers import compare_spreadsheets

def main():
    df = get_data()
    output_dir = get_output_dir('new_donors')
    output_expected_dir = output_dir.replace('output', 'output_expected')
    segment(df, output_dir)

    #compare assignments_2020.csv files
    assignments = os.path.join(output_dir, 'assignments_2020.csv')
    assignments_expected = os.path.join(output_expected_dir, 'assignments_2020.csv')
    compare_spreadsheets(assignments, assignments_expected)

    #compare assignments_2021.csv files
    assignments = os.path.join(output_dir, 'assignments_2021.csv')
    assignments_expected = os.path.join(output_expected_dir, 'assignments_2021.csv')
    compare_spreadsheets(assignments, assignments_expected)

    #compare groups.csv files
    groups = os.path.join(output_dir, 'groups.csv')
    groups_expected = os.path.join(output_expected_dir, 'groups.csv')
    compare_spreadsheets(groups, groups_expected)    

if __name__ == '__main__':
    sys.exit(main())
