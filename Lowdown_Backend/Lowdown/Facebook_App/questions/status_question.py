from fake_data import FAKE_STATUSES
from questions import MultipleChoiceQuestion
from utils import get_paged_data

class StatusQuestion(MultipleChoiceQuestion):
    QUESTION_TEXT = "Which of the following is NOT one of %s's statuses?"

    @classmethod
    def gen(cls, self_data, friend_data):
        statuses = [status['message']
                    for status in get_paged_data(friend_data, 'statuses')]
        return cls(statuses, FAKE_STATUSES)
