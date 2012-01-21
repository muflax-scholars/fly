# Copyright (c) 2011 Pragma Nolint.
# See LICENSE.txt for details.

"""Choose words from plover's dict, based on difficulty level."""

import random

from fly.models.wordchooser import interface
from fly.utils import dictionaryreader as dictread
from fly.utils import files as fileutils


class RetrieveFromLevelDictionaries(interface.WordChooserInterface):

    """
    Six dictionaries have been generated (see data/generation/
    leveldictextraction.py) which have varying levels of difficulty in
    terms of number of keys to press simultaneously. The level the user
    is at, which depends on user's speed and accuracy, determines which
    dictionary the word to type is randomly drawn from.
    """

    dictionary_filename_1 = fileutils.get_level_dict_path(1)
    dictionary_filename_2 = fileutils.get_level_dict_path(2)
    dictionary_filename_3 = fileutils.get_level_dict_path(3)
    dictionary_filename_4 = fileutils.get_level_dict_path(4)
    dictionary_filename_5 = fileutils.get_level_dict_path(5)
    dictionary_filename_6 = fileutils.get_level_dict_path(6)

    def __init__(self):
        self.dictionary_1 = dictread.load_dict(self.dictionary_filename_1)
        self.dictionary_2 = dictread.load_dict(self.dictionary_filename_2)
        self.dictionary_3 = dictread.load_dict(self.dictionary_filename_3)
        self.dictionary_4 = dictread.load_dict(self.dictionary_filename_4)
        self.dictionary_5 = dictread.load_dict(self.dictionary_filename_5)
        self.dictionary_6 = dictread.load_dict(self.dictionary_filename_6)

        self.previous_translation = ""

        # Start at lowest level
        self.dictionary = self.dictionary_1

    def get_word_and_translation(self, level):
        word = random.choice(self.dictionary.keys())
        translation = self.dictionary[word]
        return word, translation

    def set_level(self, level):
        self.dictionary = eval("self.dictionary_%s" % level)


