from urllib.parse import urlparse, urlunparse
import pandas as pd

def compare_dfs(f1, f2):
    """
    Compares either two Excel or two CSV spreadsheets by converting them to Pandas.DataFrames, 
    and using DataFrame.compare on the first to check for any differences with the second.
    
    Args:
        f1 (str): path to first spreadsheet.
        f2 (str): path to second spreadsheet.

    Returns
        pandas.DataFrame: Highlighting the differences between f1 and f2. If the file formats 
                          do not match (.csv or .xlsx), or are neither of these formats, the function
                          prints an error message and returns None.     
    """

    if f1.endswith('.csv') and f2.endswith('.csv'):
        df1 = pd.read_csv(f1)
        df2 = pd.read_csv(f2)
        
    elif f1.endswith('.xlsx') and f2.endswith('.xlsx'):
        df1 = pd.read_excel(f1)
        df2 = pd.read_excel(f2)        
        
    else:
        print('\nFILES DO NOT MATCH, OR ARE NOT .CSV or .XLSX')
        return        
    
    #print('\n' + '='*100, '\nFILE:', f1, '\n\nSHAPE DF1:', df1.shape, '\n\n', df1.head())
    #print('\n' + '='*100, '\nFILE:', f2, '\n\nSHAPE DF2:', df2.shape, '\n\n', df2.head(), '\n')

    df1 = df1.round(8)
    df2 = df2.round(8)  
    
    compare = df1.compare(df2, align_axis=0, keep_equal=False)
    return compare

def compare_spreadsheets(path_1, path_2):
    """
    Prints out results from compare_dfs(f1, f2).
    
    Args:
        path_1 (str): path to first spreadsheet.
        path_2 (str): path to second spreadsheet.    
    
    Returns:
        None.
    """
    compare = compare_dfs(path_1, path_2)
    print('\n' + '='*50)
    print('DIFFERENCES BETWEEN:')
    print(f'  - {path_1}')
    print(f'  - {path_2}', '\n')  
    print(compare) 

    if compare.columns.empty and compare.index.empty:
        print('\nTEST PASSED')
    else:
        print('\nTEST FAILED')          
