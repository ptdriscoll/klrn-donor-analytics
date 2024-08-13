import os
from src import ROOT_DIR, DATA_DONORS_PROCESSED
from src.process.donors import process_data
import pandas as pd

def get_data(data_file_processed=DATA_DONORS_PROCESSED):
    """
    Gets data from data/processed/donors.csv, running process_data() first if it 
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

def get_output_dir(dir, root_dir=ROOT_DIR):
    """
    Gets output/{dir}/ path, creates directory if it doesn't already exist, or
    removes files (but not nested directories and their files) if it does exist. 
    The output directory path points to either the root or tests directory, 
    depending on whether a test is running. 

    Args:
        dir (string): name of output directory. 
        root_dir (str): path to application root directory.  

    Returns:
        str: path to output directory.
    """
     
    if not os.getenv('TESTS', False):
        path = os.path.join(root_dir, 'output', dir) 
    else:
        path = os.path.join(root_dir, 'tests', 'output', dir)  

    #create the directory if it doesn't exist
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)

    #remove files in directory, but not any nested directores and their files    
    else:
        try:
            print(f'\nDeleting files from {path}') 
            files = os.listdir(path)
            for file in files:
                file_path = os.path.join(path, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        except OSError:
            print(f'An error occurred while deleting files from {path}')            

    return path 
 