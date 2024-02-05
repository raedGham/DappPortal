from django.urls import path
from . import views
urlpatterns = [
  path('otlist/', views.ot_list, name='ot_list'),
  # path('overtime/<int:id>/', views.overtime, name='overtime'),
  path('create_ot_form/<int:id>/', views.create_ot_form, name='create_ot_form'),
  path('ot_approve/<int:id>/', views.overtime_approve, name='overtime_approve'),  
  path('ot_reject/<int:id>/', views.overtime_reject, name='overtime_reject'),
  path('delete/<int:id>/', views.ot_delete, name='ot_delete'), 
 
]