from django.conf.urls import url

from . import views


app_name = 'expenses'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^category.json$', views.category, name='category'),
    url(r'^cuisines/$', views.cuisines, name='cuisines'),
    url(r'^download-csv/$', views.download_csv, name='download-csv'),
    url(r'^create/$', views.create, name='create'),
    url(r'^descriptions.json$', views.descriptions, name='descriptions'),
    url(r'^trends/$', views.trends, name='trends'),
]
