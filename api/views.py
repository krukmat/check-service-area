from django.http.response import HttpResponse
from helpers import HelperMethods
import json


def validate_location(request):
    lat_lng = request.GET.get('lat_lng')
    hotel_address = request.GET.get('hotel_address')
    airport_address = request.GET.get('airport_address')
    airport_code = request.GET.get('airport_code')
    hotel_name = request.GET.get('hotel_name')

    if lat_lng:
        lat_lng = lat_lng.split(',')
        lat_lng = (float(lat_lng[0]), float(lat_lng[1]))

    region_supported = {}
    region_supported['is_region_supported'] = False

    # First case
    if lat_lng:
        region_supported['is_region_supported'] = HelperMethods.is_closer_to_a_region(lat_lng)
    else:
        # Second case
        if hotel_address:
            # Convert hotel_address to hotel's coords
            hotel_coords = HelperMethods.convert_address_to_coords(hotel_address)
            if hotel_coords:
                region_supported['is_region_supported'] = HelperMethods.is_closer_to_a_region(hotel_coords)
        else:
            # Third case
            if hotel_name and airport_address:
                lat_lng = HelperMethods.search_lat_lng_hotel_near_by(airport_address, hotel_name)
                if lat_lng:
                    region_supported['is_region_supported'] = HelperMethods.is_closer_to_a_region(lat_lng)
            else:
                # Fourth case
                if hotel_name and airport_code:
                    lat_lng = HelperMethods.search_lat_lng_hotel_near_airport_code(airport_code, hotel_name)
                    if lat_lng:
                        region_supported['is_region_supported'] = HelperMethods.is_closer_to_a_region(lat_lng)

    data = json.dumps(region_supported)
    return HttpResponse(data, content_type='application/json')
