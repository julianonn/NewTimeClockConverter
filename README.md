# NewTimeClockConverter (1.0.0)

Converts payroll documents from the format required by the Students of Georgetown, Inc's internal employee management site to the format required by Paylocity. Reads, writes, analyzes payroll info, and 'sniffs' for weird or buggy hours.

### _In development!!_

## Installation and Build

1. Clone repository locally

2. [Install Python 3](https://www.python.org/downloads/)

3. If not already installed, install pip

Linux & MacOS: ```python -m ensurepip --upgrade``` or (```python3 -m ensurepip --upgrade```)

Windows ```py -m ensurepip --upgrade```

4. Install PyInstaller

```pip install pyinstaller```

5. cd into the local repository and install dependencies

```python3 setup.py install```


### Executable instructions
After doing all the above, use PyInstaller to create a single executable. 

```pyinstaller run.py --onefile -n NewTimeClockConverter ```



## License
[MIT](https://choosealicense.com/licenses/mit/)

Disclaimer: While created to assist the POps Ops role Students of Georgetown, Inc, this was a personal project completed off the clock, published with approval from the corporation.

