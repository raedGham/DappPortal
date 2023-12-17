from django.urls import path
from . import views
urlpatterns = [
  path('list/', views.list_positions, name='list_positions'),
  path('form/', views.positions, name='positions'),
  path('form/<int:id>/', views.positions, name='pos_update'),
  path('delete/<int:id>/', views.del_position, name='del_position'),
]