from collections import Counter

from extreme_amount_question import HighestAmountQuestion
from utils import get_paged_data

class MostTaggedWithQuestion(HighestAmountQuestion):
    QUESTION_TEXT = "Out of the following, who has %s been tagged most with?"

    @classmethod
    def gen(cls, self_data, friend_data):
        tags = []
        for photo in get_paged_data(friend_data, 'photos'):
            tags.extend([tag['name'] for tag in get_paged_data(photo, 'tags')])
        return cls(Counter(tags))
