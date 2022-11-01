import os
import platform
import subprocess


def display_dir(path):
    """
    Displays directory in system's default file manager
    (e.g. Finder on Mac, Explorer on Windows)
    :param: path: directory path
    """
    if os.path.exists(path) and os.path.isdir(path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
    else:
        raise Exception("systemopen: path does not exist")
