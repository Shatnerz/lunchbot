"""Actual logic for the LunchBot.

Can run with something like
    loop.run_until_complete(bot.rtm(bot.listen))
"""

from pprint import pprint
import asyncio
from random import shuffle
from lunchbot.slack import SlackClient
from lunchbot.google.geocoder import AsyncGeocoder
from lunchbot.google.places import AsyncPlaces


class LunchBot(SlackClient):
    """Websocket based, async slack bot to find lunch."""

    def __init__(self, slack_token, places_token, geocoder_token, address):
        super().__init__(slack_token)
        self.places = AsyncPlaces(places_token)
        self.geocoder = AsyncGeocoder(geocoder_token)
        self.address = address
        loop = asyncio.get_event_loop()
        loc = loop.run_until_complete(self.geocoder.get_location(address))
        self.lat = loc['lat']
        self.lng = loc['lng']

    async def listen(self, event):
        """Main loop."""
        event_type = event.get('type')
        # See: https://api.slack.com/events
        if event_type == 'message':
            await self.handle_message(event)

    async def handle_message(self, message):
        text = message.get('text')
        channel = message.get('channel')
        if text.startswith('<@{}>'.format(self.id)):  # talking to bot
            words = text.split(' ')
            if len(words) > 1:
                cmd = words[1]
                args = words[2:]
                if cmd.lower() == 'help':
                    await self.help(channel, args)
                if cmd.lower() == 'lunch':
                    await self.lunch(channel, args)

    async def help(self, channel, args):
        """Reply to help request."""
        self.rtm_message("I ain't got time for your shit", channel)

    async def lunch(self, channel, args):
        """Reply to lunch request."""
        # TODO: make smarter
        # assume first arg is type of food
        response = await self.places.nearby_search(
            self.lat, self.lng, radius=5000, type='restaurant', opennow=True)
        places = response['results']
        pprint(places)
        print()
        shuffle(places)
        place = places[0]
        pprint(places[0])
        self.rtm_message('hi', channel)

        price_level = place.get('price_level')
        rating = place.get('rating')
        icon = place.get('icon')
        name = place.get('name')
        photos = place.get('photos')
        address = place.get('vicinity')
