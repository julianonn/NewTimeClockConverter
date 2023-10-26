# NewTimeClockConverter

Converts payroll documents from the format required by the Students of Georgetown, Inc's internal employee management site to the format required by Paylocity. Reads, writes, analyzes payroll info, and 'sniffs' for weird or buggy hours.

### _In development!!_

These are just the scripts. Tkinter and Flask app versions are sitting on my computer somewhere... someday I'll commit them... maybe...

## License?
[MIT](https://choosealicense.com/licenses/mit/)

Cool.

Disclaimer: While created to assist the POps Ops role at Students of Georgetown, Inc (the Corp), this project was completed off the clock, published with full permission from the non-profit. I'm not going around sprinkling proprietary code all over the internet lol.

## Installation and Build

1. Clone repository locally

2. [Install Python 3](https://www.python.org/downloads/)

3. If not already installed, install pip

Linux & MacOS: ```python3 -m ensurepip --upgrade```

Windows ```py -m ensurepip --upgrade```

4. Install PyInstaller

```pip install pyinstaller```

5. cd into the local repository and install dependencies

```python3 setup.py install```


### Executable instructions
After doing all the above, use PyInstaller to create a single executable. 

```pyinstaller run.py --onefile -n NewTimeClockConverter ```

