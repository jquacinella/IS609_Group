#!/usr/bin/python

import twitter
import pprint

from config import *

# Connect to twitter API using custom Twitter APP and Oauth tokens from 'mrquintopolous'
api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN_KEY,
                  access_token_secret=ACCESS_TOKEN_SECRET)

# Loop thru all tweets that would display on your timeline
for tweet in api.GetHomeTimeline(): 
    pprint.pprint(tweet.AsDict())

    # NOTE: Lets break just to show one for now
    break

# Show a user
pprint.pprint(api.GetUser(screen_name='@dadaviz').AsDict())