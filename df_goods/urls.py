from django.conf.urls import url
from . import views
from views import *

urlpatterns=[
    url('^$', index),
    url(r'^list(\d+)_(\d+)_(\d+)/$', list),
    url(r'^(\d+)/$', detail),
]