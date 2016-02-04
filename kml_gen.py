import csv
import datetime
import json

import ijson
from math import radians, cos, sin, sqrt, asin

import simplekml


def run():

    start_date = datetime.datetime(2015, month=6, day=30)
    end_date = datetime.datetime(2015, month=12, day=31)
    date = None
    start = None
    end = None
    shift_distance = 0
    csv_file = open('shifts.csv')
    spamreader = csv.reader(csv_file, delimiter=',', quotechar='"')
    for row in spamreader:

        if date is not None:
            print("Distance for shift on {} from {} to {} was {}km".format(date, start, end, shift_distance))

        coords = []
        shift_distance = 0
        prev_lat = None
        prev_lon = None

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

                coords.append((lon, lat))

                prev_lon = lon
                prev_lat = lat

                # print('Was at {}, {} during shift at {}'.format(lat, lon, time))

        except StopIteration:

            path = "kml_days/{}.kml".format(date)
            kml = simplekml.Kml()
            lin = kml.newlinestring(name="Pathway",
                                    description="A pathway in Kirstenbosch",
                                    coords=coords)
            kml.save(path)
            continue


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r
