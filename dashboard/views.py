from django.shortcuts import render, HttpResponse
from vacations.models import Vacation, EmployeeLeaveStat
from overtime.models import Overtime
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def dashboard(request):
    vacWaitApp = Vacation.objects.filter(status=0)
  
    vacWaitUserApp = []
    for vac in vacWaitApp:
        if (vac.first_approval.id == request.user.id) and (vac.approval_position==1):
            vacWaitUserApp.append(vac)
        elif (vac.second_approval.id == request.user.id) and (vac.approval_position==2):
             vacWaitUserApp.append(vac)
        elif (vac.third_approval.id == request.user.id) and (vac.approval_position==3):
             vacWaitUserApp.append(vac)
        elif (vac.fourth_approval.id == request.user.id) and (vac.approval_position==4):
             vacWaitUserApp.append(vac)

    OTWaitApp = Overtime.objects.filter(status=0)
  
    OTWaitUserApp = []
    for OT in OTWaitApp:
          if (OT.first_approval.id == request.user.id) and (OT.approval_position==1):
               OTWaitUserApp.append(OT)
          elif (OT.second_approval.id == request.user.id) and (OT.approval_position==2):
               OTWaitUserApp.append(OT)
          elif (OT.third_approval.id == request.user.id) and (OT.approval_position==3):
               OTWaitUserApp.append(OT)
          elif (OT.fourth_approval.id == request.user.id) and (OT.approval_position==4):
               OTWaitUserApp.append(OT)


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


    context= {'vacWaitApp':p_vacWaitApp,
              'leavestat':ls,
              'remain': remain,
              'OTWaitApp':p_OTWaitApp,
              }
    
    return render(request,'dashboard\main.html', context)