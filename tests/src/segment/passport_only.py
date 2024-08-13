import os
import sys
from src.helpers import get_data, get_output_dir
from src.segment.passport_only import set_categories, segment
from tests.src.helpers import compare_spreadsheets

def main():
    df = get_data()
    output_dir = get_output_dir('passport_only')
    output_expected_dir = output_dir.replace('output', 'output_expected')
    df_passport = set_categories(df, output_dir)
    segment(df_passport, output_dir)

    #compare assignment.csv files
    assignments = os.path.join(output_dir, 'assignments.csv')
    assignments_expected = os.path.join(output_expected_dir, 'assignments.csv')
    compare_spreadsheets(assignments, assignments_expected)

    #compare members.csv files
    members = os.path.join(output_dir, 'members.csv')
    members_expected = os.path.join(output_expected_dir, 'members.csv')
    compare_spreadsheets(members, members_expected)    

if __name__ == '__main__':
    sys.exit(main())