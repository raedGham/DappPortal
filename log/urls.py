from django.urls import path
from . import views
urlpatterns = [
   path('list/', views.log_list, name='log_list'),
   path('form/', views.logs, name='logs'),
#   path('form/<int:id>/', views.departments, name='dep_update'),
#   path('delete/<int:id>/', views.department_delete, name='department_delete'),
]