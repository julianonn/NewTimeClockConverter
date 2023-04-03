import os
import numpy as np
import arrow
from pathlib import Path


class Writer:
    def __init__(self, p):
        self.data = {}
        self.path = Path(p)
        if not self.path.is_dir():
            raise Exception("writer.py, home directory does not exist")
        self.in_dir = None
        self.out_dir = None

    def convert(self, data):
        self.data = data
        self.handle_directories()
        self.write_files()

    def handle_directories(self):
        #  Creates new 'unconverted' directory in original path for input CSVs (unchanged)
        #  and 'converted' directory for reformatted files
        self.in_dir = self.path / 'unconverted'
        self.out_dir = self.path / 'converted'
        os.mkdir(self.in_dir)
        os.mkdir(self.out_dir)

        # Moves each input csv files to 'unconverted' directory
        if os.path.exists(self.in_dir):
            for csv in self.path.glob('*.csv*'):  # grabs all files
                csv.rename(self.in_dir.joinpath(csv.name))  # moves to input folder.

    def write_files(self):
        for key in self.data.keys():
            # call static method reformat
            df = reformat(self.data[key])
            # write out to CSV file in 'converted' directory
            fname = str(key) + '_' + arrow.now().format('YYYY-MM-DD') # ends up DEPT_YYYY-MM-DD
            out_file = (self.out_dir / fname).with_suffix('.csv')
            df.to_csv(out_file, header=False, index=True)


# STATIC METHODS
def reformat(old_df):
    df = old_df.copy(deep=True)[['id', 'hours', 'rate', 'dept']]

    # aggregate rows by employee ID
    agg_funcs = {'hours': 'sum', 'rate': 'first', 'dept': 'first'}
    df = df.groupby(df['id']).aggregate(agg_funcs)

    # reorder and add columns to mimic w/ Paylocity format
    df['E'] = 'E'
    df['REG'] = 'REG'
    df['nan1'] = np.nan
    df['nan2'] = np.nan
    order = ['E', 'REG', 'hours', 'nan1', 'rate', 'nan2', 'dept']
    df = df.reindex(columns=order)

    return df


