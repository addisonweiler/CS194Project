import random

from questions import PhotoMultipleChoiceQuestion
from utils import get_paged_data, get_sized_photo, QuestionNotFeasibleException

def get_geotagged_photo(photos):
    for _ in range(100):
        photo = random.choice(photos)
        if 'place' in photo:
            return photo
    raise QuestionNotFeasibleException()

class PhotoLocationQuestion(PhotoMultipleChoiceQuestion):
    QUESTION_TEXT = "Where was this picture taken?"

    @classmethod
    def gen(cls, self_data, friend_data):
        photos = get_paged_data(friend_data, 'photos')
        all_locations = [photo['place']['name'] for photo in photos
                            if 'place' in photo]
        photo = get_geotagged_photo(photos)
        location = photo['place']['name']
        # TODO: eliminate locations within 15 miles of the photo location.
        return cls(get_sized_photo(photo), [location], all_locations)
