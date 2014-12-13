import pickle
import networkx as nx
import operator

# Load the crawled graph object
g = pickle.load(open("graph_object", "r"))
user_dict = pickle.load(open("twitter_crawl_objects/user_name", "r"))

# Run Network's PageRank algorithm to find best nodes
pr = nx.pagerank(g, alpha=0.9)

# Sort nodes based on PageRank score
sorted_pr = sorted(pr.items(), key=operator.itemgetter(1))

# Print out top 20 nodes
# NOTE: highly similar to thedegree centrality results
for node in sorted_pr[-20:]:
    print node[1], user_dict[node[0]]['name']
