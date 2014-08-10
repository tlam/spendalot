from django.conf.urls import patterns, url


urlpatterns = patterns('keywords.views',
    url(r'$', 'index', name='index'),
)
