"""
Create a database of twitter connections to map relationships in the data science community
"""

__author__ = 'Aaron'

import twitter
import cPickle as pickle
import os
from time import sleep


def saveobject(obj, filename):
    """Shortcut to save file"""
    # import cPickle as pickle
    # Save in object directory
    target_dir = os.path.basename(__file__).split('.')[0] + '_objects'
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    filename = os.path.join(target_dir, filename)
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def readobject(filename):
    """Shortcut to read file"""
    # import cPickle as pickle
    target_dir = os.path.basename(__file__).split('.')[0] + '_objects'
    filename = os.path.join(target_dir, filename)
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


def get_to_crawl(api):
    try:
        return readobject("to_crawl")
    except IOError:
        # Get community kernel
        scientists = data_scientist_names()

        # Get user_ids for community kernel
        return provide_user_seeds(scientists, api)


def data_scientist_names():
    # Provide a seed list for the data science community
    # Not directly providing twitter ids in case we want
    # to look those up in the future

    return ["Nate Silver",
            "Mike Bostock",
            "DJ Patil",
            "Hilary Mason",
            "Drew Conway",
            "Hadley Wickham"]


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


def add_to_user_dictionary(user_id, user_dict, user):
    if user_id in user_dict.keys():
        user_dict[user_id]['count'] += 1
    else:
        user_dict[user_id] = {
            'count': 1,
            'twit_ob': user
        }


def add_to_ds_community(user_id, ds_community, follows):
    if user_id in ds_community.keys():
        ds_community[user_id]['count'] += 1
    else:
        ds_community[user_id] = {
            'count': 1,
            'follows': follows
        }


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


def get_id_errors():
    try:
        return readobject("id_errors")
    except IOError:
        return []


def extend_to_crawl(to_crawl, user_id, ds_community):
    to_crawl.extend(
        [uid for uid in ds_community[user_id]['follows'] if uid not in ds_community.keys()]
    )


def crawl_ds_community(to_crawl, ds_community, user_dict, id_errors, api):

    counter = 0
    twitter_errors = 0
    while len(to_crawl) > 0:
        user_id = to_crawl.pop()

        if user_id not in id_errors:
            try:
                if user_id not in user_dict.keys():
                    user = api.GetUser(user_id=user_id)
                else:
                    user = user_dict[user_id]['twit_ob']

                if user_id not in ds_community.keys():
                    follows = api.GetFriendIDs(user_id=user_id)
                else:
                    follows = ds_community[user_id]['follows']

            except twitter.TwitterError as error_text:
                if error_text[0][0]['code'] == 88:
                    # Exceeded limits (15/15 minutes):
                    # Add user_id back onto to_crawl and wait
                    to_crawl.append(user_id)
                    sleep(60*5)     # seconds to pause
                else:
                    id_errors.append(user_id)
                    twitter_errors += 1
            else:
                add_to_user_dictionary(user_id, user_dict, user)
                add_to_ds_community(user_id, ds_community, follows)
                extend_to_crawl(to_crawl, user_id, ds_community)

        if counter >= 5:
            print "there were {} errors in getting twitter followers".format(twitter_errors)
            print "there were {} more user ids in the to_crawl list".format(len(to_crawl))
            break

        counter += 1


def main():
    # Authenticate
    api = authenticate()

    # Load or initialize to_crawl list
    to_crawl = get_to_crawl(api)

    # Load or initialize dictionary of user information
    user_dict = get_user_dict()

    # Load or initialize ds_community link dictionary
    ds_community = get_ds_community()

    # Load or initialize list of user ids that cause errors
    id_errors = get_id_errors()

    # Crawl twitter for structure
    crawl_ds_community(to_crawl,
                       ds_community, user_dict,
                       id_errors,
                       api)

    saveobject(ds_community, "ds_community")
    saveobject(user_dict, "user_dict")
    saveobject(to_crawl, "to_crawl")


if __name__ == "__main__":
    main()