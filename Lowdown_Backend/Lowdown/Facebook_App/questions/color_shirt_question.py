import logging
import random
import requests
from time import time
import threading

from PIL import Image
from StringIO import StringIO

import point_cluster
from questions import MultipleChoiceQuestion
from utils import get_paged_data

NUM_PICTURES = 10
PARALLEL = True

logger = logging.getLogger(__name__)

def get_shirt_color(photo, tag_coords):
    x, y = tag_coords
    PERCENT_OFFSET_Y = 15

    img = photo.convert('RGB', palette=Image.ADAPTIVE, colors=256)
    rows, cols = img.size
    x = (x / 100) * cols
    y = ((y+PERCENT_OFFSET_Y) / 100) * rows

    return img.getpixel((y, x))

def get_photo_arr_with_tags(photos, friend_id):
    """Returns a photo url appropriate for the quiz window size."""
    photo_arr = [] #Url, tags

    for photo in photos:
        photo_url = ""
        found = False
        for img in photo['images']:
            if not found and img['height'] < 300:
                photo_url = img['source']
                found = True

        photo_tag = None
        found = False
        for tag in photo['tags']['data']:
            if not found and 'id' in tag and tag['id'] == friend_id:
                found = True
                photo_tag = (tag['x'], tag['y'])

        photo_arr.append((photo_url, photo_tag))
    return photo_arr


def _make_request(url, tag_coords, results):
    response = requests.get(url)
    img = Image.open(StringIO(response.content))
    results.append((img, tag_coords))

def get_photos_threaded(photos):
    threads = []
    results = []
    for photo_url, tag_coords in photos:
        if not tag_coords:
            continue
        threads.append(threading.Thread(
            target=_make_request, args=(photo_url, tag_coords, results,)))

    for thread in threads:
        if PARALLEL:
            thread.start()
        else:
            thread.run()
    if PARALLEL:
        for thread in threads:
            thread.join()
    return results

class ColorShirtQuestion(MultipleChoiceQuestion):
    QUESTION_TEXT = \
            "Of these colors, which color shirt is %s most likely to wear?"
    TEMPLATE_NAME = 'color_shirt.html'
    def __init__(self, caption, other_captions):
        super(ColorShirtQuestion, self).__init__([caption], other_captions)

    @classmethod
    def gen(cls, self_data, friend_data):
        time_start = time()
        photos = get_paged_data(friend_data, 'photos')
        photos = get_photo_arr_with_tags(photos, friend_data['id'])

        random.shuffle(photos)
        length = min(len(photos), NUM_PICTURES)
        photo_arr = []

        #Pull down photos
        if PARALLEL:
            photo_arr = get_photos_threaded(photos[:length])
        else:
            session = requests.Session()
            for photo_url, tag_coords in photos[:length]:
                if not tag_coords:
                    continue
                response = session.get(photo_url)
                img = Image.open(StringIO(response.content))
                photo_arr.append((img, tag_coords))

        #Grab colors
        color_arr = []
        for photo, tag_coords in photo_arr:
            color = get_shirt_color(photo, tag_coords)
            if color:
                color_arr.append(color)

        colors, score = point_cluster.cluster(color_arr)
        correct_answer = colors[score.index(max(score))]
        colors.remove(correct_answer)
        incorrect_answers = colors

        logger.debug("TIME: Pictures fetch: %sms",
                round(1000 * (time() - time_start)))
        return cls(
            correct_answer,
            incorrect_answers,
        )
