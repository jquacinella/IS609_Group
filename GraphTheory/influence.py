import time
import twitter
import pickle
from config import *

api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_TOKEN_KEY,
                      access_token_secret=ACCESS_TOKEN_SECRET)


tweet_id=541746341295452160
users = api.GetRetweeters(tweet_id)
followers = { }
followers_count = 0
for user in users:
    while True:
        try:
            print "User %d" % user
            followers[user] = api.GetFollowerIDs(user_id=user)
            break
        except:
            print "Sleeping ..."
            time.sleep(60*5)
            continue
    
    followers_count += len(followers[user])
    print followers_count

pickle.dump(followers, open("followers", "wb"), pickle.HIGHEST_PROTOCOL)