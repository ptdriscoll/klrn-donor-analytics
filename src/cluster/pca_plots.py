import sys
from src.helpers import get_data, get_output_dir
from .helpers import parse_args, prep_data
from .kmeans import run_kmeans

def set_range(args, max):
    """
    Sets a range that doesn't go over a max. If args is empty, the default is range(3, 4). The first 
    value in args must be at least 1. The second value is optional and inclusive, and so defaults to 
    1 higher than the start value. If one or more args exceed max, they reset to below the max.

    Args:
        args (List[int]): list of 0 or more integers.   
        max (int): Ensures that the max range is range(max, max + 1).   

    Returns:
        range: a range object.  

    Examples:
        Run 1 plot of 3 clusters:
            $ python -m src.cluster.pca_plots 
            $ python -m src.cluster.pca_plots 3 

        Run 1 plot of 4 clusters:
            $ python -m src.cluster.pca_plots 4         

        Run 3 plots of 3, 4 and 5 clusters:             
            $ python -m src.cluster.pca_plots 3 5  
    """    

    range_start = args[0] if len(args) > 0 else 3
    if range_start < 1:
        range_start = 1
    if range_start > max:
        range_start = max

    range_end = args[1] + 1 if len(args) > 1 else range_start + 1 
    if range_end <= range_start:
        range_end = range_start + 1 
    if range_end > max + 1:
        range_end = max + 1 

    return range(range_start, range_end)
   
def main():
    args = parse_args()
    clusters_range = set_range(args, 7) 

    df = get_data()
    df_std = prep_data(df)
    output_dir = get_output_dir('cluster')
    run_kmeans(df_std, output_dir, clusters_pca_scatterplots=clusters_range)

if __name__ == '__main__':
    sys.exit(main())
