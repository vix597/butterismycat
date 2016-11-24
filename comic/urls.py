'''
URL map for views
'''

from django.conf.urls import url
from . import views

app_name = "comic"
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^(?P<comic_id>[0-9]+)/$', views.comic, name="permalink"),
    url(r'archive/', views.archive, name="archive")
]
