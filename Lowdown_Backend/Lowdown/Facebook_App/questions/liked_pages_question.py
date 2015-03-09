from fake_data import FAKE_LIKES
from questions import MultipleChoiceQuestion
from utils import get_paged_data

class LikedPagesQuestion(MultipleChoiceQuestion):
    QUESTION_TEXT = "What is not one of %s's likes?"

    @classmethod
    def gen(cls, self_data, friend_data):
        likes = [like['name'] for like in get_paged_data(friend_data, 'likes')]
        fake_likes = [fake_like for fake_like in FAKE_LIKES
                          if fake_like not in likes]
        return cls(likes, fake_likes)
