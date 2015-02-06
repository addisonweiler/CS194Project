from django.shortcuts import render_to_response
from django.template.context import RequestContext
import logging
import requests
import urllib2
import json

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
   logger.debug(r.json())
   return r.json()
 
def home(request):
   # A map from name to photo url
   friends = []
   try:
      r = get_data(request, None, 'friends{name,id,picture}')
      friends = r['friends']['data']
   except AttributeError:
      logger.debug('Anonymous user')
   context = RequestContext(request,
                           {'request': request,
                            'friends': friends,
                           })
   return render_to_response('home.html',
                             context_instance=context)

def quiz(request, friend_id):
   statuses = get_data(request, friend_id, 'statuses')
   context = RequestContext(request,
                            {'request': request,
                             'statuses': statuses,
                            })
   return render_to_response('quiz.html', context_instance=context)

# Addison's Code

 # friendarr = []
 # url = ""
 # if not request.user.is_anonymous():
 #   social_user = request.user.social_auth.filter(
 #       provider='facebook',
 #   ).first()
 #   if social_user:
 #       url = u'https://graph.facebook.com/me/' \
 #             u'friends?fields=id,name,location,picture' \
 #             u'&access_token={0}'.format(
 #                 social_user.extra_data['access_token'],
 #             )
 #       request2 = urllib2.Request(url)
 #       friends = json.loads(urllib2.urlopen(request2).read()).get('data')
 #       for friend in friends:
 #           friendarr.append(friend)

 # context = RequestContext(request,
 #                          {'request': request, 'user': request.user, 'friendarr': friendarr, 'url': url})
 # return render_to_response('home.html', context_instance=context)
