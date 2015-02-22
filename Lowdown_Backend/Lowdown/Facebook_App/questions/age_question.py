import logging
from datetime import date, datetime
from questions import MultipleChoiceQuestion

logger = logging.getLogger(__name__)

class AgeQuestion(MultipleChoiceQuestion):
    QUESTION_TEXT = "How old is %s?"
    def __init__(self, age):
        fake_ages = [x for x in range(age - 3, age + 4) if x != age]
        super(AgeQuestion, self).__init__([age], fake_ages)

    @classmethod
    def gen(cls, self_data, friend_data):
        logger.warning(friend_data['birthday'])
        born = datetime.strptime(friend_data['birthday'], '%m/%d/%Y').date()
        today = date.today()
        return cls(today.year - born.year -
                   ((today.month, today.day) < (born.month, born.day)))
