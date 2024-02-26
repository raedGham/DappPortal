from django.urls import path
from . import views
urlpatterns = [
  path('main/', views.dashboard, name='dashboard'),
  path('search/', views.searchQuery, name='searchQuery'),
]