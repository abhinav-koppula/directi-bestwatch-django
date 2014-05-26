from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^bestwatch/', include('bestwatch.urls', namespace="bestwatch")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'bestwatch.views.fblogin'),
)
