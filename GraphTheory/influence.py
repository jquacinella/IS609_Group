import time
import twitter
import pickle
from config import *

# Get the twitter API
api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_TOKEN_KEY,
                      access_token_secret=ACCESS_TOKEN_SECRET)

# Right now, Hilary Mason's tweet is hardcoded
tweet_id=541746341295452160

# Grab all the users who retweeted this tweet
users = api.GetRetweeters(tweet_id)

# Build a dictionary of retweeter id to a list of follower IDs, using Twitter's API
# Note: we need to rate limit
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

# Save file for use in iPython notebook
pickle.dump(followers, open("followers", "wb"), pickle.HIGHEST_PROTOCOL)


#  Create new graph with tweet as first node
new_g = nx.DiGraph()
new_g.add_node("tweet", {'color': 'orange'})

# Initialize the layers we want to use
shell1 = ["tweet"]
shell2 = []
shell3 = []

# Add nodes to graph
count = 0
for uid in followers:
    count = count + 1
        
    new_g.add_node(uid, {'color': 'red'})
    new_g.add_edge(uid, "tweet", {'type': 'retweeted'})
    shell2.append(uid)
    
    # Add edges to graph
    follower_count = 0
    for follower in followers[uid]:
        # Trim the graph by showing only 5 followers
        follower_count = follower_count + 1
        if follower_count % 5 == 0: break

        # Add a node for the follower, connect it to the right user          
        new_g.add_node(follower, {'color': 'red'})
        new_g.add_edge(follower, uid, {'type': 'follows'})

        # Add this user to outer shell
        shell3.append(follower)

# Create node and edge labesl from properties
node_labels = nx.get_node_attributes(new_g,'id')
edge_labels = nx.get_edge_attributes(new_g,'type')
colors = nx.get_node_attributes(new_g, 'color')

# Create a networkx layout based on shells we created
pos_shell = nx.shell_layout(g, nlist=[shell1, shell2, shell3])

# Plot the graph
plt.figure(figsize=(15, 15))
nx.draw(new_g, pos_shell, arrows=True, node_size=900, node_color=colors.values())
x = nx.draw_networkx_edge_labels(new_g, pos_shell, labels = edge_labels)