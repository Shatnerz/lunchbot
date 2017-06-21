"""Module for connecting and dealing with slack."""

import argparse
import configparser
import asyncio
import aiohttp
import async_timeout
import json


class SlackClient(object):
    """Async Slack client."""
    # see: https://medium.com/@greut/a-slack-bot-with-pythons-3-5-asyncio-ad766d8b5d8f

    url = 'https://slack.com/api/{0}'

    def __init__(self, token):
        self.token = token
        self.websocket = None
        self.id = None
        self.name = None
        self.team_domain = None
        self.team_id = None
        self.team_name = None

    async def api_call(self, method, timeout=None, **kwargs):
        """Slack API Call."""
        with async_timeout.timeout(timeout):
            async with aiohttp.ClientSession() as session:
                form = aiohttp.FormData({} or kwargs)
                form.add_field('token', self.token)
                async with session.post(self.url.format(method),
                                        data=form) as response:
                    assert 200 == response.status, ('{0} with {1} failed.'
                                                    .format(method, kwargs))
                    return await response.json()

    async def rtm(self, message_handler):
        """Connect to the Real-Time Messaging Websocket

        and push messages to a queue."""
        rtm = await self.api_call('rtm.connect')
        self._first_connect(rtm)
        assert rtm['ok'], 'Error connecting to RTM.'
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(rtm['url']) as websocket:
                self.websocket = websocket
                async for msg in websocket:
                    assert msg.tp == aiohttp.MsgType.text
                    message = json.loads(msg.data)
                    asyncio.ensure_future(message_handler(message))

    def rtm_message(self, text, channel, **kwargs):
        data = {
            'type': 'message',
            'channel': channel,
            'text': text
        }
        data.update(kwargs)
        out = json.dumps(data)
        self.websocket.send_str(out)

    def _first_connect(self, message):
        """Update the instance variables on connecting to rtm."""
        team = message['team']
        self.team_id = team['id']
        self.team_domain = team['domain']
        self.team_name = team['name']
        self.id = message['self']['id']
        self.name = message['self']['name']
