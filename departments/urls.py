from django.urls import path
from . import views
urlpatterns = [
  path('list/', views.list_departments, name='list_departments'),
  path('form/', views.departments, name='departments'),
  path('form/<int:id>/', views.departments, name='dep_update'),
  path('delete/<int:id>/', views.department_delete, name='department_delete'),
]