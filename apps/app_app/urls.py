from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$', index),
    url(r'^main$', main),
    url(r'^login$', login),
    url(r'^register$', register),
    url(r'^appointments$', appointments),
    url(r'^add_appointment$', add_appointment),
    url(r'^edit_appointment/(?P<id>\d+)$', edit_appointment),
    url(r'^update_appointment/(?P<id>\d+)$', update_appointment),
    url(r'^delete/(?P<id>\d+)$', delete),
    url(r'^logout$', logout)
]
