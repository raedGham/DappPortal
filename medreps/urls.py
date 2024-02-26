from django.urls import path
from . import views
urlpatterns = [
  path('list/', views.list_medreps, name='list_medreps'),
  path('form/', views.medreps, name='medreps'),
  path('workflow/<int:id>/', views.workflow, name='m_workflow'),
  path('medrep_approve/<int:id>/', views.medrep_approve, name='medrep_approve'),  
  path('medrep_reject/<int:id>/', views.medrep_reject, name='medrep_reject'),  
  path('form/<int:id>/', views.medreps, name='medrep_update'),
  path('delete/<int:id>/', views.medrep_delete, name='medrep_delete'),
  path('single/<int:id>/',views.single_medrep, name='single_medrep'),
  path('singlePDF/<int:id>/',views.single_medrepPDF, name='single_medrepPDF'),
  path('entitlement/<int:em>',views.med_entitlement, name='med_entitlement'),
  path('entadd/<int:id>/<int:empl>', views.med_entform, name='med_ent_add'),
  path('entupd/<int:id>/<int:empl>', views.med_entform, name='med_ent_update'),
  path('entdel/<int:id>/', views.med_ent_delete, name='med_ent_delete'),
  path('pdf/<int:id>/', views.pdf_view, name='pdf_view'),
  
  
]