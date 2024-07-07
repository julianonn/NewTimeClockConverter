from pathlib import Path
import pandas as pd


from .errors import FileReadError, CSVFormatError
#from errors import FileReadError, CSVFormatError
#import csv as CSV


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
            raise FileReadError("Input folder does not exist")

    # CALLED BY DIALOG.PY
    def read(self):
        for csv in self.path.glob('*.csv*'):  # grabs all input files in input directory

            df = self.read_single(csv)
            key = self.make_dept_key(df, csv)
            self.data.update({key: df})
           


    def make_dept_key(self, df: pd.DataFrame, csv: Path) -> str:
        dept = self.get_dept(df, csv)
        key = str(dept)
        char = ord('a')
        while key in self.data.keys():
            if char > ord('z'):
                raise FileReadError("Too many duplicate department files. \nPlease aggregate (department {}).".format(dept))
            key = str(dept) + str(chr(char))
            char += 1
        return key
    
    def get_dept(self, df, csv):
        # all values in dept column should be the same
        dept = df["dept"].unique().tolist()
        if len(dept) != 1:
            raise CSVFormatError(f"File {csv.name} has multiple departments. \nExpected only one department per file.")
        if not isinstance(dept[0], int):
            print(dept, type(dept))
            raise CSVFormatError(f"File {csv.name} has invalid department number. \nExpected an integer, got {dept[0]}.")
        return dept[0]



    def read_single(self, csv: Path):

        # Validate header
        with open(csv, 'r') as f:
            lines = f.readlines()

            if len(lines) < 17:
                raise CSVFormatError(f"File {csv.name} has invalid length. \nEnsure file has a proper header (3 lines) and a footer (14 lines).")

            for l in lines[:3]:
                if not l.startswith(("!", "\'!", "\"!")):
                    raise CSVFormatError(f"File {csv.name} has invalid header. \nEnsure first 3 lines consist of the original header and start with '!'")
            
            for i, l in enumerate(lines[3:-14]):
                if not l.startswith(("Y5B", "\'Y5B", "\"Y5B")):
                    raise CSVFormatError(f"File {csv.name} has invalid lines. \nEnsure the 1st column of the {i+1}th line contains 'Y5B' and is not empty.")
            
            for l in lines[-14:]:
                if not l.startswith(("!", "\'!", "\"!")):
                    raise CSVFormatError(f"File {csv.name} has invalid footer. \nEnsure last 14 lines consist of the original footer and start with '!'")


        # map columns to their original names
        old_columns = ['FILE #', 'BATCH DESCRIPTION', 'Name', 'Temporary Department', 'Temporary Rate', 'Reg Hours']
        new_columns = ['id', 'dept-name', 'name', 'dept', 'rate', 'hours']

        # Validate whole CSV
        try:
            df = pd.read_csv(csv,
                            engine='python',
                            names=new_columns,
                            usecols=[2, 3, 4, 5, 6, 7],
                            skiprows=3,
                            skipfooter=14).reset_index(drop=True)
        except Exception as e:
            raise FileReadError(f"File {csv.name} could not be read for some unknown reason. \nI thought I caught all the possible errors. Please check formatting.")
        
        # if df empty, raise error
        if df.empty:
            raise CSVFormatError(f"File {csv.name} is empty (or empty-ish in the desired columns). \nPlease check formatting.")

        # Validate data in columns
        for i, row in df.iterrows():
            
            for j, col in enumerate(new_columns):
                if pd.isna(row[col] and col != 'dept-name'):  # dept-name can be empty
                    raise CSVFormatError(f"File {csv.name} has missing data in row {i + 4} column {old_columns[j]}.")
                
                # ID and DEPARTMENT should both be integers
                if col in ['id', 'dept']: 
                    if isinstance(row[col], int):
                        pass # all is well
                    elif isinstance(row[col], (float, str)):
                        try:
                            new_val = int(row[col])
                            df.at[i, col] = new_val
                        except:
                            raise CSVFormatError(f"File {csv.name} has invalid data in row {i + 4} column {old_columns[j]}. \nExpected an integer number, got '{row[col]}'.")
                    else:
                        raise CSVFormatError(f"File {csv.name} has invalid data in row {i + 4} column {old_columns[j]}. \nExpected an integer number, got '{row[col]}'.")

                # RATE and HOURS should both be floats
                if col in ['rate', 'hours']: 
                    if isinstance(row[col], (int, float)):
                        new_val = float(row[col])
                        df.at[i, col] = new_val   # all is well!
                    elif isinstance(row[col], str):
                        try:
                            new_val = float(row[col])
                            df.at[i, col] = new_val
                        except:
                            raise CSVFormatError(f"File {csv.name} has invalid data in row {i + 4} column {old_columns[j]}. \nExpected a number, got '{row[col]}'.")
                    else:
                        raise CSVFormatError(f"File {csv.name} has invalid data in row {i + 4} column {old_columns[j]}. \nExpected a number, got '{row[col]}'.")
                    
                # NAME and DEPARTMENT NAME can be empty 
        return df

        

    


def test():
    csv = Path("/Users/julianonn/CORP/python/payrollsos/unconverted/01-UC-5.5.csv")
    reader = Reader(csv.parent)
    reader.read()
    #reader.read_single(csv)
    print('done')


test()