from django.shortcuts import render_to_response
from django.template.context import RequestContext
import logging
import requests

logger = logging.getLogger(__name__)

def home(request):
   # A map from name to photo url
   friends = {}
   try:
      social_user = request.user.social_auth.filter(
         provider='facebook',
      ).first()
      payload = {
         'fields': 'id,name,picture',
         'access_token': social_user.extra_data['access_token'],
      }
      url = 'https://graph.facebook.com/%s/friends' % social_user.uid
      r = requests.get(url, params=payload)
      logger.debug(r.url)
      logger.debug(r.json())
      for friend in r.json()['data']:
         friends[friend['name']] = friend['picture']['data']['url']
   except AttributeError:
      logger.debug('Anonymous user')
   context = RequestContext(request,
                           {'request': request,
                            'friends': friends,
                            'user': request.user})
   return render_to_response('home.html',
                             context_instance=context)
