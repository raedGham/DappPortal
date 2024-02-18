from django.urls import path
from . import views
urlpatterns = [
  path('main/', views.admindash, name='admindash'), 
]