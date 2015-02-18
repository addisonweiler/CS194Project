from collections import defaultdict
import operator
import re

from questions import MultipleChoiceQuestion
from stopwords import STOPWORDS
from utils import get_paged_data, get_captions

def get_word_count(statuses, captions):
    word_count = defaultdict(int)
    for s in statuses + captions:
        words = re.findall(r"[\w']+", s)
        for w in words:
            w = w.lower()
            if w in STOPWORDS or len(w) < 2: continue
            word_count[w] += 1
    return word_count

def get_words(words, exclude=None):
    return list(set(filter(lambda x: x is not None and x != exclude, words)))

class MostUsedWordQuestion(MultipleChoiceQuestion):
    QUESTION_TEXT = "What is %s's most used word?"
    def __init__(self, max_word, other_words):
        super(MostUsedWordQuestion, self).__init__(max_word, other_words)


    @classmethod
    def gen(cls, self_data, friend_data):
        statuses = [status['message']
            for status in get_paged_data(friend_data, 'statuses')]
        photos = get_paged_data(friend_data, 'photos')
        word_count = get_word_count(statuses, get_captions(photos))
        max_word = max(word_count.iteritems(), key=operator.itemgetter(1))[0]
        return cls(max_word, get_words(word_count.keys(), max_word))

