from questions import MultipleChoiceQuestion
from utils import get_paged_data, QuestionNotFeasibleException

def get_liked_and_unliked_statuses(self_data, friend_id):
    self_statuses_data = get_paged_data(self_data, 'statuses')
    status_data = dict()

    for status in self_statuses_data:
        if 'likes' in status:
            status_data[status['message']] = get_paged_data(status, 'likes')

    liked_statuses = set()
    unliked_statuses = set()

    for key, val in status_data.iteritems():
        for v in val:
            if v['id'] == friend_id:
                liked_statuses.add(key)
            else:
                unliked_statuses.add(key)

    return list(liked_statuses), list(unliked_statuses)

class LikedStatusQuestion(MultipleChoiceQuestion):
    QUESTION_TEXT = "Which of the following statuses you posted did %s like?"

    @classmethod
    def gen(cls, self_data, friend_data):
        liked_statuses, unliked_statuses = \
            get_liked_and_unliked_statuses(self_data, friend_data['id'])
        if len(liked_statuses) == 0 or len(unliked_statuses) == 0:
            raise QuestionNotFeasibleException()
        return cls(liked_statuses, unliked_statuses)
