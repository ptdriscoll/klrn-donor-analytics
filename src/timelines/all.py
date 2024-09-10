import os
import sys

from .helpers import parse_args, get_data, create_timeline
from src.helpers import get_output_dir

def main():
    arg = parse_args()
    df = get_data() 
    output_dir = get_output_dir('timelines') 
    output_file = os.path.join(output_dir, f'all_{arg}.csv')  
    create_timeline(df, output_file, arg)

if __name__ == '__main__':
    sys.exit(main())
