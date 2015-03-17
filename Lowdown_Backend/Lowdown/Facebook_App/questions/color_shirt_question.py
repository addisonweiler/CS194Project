import random
import requests
import threading
import logging
from PIL import Image, ImageDraw, ImageStat
from StringIO import StringIO
import point_cluster
import math
from questions import MultipleChoiceQuestion
from utils import QuestionNotFeasibleException, get_paged_data
from time import time

logger = logging.getLogger(__name__)

NUM_PICTURES = 100
RECT_RAD = 2
CROSS_RAD = 5.0
PERCENT_DIFFERENCE_THRESHOLD = 10

def get_photo_arr_with_tags(photos, friend_id):
    """Returns a photo url appropriate for the quiz window size."""
    photo_arr = [] #Url, tags

    for photo in photos:
        photo_url = ""
        found = False
        for img in photo['images']:
            if not found and img['height'] < 400:
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

def checkPercentDifference(pointA, pointB):
    for i in range(len(pointA)):
        coordA = pointA[i]
        coordB = pointB[i]
        if coordA == 0: continue
        if abs((coordA - coordB) / coordA * 100) > PERCENT_DIFFERENCE_THRESHOLD: return True
    return False

def average(pointA, pointB):
    #Checks to make sure points are not too far off from one another
    if checkPercentDifference(pointA, pointB): return pointA
    X = (pointA[0] + pointB[0])/2.0
    Y = (pointA[1] + pointB[1])/2.0
    Z = (pointA[2] + pointB[2])/2.0
    return (int(X), int(Y), int(Z))

def get_color_avg(photo, tag_coords, percent_offset_x, percent_offset_y):
    x, y = tag_coords
    if x == 0 or y == 0: return None
    
    img = photo.convert('RGB', palette=Image.ADAPTIVE, colors=256)
    rows, cols = img.size

    x_row = int(((x + percent_offset_x) / 100) * rows)
    y_col = int(((y + percent_offset_y) / 100) * cols)
    
    lower_bound_row = int(max(0, x_row - RECT_RAD))
    upper_bound_row = int(min(x_row + RECT_RAD, rows))

    lower_bound_col = int(max(0, y_col - RECT_RAD))
    upper_bound_col = int(min(y_col + RECT_RAD, cols))

    #Gets color size within a rectangle bounds, specified by variable
    colorAvg = ()
    for i in range(lower_bound_row, upper_bound_row):
        for j in range(lower_bound_col, upper_bound_col):
            pixel = img.getpixel((i, j))
            if not colorAvg:
                colorAvg = pixel
            else:
                colorAvg = average(colorAvg, pixel)
    return colorAvg

def _make_request(url, tag_coords, results):
    response = requests.get(url)
    try:
        img = Image.open(StringIO(response.content))
        results.append((img, tag_coords))
    except:
        print url
    
def get_photos_threaded(photos):
    threads = []
    results = []
    for photo_url, tag_coords in photos:
        if not tag_coords:
            continue
        threads.append(threading.Thread(
            target=_make_request, args=(photo_url, tag_coords, results,)))

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return results


class ColorShirtQuestion(MultipleChoiceQuestion):
    QUESTION_TEXT = \
            'Of these colors, which color shirt is %s most likely to wear?'
    TEMPLATE_NAME = 'color_shirt.html'

    @classmethod
    def gen(cls, self_data, friend_data):
        time_start = time()
        photos = get_paged_data(friend_data, 'photos')
        photos = get_photo_arr_with_tags(photos, friend_data['id'])

        length = min(len(photos), NUM_PICTURES)

        #Pull down photos
        photo_arr = get_photos_threaded(photos[:length])
        photo_arr = sorted(photo_arr)

        #Grab skin color and shirt_color
        skin_color_arr = []
        shirt_color_arr = []
        
        for photo, tag_coords in photo_arr:  
            #Get Skin Color in a "Plus" Pattern  
            for n in range(-1, 2):  
                color = get_color_avg(photo, tag_coords, 0, float(n) * CROSS_RAD)
                if color: 
                    skin_color_arr.append(color)

            for n in range(-1, 2):  
                if n == 0: continue
                color = get_color_avg(photo, tag_coords, float(n) * CROSS_RAD, 0)
                if color:
                    skin_color_arr.append(color)

            #Get Shirt Color in a "Plus" Pattern
            Y_OFFSET_PERCENT = 20.0
            for n in range(-1, 2):  
                color = get_color_avg(photo, tag_coords, 0, Y_OFFSET_PERCENT + float(n) * CROSS_RAD)
                if color: shirt_color_arr.append(color)

            for n in range(-1, 2):
                if n == 0: continue
                color = get_color_avg(photo, tag_coords, float(n) * CROSS_RAD, Y_OFFSET_PERCENT)
                if color: shirt_color_arr.append(color)

        #Get average skin color of the person           
        skin_color, scores = point_cluster.cluster(skin_color_arr, 5)
        maxindex_skin = scores.index(max(scores))

        #Get average shirt colors, remove color that is closest to skin color
        shirt_color, scores = point_cluster.cluster(shirt_color_arr, 5)
        shirt_color, index = point_cluster.removeClosestColor(shirt_color, skin_color[maxindex_skin])
        
        scores = scores[:index] + scores[index+1 :] #Update score array w/removed color
        maxindex_shirt = scores.index(max(scores))

        #Get correct and incorrect answers
        correct_answer = shirt_color[maxindex_shirt]
        shirt_color.remove(correct_answer)
        incorrect_answers = shirt_color

        logger.debug("TIME: Pictures fetch: %sms",
                round(1000 * (time() - time_start)))
        return cls(
            [correct_answer],
            incorrect_answers,
        )









