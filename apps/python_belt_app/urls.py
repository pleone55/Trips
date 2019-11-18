from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^add$', views.add),
    url(r'^trips/new$', views.add_trip),
    url(r'^trips/edit/(?P<id>\d+)$', views.edit_info),
    url(r'^trips/(?P<id>\d+)$', views.trip_info),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^cancel/(?P<id>\d+)$', views.cancel),
    url(r'^join/(?P<id>\d+)$', views.join),
    url(r'^success$', views.success),
    url(r'^logout$', views.logout)
]
