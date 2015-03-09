from collections import defaultdict, OrderedDict
import operator
import re
import random

from extreme_amount_question import HighestAmountQuestion
from stopwords import STOPWORDS
from utils import get_paged_data, get_captions

def get_word_count(phrases):
    word_count = defaultdict(int)
    for phrases in phrases:
        words = re.findall(r"[\w']+", phrases)
        for w in words:
            w = w.lower()
            if w in STOPWORDS or len(w) < 2: continue
            word_count[w] += 1
    return word_count

class MostUsedWordQuestion(HighestAmountQuestion):
    QUESTION_TEXT = "Out of the following, what is %s's most used word?"

    @classmethod
    def gen(cls, self_data, friend_data):
        words = [status['message']
            for status in get_paged_data(friend_data, 'statuses')]
        words.extend(get_captions(get_paged_data(friend_data, 'photos')))
        return cls(get_word_count(words))
