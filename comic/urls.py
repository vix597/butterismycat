'''
URL map for views
'''
from django.urls import path, include

from . import views

app_name = "comic"

urlpatterns = [
    path('', views.index, name="index"),
    path('permalink/<comic_id>/', views.comic, name="permalink"),
    path('oldest/', views.oldest, name="oldest"),
    path('next/<current_id>/', views.next_comic, name="next"),
    path('prev/<current_id>/', views.prev_comic, name="prev"),
    path('random/', views.random_comic, name="random"),
    path('archive/', views.archive, name="archive"),
    path('contact/', views.contact, name="contact")
]
