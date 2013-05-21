# Copyright (c) 2011 Pragma Nolint. 
# See LICENSE.txt for details.

"""
Fly runs with three models: Alphabet, Word, and Lesson. This
module configures the game model to create these models.
"""

from fly.models import gamemodel as game_model
from fly.models.wordchooser import randomize
from fly.models.inputinterpreter import word as input_word
from fly.data import alphabetdict as ad


LESSON_MODEL_NAME = "lesson"


def get_lesson_model(gui, lesson_control):

    """Create game model to use for lesson model.

    @return: model configured for lesson
    @rtype: L{game_model.GameModel)
    """

    lesson = gui.get_current_lesson_name()
    word_chooser = lesson_control.get_word_chooser(lesson)
    if word_chooser:
        lesson_word_chooser = word_chooser
    else:
        lesson_word_chooser = leveldicts.RetrieveFromLevelDictionaries()

    word_interpreter = input_word.InterpretForWord()

    lesson_model = game_model.GameModel(LESSON_MODEL_NAME,
                                        lesson_word_chooser,
                                        word_interpreter)
    return lesson_model
       