# import logging
# import random
# import requests
# from time import time
# import threading

# from PIL import Image
# from StringIO import StringIO

# import point_cluster
# from questions import MultipleChoiceQuestion
# from utils import get_paged_data

# NUM_PICTURES = 10
# PARALLEL = True

# logger = logging.getLogger(__name__)

# def get_shirt_color(photo, tag_coords):
#     x, y = tag_coords
#     PERCENT_OFFSET_Y = 15

#     img = photo.convert('RGB', palette=Image.ADAPTIVE, colors=256)
#     rows, cols = img.size
#     x = (x / 100) * cols
#     y = ((y+PERCENT_OFFSET_Y) / 100) * rows

#     return img.getpixel((y, x))

# def get_photo_arr_with_tags(photos, friend_id):
#     """Returns a photo url appropriate for the quiz window size."""
#     photo_arr = [] #Url, tags

#     for photo in photos:
#         photo_url = ""
#         found = False
#         for img in photo['images']:
#             if not found and img['height'] < 1200:
#                 photo_url = img['source']
#                 found = True

#         photo_tag = None
#         found = False
#         for tag in photo['tags']['data']:
#             if not found and 'id' in tag and tag['id'] == friend_id:
#                 found = True
#                 photo_tag = (tag['x'], tag['y'])

#         photo_arr.append((photo_url, photo_tag))
#     return photo_arr


# def _make_request(url, tag_coords, results):
#     response = requests.get(url)
#     img = Image.open(StringIO(response.content))
#     results.append((img, tag_coords))

# def get_photos_threaded(photos):
#     threads = []
#     results = []
#     for photo_url, tag_coords in photos:
#         if not tag_coords:
#             continue
#         threads.append(threading.Thread(
#             target=_make_request, args=(photo_url, tag_coords, results,)))

#     for thread in threads:
#         if PARALLEL:
#             thread.start()
#         else:
#             thread.run()
#     if PARALLEL:
#         for thread in threads:
#             thread.join()
#     return results

# class ColorShirtQuestion(MultipleChoiceQuestion):
#     QUESTION_TEXT = \
#             'Of these colors, which color shirt is %s most likely to wear?'
#     TEMPLATE_NAME = 'color_shirt.html'

#     @classmethod
#     def gen(cls, self_data, friend_data):
#         time_start = time()
#         photos = get_paged_data(friend_data, 'photos')
#         photos = get_photo_arr_with_tags(photos, friend_data['id'])

#         random.shuffle(photos)
#         length = min(len(photos), NUM_PICTURES)
#         photo_arr = []

#         #Pull down photos
#         if PARALLEL:
#             photo_arr = get_photos_threaded(photos[:length])
#         else:
#             session = requests.Session()
#             for photo_url, tag_coords in photos[:length]:
#                 if not tag_coords:
#                     continue
#                 response = session.get(photo_url)
#                 img = Image.open(StringIO(response.content))
#                 photo_arr.append((img, tag_coords))

#         #Grab colors
#         color_arr = []
#         for photo, tag_coords in photo_arr:
#             color = get_shirt_color(photo, tag_coords)
#             if color:
#                 color_arr.append(color)

#         colors, score = point_cluster.cluster(color_arr)
#         correct_answer = colors[score.index(max(score))]
#         colors.remove(correct_answer)
#         incorrect_answers = colors

#         logger.debug("TIME: Pictures fetch: %sms",
#                 round(1000 * (time() - time_start)))
#         return cls(
#             [correct_answer],
#             incorrect_answers,
#         )
