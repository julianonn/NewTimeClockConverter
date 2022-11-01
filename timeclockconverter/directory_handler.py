import os
from pathlib import Path
from .file_factory import FileFactory


class DirectoryHandler:
    """
    Called in Dialog.convert().
    Creates input ('unconverted') and output ('converted') directories.
    Moves all input files to input directory.
    Instantiates a FileFactory object for every unconverted file.
    """
    def __init__(self, p):
        """
        :param p: pathlib.Path object with path of selected input directory
        """
        self.homepath = Path(p)
        self.inpath = self.homepath / 'unconverted'
        self.outpath = self.homepath / 'converted'

        # move all files in chosen directory to new 'input' directory
        self.create_input_directory()
        self.move_input_files()

        self.create_output_directory()
        self.make_outfiles()

    def create_input_directory(self):
        """ Creates new 'unconverted' directory in homepath for inputs."""
        os.mkdir(self.inpath)

    def move_input_files(self):
        """Moves each input csv file to 'unconverted' directory"""
        if os.path.exists(self.inpath):
            for csv_file in self.homepath.glob('*.csv*'):  # grabs all files
                csv_file.rename(self.inpath.joinpath(csv_file.name))  # moves to input folder.

    def create_output_directory(self):
        """ Creates new 'converted' directory in homepath for outputs."""
        os.mkdir(self.outpath)

    def make_outfiles(self):
        """
        Called after creating input/unconverted and output/converted directories.
        For every unconverted CSV file in input, create a corresponding converted
        file in output directory by instantiating a FileFactory object.
        """
        if os.path.exists(self.outpath):
            for csvfile in self.inpath.glob('*.csv*'):  # grabs all input files in input
                f = FileFactory(Path(csvfile), self.outpath)  # creates converted file in output folder
