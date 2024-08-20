import os
import sys
from src import DATA_DONORS_NEW_PROCESSED
from src.helpers import get_output_dir
from src.process.new_donors import process_data
import pandas as pd

def get_data(data_file_processed=DATA_DONORS_NEW_PROCESSED):
    """
    Gets data from data/processed/donors-new.csv, running process_data() first if it 
    doesn't exist, and returning a pandas.DataFrame.

    Arg:
        data_file_processed (str): path to where csv data file is or will be.               

    Returns:
        pandas.DataFrame.
    """

    #create processed data if it doesn't exist
    if not os.path.isfile(data_file_processed):
        process_data()

    df = pd.read_csv(data_file_processed) 
    return df 

def segment(df, output_dir):
    """
    Each year of data is iterated over:
        -The first year includes all new donors over all years, and each donors donations over all 
         years are aggregated, including renewals and add gifts, and their years of donations counted.
        -The next year excludes new donors from the previous year, as well as their subsequent donations
         over all years.
        -This is repeated for each year. 

    Output:
        -For each year's iteration, each donor is assigned a category of: 'Neither', 'Passport', 'Gift', 
         or 'Both' based on Passport and Gift flags, and the data is saved to to assignments_<year>.csv.
        -For each year's iteration, assignments are aggregated by categories and appended to a dataframe 
         accumulator. When the iterations finishes, the dataframe acculator is saved to groups.csv.     
            
    Args:
        df (pandas.DataFrame): data from data/processed/<NAME>-donors.csv.  
        output_dir (str): path to output directory.          

    Returns:
        None.       
    """

    print('\nDF SHAPE:', df.shape)
    print('\nDONORS:', df['ID'].unique().size)
    print('\n', df.tail(15))

    categories_map = {0: 'Neither', 1: 'Passport', 2: 'Gift', 3: 'Both'}

    def set_category_col(a, b):
        c = 0 if a == 0 else 1
        d = 0 if b == 0 else 2 
        return c + d

    #create accumulator df, and aggreg dict to group donors, and aggreg dict to group categories 
    df_groups = pd.DataFrame(index=list(categories_map.values()))
    print('\n', df_groups.tail(15))

    df_groups.sort_index(inplace=True)
    agg_donors = {'Total_Payments':'sum', 'Status':'max', 'Passport':'max', 'Gift':'max', 'Years': 'nunique'}
    agg_catagories = {'Total_Payments':'sum', 'Status':'mean', 'Passport':'mean', 'Gift':'mean', 'Years': 'sum'}

    #for each year, create totals from that year to last year in data 
    years = df['Years'].sort_values().unique()
    first_iteration = True
    for year in years[:-1]: #don't loop last year
        #filter years and aggregate donors accross those years 
        df_temp = df[df['Years'] >= year]
        donors = df_temp.groupby('ID').agg(agg_donors)             
        
        #categorize donors
        donors['Category'] = donors.apply(lambda x: set_category_col(x['Passport'], x['Gift']), axis=1)
        donors['Category'] = donors['Category'].map(categories_map)
        donors.to_csv(os.path.join(output_dir, 'assignments_' +  str(int(year)) + '.csv'))

        #if first iteration, save generically named duplicate file
        if first_iteration:
            donors.to_csv(os.path.join(output_dir, 'assignments.csv'))
            first_iteration = False  
        
        #get donor category averages
        #annual payments = sum of donor payments per category / sum of donor years paying
        group = donors.groupby('Category').agg(agg_catagories)  
        group['Annual_Payments'] = group['Total_Payments'] / group['Years']
        group['Frequencies'] = donors.groupby('Category').size()
        
        print('\n\nGROUP FOR', year, '-', len(donors), 'DONORS\n')
        print(group, '\n')        
        
        #add to accumulator df_groups
        group.sort_index(inplace=True)
        year = str(int(year))
        df_groups['Total_Pledges_since_' + year] = group['Total_Payments']
        df_groups['Ann_Pledges_since_' + year] = group['Annual_Payments']
        df_groups['Status_from_' + year] = group['Status']  
        df_groups['Freq_since_' + year] = group['Frequencies']          

    print('\n\nGROUP TOTALS', '-', df['ID'].unique().size, 'DONORS\n')
    print(df_groups, '\n')

    df_groups.to_csv(os.path.join(output_dir, 'groups.csv'))

def main():    
    df = get_data()
    output_dir = get_output_dir('new_donors')
    segment(df, output_dir)

if __name__ == '__main__':
    sys.exit(main())
