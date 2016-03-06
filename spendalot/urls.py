from django.conf.urls import include, url
from django.contrib import admin

from . import views


admin.autodiscover()

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^categories/', include('categories.urls', namespace='categories'), name='categories'),
    url(r'^expenses/', include('expenses.urls', namespace='expenses'), name='expenses'),
    url(r'^statements/', include('statements.urls', namespace='statements'), name='statements'),
    url(r'^admin/', include(admin.site.urls)),
]
