import os
import sys
from src.helpers import get_data, get_output_dir

def set_categories(df, output_dir=None):
    """
    Creates a Category column in df and sets values based on Passport and Gift flags:
        0: Neither
        1: Passport
        2: Gift
        3: Both

    Saves updated df to output_dir, and returns updated df.

    Args:
        df (pandas.DataFrame): data from data/processed/<NAME>-donors.csv.  
        output_dir (str): path to output directory.          

    Returns:
        pandas.DataFrame.       
    """

    categories_map = {0: 'Neither', 1: 'Passport', 2: 'Gift', 3: 'Both'}

    def set_category(a, b):
        c = 0 if a == 0 else 1
        d = 0 if b == 0 else 2 
        return c + d

    df['Category'] = df.apply(lambda x: set_category(x['Passport'], x['Gift']), axis=1)
    df['Category'] = df['Category'].map(categories_map)

    print('\nDF SHAPE:', df.shape)
    print('\n', df.tail(15))
    
    if output_dir:
        df.to_csv(os.path.join(output_dir, 'assignments.csv'), index=False)
        
    return df

def aggregate(df, output_dir):
    """
    Aggregates categories from set_categories(), and saves results to output_dir.

    Args:
        df (pandas.DataFrame): data from data/processed/<NAME>-donors.csv.  
        output_dir (str): path to output directory.          

    Returns:
        None.
    """
    aggreg = { 
        'Total_Count': 'sum',
        'Total_Payments': 'sum',
        'Num_Years': 'sum',
        'Status': 'mean',    
        'Sustainer': 'mean',
        'Major': 'mean',
        'Passport': 'mean',
        'Gift': 'mean',
        'Rejoin': 'mean',
        'Renew': 'mean',
        'Add': 'mean',
        'New': 'mean',
        'Online': 'mean'
    }

    df = df.drop(['ID'], axis=1)
    groups = df.groupby('Category').agg(aggreg)   
    groups['Frequencies'] = df.groupby('Category').size()   
    groups['Annual_Payment'] = groups['Total_Payments'] / groups['Num_Years']
    groups['Annual_Count'] = groups['Total_Count'] / groups['Num_Years']  
    groups = groups.drop(['Total_Count', 'Num_Years', 'Passport', 'Gift'], axis=1)
    #groups = groups.drop(['Passport', 'Gift'], axis=1)

    groups.to_csv(os.path.join(output_dir, 'groups.csv'))
    print('\n\nGROUPS:\n', groups)

def main():
    df = get_data()
    output_dir = get_output_dir('passport_gifts')
    df_passport_gifts = set_categories(df, output_dir)
    aggregate(df_passport_gifts, output_dir)

if __name__ == '__main__':
    sys.exit(main())
