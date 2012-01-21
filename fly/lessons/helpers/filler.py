# Copyright (c) 2011 Pragma Nolint.
# See LICENSE.txt for details.

"""Populates lesson object by reading lesson files and interpreting data."""

import re
import logging
logger = logging.getLogger(__name__)

from fly.translation import wordstochords


class LessonFiller(object):

    """Reads lesson and chords file and populates lesson with information."""

    def __init__(self, dictionary=None):

        """If a dictionary is provided, chords will be compressed.

        An attempt will be made to provide only the minimum number of chords
        that are required to type a word. For example, "he is" can be typed "E"
        then "S" or "E/S", where the latter is compressed. This fixes a bug in 
        sentence mode.

        @param dictionary: plover keystroke to translation dict
        @type dictionary: dict
        """

        self.compressor = None
        if dictionary:
            self.compressor = ChordCompressor(dictionary)

    def populate_lesson(self, lesson):

        """Read the files belonging to the lesson to populate the lesson.

        @param lesson: lesson object to populate.
        @type lesson: L{lessons.container.Lesson}
        """

        # Read lesson and chords file to get lists of content, store on lesson
        translation_sentence_list = self.get_sentences_list(lesson.file_path)
        lesson.sentences_list = translation_sentence_list

        chord_sentence_list = self.get_sentences_list(lesson.chords_file_path)
        lesson.chord_sentences_list = chord_sentence_list

        chords_list = self.get_chords_list(lesson)

        # Generate a translation list, which has punctuation split out as well,
        # and a map so we know which sentence each chord belongs to.
        lesson.translation_list, lesson.sentence_map, lesson.chords_list =\
            self.generate_translation_for_sentences(translation_sentence_list, 
                                                    chords_list)

        # Regenerate chord sentence list based on chords list, if this has 
        # changed.
        if chords_list != lesson.chords_list:
            lesson.chord_sentences_list = \
                    self.regenerate_chord_sentences(lesson.sentence_map, 
                                                    lesson.chords_list)

        # For convenience, map from chord to translation.
        lesson.chord_translation_dict = self.get_translation_dict(lesson)

    def regenerate_chord_sentences(self, sentence_map, chords_list):

        """Recreate list of chord sentences after chord list change.

        @param sentence_map: dict mapping sentences to words in sentence.
                             {index of sentence: [indices of words in sentence
                             out of total words0]}
        @param chords_list: list of chords to type

        @type sentence_map: dict of {int: list of int} 
        @type chords_list: list of str

        @return: list of steno sentences
        @rtype: list of str
        """

        chord_sentences = []
        for index, index_list in sentence_map.iteritems():
            chords = []
            for ind in index_list:
                if ind < len(chords_list):
                    chords.append(chords_list[ind])
            chord_sentences.append(' '.join(chords))
        return chord_sentences

    @staticmethod
    def get_chords_list(lesson):

        """Get a list of chords from the chords file.

        @param lesson: lesson object which knows about chord file path
        @type lesson: L{lessons.container.Lesson}

        @return: list of chords
        @rtype: list of str
        """
        
        with open(lesson.chords_file_path) as f:
            chords_list = f.read().split()
            chords_list = [s.strip() for s in chords_list]

        return chords_list

    @staticmethod
    def get_sentences_list(file_path):
        
        """Get a list of sentences from the file.

        For example, might return something like ["roses are red", "violets 
        are blue"]

        @param filePath: path to file containing sentences
        @type filePath: str

        @return: list of sentences
        @rtype: list of str
        """

        sentence_list = []

        with open(file_path) as f:
            split_list = f.read().split('\n')

        for line in split_list:
            if line.find("<") != -1 or line.find(">") != -1:
                continue
            if line == "":
                continue

            sentence_list.append(line)
        return sentence_list

    def generate_translation_for_sentences(self, 
                                           translation_sentence_list, 
                                           chords_list):

        """Generate a list of chords and a map from sentence to chord.

        Chords list is potentially modified based on translation (some chords
        may be compressed if possible). 

        @param translation_sentence_list: list of sentences
        @param chords_list: list of chords

        @type translation_sentence_list: list of str
        @type chords_list: list of str

        @return: tuple (list of word translations, dict of sentence
                 number to list of indices in translation list which correspond
                 to sentence, list of chords)

        @rtype: tuple (list of str, dict of int: list of int., list of str)
        """

        final_translations_list = []
        sentence_map = {}
        total_word_count = 0
        i = 0
        new_chords_list = chords_list

        for sentence in translation_sentence_list:
            word_count = 0
            translation_list = self.get_translations_from_sentence(sentence)

            for word in translation_list:
                split_words = re.split("([-.,?!:;\"])", word)
                words_and_punctuation = [w for w in split_words if w is not ""]
                final_translations_list.extend(words_and_punctuation)
                word_count += len(words_and_punctuation)
                total_word_count += len(words_and_punctuation)

            if word_count == 0:
                continue

            word_indices = self.generate_word_indices(word_count, 
                                                      total_word_count)
            sentence_map[i] = word_indices
            i += 1
       
        if self.compressor is not None:
            new_chords_list, final_translations_list, new_sentence_map = \
                    self.compressor.compress_chords(chords_list, 
                                                    final_translations_list, 
                                                    sentence_map)
        else:
            new_chords_list = chords_list
            new_sentence_map = sentence_map

        return final_translations_list, new_sentence_map, new_chords_list

    @staticmethod
    def get_translations_from_sentence(sentence):

        """Split sentence into words and reject directives.

        @param sentence: translated sentence to split
        @type sentence: str

        @return: list of words in sentence, with punctuation still attached.
        @rtype: list of str
        """

        translation_list = sentence.split()
        valid_translation_list = []
        for t in translation_list:
            # Directives are not allowed
            if t.find("<") != -1 or t.find(">") != -1:
                continue

            t = t.lower().strip()
            valid_translation_list.append(t)

        return valid_translation_list

    @staticmethod
    def generate_word_indices(word_count, total_word_count):

        """Generate indices for word_count words up to total_word_count.

        @param word_count: number of words to generate indices for
        @param total_word_count: number of words seen so far including 
                                 words in word_count.

        @type word_count: int
        @type total_word_count: int

        @return: list of word indices
        @rtype: list of int
        """

        end = total_word_count - 1
        start = total_word_count - word_count
        index = start
        word_indices = []
        while index <= end:
            word_indices.append(index)
            index += 1

        return word_indices

    @staticmethod
    def get_translation_dict(lesson):

        """Create a dict of chord: translation for lesson data.

        @param lesson: lesson object
        @type lesson: L{lessons.container.Lesson}

        @return: dict of chord: translation
        @rtype: dict of str: str 
        """

        word_getter = wordstochords.WordToChordTranslator.yield_word
        translation_list = []
        
        with open(lesson.file_path) as f:
            data = f.readlines()
            for line in data:
                for word in word_getter(line):
                    translation_list.append(word)

        chord_translation_dict = {}
        for chord, translation in zip(lesson.chords_list, translation_list):
            chord_translation_dict[chord] = translation
        return chord_translation_dict


