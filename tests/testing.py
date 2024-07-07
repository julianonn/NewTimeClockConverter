import sys, os
import traceback
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print('\n', sys.path, '\n')
print('\n', os.getcwd(), '\n')



from timeclockconverter.reader import Reader
from timeclockconverter.writer import Writer
from timeclockconverter.watchdog import Watchdog
from pathlib import Path


def test_run(path: Path):
    r = Reader(path)
    try:
        r.read()
        data = r.data  # store dictionary of dataframes
        tock = Watchdog()
        tock.sniff(data)
        w = Writer(path)
        #w.convert(data)

    except Exception as e:
        traceback.print_exc()
        print(e)



if __name__ == '__main__':
    print("\n\n--------------- NO FILE --------------------")
    test_run(Path('tests/no-file'))

    print("\n\n--------------- OK FORMAT --------------------")
    test_run(Path('tests/OK-format'))

    print("\n\n--------------- DEPARTMENT READ FAIL --------------------")
    test_run(Path('tests/bad-read-dept'))

    print("\n\n--------------- EMPID READ FAIL --------------------")
    test_run(Path('tests/bad-read-empID'))

    print("\n\n--------------- HOURS READ FAIL --------------------")
    test_run(Path('tests/bad-read-hours'))
