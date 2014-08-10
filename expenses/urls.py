from django.conf.urls import patterns, url


urlpatterns = patterns('expenses.views',
    url(r'$', 'index', name='index'),
)
