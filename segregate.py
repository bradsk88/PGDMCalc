import json
import datetime
from math import sin, radians, cos, sqrt, asin

import ijson
import simplekml

from calc_distance import haversine

MIN_DATE = datetime.datetime(2015, month=6, day=29)

def run():

    json_file = open('/home/bradsk88/Desktop/finance/LocationHistory.json')
    locations = ijson.parse(json_file)

    prev_lat = 0
    prev_lon = 0
    prev_appended_lat = 0
    prev_appended_lon = 0
    timestamp = None

    total_kms = 0

    date_name = None

    events = []

    cont = True

    while (cont):
        cont = False
        (lat, lon) = (None, None)
        prefix, event, value = next(locations, None)

        cont = True

        if prefix == 'locations.item.timestampMs':
            i_date = datetime.datetime.fromtimestamp(int(value)/1000)
            if i_date < MIN_DATE:
                return

            timestamp = value

            if i_date.date() != date_name:
                # Date has changed
                if date_name is not None:

                    with open("days/{}.json".format(date_name.strftime("%Y-%m-%d")), 'w') as outfile:
                        json.dump(list(reversed(events)), outfile, indent=3)
                        print("Wrote to {}".format(outfile.name))
                        events = []
                    date_name = i_date.date()
                else:
                    date_name = i_date.date()
            continue


        if (prefix, event) == ('locations.item.latitudeE7', 'number'):
            lat = value / 10000000
            lat_e7 = value
            next(locations)
            prefix, event, value = next(locations)
            if (prefix, event) == ('locations.item.longitudeE7', 'number'):
                lon = value / 10000000
                lon_e7 = value

                if prev_lat and prev_lon:
                    distance = haversine(prev_lat, prev_lon, lat, lon)
                    total_kms += distance
                    # print("Distance From {}, {} to {}, {}: {}km [Total: {}km]".format(prev_lat, prev_lon, lat, lon, distance, total_kms))

                difference_lat = abs(lat - prev_appended_lat)
                difference_lon = abs(lon - prev_appended_lon)

                if max(difference_lat, difference_lon) > 0.000001:

                    events.append({
                        'timestampMs': timestamp,
                        'lat': lat,
                        'latitudeE7': lat_e7,
                        'lon': lon,
                        'longitudeE7': lon_e7,
                        'pretty': i_date.ctime(),
                        'url': 'https://www.google.com/maps/embed/v1/place?key=AIzaSyB11SGRNV4ENjbc1WjeqxB-GyYIz8cdZV4&q={lat},{lon}'.format(lat=lat, lon=lon)
                    })

                    prev_appended_lat = lat
                    prev_appended_lon = lon

                prev_lat = lat
                prev_lon = lon
