import networkx as nx
import matplotlib.pyplot as plt
from helpers import *
import random

import numpy as np

def create_test_object(user_dict, size=3):
    # Set some parameters
    count_options = [1, 2, 3, 4, 5]
    max_follows = 3

    # For consistency.
    random.seed(835)
    # Grab a random sample of user ids from the user_dict
    uids = random.sample(user_dict.keys(), size)

    # Build test object
    test_object = {}
    for current_id in uids:
        # Each node has follows a random number of other nodes up to max_follows
        num_follows = random.choice(xrange(max_follows)) + 1
        # Sample from nodes that will be in the graph
        follows = random.sample(uids, num_follows)
        # Filter this so the node does not follow itself
        follows = [i for i in follows if i != current_id]

        # test_object[current_id] = {'name': user_dict[current_id]['twit_ob'].name,
        #                            'count': random.choice(count_options),
        #                            'follows': follows}
        test_object[current_id] = {'name': user_dict[current_id]['name'],
                                   'count': random.choice(count_options),
                                   'follows': follows}
    # Print out the test object for comparison to generated graph
    for k in test_object.keys():
        print test_object[k]
    return test_object


def graph_construction(graph_info, user_dict, size=None):
    # Initialize directed graph
    g = nx.DiGraph()

    # If size is not specified, use entire set
    if not size:
        size = len(user_dict.keys())

    # Get a random sample of size=size to plot
    # random.seed(425)  # For consistency while experimenting
    # uids_in_graph = random.sample(user_dict_filtered.keys(), size)
    
    # Filter out nodes that have low counts
    user_dict_filtered = {}
    for uid in user_dict:
        if user_dict[uid]['count'] >= 2:
            user_dict_filtered[uid] = user_dict[uid]

    uids_in_graph = user_dict_filtered.keys()

    # Add nodes to graph
    for uid in uids_in_graph:
        g.add_node(uid, {'handle': user_dict_filtered[uid]['name']})

    # Add edges to graph
    for uid in uids_in_graph:
        follows_in_graph = [i for i in graph_info[uid]['follows'] if i in uids_in_graph]
        for i in follows_in_graph:
            g.add_edge(uid, i, color='blue')

    # Get label info
    node_labels = nx.get_node_attributes(g, 'handle')

    # Find the in degree of each node
    degree = g.in_degree()

    pickle.dump(g, open('graph_object', 'wb'), pickle.HIGHEST_PROTOCOL)

    # Plot graph with spring layout
    fig = plt.figure(figsize=(10, 10), facecolor='black')
    pos_spring = nx.spring_layout(g)
    nx.draw(g, pos_spring, arrows=True, with_labels=False, node_size=[v * 4 for v in degree.values()])
    nx.draw_networkx_labels(g, pos_spring, labels=node_labels, font_weight='bold', font_size=11, font_color="white")
    plt.savefig('spring_layout.png', facecolor='grey')
    plt.show()

    # Plot new graph with shell layout
    fig = plt.figure(figsize=(10, 10))

    # Shell calculations
    shell1 = []; shell2 = []; shell3 = [];
    for uid in user_dict_filtered:
        if degree[uid] < 50:
            shell1.append(uid)
        elif degree[uid] >= 50 and degree[uid] < 90:
            shell2.append(uid)
        elif degree[uid] >= 90:
            shell3.append(uid)
    shells = [shell3, shell2, shell1]
    pos_shell = nx.shell_layout(g, nlist=shells)

    # Draw graph and labels
    nx.draw(g, pos_shell, arrows=True, with_labels=False)#, node_size=[v * 4 for v in degree.values()])
    nx.draw_networkx_labels(g, pos_shell, labels=node_labels, font_weight='bold', font_size=11, font_color="white")

    # Print figure
    plt.savefig('shell_layout.png', facecolor='grey')
    plt.show()
    



def main():
    global DEBUG
    DEBUG = False

    object_location = 'twitter_crawl_objects'
    nodes_to_plot = 100

    user_dict = readobject('user_name', dir_flag=False, alt_dir=object_location)

    if DEBUG:
        nodes_to_plot = 10
        graph_info = create_test_object(user_dict, size=nodes_to_plot)
        user_dict = {k: user_dict[k] for k in graph_info.keys()}
    else:
        graph_info = readobject('ds_community', dir_flag=False, alt_dir=object_location)

    graph_construction(graph_info, user_dict, size=nodes_to_plot)


if __name__ == "__main__":
    main()