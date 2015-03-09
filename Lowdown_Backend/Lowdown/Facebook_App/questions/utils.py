def get_paged_data(user_data, field_name):
    """Returns all the data for a given field, scrolling through up to max_pages
    of data.

    Args:
        user_data: the main JSON blob returned by Facebook.
        field_name: the name of the field to return the data for.

    Returns:
        An array of dicts that the paged field contains. That is, for statuses,
        this method would return
        [
            {
                "id":       "2157624",
                "from":     { ... },
                "message":  "Status message here.",
                "likes":    { paged data here },
            },
            {
                ...
            },
        ]
    """
    # TODO: actually implement paging.
    return user_data[field_name]['data']

def get_captions(photos):
    """Retrns all the captions on the photos, possibly with duplicates."""
    return [get_caption(photo) for photo in photos]

def get_photo_comments(photo):
    if 'comments' not in photo:
        return []
    comments = get_paged_data(photo, 'comments')
    return ['"%s" -%s' % (comment['message'], comment['from']['name'])
            for comment in comments]

def get_caption(photo):
    return photo['name'] if 'name' in photo else None

def get_sized_photo(photo):
    """Returns a photo url appropriate for the quiz window size."""
    for img in photo['images']:
        if img['height'] < 900 and img['width'] < 600:
            return img['source']
    return ''

class QuestionNotFeasibleException(Exception):
    pass
