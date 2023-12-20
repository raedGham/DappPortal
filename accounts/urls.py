from django.urls import path
from . import views
urlpatterns = [
 # path('list/', views.list_departments, name='list_profiles'),
  path('form/', views.profiles, name='profiles'),
 # path('form/<int:id>/', views.departments, name='profile_update'),
 # path('delete/<int:id>/', views.department_delete, name='profile_delete'),
]