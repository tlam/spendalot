from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'spendalot.views.home', name='home'),
    url(r'^categories/', include('categories.urls', namespace='categories'), name='categories'),
    url(r'^expenses/', include('expenses.urls', namespace='expenses'), name='expenses'),
    url(r'^keywords/', include('keywords.urls', namespace='keywords'), name='keywords'),
    url(r'^statements/', include('statements.urls', namespace='statements'), name='statements'),
    url(r'^admin/', include(admin.site.urls)),
)
