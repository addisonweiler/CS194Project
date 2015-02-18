from questions import MultipleChoiceQuestion
from utils import get_paged_data, get_captions, get_caption

import requests
from PIL import Image
from StringIO import StringIO
import random

import Point_Cluster

import logging
logger = logging.getLogger(__name__)

def get_shirt_color(photo_url, tag_coords):
    x, y = tag_coords

    PERCENT_OFFSET_Y = 15

    #Grab file from url, open it as a string
    response = requests.get(photo_url)
    img = Image.open(StringIO(response.content))
    img = img.convert('RGB', palette=Image.ADAPTIVE, colors=256)
    
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

class ColorShirtQuestion(MultipleChoiceQuestion): 
    QUESTION_TEXT = "Of these colors, which is %s most likely to wear?" 
    def __init__(self, caption, other_captions): 
        super(ColorShirtQuestion, self).__init__([caption], other_captions) 

    @classmethod
    def gen(cls, self_data, friend_data):
        photos = get_paged_data(friend_data, 'photos')
        photos = get_photo_arr_with_tags(photos, friend_data['id'])

        correctAnswer = "HI"
        photo_url = None

        random.shuffle(photos)
        color_arr = []
        for photo, tag_coords in photos[:100]:
            if not tag_coords: continue
            color = get_shirt_color(photo, tag_coords)
            color_arr.append(color)

        colors, score = Point_Cluster.cluster(color_arr)
        correctAnswer = colors[score.index(max(score))]
        colors.remove(correctAnswer)
        incorrectAnswers = colors

        return cls(
            correctAnswer,
            incorrectAnswers,
        )
