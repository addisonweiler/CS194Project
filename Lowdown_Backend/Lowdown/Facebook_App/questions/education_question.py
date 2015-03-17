from datetime import date, datetime
from fake_data import FAKE_COLLEGES, FAKE_DEGREES, FAKE_HIGH_SCHOOLS
from questions import MultipleChoiceQuestion
from utils import QuestionNotFeasibleException

def _get_education(ed_data, school_type):
    for school in ed_data:
        if school['type'] == school_type:
            return school
    raise QuestionNotFeasibleException('No %s listed.' % school_type)

def get_high_school(ed_data):
    return _get_education(ed_data, 'High School')

def get_college(ed_data):
    return _get_education(ed_data, 'College')

def get_school_name(school):
    return school['school']['name']

class HighSchoolQuestion(MultipleChoiceQuestion):
    QUESTION_TEXT = 'Where did %s go to high school?'

    @classmethod
    def gen(cls, self_data, friend_data):
        return cls(
            [get_school_name(get_high_school(friend_data['education']))],
            FAKE_HIGH_SCHOOLS
        )

class CollegeQuestion(MultipleChoiceQuestion):
    QUESTION_TEXT = 'Where did %s go to college?'

    @classmethod
    def gen(cls, self_data, friend_data):
        return cls(
            [get_school_name(get_college(friend_data['education']))],
            FAKE_COLLEGES
        )

class DegreeQuestion(MultipleChoiceQuestion):
    QUESTION_TEXT = 'What degree did %s get at COLLEGE?'

    def __init__(self, college, degree):
        self.college = college
        return super(DegreeQuestion, self).__init__([degree], FAKE_DEGREES)

    @classmethod
    def gen(cls, self_data, friend_data):
        college = get_college(friend_data['education'])
        if 'concentration' not in college:
            raise QuestionNotFeasibleException('No degree listed')
        degrees = college['concentration']
        if len(degrees) == 1:
            degree = degrees[0]['name']
        elif len(degrees) == 2:
            degree = '%s and %s' % (degrees[0]['name'], degrees[1]['name'])
        else:
            raise QuestionNotFeasibleException('More than 2 degrees')
        
        return cls(get_school_name(college), degree)

    def question_text(self):
        return self.QUESTION_TEXT.replace('COLLEGE', self.college) \
                .replace('%s', self.name)
