import logging
import requests

logger = logging.getLogger(__name__)

def get_data(request, target, fields):
    social_user = request.user.social_auth.filter(
         provider='facebook',
    ).first()
    if target is None:
         target = social_user.uid
    payload = {
         'fields': fields,
         'access_token': social_user.extra_data['access_token'],
    }
    url = 'https://graph.facebook.com/%s' % target
    r = requests.get(url, params=payload)
    logger.debug(r.url)
    return r.json()
