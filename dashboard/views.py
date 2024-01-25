from django.shortcuts import render, HttpResponse
from vacations.models import Vacation, EmployeeLeaveStat

# Create your views here.

def dashboard(request):
    vacWaitApp = Vacation.objects.filter(status=0)
    print(vacWaitApp)
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

    leavestat = EmployeeLeaveStat.objects.filter(employee=request.user.id)

    if not leavestat:
         remain=""
         ls=[]
    else:
         remain = leavestat[0].total_annual - leavestat[0].daystaken_current 
         ls= leavestat[0]

    context= {'vacWaitApp':vacWaitUserApp,
              'leavestat':ls,
              'remain': remain,
              }
    
    return render(request,'dashboard\main.html', context)