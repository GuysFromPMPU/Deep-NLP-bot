import datetime

from enum import Enum, auto
from calendar import monthrange

import pymorphy2

morph = pymorphy2.MorphAnalyzer()


class ChatStatus(Enum):
    Buying = auto()


class BuyStatus(Enum):
    Choosing = auto()
    Selected = auto()


def right_form_from_number(word, number):
    word = morph.parse(word)[0]
    return word.make_agree_with_number(number).word


def last_day_in_month(date):
    last_day = datetime.date(
        date.year, date.month, monthrange(date.year, date.month)[1]
    )
    return last_day
