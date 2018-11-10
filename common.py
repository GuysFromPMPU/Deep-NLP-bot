from enum import Enum, auto

import pymorphy2

morph = pymorphy2.MorphAnalyzer()

class ChatStatus(Enum):
    Buying = auto(),
    FAQ = auto()


def right_form_from_number(word, number):
    word = morph.parse(word)[0]
    return word.make_agree_with_number(number).word