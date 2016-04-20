__author__ = 'matiasleandrokruk'

from django.conf import settings

# Create your views here.
from haversine import haversine
import googlemaps
import requests
import json

MINIMAL_RADIUS = 50
regions = [
    (34.051203, -118.243386), #Los Angeles
    (37.774857, -122.419623), # San Francisco
    (40.714298, -74.005813), # New York
    (38.895193, -77.036628),  # Washington DC
    (33.749052, -84.388331),  # Atlanta
    (41.850033, -87.650052),   # Chicago
    (32.802771, -96.770022), #Dallas
    (29.954639, -90.075078),  # New Orleans
    (36.114592, -115.173733), # Las Vegas
    (25.77439, -80.193701)   #Miami
]


class HelperMethods(object):

    @staticmethod
    def is_closer_to_a_region(lat_lng):
        # The first region that fits the MINIMAL_RADIUS
        for region in regions:
            if haversine(lat_lng, region, miles=True) <= MINIMAL_RADIUS:
                return True
        return False

    @staticmethod
    def convert_address_to_coords(address):
        gmaps = googlemaps.Client(settings.GOOGLE_API_KEY)
        result = gmaps.geocode(address)
        if len(result) > 0:
            lat_lng = result[0]['geometry']['location']
            return lat_lng['lat'], lat_lng['lng']
        return None

    @staticmethod
    def search_lat_lng_hotel_near_by(airport_code_address, hotel_name):
        lat, lng = HelperMethods.convert_address_to_coords(airport_code_address)
        return HelperMethods.search_near_by(lat, lng, 'hotel', hotel_name)

    @staticmethod
    def search_near_by(lat, lng, type, name):
        gmaps = googlemaps.Client(settings.GOOGLE_API_KEY)
        result = gmaps.places_nearby(location=(lat, lng), rank_by='distance', type=type, name=name)
        if 'results' in result and len(result['results']) > 0:
            location = result['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        return None

    @staticmethod
    def search_lat_lng_hotel_near_airport_code(airport_code, hotel_name):
        lat, lng = HelperMethods.search_lat_lng_from_airport_code(airport_code)
        return HelperMethods.search_near_by(lat, lng, 'hotel', hotel_name)

    @staticmethod
    def search_lat_lng_from_airport_code(airport_code):
        string_url = "?user_key=".join(["/".join([settings.AIRPORT_API_URL, airport_code]), settings.AIRPORT_API_KEY])
        r = requests.get(string_url)
        if r.status_code == 200:
            # remove the callback(...) wrapper
            if 'callback(' in r.text:
                result = r.text[9:]
                result = result[:-1]
                json_result = json.loads(result)
                # Check is there a valid airport
                if len(json_result['airports']) > 0:
                    return json_result['airports'][0]['lat'], json_result['airports'][0]['lng']
        return None