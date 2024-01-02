from django.urls import path
from . import views
urlpatterns = [
  path('list/', views.list_profiles, name='list_profiles'),
  path('form/', views.profiles, name='profiles'),
  path('form/<int:id>/', views.profiles, name='profile_update'),
  path('delete/<int:id>/', views.profile_delete, name='profile_delete'),
  path('hierarchy/', views.hierarchy, name='hierarchy'),
]