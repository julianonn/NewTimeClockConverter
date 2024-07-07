# NewTimeClockConverter

Converts payroll documents from the format required by the Students of Georgetown, Inc's internal employee management site to the format required by Paylocity. Reads, writes, analyzes payroll info, and 'sniffs' for weird or buggy hours.

### _In development!!_

These are just the scripts. Tkinter and Flask app versions are sitting on my computer somewhere... someday I'll commit them... maybe...

## License
[MIT](https://choosealicense.com/licenses/mit/)

Disclaimer: While created to assist the POps Ops role at Students of Georgetown, Inc (the Corp), this project was published with full permission from the organization. I'm not going around sprinkling proprietary code all over the internet lol.




## Installation for non-programmers

Look to your right and find the 'Releases' widget (between 'About' and 'Packages'). Select MacOS-v1.1, then click and download your first option: NewTimeClockConverter_v1.1. The version (v1.1) might be different. Just choose the latest. You don't need either of the 'Source Code' zip files unless you particularly desire them. 



## Installation & build FOR DEVELOPERS

1. Clone repository locally
2. [Install Python 3](https://www.python.org/downloads/)

MAC USERS: 

3. If not already installed, install pip: `python3 -m ensurepip --upgrade`

4. Create a virtual environment: `python3 -m venv .venv`

5. Install dependencies: `pip install -r requirements.txt`

6. Run the main program: `python3 run.py` and wait for the GUI to pop up.

7. To build into an executable, run `pyinstaller --onefile --windowed -n NewTimeClockConverter run.py`, and look in the `dist` folder for `NewTimeClockConverter.app`

WINDOWS USERS: 

Replace `python3` with `py` or `python` (whichever works on your system). Look for or `NewTimeClockConverter.exe` instead of `...app`.


