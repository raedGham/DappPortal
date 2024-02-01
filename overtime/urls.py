from django.urls import path
from . import views
urlpatterns = [
  path('otlist/', views.ot_list, name='ot_list'),
  path('overtime/', views.overtime, name='overtime'),
  path('ot_approve/<int:id>/', views.overtime_approve, name='overtime_approve'),  
  path('ot_reject/<int:id>/', views.overtime_reject, name='overtime_reject'),
  path('delete/<int:id>/', views.ot_delete, name='ot_delete'), 
 
]