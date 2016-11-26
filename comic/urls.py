'''
URL map for views
'''

from django.conf.urls import url
from . import views

app_name = "comic"
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^(?P<comic_id>[0-9]+)/$', views.comic, name="permalink"),
    url(r'oldest/', views.oldest, name="oldest"),
    url(r'next/(?P<current_id>[0-9]+)/$', views.next_comic, name="next"),
    url(r'prev/(?P<current_id>[0-9]+)/$', views.prev_comic, name="prev"),
    url(r'random/', views.random_comic, name="random"),
    url(r'archive/', views.archive, name="archive")
]
