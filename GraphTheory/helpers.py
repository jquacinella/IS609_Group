"""
Various Utilities
"""

import os
import cPickle as pickle


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


def readobject(filename, dir_flag=True, alt_dir=''):
    """
    Shortcut to read file

    Input:
    filename: name of file to be loaded
    dir_flag: If True (default) looks for filename in a directory
        with name <basename>_objects (e.g. readobject called from
        sandbox.py will look for file in directory sandbox_objects
    alt_dir: Alternative path to file. Default is working directory
    """
    # import cPickle as pickle
    if dir_flag:
        target_dir = os.path.basename(__file__).split('.')[0] + '_objects'
    else:
        target_dir = alt_dir
    filename = os.path.join(target_dir, filename)
    with open(filename, 'rb') as input_file:
        return pickle.load(input_file)