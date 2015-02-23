import random

from questions import MultipleChoiceQuestion
from utils import get_paged_data, get_photo_comments, get_sized_photo, QuestionNotFeasibleException

def get_commented_photo(photos):  
    for _ in range(100):
        photo = random.choice(photos) 
        comments = get_photo_comments(photo)
        # We don't want photos with more than 4 comments because then they tend
        # to be conversational and perhaps unrelated to the picture.
        if comments and len(comments) <= 4:
            return photo 
    raise QuestionNotFeasibleException()

def get_all_comments(photos):
    all_comments = []
    for photo in photos:
        all_comments.extend(get_photo_comments(photo))
    return all_comments

class PhotoCommentQuestion(MultipleChoiceQuestion): 
    QUESTION_TEXT = "Which of the following is the correct comment for the " \
            + "above picture?"
    def __init__(self, image, comments, other_comments): 
        self.image = image 
        super(PhotoCommentQuestion, self).__init__(comments, other_comments) 

    @classmethod
    def gen(cls, self_data, friend_data):
        photos = get_paged_data(friend_data, 'photos')
        photo = get_commented_photo(photos)

        return cls(
            get_sized_photo(photo),
            get_photo_comments(photo),
            get_all_comments(photos),
        )
