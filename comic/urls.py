'''
URL map for views
'''

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^(?P<comic_id>[0-9]+)/$', views.comic, name="comic"),
    url(r'archive/', views.archive, name="archive")
]
