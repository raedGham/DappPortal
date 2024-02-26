from django.shortcuts import render, HttpResponse
from vacations.models import Vacation, EmployeeLeaveStat
from overtime.models import Overtime
from medreps.models import Medrep
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def dashboard(request):
    query =""
    if 'query' in request.GET:
      query = request.GET['query'] 

    if query!="":     
     vacWaitApp = Vacation.objects.filter(status=0 , employee__first_name__icontains=query )   
    else:
     vacWaitApp = Vacation.objects.filter(status=0)   
    vacWaitUserApp = []

    for vac in vacWaitApp:
      if vac.first_approval is not None:
          if (vac.first_approval.id == request.user.id) and (vac.approval_position==1):
            vacWaitUserApp.append(vac)

      if vac.second_approval is not None:
          if (vac.second_approval.id == request.user.id) and (vac.approval_position==2):
            vacWaitUserApp.append(vac)
      
      if vac.third_approval is not None:
          if (vac.third_approval.id == request.user.id) and (vac.approval_position==3):
            vacWaitUserApp.append(vac)           
      
      if vac.fourth_approval is not None:
          if (vac.fourth_approval.id == request.user.id) and (vac.approval_position==4):
            vacWaitUserApp.append(vac)           

# ------------------------------ OVERTIME
    OTWaitApp = Overtime.objects.filter(status=0)
  
    OTWaitUserApp = []
    for OT in OTWaitApp:
       if OT.first_approval is not None:
          if (OT.first_approval.id == request.user.id) and (OT.approval_position==1):
            OTWaitUserApp.append(OT)

       if OT.second_approval is not None:
          if (OT.second_approval.id == request.user.id) and (OT.approval_position==2):
            OTWaitUserApp.append(OT)
      
       if OT.third_approval is not None:
          if (OT.third_approval.id == request.user.id) and (OT.approval_position==3):
            OTWaitUserApp.append(OT)           
      
       if OT.fourth_approval is not None:
          if (OT.fourth_approval.id == request.user.id) and (OT.approval_position==4):
            OTWaitUserApp.append(OT)           

# --------------------------------------  medrep
    medWaitApp = Medrep.objects.filter(status=0)
  
    medWaitUserApp = []
    for MED in medWaitApp:
       if MED.first_approval is not None:
          if (MED.first_approval.id == request.user.id) and (MED.approval_position==1):
            medWaitUserApp.append(MED)

       if MED.second_approval is not None:
          if (MED.second_approval.id == request.user.id) and (MED.approval_position==2):
            medWaitUserApp.append(MED)
      
       if MED.third_approval is not None:
          if (MED.third_approval.id == request.user.id) and (MED.approval_position==3):
            medWaitUserApp.append(MED)           
      
       if MED.fourth_approval is not None:
          if (MED.fourth_approval.id == request.user.id) and (MED.approval_position==4):
            medWaitUserApp.append(MED)     


    leavestat = EmployeeLeaveStat.objects.filter(employee=request.user.id)

    if not leavestat:
         remain=""
         ls=[]
    else:
         remain = leavestat[0].total_annual - leavestat[0].daystaken_current 
         ls= leavestat[0]
  
    p = Paginator(vacWaitUserApp,20)
    page = request.GET.get('page')
    p_vacWaitApp = p.get_page(page)

    p1 = Paginator(OTWaitUserApp,20)
    page1 = request.GET.get('page')
    p_OTWaitApp = p1.get_page(page1)

    p2 = Paginator(medWaitUserApp,20)
    page1 = request.GET.get('page')
    p_medWaitApp = p2.get_page(page1)

    context= {'vacWaitApp':p_vacWaitApp,
              'leavestat':ls,
              'remain': remain,
              'OTWaitApp':p_OTWaitApp,
              'medWaitApp':p_medWaitApp,
              }
    
    return render(request,'dashboard\main.html', context)


def searchQuery(request):

    
   return HttpResponse("search Query")