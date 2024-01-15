from django.urls import path
from . import views
urlpatterns = [
  path('list/', views.list_vacations, name='list_vacations'),
  path('form/', views.vacations, name='vacations'),
  path('workflow/<int:id>/', views.workflow, name='workflow'),
  path('vacation_approve/<int:id>/', views.vacation_approve, name='vacation_approve'),  
  path('vacation_reject/<int:id>/', views.vacation_reject, name='vacation_reject'),  
  path('form/<int:id>/', views.vacations, name='vac_update'),
  path('delete/<int:id>/', views.vacation_delete, name='vacation_delete'),
  path('single/<int:id>/',views.single_vacation, name='single_vacation'),
  path('singlePDF/<int:id>/',views.single_vacationPDF, name='single_vacationPDF'),
  path('entitlement/<int:em>',views.entitlement, name='entitlement'),
  path('entadd/<int:id>/<int:empl>', views.entform, name='ent_add'),
  path('entupd/<int:id>/<int:empl>', views.entform, name='ent_update'),
  path('entdel/<int:id>/', views.ent_delete, name='ent_delete'),
  
]