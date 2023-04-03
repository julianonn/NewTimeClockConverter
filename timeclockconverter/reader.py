from pathlib import Path
import pandas as pd


class Reader:
    """
    Reads each CSV in directory into a pandas dataframe, deleting moot
    columns and headers.

    Stores each file's corresponding dataframe in the dictionary 'data', where the
    key is the file's department number.

    If there are repeat departments, each is assigned a unique key
    (i.e. 9, 9a, 9b, 9c, 9d ...)

    'path' stores path of directory holding CSVs.
    """
    def __init__(self, p):
        self.data = {}
        self.path = Path(p)

        if not self.path.is_dir():
            raise Exception("reader.py, input directory does not exist")

    # CALLED BY DIALOG.PY
    def read(self):

        for csv in self.path.glob('*.csv*'):  # grabs all input files in input directory
            try:
                df = into_df(csv)
                key = self.make_dept_key(df)
                self.data.update({key: df})
            except Exception as e:
                raise Exception("READ ERROR: ", str(e))

    # METHODS CALLED FOR EVERY FILE

    def make_dept_key(self, df):
        dept = get_dept(df)
        key = str(dept)
        char = ord('a')
        while key in self.data.keys():
            if char > ord('z'):
                raise Exception("too many duplicate department files. please aggregate.")
            key = str(dept) + str(chr(char))
            char += 1
        return key


# STATIC METHODS
def into_df(csv):
    if csv.suffix != '.csv':
        raise Exception("read.py, not CSV")
    df = pd.read_csv(csv,
                     engine='python',
                     names=['id', 'dept-name', 'name', 'dept', 'rate', 'hours'],
                     usecols=[2, 3, 4, 5, 6, 7],
                     skiprows=3,
                     skipfooter=14)
    return df


def get_dept(df):
    try:
        return df["dept"].iloc[0]
    except Exception as e:
        raise Exception('empty unconverted file detected')
