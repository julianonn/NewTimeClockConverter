import os
import tkinter as tk
from tkinter import messagebox as msg
from tkinter import filedialog as fd
from .reader import Reader
from .writer import Writer
from .watchdog import Watchdog
from .sys_open import display_dir
import traceback


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
        self.data = None

        self.errors = []

        self.title('New TimeClockConverter :)')
        self.geometry('800x600')

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
        
        self.btn_reset = tk.Button()
        self.btn_scan = tk.Button()
        self.btn_convert = tk.Button()

        self.lbl_selected = tk.Label(text='Selected: ', justify='left', fg='red')
        self.lbl_selected.pack(padx=2, pady=2)

        self.lbl_watchdog = tk.Label(text="", justify='left')
        self.lbl_watchdog.pack(padx=2, pady=2)

        self.lbl_read_status = tk.Label(text="", justify='left')
        self.lbl_read_status.pack(padx=2, pady=2)

        self.lbl_convert_status = tk.Label(text="", justify='left')
        #self.lbl_convert_status.pack(padx=2, pady=2)


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
            self.add_reset_button()
            self.add_scan_button()

    def confirm_selected(self):
        self.lbl_selected['text'] += self.path
        self.lbl_selected['fg'] = 'green'

    def add_reset_button(self):
        if self.path is not None:
            self.btn_reset = tk.Button(text='Reset', command=self.reset)
            self.btn_reset.pack(padx=2, pady=5)

    def add_scan_button(self):
        if self.path is not None:
            self.btn_scan = tk.Button(text='Scan for errors', command=self.scan)
            self.btn_scan.pack(padx=2, pady=5)

    def add_convert_button(self):
        """
        Makes convert button visible
        """
        if self.path is not None:
            self.btn_convert = tk.Button(text='Convert', command=self.convert)
            self.btn_convert.pack(padx=2, pady=5)

    def reset(self):
        print("resetting")
        self.path = None
        self.data = None
        self.errors = []

        self.btn_choose.pack(padx=2, pady=5)
        self.btn_scan.pack_forget()
        self.btn_reset.pack_forget()
        self.btn_convert.pack_forget()

        self.lbl_selected['text'] = 'Selected: '
        self.lbl_selected['fg'] = 'red'
        self.lbl_read_status['text'] = ''
        self.lbl_watchdog['text'] = ''
        self.lbl_convert_status['text'] = ''
        self.lbl_convert_status.pack_forget()


    def scan(self):
        print('scanning')
        if self.path is not None:
            r = Reader(self.path)
            try:
                r.read()
                self.data = r.data  # store dictionary of dataframes

                tock = Watchdog()  # all my phantom tollbooth fans :,]
                tock.sniff(self.data)

                # if okay, make the convert button visible
                self.update_read_status_lbl("Success! Ready to convert.", color='green')
                self.update_watchdog_lbl(tock)
                self.btn_scan.pack_forget()
                self.add_convert_button()

            except Exception as e:
                traceback.print_exc()
                print(e)
                self.update_read_status_lbl(
                    f"FATAL FILE ERROR.\n{str(e)}\n", 
                    color='red')
                #self.reset()
        return
            

    def convert(self):
        print('converting')
        self.lbl_convert_status.pack(padx=2, pady=2)
        try:
            w = Writer(self.path)
            w.convert(self.data)
            
            self.update_convert_status_lbl("Success! Files converted.", color='green')
            display_dir(self.path)
        
        except Exception as e:
            traceback.print_exc()
            print(e)
            self.update_convert_status_lbl(f"FATAL FILE ERROR.\n{e}", color='red')
        return


    def update_watchdog_lbl(self, tock):
        s_w = "\n".join(tock.msg)
        self.lbl_watchdog['text'] = "**WARNINGS**\n" + s_w


    def update_read_status_lbl(self, msg: str, color='green'):
        #self.errors.append("FATAL ERROR. Docs remain UNCONVERTED and likely INCORRECT: {}\n".format(error))
        self.lbl_read_status['text'] = msg #"\n".join(self.errors)
        self.lbl_read_status['fg'] = color


    def update_convert_status_lbl(self, msg: str, color='green'):
        #self.errors.append("FATAL ERROR DURING CONVERT. Docs remain UNCONVERTED and likely INCORRECT: {}\n".format(error))
        self.lbl_convert_status['text'] = msg
        self.lbl_convert_status['fg'] = color