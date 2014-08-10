from django.conf.urls import patterns, url


urlpatterns = patterns('statements.views',
    url(r'$', 'index', name='index'),
)
