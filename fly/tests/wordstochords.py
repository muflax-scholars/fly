# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""Test translation of words to chords for generating lesson translations."""

# Hack so that all modules can be imported from Fly, 
# but this can be run just by calling it as a script.
import sys, os
sys.path.append(os.path.dirname(os.getcwd()))

import os
import unittest

from fly.translation import wordstochords
from fly.translation import ploverfacade
from fly.utils import files as fileutils


class WordsToChordsTest(unittest.TestCase):

    """Given an english word, can the wordstochords module translate?"""

    def setUp(self):

        """Create WordToChord translator."""

        plover_control = ploverfacade.PloverControl()
        plover_control.set_up_steno("dummy_callback")
        dictionary = plover_control.get_dictionary()
        self.translator = wordstochords.WordToChordTranslator(dictionary)

    def test_translate_simple(self):

        """Translate word 'simple'.""" 

        translation = self.translator.translate_word('simple')
        expected_translation = "S*EUPL"
        self.assertTrue(translation == expected_translation,
                        "actually %s" % translation)
    
    def test_translate_untranslatable(self):

        """Translate word that's not in dict to fingerspelled word.""" 

        # Pick a word that will never make the dictionary
        translation = self.translator.translate_word('asdfwnkdfesfqqe')
        expected = "A*/S*/TK*/TP*/W*/TPH*/K*/TK*/TP*/*E/S*/TP*/KW*/KW*/*E"
        self.assertTrue(translation == expected,
                        "actually %s" % translation)

    def test_word_with_apostrophe(self):

        """Translate a word containing an apostrophe."""

        translation = self.translator.translate_word("how's")
        expected = "HO*US"
        self.assertTrue(translation == expected,
                        "actually %s" % translation)

    def test_translate_from_file_apostrophe(self):
        
        """Check word in file with apostrophe translates correctly"""
        
        data_dir = fileutils.get_test_data_directory()
        apostrophe_file = os.path.join(data_dir, "test_apostrophe.les")
        chord_list = self.translator.translate_from_file(apostrophe_file)
        expected = ["HO*US"]
        self.assertTrue(chord_list == expected, 
                        "actually %s" % chord_list)

    def test_word_with_apostrophe_ess(self):

        """Test word with "'s" that doesn't appear in dict translates."""

        translation = self.translator.translate_word("maid's")
        expected = "PHAEUD/A*ES"
        self.assertTrue(translation == expected,
                        "actually %s" % translation)
        


if __name__ == '__main__':
    unittest.main()


