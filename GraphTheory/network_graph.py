import networkx as nx
import matplotlib.pyplot as plt
from helpers import *
import random


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

        test_object[current_id] = {'name': user_dict[current_id]['twit_ob'].name,
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
    random.seed(425)  # For consistency while experimenting
    uids_in_graph = random.sample(user_dict.keys(), size)

    # Add nodes to graph
    for uid in uids_in_graph:
        g.add_node(uid, {'handle': user_dict[uid]['twit_ob'].name})

    # Add edges to graph
    for uid in uids_in_graph:
        follows_in_graph = [i for i in graph_info[uid]['follows'] if i in uids_in_graph]
        for i in follows_in_graph:
            g.add_edge(uid, i, color='blue')

    # Get label info
    node_labels = nx.get_node_attributes(g, 'handle')

    # Plot
    plt.figure(figsize=(10, 10))

    pos = nx.spring_layout(g)
    nx.draw(g, pos, arrows=True)
    nx.draw_networkx_labels(g, pos, labels=node_labels)

    plt.show()


def main():
    global DEBUG
    DEBUG = False

    object_location = 'twitter_objects'
    nodes_to_plot = 100

    user_dict = readobject('user_dict', dir_flag=False, alt_dir=object_location)

    if DEBUG:
        nodes_to_plot = 10
        graph_info = create_test_object(user_dict, size=nodes_to_plot)
        user_dict = {k: user_dict[k] for k in graph_info.keys()}
    else:
        graph_info = readobject('ds_community', dir_flag=False, alt_dir=object_location)

    graph_construction(graph_info, user_dict, size=nodes_to_plot)


if __name__ == "__main__":
    main()