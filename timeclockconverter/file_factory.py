from .reformatter import get_department, make


class FileFactory:
    """
    Called by DirectoryHandler.
    Calls reformatter.make() to create df, the converted pandas.DataFrame
    Reads df to a CSV file in target directory

    :param: filepath: path of unconverted input file
    :param: targetdir: directory where converted output file should go
    """
    def __init__(self, filepath, targetdir):
        self.df = make(filepath)
        outfile_name = str(get_department(self.df))
        outpath = (targetdir / outfile_name).with_suffix('.csv')
        self.df.to_csv(outpath, header=False, index=True)

