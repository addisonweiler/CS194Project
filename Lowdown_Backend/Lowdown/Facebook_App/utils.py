import logging
import requests

logger = logging.getLogger(__name__)

def get_data(request, target, fields):
    social_user = request.user.social_auth.filter(
         provider='facebook',
    ).first()
    if target is None:
         target = social_user.uid
    # TODO: this sets the fetch limit to 500. Going forward we should check the
    # result and reduce this if the server denies the request.
    fields = fields.replace("%s", "500")
    payload = {
         'fields': fields,
         'access_token': social_user.extra_data['access_token'],
    }
    url = 'https://graph.facebook.com/%s' % target
    r = requests.get(url, params=payload)
    logger.debug(r.url)
    return r.json()