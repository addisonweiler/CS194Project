from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^Facebook_App/', include('Facebook_App.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
