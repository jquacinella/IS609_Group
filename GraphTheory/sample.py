import twitter
import pprint

# Connect to twitter API using custom Twitter APP and Oauth tokens from 'mrquintopolous'
api = twitter.Api(consumer_key='AjU9aXjAVGnAStPSXcpKuL9fJ',
                consumer_secret='JF2Xc6uNfAW0NroCBtqlT860V6pWWPVmm0MI9RmTuCR6jmMdr0',
                access_token_key='16562593-NYrbJNK8w1cd5aujWhJUoTfGz6MR3Y5u7Xa1WdbCh',
                access_token_secret='N5KPbswRrjWPFaOIkaFNmVGAWgHeg1bIZafJPXoBa29Rc')

# Loop thru all tweets that would display on your timeline
for tweet in api.GetHomeTimeline(): 
    pprint.pprint(tweet.AsDict())

    # NOTE: Lets break just to show one for now
    break

# Show a user
pprint.pprint(api.GetUser(screen_name='@dadaviz').AsDict()