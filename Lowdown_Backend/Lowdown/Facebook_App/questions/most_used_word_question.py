from collections import defaultdict, OrderedDict
import operator
import re
import random

from questions import MultipleChoiceQuestion
from stopwords import STOPWORDS
from utils import get_paged_data, get_captions

logger = logging.getLogger(__name__)

def get_word_count(statuses, captions):
    word_count = defaultdict(int)
    for s in statuses + captions:
        words = re.findall(r"[\w']+", s)
        for w in words:
            w = w.lower()
            if w in STOPWORDS or len(w) < 2: continue
            word_count[str(w)] += 1
    return word_count

def get_words(word_count, words, exclude=None):
    return list(set(filter(lambda x: x is not None 
        and x != exclude 
        and word_count[str(x)] < word_count[str(exclude)]
        and word_count[str(x)] != 1, words)))

def get_freq_word(word_count):
    ordered_list = sorted(word_count.items(), key=lambda t: t[1], reverse=True)
    top_10_words = ordered_list[0:10]
    return random.choice(top_10_words)[0]


class MostUsedWordQuestion(MultipleChoiceQuestion):
    QUESTION_TEXT = "Of of the following, what is %s's most used word?"
    def __init__(self, max_word, other_words):
        super(MostUsedWordQuestion, self).__init__([max_word], other_words)

    @classmethod
    def gen(cls, self_data, friend_data):
        statuses = [status['message']
            for status in get_paged_data(friend_data, 'statuses')]
        photos = get_paged_data(friend_data, 'photos')
        word_count = get_word_count(statuses, get_captions(photos))
        max_word = get_freq_word(word_count)
        
        return cls(max_word, get_words(word_count, word_count.keys(), max_word))

