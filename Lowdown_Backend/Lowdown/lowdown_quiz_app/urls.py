from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'mysite.myapp.views.home', name="home"),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
