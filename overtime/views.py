from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from .models import Overtime
from accounts.models import Account
from positions.models import Position
from datetime import timedelta, datetime
from .forms import OvertimeForm,OvertimeFormSet
from dapp.utils import GetFilterDepList 

# Create your views here.

def getAppEmp(ot):
   if ot.approval_position == 1 :
      return ot.first_approval.id
   elif ot.approval_position == 2:
      return ot.second_approval.id
   elif ot.approval_position == 3:
      return ot.third_approval.id
   elif ot.approval_position == 4:
      return ot.fourth_approval.id

@login_required(login_url='login')
def ot_list(request):
    if request.GET.get('employee') is not None:
      selected_emp = request.GET.get('employee')
    else:
      selected_emp=-1 
         
    
    FilterDepList= GetFilterDepList(request.user)
    emps = Account.objects.filter(department__name__in=FilterDepList).order_by("username")
    p_ots = Overtime.objects.all()
    context={
       'p_ots':p_ots,
       'emps' : emps,
       'selected_emp':int(selected_emp),
    }
    return render(request, 'overtime/ot_list.html', context)


@login_required(login_url='login')
def overtime(request,id):
 employee = Account.objects.get(id=id)
 overtime = Overtime.objects.filter(employee=id)
 formset = OvertimeFormSet(request.POST or None)

 if request.method == "POST":
   
    if formset.is_valid():
       
       formset.instance = overtime
       formset.save()
       return redirect("overtime", pk=employee.id)
    else:
       return HttpResponse("invalid")

 context = {  
      'formset': formset,    
      'overtime': overtime,
      'employee': employee,
   }       
      
 return render(request, 'overtime\\overtime.html', context)



@login_required(login_url='login')     
def overtime_approve(request, id):   
   ot = Overtime.objects.get(id=id) 

   if ot.approval_position == 1 :
      ot.first_app_status = 1
      ot.approval_position = 2
   elif  ot.approval_position == 2 : 
      ot.second_app_status = 1
      ot.approval_position = 3
   elif  ot.approval_position == 3 : 
      ot.third_app_status = 1
      ot.approval_position = 4
   elif  ot.approval_position == 4 : 
      print("Approval position = 4")
      ot.fourth_app_status = 1
      ot.status = 1       
   ot.save()
   return redirect('ot_list') 

@login_required(login_url='login')
def overtime_reject(request, id):   
   ot = Overtime.objects.get(id=id) 
   ot.status = 2    
   ot.save()
   return redirect('ot_list') 


@login_required(login_url='login')
def ot_delete(request,id):
      ot = Overtime.objects.get(id=id)
      if request.method == "POST":                
         ot.delete()
         return redirect('ot_list')
      
      return render(request,
                  'overtime/ot_delete.html',
                  {'ot': ot}) 