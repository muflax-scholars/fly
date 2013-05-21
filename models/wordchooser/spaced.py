# Copyright muflax <mail@muflax.com>, 2013

"""Retrieval of words based on spaced repetition."""

from collections import OrderedDict
import random

from fly.models.wordchooser import interface


class RetrieveSpaced(interface.WordChooserInterface):

    """Words are retrieved randomly from plover's dict."""

    def __init__(self, word_translation_dict, word_list):

        """
        @param word_translation_dict: dict mapping steno chord to 
        english translation for every
        chord in word_list
        @param word_list: list of steno words to present to user

        @type word_translation_dict: dict
        @type word_list: list
        """

        # parameters
        self.minimum_queue_size = 6
        self.initial_spacing    = 1.0
        self.spacing_factor     = 2.0
        self.max_spacing        = self.spacing_factor**5
        
        # put every (unique) word in the new word queue and store a spacing interval for them
        self.new_queue = list(OrderedDict.fromkeys(word_list))
        self.spacing   = {word: self.initial_spacing for word in word_translation_dict.keys()}

        # what words to display next
        self.queue     = []
        self.last_word = None
        self.was_wrong = False
        
        self.word_translation_dict = word_translation_dict

    def get_word_and_translation(self):
        # add new word to beginning of learning queue if it's small enough
        if len(self.queue) < self.minimum_queue_size:
            new_word = self.new_queue.pop(0)
            self.queue.insert(0, new_word)

        # remove word from learning queue
        word = self.queue.pop(0)
        translation = self.word_translation_dict[word]
        self.last_word = word
        self.was_wrong = True
        
        print self.queue
        
        return word, translation

    def on_right_word_entered(self):
        word = self.last_word
        
        # reinsert word into queue if necessary
        spacing = self.spacing[word] * self.spacing_factor
        if spacing < self.max_spacing:
            self.spacing[word] = spacing
            self.queue.insert(int(round(spacing)), word)

    def on_wrong_word_entered(self):
        word = self.last_word
        
        # reset spacing and reinsert word into queue
        if self.was_wrong == False:
            spacing = self.initial_spacing
            self.spacing[word] = spacing
            self.queue.insert(int(round(spacing)), word)
            self.was_wrong = True