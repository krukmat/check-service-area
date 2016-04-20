from django.test import TestCase

# Create your tests here.
from helpers import *
from mock import patch, MagicMock
from django.test import Client
from django.core.urlresolvers import reverse


class HelpersTestCase(TestCase):

    def test_is_closer_to_a_region(self):
        # Close
        result = HelperMethods.is_closer_to_a_region((38.887563, -77.019929))
        self.assertTrue(result)
        # Not close: Buenos Aires
        result = HelperMethods.is_closer_to_a_region((-34.608192, -58.373382))
        self.assertFalse(result)

    def test_convert_address_to_coords(self):
        result = HelperMethods.convert_address_to_coords('1600 Amphitheatre Parkway, Mountain View, CA')
        self.assertEqual(result, (37.4224497, -122.0840329))
        # Invalid address
        result = HelperMethods.convert_address_to_coords('lalalalal ffrrff, Perinola, FRFRG')
        self.assertIsNone(result)

    @patch('api.helpers.HelperMethods.convert_address_to_coords', MagicMock(return_value=(38.887563, -77.019929)))
    def test_search_lat_lng_hotel_near_by(self):
        return_value = HelperMethods.search_lat_lng_hotel_near_by('', 'Sheraton')
        self.assertIsNotNone(return_value)

    def test_search_lat_lng_from_airport_code(self):
        return_value = HelperMethods.search_lat_lng_from_airport_code('mdq')
        self.assertEqual(return_value[0], -37.934167)
        self.assertEqual(return_value[1], -57.573333)
        # Invalid airport
        return_value = HelperMethods.search_lat_lng_from_airport_code('mddfqg')
        self.assertIsNone(return_value)


class ViewTestCase(TestCase):

    def test_lat_lng_case(self):
        client = Client()
        # BAD
        response = client.get(reverse('query') + '?lat_lng=19.939037,-90.119577')
        self.assertEqual(response.status_code, 200)
        _object = json.loads(response.content)
        self.assertEqual(_object['is_region_supported'], False)
        # http://192.168.99.100:6666/query?lat_lng=38.887563,-77.019929
        response = client.get(reverse('query') + '?lat_lng=38.887563,-77.019929')
        _object = json.loads(response.content)
        self.assertEqual(_object['is_region_supported'], True)

    def test_hotel_address(self):
        # Case OK
        client = Client()
        response = client.get(reverse('query') + '?hotel_address=4835%20Collins%20Ave%20Miami%20Beach%20FL')
        self.assertEqual(response.status_code, 200)
        _object = json.loads(response.content)
        self.assertEqual(_object['is_region_supported'], True)

        # Case BAD
        response = client.get(reverse('query') + '?hotel_address=3%20Statehouse%20Plaza%20Little%20Rock%20AR')
        self.assertEqual(response.status_code, 200)
        _object = json.loads(response.content)
        self.assertEqual(_object['is_region_supported'], False)

    def test_airport_address(self):
        # Case OK
        client = Client()
        response = client.get(reverse('query') + '?airport_address=2100%20NW%2042nd%20Ave.%20Miami,%20Fl&hotel_name=Marriot')
        self.assertEqual(response.status_code, 200)
        _object = json.loads(response.content)
        self.assertEqual(_object['is_region_supported'], True)

        # Case BAD
        response = client.get(reverse('query') + '?airport_address=2100%20NW%2042nd%20Ave.%20Miami,%20Fl&hotel_name=Coral+Creek+Plaza')
        self.assertEqual(response.status_code, 200)
        _object = json.loads(response.content)
        self.assertEqual(_object['is_region_supported'], False)

    def test_airport_code(self):
        # Case OK
        client = Client()
        response = client.get(
            reverse('query') + '?airport_code=MIA&hotel_name=Marriot')
        self.assertEqual(response.status_code, 200)
        _object = json.loads(response.content)
        self.assertEqual(_object['is_region_supported'], True)
        # Case BAD
        response = client.get(
            reverse('query') + '?airport_code=MIA&hotel_name=Coral+Creek+Plaza')
        self.assertEqual(response.status_code, 200)
        _object = json.loads(response.content)
        self.assertEqual(_object['is_region_supported'], False)

