from django.conf.urls import patterns, url


urlpatterns = patterns('expenses.views',
    url(r'^$', 'index', name='index'),
    url(r'^descriptions.json$', 'descriptions', name='descriptions'),
    url(r'^create/$', 'create', name='create'),
)
