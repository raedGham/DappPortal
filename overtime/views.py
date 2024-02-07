from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from .models import Overtime
from accounts.models import Account
from positions.models import Position
from datetime import timedelta, datetime
from .forms import OvertimeForm
from dapp.utils import GetFilterDepList 
from decimal import Decimal
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

def create_ot_form(request):
    form = OvertimeForm()
    context = {
        "form": form
    }
    return render(request, "overtime/ot_form.html", context)
   

@login_required(login_url='login')
def overtime(request,id):
 employee = Account.objects.get(id=id)
 overtime = Overtime.objects.filter(employee=id)
 form = OvertimeForm(request.POST or None)

 if request.method == "POST":
   
    if form.is_valid():
       ot_date= form.cleaned_data['ot_date']
       from_time= form.cleaned_data['from_time']
       to_time=  form.cleaned_data['to_time']
       FT = datetime.combine(ot_date, from_time)
       TT = datetime.combine(ot_date, to_time)                            
       TD = TT -FT             
       ot = form.save(commit=False)
       ot.employee = employee
       ot.total_hours = (TD.total_seconds()/60) /60
       ot.straight = Decimal(ot.total_hours) * ot.rate       
       ot.save()       
       return HttpResponse("Success")
    else:
       return HttpResponse("Invalid")
    

 context = {  
      'form': form,    
      'overtime': overtime,
      'employee': employee,
   }       
      
 return render(request, 'overtime\\overtime.html', context)


@login_required(login_url='login')     
def ot_update(request, id):   
    if request.method == "POST":            
            ot = Overtime.objects.get(pk=id)
            form = OvertimeForm(request.POST, instance = ot)  
            if form.is_valid():
               ot.ot_date= form.cleaned_data['ot_date']
               ot.from_time= form.cleaned_data['from_time']
               ot.to_time=  form.cleaned_data['to_time']
               ot.rate=  form.cleaned_data['rate']
               ot.reason=  form.cleaned_data['reason']
               FT = datetime.combine(ot.ot_date, ot.from_time)
               TT = datetime.combine(ot.ot_date, ot.to_time)                            
               TD = TT -FT                
               ot.total_hours = (TD.total_seconds()/60) /60
               print(ot.total_hours)
               ot.straight = Decimal(ot.total_hours) * Decimal(ot.rate)                
               ot.save()
               return redirect('ot_list')
            else:
                return HttpResponse(form.errors)
                # return redirect('ot_list')
    else: # get
       overtime = Overtime.objects.get(pk=id)          
       form = OvertimeForm(instance=overtime) 
       context = {'form':form,
                  'ot': overtime}
    return render(request, 'overtime\\overtimeSF.html', context)    
          



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
      
      return render(request,'overtime/ot_delete.html',{'ot': ot}) 