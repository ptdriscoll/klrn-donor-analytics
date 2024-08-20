# name of raw xlsx file for cluster profiles or segment analyses
DATA_DONORS = 'donors-5-years-2024-07-31.xlsx'

# name of xlsx file with demographics, to merge with analysis files 
DATA_DEMOGRAPHICS = '2022-09-26-demographics.xlsx'

# the date range to filter data - both are inclusive
DATA_START = '2019-08-01' 
DATA_END = '2024-07-31'

# what month to set annual timeframe cutoff, which is inclusive 
# references:
#   -https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html
#   -https://stackoverflow.com/questions/22205159/format-pandas-datatime-object-to-show-fiscal-years-from-feb-to-feb-and-be-format
YEAR_CUTOFF = 'Y-JUL' 

# path to Passport database application
PASSPORT_APP = 'T:\\Public Relations\\ONLINE\\Passport\\STATS'

# the date range to filter Passport views - both are inclusive
PASSPORT_VIEWS_START_DATE = '2019-08-01' 
PASSPORT_VIEWS_END_DATE = '2024-07-31'
