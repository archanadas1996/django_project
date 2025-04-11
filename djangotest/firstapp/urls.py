from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='list'),
    path('create/', views.create, name='create'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('delete/<int:pk>/', views.delete, name='delete'),
] 