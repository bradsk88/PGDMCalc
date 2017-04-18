import csv
import datetime
import json

import ijson
from math import radians, cos, sin, sqrt, asin

import math


def run():

    start_date = datetime.datetime(2016, month=1, day=1)
    end_date = datetime.datetime(2016, month=4, day=1)
    date = None
    start = None
    end = None
    shift_distance = 0
    csv_file = open('shifts.csv')
    spamreader = csv.reader(csv_file, delimiter=',', quotechar='"')
    shifts = []

    i_date = None

    for row in spamreader:

        if i_date is not None and date is not None:

            if i_date < start_date:
                break

            if i_date > end_date:
                continue

            print("Distance for shift on {} from {} to {} was {}km".format(date, start, end, shift_distance))
            shifts.append({
                'date': date,
                'start': start,
                'end': end,
                'kilometers': '%0d' % shift_distance
            })


        shift_distance = 0
        prev_lat = None
        prev_lon = None

        if not row: 
            print("Reached end of file")
            break

        date = row[0]
        start = row[1]
        end = row[2]

        if date == 'date':
            continue

        i_date = datetime.datetime.strptime(date, '%Y-%m-%d')
        i_start = datetime.datetime.strptime(start, "%I:%M %p").time()
        i_end = datetime.datetime.strptime(end, "%I:%M %p").time()

        json_file = open('days/{}.json'.format(date))
        locations = json.load(json_file)
        time = None

        try:

            # print("{}: Shift started at {}".format(date, start))

            for location in locations:
                time = datetime.datetime.fromtimestamp(int(location['timestampMs'])/1000).time()
                if not time:
                    continue
                if time < i_start:
                    continue
                if time > i_end:
                    # print("{}: Shift ended at {}".format(date, end))
                    raise StopIteration()

                lat = location['lat']
                lon = location['lon']

                if prev_lat is not None and prev_lon is not None:
                    distance = haversine(prev_lon, prev_lat, lon, lat)
                    shift_distance += distance

                prev_lon = lon
                prev_lat = lat

                # print('Was at {}, {} during shift at {}'.format(lat, lon, time))

        except StopIteration:
            continue

    with open('shifts_after.csv', 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Date', 'Shift Start', 'Shift End', 'Distance (km)'])
        for shift in shifts:
            spamwriter.writerow([shift['date'], shift['start'], shift['end'], shift['kilometers']])


def haversine(lon1, lat1, lon2, lat2):
    # deltas between origin and destination coordinates
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)

    # a central angle between the two points
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
    * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)

    # the determinative angle of the triangle on the surface of the sphere (Earth)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    # a spherical distance between the two points, i.e. hills etc are not considered
    r = 6371
    return r * c
