from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
   url(r'^$', 'Facebook_App.views.home', name='home'),
   url(r'^quiz/(\d+)$', 'Facebook_App.views.blank_quiz', name='blank_quiz'),
   url(r'^quiz/(\d+)/content$', 'Facebook_App.views.quiz', name='quiz'),
   url(r'^quiz_grade', 'Facebook_App.views.quiz_grade', name='quiz_grade'),
   (r'^about_us/$', TemplateView.as_view(template_name='about_us.html')),
   url('', include('social.apps.django_app.urls', namespace='social')),
   url('', include('django.contrib.auth.urls', namespace='auth')),
   url(r'^admin/', include(admin.site.urls)),
) 
