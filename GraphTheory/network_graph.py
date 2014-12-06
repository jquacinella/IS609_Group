import networkx as nx
import matplotlib.pyplot as plt
from helpers import *
import random


def graph_construction(graph_info, user_dict, size=None):

    g = nx.DiGraph()
    if not size:
        size = len(user_dict.keys())
    random.seed(425)  # For consistency while experimenting
    uids_in_graph = random.sample(user_dict.keys(), size)

    for uid in uids_in_graph:
        g.add_node(uid, {'handle': user_dict[uid]['twit_ob'].name})

    for uid in uids_in_graph:
        follows_in_graph = [i for i in graph_info[uid]['follows'] if i in uids_in_graph]
        for i in follows_in_graph:
            g.add_edge(uid, i)

    node_labels = nx.get_node_attributes(g, 'handle')

    plt.figure(figsize=(10, 10))

    pos = nx.spring_layout(g)
    nx.draw(g, pos, arrows=True)
    nx.draw_networkx_labels(g, pos, labels=node_labels)

    plt.show()


def main():

    object_location = 'twitter_objects'
    nodes_to_plot = 1000
    graph_info = readobject('ds_community', dir_flag=False, alt_dir=object_location)
    user_dict = readobject('user_dict', dir_flag=False, alt_dir=object_location)

    graph_construction(graph_info, user_dict, size=nodes_to_plot)


if __name__ == "__main__":
    main()