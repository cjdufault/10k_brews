"""
Uses OpenStreetMap's Nominatim API to get latitude and longitude based on an address
"""
import requests

osm_search_url = 'https://nominatim.openstreetmap.org/search.php?format=jsonv2&q='


def get(address='', city='', state='', zip_code=''):

    # check that we've been given *something*
    if address != '' or city != '' or state != '' or zip_code != '':
        query = f'{address}%20{city}%20{state}%20{zip_code}'    # concat all info to form query
        response = request(query)

        # extract relevant data
        latitude = response['lat']
        longitude = response['lon']

        return latitude, longitude

    return None


def request(query):
    request_url = osm_search_url + query
    response = requests.request('GET', request_url).json()
    return response[0]
