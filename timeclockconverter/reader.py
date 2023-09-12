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
            raise RuntimeError("Input folder does not exist")

    # CALLED BY DIALOG.PY
    def read(self):
        for csv in self.path.glob('*.csv*'):  # grabs all input files in input directory
            df = into_df(csv)

            validate(df, csv)

            try:
                key = self.make_dept_key(df)
            except RuntimeError as e:
                raise RuntimeError(e)
            except Exception as e:
                raise RuntimeError("File {} could not be read. Please check formatting.".format(csv.name))
            
            self.data.update({key: df})
           
    # METHODS CALLED FOR EVERY FILE

    def make_dept_key(self, df):
        dept = get_dept(df)
        key = str(dept)
        char = ord('a')
        while key in self.data.keys():
            if char > ord('z'):
                raise RuntimeError("Too many duplicate department files. Please aggregate (department {}).".format(dept))
            key = str(dept) + str(chr(char))
            char += 1
        return key


# STATIC METHODS
def into_df(csv):
    if csv.suffix != '.csv':
        raise Exception("One of the input files ({}) is not a CSV".format(csv))
    try:
        df = pd.read_csv(csv,
                        engine='python',
                        names=['id', 'dept-name', 'name', 'dept', 'rate', 'hours'],
                        usecols=[2, 3, 4, 5, 6, 7],
                        skiprows=3,
                        skipfooter=14)
    except Exception as e:
        raise RuntimeError("File {} could not be read. Please check formatting.".format(csv.name))
    
    return df


def get_dept(df):
    try:
        return df["dept"].iloc[0]
    except Exception as e:
        raise RuntimeError('Empty unconverted file detected')
    

def validate(df, csv):
    failed_id = all(isinstance(x, (int, float)) for x in list(df['id']))
    failed_dept = all(isinstance(x, (int, float)) for x in list(df['dept']))
    failed_name = all(isinstance(x, str) for x in list(df['name']))
    failed_dept_name = all(isinstance(x, str) for x in list(df['dept-name']))
    failed_rate = all(isinstance(x, (int, float)) for x in list(df['rate']))
    failed_hours = all(isinstance(x, (int, float)) for x in list(df['hours']))

    failed_cols = []
    if failed_id:
        failed_cols.append('employee id')
    if failed_dept:
        failed_cols.append('department number')
    if failed_name:
        failed_cols.append('employee name')
    if failed_dept_name:
        failed_cols.append('department name')
    if failed_rate:
        failed_cols.append('rate')
    if failed_hours:
        failed_cols.append('hours')
    
    if failed_cols:
        raise RuntimeError("File {} has invalid data in column(s): {}".format(csv, ", ".join(failed_cols)))

    
