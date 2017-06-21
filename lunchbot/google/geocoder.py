"""Just messing around with the Google Geocoding API.

see: https://developers.google.com/maps/documentation/geocoding/intro
"""

import asyncio
import aiohttp
import async_timeout
import requests
from lunchbot.google.exception import handle_bad_response


class Geocoder(object):
    """Handle Google Geocoder Calls."""
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    api_key = None

    def __init__(self, api_key=None):
        self.api_key = api_key

    def _prep_params(self, address, kwargs):
        """Prep the params for the geocoder call."""
        # This seems unecessary but removes duplication with the async class
        params = {
            'key': self.api_key,
            'address': address
        }
        params.update(kwargs)
        return params

    def get_geocoding(self, address, **kwargs):
        """Return the full response from the API call.

        Returns a list of json.

        Args:
            address (str): The street address that you want to geocode,
                in the format used by the national postal service of
                the country concerned.
            bounds (str, optional): The bounding box of the viewport within
                which to bias geocode results more prominently. This
                parameter will only influence, not fully restrict, results
                from the geocoder.
            language (str, optional): The language in which to return results.
            region (str, optional): The region code, specified as a
                ccTLD ("top-level domain") two-character value. This parameter
                will only influence, not fully restrict, results from the
                geocoder.
            components )str, optinal):  The component filters, separated by a
                pipe (|). Each component filter consists of a component:value
                pair and will fully restrict the results from the geocoder.
        """
        params = self._prep_params(address, kwargs)
        request = requests.get(self.url, params=params)
        response = request.json()
        if response['status'] == 'OK':
            return response['results']
        else:
            handle_bad_response(response)

    def get_location(self, address, **kwargs):
        """Returns {'lat': 123. 'lng': 456} for the given address."""
        geocoding = self.get_geocoding(address, **kwargs)
        if len(geocoding) < 1:
            msg = 'Address returned more than one result.'
            raise GoogleGeocodingException(msg)
        else:
            return geocoding[0]['geometry']['location']


class AsyncGeocoder(Geocoder):
    """An async version of the above."""
    async def get_geocoding(self, address, **kwargs):
        """Return the full response from the API call.

        Returns a list of json.
        """
        params = self._prep_params(address, kwargs)
        with async_timeout.timeout(10):
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, params=params) as response:
                    response_json = await response.json()
                    if response_json['status'] == 'OK':
                        return response_json['results']
                    else:
                        handle_bad_response(response_json)

    async def get_location(self, address, **kwargs):
        """Returns {'lat': 123. 'lng': 456} for the given address."""
        geocoding = await self.get_geocoding(address, **kwargs)
        if len(geocoding) < 1:
            msg = 'Address returned more than one result.'
            raise GoogleGeocodingException(msg)
        else:
            return geocoding[0]['geometry']['location']