class ChordCompressor(object):

    """Makes multiple chords into single chord if possible.

    This class was created to fix a bug in sentence mode where words such as
    'he is' would have chords E S, but also in dictionary correspond to E/S, 
    meaning the translation would be (in Fly) 'he he is'. This solves the 
    problem for lessons where words are in order, but the problem remains in 
    any mode where it's not known what the next chord will be and thus not 
    possible to compress. Tricky!
    """

    def __init__(self, dictionary):

        """
        @param dictionary: plover keystroke to translation dict
        @type dictionary: dict
        """

        self.dictionary = dictionary

    def compress_chords(self, chords_list, translation_list, sentence_map):

        """For chords in chords list, attempt to compress.

        @param chords_list: list of chords to type
        @param translation_list: list of words in sentence
        @param sentence_map: dict mapping sentences to words in sentence.
                             {index of sentence: [indices of words in sentence
                             out of total words0]}

        @type chords_list: list of str
        @type sentence_map: dict of {int: list of int} 
        @type translation_list: list of str
        """

        if not len(chords_list) == len(translation_list):
            logger.error("Expected length of steno words list to equal "
                         "length of translation list. That it doesn't "
                         "indicates a bug.")

        new_chords_list = chords_list
        new_translation_list = translation_list

        # Keep compressing until there's no more to be done
        latest_chords_list, latest_translation_list, new_sentence_map = \
            self.__compress(chords_list, translation_list, sentence_map)

        while new_chords_list != latest_chords_list and \
             new_translation_list != latest_translation_list:
              
             new_translation_list = latest_translation_list
             new_chords_list = latest_chords_list

             latest_chords_list, latest_translation_list, new_sentence_map = \
                 self.__compress(new_chords_list, 
                                 new_translation_list, 
                                 sentence_map)

        return new_chords_list, new_translation_list, new_sentence_map

    def __compress(self, chords_list, translation_list, sentence_map):
        
        """Do a single compress run.

        @param chords_list: list of chords to type
        @param translation_list: list of words in sentence
        @param sentence_map: dict mapping sentences to words in sentence.
                             {index of sentence: [indices of words in sentence
                             out of total words0]}

        @type chords_list: list of str
        @type sentence_map: dict of {int: list of int} 
        @type translation_list: list of str
        """

        new_chords_list = []
        new_translation_list = []
        new_sentence_map = sentence_map

        i = 0
        total_word_count = 0
        already_added = False

        for chord, translation in zip(chords_list, translation_list):
            chord_on_boundary = self.is_chord_on_boundary(sentence_map, i)
            i += 1
            total_word_count += 1
            
            if already_added:
                already_added = False
                continue

            if i >= len(chords_list):
                # end of list
                new_chords_list.append(chord)
                new_translation_list.append(translation)
                break

            second_chord = chords_list[i]
            compressed_chord = '%s/%s' % (chord, second_chord)

            if compressed_chord not in self.dictionary:
                compressed_chord = '%s%s' % (chord, second_chord)

            if compressed_chord not in self.dictionary:
                new_chords_list.append(chord)
                new_translation_list.append(translation)
                continue

            dict_translation = self.dictionary[compressed_chord]
            proposed_trans = ' '.join([translation, translation_list[i]])
            if proposed_trans.lower() == dict_translation.lower():
                if chord_on_boundary:
                    raise RuntimeError("Cannot compress word across "
                                       "sentence boundaries. Please alter "
                                       "lesson file so that \"%s\" "
                                       "and \"%s\" are on same line." % \
                                       (translation, translation_list[i]))
                new_chords_list.append(compressed_chord)
                new_translation_list.append(proposed_trans)
                new_sentence_map = \
                        self.generate_new_sentence_map(sentence_map,
                                                       total_word_count)
                already_added = True
            else:
                new_chords_list.append(chord)
                new_translation_list.append(translation)

        return new_chords_list, new_translation_list, new_sentence_map

    def is_chord_on_boundary(self, sentence_map, index):

        """Determine whether the chord is at the end of a sentence.
        If it is, it can't be compressed with the next chord. 

        @param sentence_map: dict mapping sentences to words in sentence.
                             {index of sentence: [indices of words in sentence
                             out of total words0]}
        @param index: int indicating where in the total list of words the word
                      is placed.

        
        @type sentence_map: dict of {int: list of int} 
        @type index: int

        @return: whether the chord is at the end of a sentence
        @rtype: bool
        """

        for sentence_number, index_list in sentence_map.iteritems():
            if not index in index_list:
                continue
            if index == index_list[-1]:
                return True
        return False

    def generate_new_sentence_map(self, sentence_map, total_word_count):

        """If the chord list has changed, update the sentence map.

        @param sentence_map: dict mapping sentences to words in sentence.
                             {index of sentence: [indices of words in sentence
                             out of total words0]}
        @param total_word_count: word we're up to in the list of all words
       
        @type sentence_map: dict of {int: list of int} 
        @type total_word_count: int
        
        @rtype: dict of {int: list of int} 
        """

        new_sentence_map = sentence_map
        for index, index_list in enumerate(new_sentence_map.values()):
            if total_word_count - 1 in index_list:
                sentence_ind = index

        for key, index_list in new_sentence_map.iteritems():
            if key == sentence_ind:
                index_list.pop()
            if key > sentence_ind:
                new_sentence_map[key] = [n - 1 for n in sentence_map[key]]

        return new_sentence_map


