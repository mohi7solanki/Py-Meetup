import logging
from datetime import datetime

import tweepy
from decouple import config


logging.basicConfig(filename='errors.log', level=logging.INFO)


def construct_tweet(event):
    event_tweet = '''{} on {} at {} more details at {}'''.format(
        event['name'].strip(),
        datetime.strptime(event['local_date'], "%Y-%m-%d").strftime("%-m %B"),
        datetime.strptime(event['local_time'], "%H:%M").strftime("%I:%M %p"),
        event['link'],
    )
    event_tweet += '\n#meetup #python_meetup #bengaluru'
    return event_tweet


def login():
    auth = tweepy.OAuthHandler(
        config('consumer_key'), config('consumer_secret')
    )
    auth.set_access_token(config('access_token'), config('access_secret'))
    return tweepy.API(auth)


def tweet(api, event, max_retry=5):
    event_tweet = construct_tweet(event)
    try:
        api.update_status(status=event_tweet)
    except Exception as e:
        if max_retry != 1:
            tweet(api, event, max_retry - 1)
        else:
            logging.error(e)
