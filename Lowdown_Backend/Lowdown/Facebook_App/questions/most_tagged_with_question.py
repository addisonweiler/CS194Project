from datetime import datetime
from collections import defaultdict
from math import exp

from extreme_amount_question import HighestAmountQuestion
from utils import get_paged_data

def weight(photo):
    taken = datetime.strptime(photo['created_time'][:10], '%Y-%m-%d')
    days_elapsed = (datetime.now() - taken).days + 1
    if days_elapsed < 0:
        raise Exception('Picture is dated ahead of today')
    return int(10 * exp((-0.002) * days_elapsed))

class MostTaggedWithQuestion(HighestAmountQuestion):
    QUESTION_TEXT = \
            'Out of the following, who has %s been tagged most with recently?'

    @classmethod
    def gen(cls, self_data, friend_data):
        tags = defaultdict(int)
        for photo in get_paged_data(friend_data, 'photos'):
            for tag in get_paged_data(photo, 'tags'):
                if 'id' not in tag:
                    continue        # Ignore tags of non-fb objects
                tags[tag['name']] += weight(photo)
        del tags[friend_data['name']]
        return cls(tags)
