from django.urls import path
from . import views
urlpatterns = [
  path('otlist/', views.ot_list, name='ot_list'),
 
]