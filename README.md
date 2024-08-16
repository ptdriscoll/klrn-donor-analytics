# KLRN Donor Analytics Suite

A comprehensive suite of Python tools to analyze KLRN TV donors. Features include:

- **Cluster Analysis:** Identifies and groups donors based on shared characteristics and behaviors

- **Segment Creation:** Develops segments for detailed comparisons and insights based on donor behaviors

- **Data Augmentation:** Enhances analyses with additional layers of demographics and PBS Passport viewing data

This suite provides a framework to understand KLRN donors through comprehensive analysis and data integration.

### Data Setup

Cluster and segment analyses use data downloaded into an .xlsx file from an Allegiance Fundraising database. The Excel file is placed in the `data/raw/` directory.

The database query is constructed with Allegiance's [Analysis Reports](https://alleg.tv/userguides172/FR-AnalysisReports/AnalysisReports.html), using the Pledge type. This is the [specific query](images/2022-09-26-donors.jpg).

Using a list of donor ids from the Allegiance download, demographics are pulled into a separate .xlsx file from WealthEngine. This Excel file needs to have `AcctID`, `Gender`, `Age`, and `Income` columns. The file is placed in the `data/raw/` directory.

PBS Passport video views are layered over data using [KLRN's Passport Analytics Database](https://github.com/ptdriscoll/klrn-passport-analytics-database), which is a desktop application.

Tests can be set up by running a small dataset from an Allegiance download that covers all variables, and in turn using the ids from that data pull to get demographics and Passport views, and then inspecting results to make sure they are what was expected. NOTE: code for cluster tests always produce four clusters.

Verified spreadsheets for expected outcomes are placed in `tests/data_expected/` and `tests/output_expected/`, in parallel with spreadsheets saved by code to `data/` and `output/` (NOTE: code for cluster tests expect four clusters):

- `tests/data_expected/processed/`
- `tests/output_expected/cluster/`
- `tests/output_expected/new_donors/`
- `tests/output_expected/passport_gifts/`
- `tests/output_expected/passport_only/`

### Config Setup

Configuration is set up under `src/config.py`:

- All date formats are `'2022-09-30'`
- `DATA_DONORS` = `<name of raw xlsx file from Allegiance database download>`
- `DATA_DEMOGRAPHICS` = `<name of xlsx file with demographics from WealthEngine download>`
- `DATA_START` = `<start of date range to filter data>`
- `DATA_END` = `<end of date range to filter data, which is inclusive>`
- `YEAR_CUTOFF` = `<pandas shorthand code representing a time interval>` - i.e., the fiscal year is `Y-SEP` - [reference](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html)
- `PASSPORT_APP` = `<path to directory where Passport database app is located on computer system>`
- `PASSPORT_VIEWS_START_DATE` = `<start of date range to filter Passport views>`
- `PASSPORT_VIEWS_END_DATE` = `<end of date range to filter Passport views, which is inclusive>`

Dates for tests are set up at the end of `src/__init__.py`, under the comment `CUSTOM DATES FOR TESTS`:

- All date formats are `'2022-09-30'`
- `DATA_START` = `<start of date range to filter data>`
- `DATA_END` = `<end of date range to filter data, which is inclusive>`
- `YEAR_CUTOFF` = `<pandas shorthand code representing a time interval>` - i.e., the fiscal year is `Y-SEP` - [reference]
- `PASSPORT_VIEWS_START` = `<start of date range to filter Passport views>`
- `PASSPORT_VIEWS_END` = `<end of date range to filter Passport views, which is inclusive>`

### Code Setup

This application uses a Conda enviornment to manage dependencies. If you don't have Conda installed, you get it at [Anaconda](https://www.anaconda.com/download/) or [Miniconda](https://docs.anaconda.com/miniconda/).

The environment is defined in `environment.yml`. By default `name` is set to `klrn-donor-analysis`, but that can be changed.

In an Anaconda Prompt, from the application's root directory, there are two options to set up the environment:

- Option 1, system-wide environment:

  - **Create Environment:** `conda env create -f environment.yml`
  - **Activate Environment:** `conda activate <name>`
  - **Update Environment:** `conda env update -f environment.yml`

- Option 2, working-directory environment:

  - **Create Environment:** `conda env create -p venv -f environment.yml`
  - **Activate Environment:** `conda activate ./venv`
  - **Update Environment:** `conda env update -p ./venv -f environment.yml`

### Running Commands

Processes data, and outputs to `data/processed/`:

- `python -m src.process.donors`
- `python -m src.process.new_donors`
- `python -m src.process.demographics`

Runs cluster analysis (if needed, also runs `src.process.donors`), and outputs to `output/cluster/`:

- `python -m src.cluster.elbow_plot <number>`
  - Evaluates optimal number of clusters by generating an elbow plot that visualizes where adding more clusters no longer significantly reduces tightness within clusters. The `<number>` parameter is optional and defaults to `9`, plotting a range from 1 to 9 clusters.
- `python -m src.cluster.pca_plots <number> <number>`
  - Evaluates optimal number of clusters by creating PCA model scatterplots that show a range of clusters. The `<number> <number>` parameters are optional and default to `3 5`, generating plots for three, four, and five clusters.
- `python -m src.cluster.kmeans <number>`
  - Runs cluster analysis, generates a PCA model plot, frequencies plot and a spreadsheet (`assignments.csv`) assigning cluster groups to donors. The `<number>` parameter is optional and defaults to `4`, creating four cluster groups.

Creates donor segments (if needed, also runs either `src.process.donors` or `src.process.new_donors`), and outputs `assignments.csv` to respective folder in `output/`

- `python -m src.segment.new_donors`
- `python -m src.segment.passport_gifts`
- `python -m src.segment.passport_only`

After cluster or segment commands have run, demographics can be added:

python -m src.augment.demographics cluster
python -m src.augment.demographics new_donors
python -m src.augment.demographics passport_gifts
python -m src.augment.demographics passport_only

python -m src.augment.passport cluster
python -m src.augment.passport new_donors
python -m src.augment.passport passport_gifts
python -m src.augment.passport passport_only

### References

- [Allegiance Fundraising: Analysis Reports User Guide](https://alleg.tv/userguides172/FR-AnalysisReports/AnalysisReports.html)
- [KLRN Passport Analytics Database](https://github.com/ptdriscoll/klrn-passport-analytics-database)
- [pandas Time series / date functionality](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html)
- [Anaconda](https://www.anaconda.com/download/)
- [Miniconda](https://docs.anaconda.com/miniconda/)
