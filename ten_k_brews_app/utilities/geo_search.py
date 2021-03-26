"""
Methods for searching for Establishments by their location, e.g. returning the X number closest to Y location
"""
import math
from ..models import Establishment


def get_closest_establishments(coord, num_returned):
    establishments = Establishment.objects.all()
    closest_dict = select_closest(coord, num_returned, establishments)

    # sorted list of Establishment objects, in order of distance
    closest_list = []
    for i in range(len(closest_dict)):
        min_value = min(closest_dict.values())
        keys = list(closest_dict.keys())
        values = list(closest_dict.values())
        min_value_key = keys[values.index(min_value)]

        # remove the closest entry and add the corresponding Establishment to closest_list
        closest_dict.pop(min_value_key)
        closest_list.append(Establishment.objects.get(pk=int(min_value_key)))

    return closest_list


# takes 2 sets of coordinates (tuples) and finds the distance between them in degrees lat/lon
def get_distance(coord_1, coord_2):
    lat_diff = abs(coord_1[0] - coord_2[0])
    lon_diff = abs(coord_1[1] - coord_2[1])
    return math.sqrt((lat_diff ** 2) + (lon_diff ** 2))     # say hello to my friend Pythagoras


# selects the X closest establishments to given coordinates
def select_closest(coord, num_returned, establishments):
    coordinates = float(coord[0]), float(coord[1])
    closest_dict = {}

    for establishment in establishments:
        distance = get_distance(coordinates, (float(establishment.latitude), float(establishment.longitude)))

        # add to closest_dict if there's less than num_returned in there
        if len(closest_dict) < num_returned:
            closest_dict[str(establishment.pk)] = distance
        else:
            max_value = max(closest_dict.values())

            # if establishment closer than the max value in dict, pop the entry w/ max value & add establishment
            if max_value > distance:
                keys = list(closest_dict.keys())
                values = list(closest_dict.values())
                max_value_key = keys[values.index(max_value)]  # get key for max value

                closest_dict.pop(max_value_key)
                closest_dict[str(establishment.pk)] = distance

    return closest_dict
