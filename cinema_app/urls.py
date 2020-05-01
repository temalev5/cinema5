from django.urls import path,re_path
from . import views

urlpatterns = [
    path('room', views.room),
    path('',views.movie,name="home")
]