import random

from questions import MultipleChoiceQuestion
from utils import get_paged_data, get_captions, get_caption

def get_captioned_photo(photos):  
    while True: 
        photo = random.choice(photos) 
        if get_caption(photo): 
            return photo 
    return None 

def get_sized_photo(photo): 
    """Returns a photo url appropriate for the quiz window size.""" 
    for img in photo['images']: 
        if img['height'] < 400 and img['width'] < 600: 
            return img['source'] 
    return ''

class ImageCaptionQuestion(MultipleChoiceQuestion): 
    QUESTION_TEXT = "Which of the following is the caption for the above picture?" 
    def __init__(self, image, caption, other_captions): 
        self.image = image 
        super(ImageCaptionQuestion, self).__init__(caption, other_captions) 

    @classmethod
    def gen(cls, self_data, friend_data):
        photos = get_paged_data(friend_data, 'photos')
        photo = get_captioned_photo(photos)
        caption = get_caption(photo)

        return cls(
            get_sized_photo(photo),
            caption,
            get_captions(photos, caption),
        )
