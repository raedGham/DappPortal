from django.urls import path
from . import views
urlpatterns = [
  path('list/', views.list_profiles, name='list_profiles'),
  path('listPDF/', views.profilesPDF, name='profilesPDF'),
  path('form/', views.profiles, name='profiles'),  
  path('form/<int:id>/', views.profiles, name='profile_update'),
  path('delete/<int:id>/', views.profile_delete, name='profile_delete'),
  path('hierarchy/', views.hierarchy, name='hierarchy'),
  path('login/', views.login, name='login'),
  path('logout/', views.logout, name='logout'),
  path('modify/', views.modifypassword)
]