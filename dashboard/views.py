from django.shortcuts import render, HttpResponse
from vacations.models import Vacation

# Create your views here.

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


    return render(request,'dashboard\main.html', {'vacWaitApp':vacWaitUserApp})