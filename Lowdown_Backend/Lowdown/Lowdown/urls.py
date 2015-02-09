from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^Facebook_App/', include('Facebook_App.urls')),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^$', include('Facebook_App.urls')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
