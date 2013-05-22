# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Provides file path information about files in Fly."""

import os, os.path
from fly.plover import config as conf


def get_base_directory():
    """Get the main directory of the game."""
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def get_plover_dict_path():
    """Return the file path of the plover dictionary."""
    config = conf.get_config()
    dictionary_filename = config.get(conf.DICTIONARY_CONFIG_SECTION,
                                     conf.DICTIONARY_FILE_OPTION)
    return dictionary_filename


def get_lessons_directory():
    """Get the directory with the lesson files."""
    return os.path.join(get_base_directory(), 'data', 'lessons')


def get_test_data_directory():
    """Return the file path to the directory containing test data."""
    return os.path.join(get_base_directory(), 'tests', 'data')
