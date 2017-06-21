"""Main file to start the bot."""
# TODO: Generate a config template if none given.

import argparse
import configparser
import asyncio
from lunchbot import LunchBot


def parse_args():
    """Parse and return the command line arguments."""
    description = 'Launch and manage LunchBot.'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--config', default='config.ini')
    return parser.parse_args()


def read_config(path):
    """Use configparser to read and output the config file."""
    config = configparser.ConfigParser()
    config.read(path)
    return config


def main():
    args = parse_args()
    config = read_config(args.config)
    print(config['ApiKeys']['GooglePlaces'])

    bot = LunchBot(slack_token=config['Slack']['ApiToken'],
                   places_token=config['ApiKeys']['GooglePlaces'],
                   geocoder_token=config['ApiKeys']['GoogleGeocoder'],
                   address=config['HomeBase']['Address'])

    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(bot.rtm(bot.listen))
    loop.close()

    async_test(config['Slack']['ApiToken'])


def async_test(token):
    print(token)
    bot = LunchBot(token)
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    # response = loop.run_until_complete(sc.api_call('auth.test'))
    # print(response)
    loop.run_until_complete(bot.rtm(bot.listen))
    loop.close()


if __name__ == '__main__':
    main()
