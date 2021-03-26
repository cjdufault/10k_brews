"""
Uses OpenStreetMap's Nominatim API to get latitude and longitude based on an address
"""
import requests

osm_search_url = 'https://nominatim.openstreetmap.org/search?format=jsonv2&q='


def get_coordinates(address):
    response = request(address)

    if response:
        # extract relevant data
        latitude = float(response['lat'])
        longitude = float(response['lon'])

        return latitude, longitude


def request(query):
    request_url = osm_search_url + query
    response = requests.request('GET', request_url).json()

    if response:
        return response[0]
