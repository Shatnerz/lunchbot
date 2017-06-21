"""Make actual calls to google."""

# We will need the config for the api keys.
# Let's just assume it is up one directory.

import os
import pytest
import configparser
import lunchbot.google.geocoder as geocoder
import lunchbot.google.places as places


# Test using the Whitehouse location
whitehouse_address = '1600 Pennsylvania Ave NW, Washington, DC 20500'
whitehouse_lat = 38.8976633
whitehouse_lng = -77.0365739


@pytest.fixture
def config():
    """Return the config."""
    this_dir = os.path.dirname(__file__)
    config_path = os.path.join(this_dir, '..', 'config.ini')
    config_path = os.path.abspath(config_path)
    config_obj = configparser.ConfigParser()
    config_obj.read(config_path)
    return config_obj


@pytest.fixture
def Places(config):
    return places.Places(config['ApiKeys']['GooglePlaces'])


@pytest.fixture
def AsyncPlaces(config):
    return places.AsyncPlaces(config['ApiKeys']['GooglePlaces'])


@pytest.fixture
def Geocoder(config):
    return geocoder.Geocoder(config['ApiKeys']['GoogleGeocoder'])


@pytest.fixture
def AsyncGeocoder(config):
    return geocoder.AsyncGeocoder(config['ApiKeys']['GoogleGeocoder'])


class TestSync():
    def test_get_location(self, Geocoder):
        response = Geocoder.get_location(whitehouse_address)
        expected_response = {'lat': whitehouse_lat, 'lng': whitehouse_lng}
        assert response == expected_response

    def test_nearby_search(self, Places):
        """Just make sure no exceptions are raised."""
        response = Places.nearby_search(whitehouse_lat, whitehouse_lng)


class TestAsync():
    @pytest.mark.asyncio
    async def test_get_location(self, AsyncGeocoder):
        response = await AsyncGeocoder.get_location(whitehouse_address)
        expected_response = {'lat': whitehouse_lat, 'lng': whitehouse_lng}
        assert response == expected_response

    @pytest.mark.asyncio
    async def test_nearby_search(self, AsyncPlaces):
        response = await AsyncPlaces.nearby_search(whitehouse_lat, whitehouse_lng)
