import random

from questions import PhotoMultipleChoiceQuestion
from utils import get_paged_data, get_captions, get_caption, get_sized_photo, QuestionNotFeasibleException

def get_captioned_photo(photos):
    for _ in range(100):
        photo = random.choice(photos)
        if get_caption(photo):
            return photo
    raise QuestionNotFeasibleException()

class PhotoCaptionQuestion(PhotoMultipleChoiceQuestion):
    QUESTION_TEXT = \
            'Which of the following is the caption for the above picture?'

    @classmethod
    def gen(cls, self_data, friend_data):
        photos = get_paged_data(friend_data, 'photos')
        photo = get_captioned_photo(photos)

        return cls(
            get_sized_photo(photo),
            [get_caption(photo)],
            get_captions(photos),
        )
