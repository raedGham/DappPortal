from django.urls import path
from . import views
urlpatterns = [
  path('otlist/', views.ot_list, name='ot_list'),
  path('overtime/<int:id>/', views.overtime, name='overtime'),
  path('ot_by_date/<str:otdate>/', views.ot_by_date, name='ot_by_date'),
  path('workflow/<int:id>/', views.workflow, name='o_workflow'),
  path('create_ot_form/', views.create_ot_form, name='create_ot_form'), 
  path('create_ot_By_date_form/', views.create_ot_By_date_form, name='create_ot_By_date_form'), 
  path('ot_approve/<int:id>/', views.overtime_approve, name='overtime_approve'),  
  path('ots_approve/', views.ots_approve, name='ots_approve'), 
  path('ot_reject/<int:id>/', views.overtime_reject, name='overtime_reject'),
  path('delete/<int:id>/', views.ot_delete, name='ot_delete'), 
  path('update/<int:id>/', views.ot_update, name='ot_update'), 
 
]