from django.conf.urls import patterns, url


urlpatterns = patterns('categories.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<slug>\w+)/$', 'details', name='details'),
    url(r'^(?P<slug>\w+).json$', 'details_json', name='details_json'),
)
