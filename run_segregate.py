from segregate import run
import datetime
import sys

def __main__():

    file_location = sys.argv[1]

    if not file_location:
        print("First argument to script should be path to LocationHistory.json file")

    max_date_string = sys.argv[2] if len(sys.argv) > 2 else None
    max_date = None
    if max_date_string:
        max_date = datetime.datetime.strptime(max_date_string, "%Y-%m-%d")
    if not max_date:
        print("Second argument to script should be max date.  Format: YYYY-MM-DD")
        return

    run(file_location, max_date)
__main__()
