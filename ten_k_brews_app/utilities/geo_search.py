"""
Methods for searching for Establishments by their location, e.g. returning the X number closest to Y location
"""
import math
from ..models import Establishment


# returns a list of N establishments, sorted by distance from inputted coordinates
def get_closest_establishments(coordinates, num_returned):
    establishments = Establishment.objects.all()
    closest = select_closest(coordinates, num_returned, establishments)

    establishments = []
    for item in closest:
        establishment = Establishment.objects.get(pk=item[0])
        establishments.append(establishment)

    return establishments


# takes 2 sets of coordinates (tuples) and finds the distance between them in degrees lat/lon
def get_distance(coord_1, coord_2):
    lat_diff = abs(coord_1[0] - coord_2[0])
    lon_diff = abs(coord_1[1] - coord_2[1])
    return math.sqrt((lat_diff ** 2) + (lon_diff ** 2))     # say hello to my friend Pythagoras


# selects the X closest establishments to given coordinates
def select_closest(coordinates, num_returned, establishments):
    closest = {}

    for establishment in establishments:
        distance = get_distance(coordinates, (float(establishment.latitude), float(establishment.longitude)))

        # add to closest if there's less than num_returned in there
        if len(closest) < num_returned:
            closest[establishment.pk] = distance
        else:
            max_value = max(closest.values())

            # if establishment closer than the max value in dict, pop the entry w/ max value & add establishment
            if max_value > distance:
                keys = list(closest.keys())
                values = list(closest.values())
                max_value_key = keys[values.index(max_value)]  # get key for max value

                closest.pop(max_value_key)
                closest[establishment.pk] = distance

    return sorted(closest.items(), key=lambda item: item[1])
