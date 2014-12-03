"""
Create a database of twitter connections to map relationships in the data science community
"""

__author__ = 'Aaron'

import twitter
import cPickle as pickle
import os
from time import sleep
from datetime import datetime

from config import *


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
    api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_TOKEN_KEY,
                      access_token_secret=ACCESS_TOKEN_SECRET)
    return api


def get_depth_stats(depth_target):
    try:
        ds = readobject("depth_stats")
        ds['target'] = depth_target
        return ds
    except IOError:
        return {'current': 0,
                'target': depth_target}


def get_to_crawl(api):
    try:
        return readobject("to_crawl")
    except IOError:
        # Get community kernel
        scientists = data_scientist_names()

        # Get user_ids for community kernel
        return provide_user_seeds(scientists, api)


def get_next_level_crawl():
    try:
        return readobject("next_level_crawl")
    except IOError:
        return []


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


def crawl_ds_community(depth_target, api):
        # Load or initialize depth_stats
        depth_stats = get_depth_stats(depth_target)

        # Load or initialize to_crawl list
        to_crawl = get_to_crawl(api)

        # Load or initialize next_level_crawl
        next_level_crawl = get_next_level_crawl()

        # Load or initialize dictionary of user information
        user_dict = get_user_dict()

        # Load or initialize ds_community link dictionary
        ds_community = get_ds_community()

        # Load or initialize list of user ids that cause errors
        id_errors = get_id_errors()

        # Crawl ....
        while depth_stats['current'] <= depth_stats['target']:
            saveobject(depth_stats, "depth_stats")
            crawl_specified_depth(to_crawl, next_level_crawl,
                                  ds_community,
                                  user_dict,
                                  id_errors,
                                  api)
            depth_stats['current'] += 1
            to_crawl = next_level_crawl
            next_level_crawl = []
            depth_stats[depth_stats['current']] = to_crawl

        saveobject(ds_community, "ds_community")
        saveobject(user_dict, "user_dict")
        saveobject(to_crawl, "to_crawl")
        saveobject(id_errors, "id_errors")
        saveobject(depth_stats, "depth_stats")


def crawl_specified_depth(to_crawl, next_level_crawl,
                          ds_community,
                          user_dict,
                          id_errors,
                          api):

    counter = 0
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
                if (type(error_text.message[0]) is dict and
                        'message' in error_text.message[0].keys() and
                        error_text.message[0]['message'] == 'Rate limit exceeded'):
                    # Exceeded limits (15/15 minutes):
                    # Add user_id back onto to_crawl and wait
                    to_crawl.append(user_id)
                    print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print "counter = {0}".format(counter)
                    print 'Rate limit exceeded. Sleep 5'
                    sleep(60*5)     # seconds to pause
                else:
                    id_errors.append(user_id)
            else:
                add_to_user_dictionary(user_id, user_dict, user)
                add_to_ds_community(user_id, ds_community, follows)
                next_level_crawl.extend(follows)

        if counter % 15 == 0:
            # Heartbeat: feedback to show things are progressing
            print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print "counter = {0}".format(counter)
            saveobject(ds_community, "ds_community")
            saveobject(user_dict, "user_dict")
            saveobject(to_crawl, "to_crawl")
            saveobject(next_level_crawl, "next_level_crawl")
            saveobject(id_errors, "id_errors")
            print 'files saved'

        counter += 1


def main():
    # Set Depth Target
    depth_target = 3

    # Authenticate
    api = authenticate()

    # Crawl twitter for structure
    crawl_ds_community(depth_target, api)


if __name__ == "__main__":
    main()