from django.conf.urls import patterns, url


urlpatterns = patterns('expenses.views',
    url(r'^$', 'index', name='index'),
    url(r'^category.json$', 'category', name='category'),
    url(r'^download-csv/$', 'download_csv', name='download-csv'),
    url(r'^create/$', 'create', name='create'),
    url(r'^descriptions.json$', 'descriptions', name='descriptions'),
    url(r'^trends/$', 'trends', name='trends'),
)
