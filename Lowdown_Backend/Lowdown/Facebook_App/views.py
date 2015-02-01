from django.shortcuts import render_to_response
from django.template.context import RequestContext
import logging

logger = logging.getLogger(__name__)

def foo():
   logger.debug("test")

def home(request):
   logger.debug("foobar")
   context = RequestContext(request,
                           {'request': request,
                            'user': request.user})
   return render_to_response('home.html',
                             context_instance=context)
