from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'Facebook_App.views.home', name='home'),
    url(r'^quiz/(\d+)$', 'Facebook_App.views.quiz', name='quiz'),
   url('', include('social.apps.django_app.urls', namespace='social')),
   url('', include('django.contrib.auth.urls', namespace='auth')),
   url(r'^admin/', include(admin.site.urls)),
)
