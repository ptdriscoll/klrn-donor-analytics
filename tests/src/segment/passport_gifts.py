import os
import sys
from src.helpers import get_data, get_output_dir
from src.segment.passport_gifts import set_categories, aggregate
from tests.src.helpers import compare_spreadsheets

def main():
    df = get_data()
    output_dir = get_output_dir('passport_gifts')
    output_expected_dir = output_dir.replace('output', 'output_expected')
    df_passport_gifts = set_categories(df, output_dir)
    aggregate(df_passport_gifts, output_dir)

    #compare assignments.csv files
    assignments = os.path.join(output_dir, 'assignments.csv')
    assignments_expected = os.path.join(output_expected_dir, 'assignments.csv')
    compare_spreadsheets(assignments, assignments_expected)

    #compare groups.csv files
    groups = os.path.join(output_dir, 'groups.csv')
    groups_expected = os.path.join(output_expected_dir, 'groups.csv')
    compare_spreadsheets(groups, groups_expected)    

if __name__ == '__main__':
    sys.exit(main())
