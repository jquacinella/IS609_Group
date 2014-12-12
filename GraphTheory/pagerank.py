import pickle
import networkx as nx
import operator

g = pickle.load(open("graph_object", "r"))
user_dict = pickle.load(open("twitter_crawl_objects/user_name", "r"))

pr = nx.pagerank(g, alpha=0.9)
sorted_pr = sorted(pr.items(), key=operator.itemgetter(1))

for node in sorted_pr[-20:]:
    print node[1], user_dict[node[0]]['name']
