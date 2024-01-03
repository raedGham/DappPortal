from django.urls import path
from . import views
urlpatterns = [
  path('list/', views.list_vacations, name='list_vacations'),
  path('form/', views.vacations, name='vacations'),
  path('form/<int:id>/', views.vacations, name='vac_update'),
  path('delete/<int:id>/', views.vacation_delete, name='vacation_delete'),
  path('single/<int:id>/',views.single_vacation, name='single_vacation'),
]