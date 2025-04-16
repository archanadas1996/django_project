from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='movie_list'),
    path('add/', views.add_movie, name='add_movie'),
    path('edit/<int:movie_id>/', views.edit_movie, name='edit_movie'),
    path('delete/<int:movie_id>/', views.delete_movie, name='delete_movie'),
    path('add/censor-info/', views.add_censor_info, name='add_censor_info'),
    path('add/director/', views.add_director, name='add_director'),
    path('add/actor/', views.add_actor, name='add_actor'),
] 