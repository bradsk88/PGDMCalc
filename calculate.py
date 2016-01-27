import json
from math import sin, radians, cos, sqrt, asin

import ijson


def run():

    json_file = open('/home/bradsk88/Desktop/finance/LocationHistory.json')
    locations = ijson.parse(json_file)

    prev_lat = None
    prev_lon = None

    total_kms = 0

    cont = True
    while (cont):
        cont = False
        (lat, lon) = (None, None)
        prefix, event, value = next(locations, None)

        cont = True

        if (prefix, event) == ('locations.item.latitudeE7', 'number'):
            lat = value / 10000000
            next(locations)
            prefix, event, value = next(locations)
            if (prefix, event) == ('locations.item.longitudeE7', 'number'):
                lon = value / 10000000

                if prev_lat and prev_lon:
                    distance = haversine(prev_lat, prev_lon, lat, lon)
                    total_kms += distance
                    print("Distance From {}, {} to {}, {}: {}km [Total: {}km]".format(prev_lat, prev_lon, lat, lon, distance, total_kms))

                prev_lat = lat
                prev_lon = lon


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

run()
