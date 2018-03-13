import json
import logging
import pickle
import time
from datetime import datetime

import requests
from decouple import config

from tweet import login, tweet
from utils import next_month

URL = 'https://api.meetup.com/find/upcoming_events'

logging.basicConfig(filename='errors.log', level=logging.INFO)

date = next_month(datetime.today())

params = {
    'end_date_range': f'{date.strftime("%Y-%m-%d")}T00:00:00',
    'key': config('key'),
    'lat': 12.9716,
    'lon': 77.5946,
    'order': 'time',
    'radius': 50,
    'text': 'python',
}


def get_previous_events():
    with open('previous_events.pickle', 'rb') as f:
        try:
            previous_events = pickle.load(f)
        except EOFError:
            previous_events = set()
    return previous_events


def filter_events(events):
    """Remove events that has been tweeted previously."""
    previous_events = get_previous_events()
    with open('previous_events.pickle', 'wb') as f:
        filtered_events = filter(
            lambda x: x['id'] not in previous_events, events
        )
        current_events = set(event['id'] for event in events)
        pickle.dump(current_events, f)
    return filtered_events


def main():
    try:
        res = requests.get(URL, params=params)
        data = json.loads(res.text)
        events = filter_events(data['events'])
        api = login()
        for event in events:
            tweet(api, event)
            print(f'Tweeted event {event["name"]} successfully!')
            time.sleep(3 * 60)

    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    main()
