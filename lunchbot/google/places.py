"""Just messing around with the Google Places API.

see: https://developers.google.com/places/web-service/search
"""

import asyncio
import aiohttp
import async_timeout
import requests
import time
from lunchbot.google.exception import handle_bad_response


class Places(object):
    """Handle Google Places API Calls."""
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    api_key = None

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.next_page_token = None

    def _prep_nearby_search_params(self, lat, lng, radius, kwargs):
        location = ','.join([str(lat), str(lng)])
        params = {
            'key': self.api_key,
            'location': location,
            'radius': radius
        }
        params.update(kwargs)
        if 'rankby' in params:
            params.pop('radius')
        return params

    def nearby_search(self, lat, lng, radius=50000, **kwargs):
        """Make a nearby search call.

        Latitude/longitude can be found via Google Geocoder API.
        Args:
            lat (float): Latitude
            long (float): Longitude
            radius (float, default=50000): Defines the distance (in meters)
                within which to return place results. The maximum allowed
                radius is 50 000 meters.
            keyword (str, optional): A term to be matched against all
                content that Google has indexed for this place, including
                but not limited to name, type, and address, as well as
                customer reviews and other third-party content.
            language (str, optional):  The language code, indicating in
                which language the results should be returned
            minprice (int, optional):  Valid values range between
                0 (most affordable) to 4 (most expensive), inclusive.
            maxprice (int, optional):  Valid values range between
                0 (most affordable) to 4 (most expensive), inclusive.
            name (str, optional): Equivalent to keyword.
            opennow (optional): Returns only those places that are
                open for business at the time the query is sent.
                Places that do not specify opening hours in the Google
                Places database will not be returned if you include
                this parameter in your query.
            rankby (str, optional):  Specifies the order in which results
                are listed. Note that rankby must not be included if radius
                is specified. Including ranby will take precendence over
                radius. Options: prominence (default), distance
            type (str, optional): Restricts the results to places matching
                the specified type. Only one type may be specified.
                See: https://developers.google.com/places/web-service/supported_types
            pagetoken (str, optional):  Returns the next 20 results from a
                previously run search. Setting a pagetoken parameter
                will execute a search with the same parameters used
                previously — all parameters other than pagetoken will be
                ignored.
        """
        params = self._prep_nearby_search_params(lat, lng, radius, kwargs)
        request = requests.get(self.url, params=params)
        response = request.json()
        if response['status'] == 'OK':
            self.next_page_token = response.get('next_page_token')
            return response
        else:
            handle_bad_response(response)

    def next_page(self, token=None):
        """Return the next page of search results."""
        # This needs updated if I include the other Google Places calls
        if not token:
            token = self.next_page_token
        return self.nearby_search(None, None, pagetoken=token)


class AsyncPlaces(Places):
    """An Async focused version of the Places class."""
    async def nearby_search(self, lat, lng, radius=50000, **kwargs):
        params = self._prep_nearby_search_params(lat, lng, radius, kwargs)
        with async_timeout.timeout(10):
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, params=params) as response:
                    response_json = await response.json()
                    if response_json['status'] == 'OK':
                        self.next_page_token = response_json.get('next_page_token')
                        return response_json
                    else:
                        handle_bad_response(response_json)

    async def next_page(self):
        return await self.nearby_search(None, None, pagetoken=self.next_page_token)
