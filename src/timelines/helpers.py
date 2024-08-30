import argparse
from src.process.helpers import clean
from src import DATA_DONORS_RAW, DATA_DONORS_WORKING

def parse_args():
    """
    Parses command-line argument that will be translated into an offset alias to be added
    to a pandas dt.to_period() method to set time period frequencies. Options include:
        -annual
        -weekly

    Examples:
        $ python -m src.timeline.passport_gifts annual
        $ python -m src.timeline.passport_gifts weekly

    Returns:
        str: time period specified by the user.
    """
    parser = argparse.ArgumentParser(description='Run timelines module')
    parser.add_argument(
        'frequency',
        type=str,
        help=('Specify time period frequency to plot timeline, e.g. annual or weekly') 
    )
    arg, unknown = parser.parse_known_args()
    return arg.frequency

def get_data():
    """
    Gets dataframe from donors working data in data/processed/, creating 
    donors working data from donors raw data in data/raw/ if needed.

    Returns:
        pandas.DataFrame.
    """
    cols_new = ['ID', 'Status', 'Sustainer', 'Major', 'Passport', 'Date', 'Type', 'Gift', 'Page']
    cols_keep = ['Count', 'Paid to Date', 'Balance']
    df = clean(DATA_DONORS_RAW, DATA_DONORS_WORKING, cols_new, cols_keep)
    return df
