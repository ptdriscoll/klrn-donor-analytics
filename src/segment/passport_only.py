import os
import sys
from src.helpers import get_data, get_output_dir

def set_categories(df, output_dir):
    """
    Drops unneeded columns, sets Passport column to 0 or 1 values, save assignments.csv to 
    output_dir and returns df.

    Args:
        df (pandas.DataFrame): data from data/processed/<NAME>-donors.csv.  
        output_dir (str): path to output directory.          

    Returns:
        pandas.DataFrame.
    """    
    df = df.copy()
    df = df[['ID', 'Status', 'Passport']]
    df['Passport'] = df['Passport'].map(lambda x: 1.0 if x > 0 else 0)

    print('\n', df.shape)
    print('\n', df.tail())
    print('\nACTIVE DONORS: ', df['Status'].sum())

    df.to_csv(os.path.join(output_dir, 'assignments.csv'), index=False)
    return df

def segment(df, output_dir):
    """
    Prints out numbers of Passport members vs. non-Passport, and currently active members who
    have Passport vs. active members who do not have Passport. Also, saves ID column of Passport 
    members, both active and non-active to output_dir.

    Args:
        df (pandas.DataFrame): data from data/processed/<NAME>-donors.csv.  
        output_dir (str): path to output directory.          

    Returns:
        None.
    """     
    df_passport = df[df['Passport'] == 1.0]
    df_not_passport = df[df['Passport'] == 0]
    df_active = df_passport[df_passport['Status'] == 1.0]
    df_not_active = df_passport[df_passport['Status'] == 0]

    total = df_passport.shape[0] + df_not_passport.shape[0]
    print('\nPASSPORT DONORS:', df_passport.shape[0], "{:.0%}".format(df_passport.shape[0] / total))
    print('NON-PASSPORT:', df_not_passport.shape[0], "{:.0%}".format(df_not_passport.shape[0] / total))
    print('TOTAL:', total)

    total = df_active.shape[0] + df_not_active.shape[0]
    print('\nACTIVE PASSPORT:', df_active.shape[0], "{:.0%}".format(df_active.shape[0] / total))
    print('NON-ACTIVE:', df_not_active.shape[0], "{:.0%}".format(df_not_active.shape[0] / total))
    print('TOTAL:', total)

    df_passport = df_passport.rename({'ID': 'IDS'}, axis=1) #fixes to_csv glitch
    df_passport['IDS'].to_csv(os.path.join(output_dir, 'members.csv'), index=False)

def main():
    df = get_data()
    output_dir = get_output_dir('passport_only')
    df_passport = set_categories(df, output_dir)
    segment(df_passport, output_dir)

if __name__ == '__main__':
    sys.exit(main())
    