from datetime import date, datetime
from questions import MultipleChoiceQuestion
from utils import QuestionNotFeasibleException

class AgeQuestion(MultipleChoiceQuestion):
    QUESTION_TEXT = "How old is %s?"

    @classmethod
    def gen(cls, self_data, friend_data):
        try:
            born = datetime.strptime(friend_data['birthday'], '%m/%d/%Y').date()
        except ValueError:
            raise QuestionNotFeasibleException('Birthday or year not provided.')
        today = date.today()
        age = (today.year - born.year -
               ((today.month, today.day) < (born.month, born.day)))
        fake_ages = [x for x in range(age - 3, age + 4) if x != age]
        return cls([age], fake_ages)
