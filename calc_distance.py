import csv
import datetime
import json

import ijson


def run():

    start_date = datetime.datetime(2015, month=6, day=30)
    end_date = datetime.datetime(2015, month=12, day=31)
    i_date = None
    csv_file = open('shifts.csv')
    spamreader = csv.reader(csv_file, delimiter=',', quotechar='"')
    for row in spamreader:
        date = row[0]
        start = row[1]
        end = row[2]

        if date == 'date':
            continue

        i_date = datetime.datetime.strptime(date, '%Y-%m-%d')
        i_start = datetime.datetime.strptime(start, "%H:%M %p").time()
        i_end = datetime.datetime.strptime(end, "%H:%M %p").time()

        json_file = open('days/{}.json'.format(date))
        locations = json.load(json_file)
        time = None

        try:

            print("{}: Shift started at {}".format(date, start))

            for location in locations:
                time = datetime.datetime.fromtimestamp(int(location['timestampMs'])/1000).time()
                if not time:
                    continue
                if time < i_start:
                    continue
                if time > i_end:
                    print("{}: Shift ended at {}".format(date, end))
                    raise StopIteration()

                lat = location['lat']
                lon = location['lon']

                print('Was at {}, {} during shift at {}'.format(lat, lon, time))

        except StopIteration:
            continue


run()
