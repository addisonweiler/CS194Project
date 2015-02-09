import random
import json

class Question(object):
    pass

class MultipleChoiceQuestion(Question):
    QUESTION_TEXT = "Must override this class and field"
    NUM_WRONG_ANSWERS = 3
    def __init__(self, correct_answer, wrong_answers):
        self.checked = -1
        self.correct_index = random.randint(0, self.NUM_WRONG_ANSWERS)
        self.questionArr = random.sample(wrong_answers, self.NUM_WRONG_ANSWERS)
        self.questionArr.insert(self.correct_index, correct_answer)

    def set_name(self, name):
        self.name = name

    def question_text(self):
        if "%s" in self.QUESTION_TEXT:
            return self.QUESTION_TEXT % self.name
        else:
            return self.QUESTION_TEXT    

class StatusQuestion(MultipleChoiceQuestion):
    QUESTION_TEXT = "Which of the following is NOT one of %s's statuses?"
    def __init__(self, statuses, self_statuses):
        wrong_status = random.choice(self_statuses)
        super(StatusQuestion, self).__init__(wrong_status, statuses)

class ImageCaptionQuestion(MultipleChoiceQuestion):
    QUESTION_TEXT = "Which of the following is the caption for the above picture?"
    def __init__(self, image, caption, other_captions):
        self.image = image
        super(ImageCaptionQuestion, self).__init__(caption, other_captions)

class LikedStatusQuestion(MultipleChoiceQuestion):
    QUESTION_TEXT = "Which of the following statuses did %s like?"
    def __init__(self, liked_statuses, other_statuses):
        liked_status = random.choice(liked_statuses)
        super(LikedStatusQuestion, self).__init__(liked_status, other_statuses)

class MostUsedWordQuestion(MultipleChoiceQuestion):
    QUESTION_TEXT = "What is %s's most used word?"
    def __init__(self, max_word, other_words):
        super(MostUsedWordQuestion, self).__init__(max_word, other_words)
