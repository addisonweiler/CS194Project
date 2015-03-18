from collections import Counter
import re

from extreme_amount_question import HighestAmountQuestion
from stopwords import STOPWORDS
from utils import get_paged_data, get_captions

def get_word_count(phrases):
    count = Counter()
    for phrase in phrases:
        count += Counter([word.lower() for word in re.findall(r"[\w']+", phrase)
                      if word not in STOPWORDS and len(word) > 2])
    return count

class MostUsedWordQuestion(HighestAmountQuestion):
    QUESTION_TEXT = "Out of the following, what is %s's most used word?"

    @classmethod
    def gen(cls, self_data, friend_data):
        phrases = [status['message']
            for status in get_paged_data(friend_data, 'statuses')]
        phrases.extend(get_captions(get_paged_data(friend_data, 'photos')))
        # We deduplicate phrases because an album of pictures can produce
        # hundreds of the same exact caption.
        word_count = get_word_count(set(phrases))
        del word_count[friend_data['first_name'].lower()]
        return cls(word_count)
