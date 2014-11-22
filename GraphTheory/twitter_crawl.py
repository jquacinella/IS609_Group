"""
Create a database of twitter connections to map relationships in the data science community
"""

__author__ = 'Aaron'

import twitter
import cPickle as pickle


def saveobject(obj, filename):
    """Shortcut to save file"""
    # import cPickle as pickle
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def readobject(filename):
    """Shortcut to read file"""
    # import cPickle as pickle
    with open(filename, 'rb') as input_file:
        return pickle.load(input_file)


def authenticate():
    # Twitter credentials
    # Connect to twitter API using custom Twitter APP and Oauth tokens from 'mrquintopolous'
    api = twitter.Api(consumer_key='AjU9aXjAVGnAStPSXcpKuL9fJ',
                      consumer_secret='JF2Xc6uNfAW0NroCBtqlT860V6pWWPVmm0MI9RmTuCR6jmMdr0',
                      access_token_key='16562593-NYrbJNK8w1cd5aujWhJUoTfGz6MR3Y5u7Xa1WdbCh',
                      access_token_secret='N5KPbswRrjWPFaOIkaFNmVGAWgHeg1bIZafJPXoBa29Rc')
    return api


def data_scientist_names():
    # Provide a seed list for the data science community
    # Not directly providing twitter ids in case we want
    # to look those up in the future

    # return ["Nate Silver",
    #         "Mike Bostock",
    #         "DJ Patil",
    #         "Hilary Mason",
    #         "Drew Conway",
    #         "Hadley Wickham"]

    # Start with this
    return ["Hilary Mason"]


def add_to_user_dictionary(kwargs, api, user_dict):
    # kwargs is a dictionary with the appropriate user identification
    try:
        user = api.GetUser(**kwargs)
        user_dict[user.id] = user
    except twitter.TwitterError:
        print "error getting user info"


def provide_user_seeds(names, api):
    # For now a simple lookup dictionary populated manually
    translator = {"Nate Silver": "FiveThirtyEight",
                  "Mike Bostock": "mbostock",
                  "DJ Patil": "dpatil",
                  "Hilary Mason": "hmason",
                  "Drew Conway": "drewconway",
                  "Hadley Wickham": "hadleywickham"}
    # TODO: add case checking. e.g. hilary matches HilArY
    return [api.GetUser(screen_name=translator[n]).id for n in names]


def get_user_dict():
    try:
        return readobject("user_dict")
    except IOError:
        return {}


def get_ds_community():
    try:
        return readobject("ds_community")
    except IOError:
        return {}


def crawl_ds_community(user_seeds, ds_community, user_dict, api):
    # TODO: keep track of IDs that cause errors and skip those
    # Produce a dictionary in the form {member_id: [list of friends ids]}

    # Initiate list to be crawled
    to_crawl = user_seeds

    counter = 0
    follower_errors = 0
    while len(to_crawl) > 0:
        user_id = to_crawl.pop()

        if user_id not in user_dict.keys():
            kw = {"user_id": user_id}
            add_to_user_dictionary(kw, api, user_dict)

        if user_id not in ds_community.keys():
            try:
                follows = api.GetFriendIDs(user_id=user_id)
                ds_community[user_id] = follows
                to_crawl = to_crawl + [id for id in follows if id not in ds_community.keys()]
            except twitter.TwitterError:
                follower_errors += 1
        else:
            follows = ds_community[user_id]
            to_crawl = to_crawl + [id for id in follows if id not in ds_community.keys()]

        if counter >= 100:
            saveobject(ds_community, "ds_community")
            saveobject(user_dict, "user_dict")
            print "there were {} errors in getting twitter followers".format(follower_errors)
            break

        counter += 1

    return ds_community, user_dict


def main():
    # Authenticate
    api = authenticate()

    # Get community kernel
    scientists = data_scientist_names()

    # Get user_ids for community kernel
    user_seeds = provide_user_seeds(scientists, api)

    # Load or initialize dictionary of user information
    user_dict = get_user_dict()

    # Load or initialize ds_community link dictionary
    ds_community = get_ds_community()

    # Crawl twitter for structure
    ds_community, user_dict = crawl_ds_community(user_seeds, ds_community, user_dict, api)

    print ds_community
    print user_dict

    saveobject(ds_community, "ds_community")
    saveobject(user_dict, "user_dict")


if __name__ == "__main__":
    main()