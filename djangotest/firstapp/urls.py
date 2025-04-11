from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.list, name='list'),
    path('create/', views.create, name='create'),
    path('', views.list, name='home'),  # Default route to list view
] 