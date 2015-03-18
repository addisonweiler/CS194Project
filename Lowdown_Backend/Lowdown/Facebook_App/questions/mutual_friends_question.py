import logging

from questions import MultipleChoiceQuestion
from utils import get_paged_data

logger = logging.getLogger(__name__)

def get_context_data(user_data, field_name):
    return user_data[field_name]['mutual_friends']['data']

class MutualFriendsQuestion(MultipleChoiceQuestion):
    QUESTION_TEXT = \
            "Of the following, which is not a mutual friend of you and %s?"

    @classmethod
    def gen(cls, self_data, friend_data):
        mutual_friends = [context['name'] for context in
                          get_context_data(friend_data, 'context')]
        non_mutual_friends = [friends['name'] for friends in
                              get_paged_data(self_data, 'friends')]
        results = []
        for friend in non_mutual_friends:
          if not friend in mutual_friends:
            results.append(friend)
        
        return cls(results, mutual_friends)
