import logging

from questions import MultipleChoiceQuestion
from utils import get_paged_data

logger = logging.getLogger(__name__)

def get_context_data(user_data, field_name):
    return user_data[field_name]['mutual_friends']['data']

class MutualFriendsQuestion(MultipleChoiceQuestion):
    QUESTION_TEXT = \
            "Of the following, which is not a mutual friend of you and %s?"

    def __init__(self, mutual_friends, only_my_friends):
        super(MutualFriendsQuestion, self) \
               .__init__(mutual_friends, only_my_friends)

    @classmethod
    def gen(cls, self_data, friend_data):
        mutual_friends = [context for context in
                          get_paged_data(friend_data['context'],
                                         'mutual_friends')]
        non_mutual_friends = [friends for friends in
                              get_paged_data(friend_data, 'friends')]

        #TODO: Get more users so this quetsion becomes feasible.

        return cls(mutual_friends, non_mutual_friends)
