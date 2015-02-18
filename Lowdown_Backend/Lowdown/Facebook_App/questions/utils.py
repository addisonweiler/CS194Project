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

def get_captions(photos, exclude=None): 
    all_captions = [get_caption(photo) for photo in photos] 
    return list(set(filter(lambda x: x is not None and x != exclude, all_captions)))

def get_caption(photo): 
    return photo['name'] if 'name' in photo else None

def get_sized_photo(photo):
    """Returns a photo url appropriate for the quiz window size."""
    for img in photo['images']:
        if img['height'] < 400 and img['width'] < 600:
            return img['source']
    return ''

class QuestionNotFeasibleException(Exception):
    pass
