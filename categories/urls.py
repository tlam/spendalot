from django.conf.urls import url

from . import views


app_name = 'categories'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^categories.json$', views.categories_json, name='categories_json'),
    url(r'^category_stats.json$', views.category_stats_json, name='category_stats_json'),
    url(r'^prediction/$', views.prediction, name='prediction'),
    url(r'^(?P<slug>\w+)/$', views.details, name='details'),
    url(r'^(?P<slug>\w+).json$', views.details_json, name='details_json'),
]
