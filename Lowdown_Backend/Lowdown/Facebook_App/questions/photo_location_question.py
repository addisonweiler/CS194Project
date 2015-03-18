from math import sqrt
import random

from questions import PhotoMultipleChoiceQuestion
from utils import get_paged_data, get_sized_photo, QuestionNotFeasibleException

def get_geotagged_photo(photos):
    for _ in range(100):
        photo = random.choice(photos)
        if 'place' in photo:
            return photo
    raise QuestionNotFeasibleException()

def lat_diff(loc1, loc2):
    return float(loc1['latitude']) - float(loc2['latitude'])

def lon_diff(loc1, loc2):
    return float(loc1['longitude']) - float(loc2['longitude'])

def _distance_miles(loc1, loc2):
    return sqrt(lat_diff(loc1, loc2) ** 2 + lon_diff(loc1, loc2) ** 2) * 60.0

def distance_miles(photo1, photo2):
    return _distance_miles(
        photo1['place']['location'],
        photo2['place']['location']
    )

def get_unique_locations(photos):
    """Gets the names of all locations that are not within 60 miles of each
    other.

    IMPORTANT: later photo locations are the ones used in case of a conflict.
    This matters because if the true location of a displayed photo is part of
    the set of photos, it better be last, otherwise the right answer and a
    location within a mile could show up, which this function is trying to
    prevent.
    """
    locations = []
    for i in range(len(photos)):
        for j in range(i + 1, len(photos) + 1):
            if j == len(photos):
                locations.append(photos[i]['place']['name'])
            elif distance_miles(photos[i], photos[j]) < 10.0:
                # debug += [photos[i]['place']['name'] + photos[j]['place']['name'] + str(distance_miles(photos[i], photos[j]))]
                break
    return locations

class PhotoLocationQuestion(PhotoMultipleChoiceQuestion):
    QUESTION_TEXT = "Where was this picture taken?"

    @classmethod
    def gen(cls, self_data, friend_data):
        photos = get_paged_data(friend_data, 'photos')
        chosen_photo = get_geotagged_photo(photos)
        location = chosen_photo['place']['name']
        all_locations = get_unique_locations(
            [photo for photo in photos if 'place' in photo] + [chosen_photo]
        )
        return cls(get_sized_photo(chosen_photo), [location], all_locations)
