from datetime import date, datetime
from random import randint

from questions import MultipleChoiceQuestion

class BirthdayQuestion(MultipleChoiceQuestion):
    FORMAT = '%B %d'
    QUESTION_TEXT = "What is %s's birthday?"
    def __init__(self, birthday):
        fake_dates = [date.fromordinal(randint(1, 365) + 711750)
                          .strftime(self.FORMAT)
                      for _ in range(5)]
        birthday = birthday.strftime(self.FORMAT)
        super(BirthdayQuestion, self).__init__([birthday], fake_dates)

    @classmethod
    def gen(cls, self_data, friend_data):
        try:
            born = datetime.strptime(friend_data['birthday'], '%m/%d/%Y').date()
        except ValueError as e:
            born = datetime.strptime(friend_data['birthday'], '%m/%d').date()
        return cls(born)
