from django.urls import path
from . import views
urlpatterns = [
  path('list/', views.list_positions, name='list_positions'),
]