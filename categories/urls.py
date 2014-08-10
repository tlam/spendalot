from django.conf.urls import patterns, url


urlpatterns = patterns('categories.views',
    url(r'$', 'index', name='index'),
)
