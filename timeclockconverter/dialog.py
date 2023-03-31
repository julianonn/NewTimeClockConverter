import os
import tkinter as tk
from tkinter import messagebox as msg
from tkinter import filedialog as fd
from .reader import Reader
from .writer import Writer
from .watchdog import Watchdog
from .sys_open import display_dir



class Dialog(tk.Tk):
    """
    Derived from tkinter.TK.
    Creates dialog, prompts user to choose directory.
    Calls DirectoryHandler with chosen path.
    Displays messagebox with errors.
    """

    def __init__(self):
        """
        Initializes dialog
        Creates Button to call select_directory()
        """
        super().__init__()

        self.path = None
        self.dir_handler = None

        self.title('New TimeClockConverter :)')
        self.geometry('600x400')

        reqs = '''
        REQUIREMENTS:
        1.  Folder must contain ONLY unconverted timesheet files
        2.  All timesheet files must be in csv format
        3.  All files must have proper headers and footers
                a.  header = 3 lines
                b.  footer = 14 lines
                c.  reference Ops or GM manual for proper formatting
        '''

        self.hi_ops = tk.Label(text="hi ops <3", fg='magenta', font=12)
        self.hi_ops.pack(padx=2, pady=10)

        self.lbl_reqs = tk.Label(text=reqs, justify='left')
        self.lbl_reqs.pack(padx=2, pady=2)

        self.btn_choose = tk.Button(text='Choose Folder', command=self.select_directory)
        self.btn_choose.pack(padx=2, pady=5)
        self.btn_convert = tk.Button()

        self.lbl_selected = tk.Label(text='Selected: ', justify='left', fg='red')
        self.lbl_selected.pack(padx=2, pady=2)

    def select_directory(self):
        """
        Prompts user to choose directory with Tkinter GUI.
        Assigns choice to instance attribute path.
        If choice is valid, makes CONVERT button visible
        """
        self.path = fd.askdirectory(
            title='Select folder of unconverted documents',
            initialdir=os.getcwd()
        )
        if self.path is not None:
            self.confirm_selected()
            self.add_convert_button()

    def confirm_selected(self):
        self.lbl_selected['text'] += self.path
        self.lbl_selected['fg'] = 'green'

    def add_convert_button(self):
        """
        Makes convert button visible
        """
        if self.path is not None:
            self.btn_convert = tk.Button(text='Scan & Convert', command=self.run)
            self.btn_convert.pack(padx=2, pady=5)

    def run(self):
        """
        Creates DirectoryHandler object with path, initiating file conversion.
        Displays chosen directory after conversion.
        Displays error as message box if applicable.
        """
        try:
            if self.path is not None:
                #self.dir_handler = DirectoryHandler(self.path)
                #display_dir(self.path)
                #self.path = None

                r = Reader(self.path)
                r.read()
                data = r.data  # store dictionary of dataframes
                w = Writer(self.path)
                w.convert(data)

                tock = Watchdog()  # all my phantom tollbooth fans :,]
                tock.sniff(data)




        except Exception as e:
            msg.showerror("ERROR:" + str(e))
