import os
import tkinter as tk
from tkinter import messagebox as msg
from tkinter import filedialog as fd

from .sys_open import display_dir
from .directory_handler import DirectoryHandler


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
        self.dh = None

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

        self.label1 = tk.Label(text=reqs, justify='left')
        self.label1.pack(padx=2, pady=2)

        self.button1 = tk.Button(text='Choose Folder', command=self.select_directory)
        self.button1.pack(padx=2, pady=5)
        self.button2 = tk.Button()

        self.label2 = tk.Label(text='Selected: ', justify='left', fg='red')
        self.label2.pack(padx=2, pady=2)

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
            self.add_convert_button()

    def add_convert_button(self):
        """
        Makes convert button visible
        """
        if self.path is not None:
            self.label2['text'] += self.path
            self.label2['fg'] = 'green'
            self.button2 = tk.Button(text='Convert', command=self.convert)
            self.button2.pack(padx=2, pady=5)

    def convert(self):
        """
        Creates DirectoryHandler object with path, initiating file conversion.
        Displays chosen directory after conversion.
        Displays error as message box if applicable.
        """
        try:
            if self.path is not None:
                self.dh = DirectoryHandler(self.path)
                display_dir(self.path)
                self.path = None
        except Exception as e:
            msg.showerror("ERROR:" + e)





