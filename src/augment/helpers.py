import argparse

def parse_args():
    """
    Parses command-line argument to add as file_data argument to merge function. Options include:
        -cluster
        -new_donors
        -passport_gifts
        -passport_only

    Examples:
        $ python -m augment.demographics cluster 
        $ python -m augment.demographics new_donors 
        $ python -m augment.demographics passport_gifts 
        $ python -m augment.demographics passport_only

    Returns:
        str: filename specified by the user.
    """
    parser = argparse.ArgumentParser(description='Run augment module')
    parser.add_argument(
        'filename',
        type=str,
        help=('''Specify name of file to merge data overlay into, e.g. 
              cluster, new_donors, passport_gifts or passport_only'''
        ) 
    )
    arg, unknown = parser.parse_known_args()
    return arg.filename
