from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from .models import Overtime
from accounts.models import Account
from positions.models import Position
from datetime import timedelta, datetime
from .forms import OvertimeForm

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
    p_ots = Overtime.objects.all()
    return render(request, 'overtime/ot_list.html', {'p_ots':p_ots})


@login_required(login_url='login')
def overtime(request, id=0):
     
     if request.method == "POST":
       if id == 0: # to create a new record and append it to the table            
            form = OvertimeForm(request.POST)
            if form.is_valid():
               employee= form.cleaned_data['employee']
               vac_date= form.cleaned_data['ot_date']
               from_time= form.cleaned_data['from_time']
               to_time= form.cleaned_data['to_time']
               rate = form.cleaned_data['rate']               
               reason  = form.cleaned_data['reason']
            #    if ampm.lower() == 'am' or ampm.lower() =='pm':
            #       if to_date>from_date:
            #          to_date = from_date
            #          x = 0.5
            #    else:      
            #       x = RequestedVac(from_date, to_date)
           
               # set Vacation Approval Workflow
               if employee.is_head :
                     first_app = employee
               else:   
                     first_app = employee.head_dep
                
               second_app = first_app.head_dep
               third_app = Account.objects.get(position = Position.objects.get(title="Admin Head"))
               fourth_app = Account.objects.get(position = Position.objects.get(title="Superintendent"))
               
               
               overtime = Overtime.objects.create(employee=employee,ot_date=vac_date,from_time=from_time, to_time=to_time,rate=rate,
                                                  reason=reason,  first_approval= first_app, 
                                                  second_approval= second_app,third_approval = third_app, fourth_approval = fourth_app)
              
               overtime.save()

                   
               return redirect('ot_list')
            else:
               return HttpResponse("Invalid Form")
            
       else: # to update the edited record in the table
            print("the update submitted")
            overtime = Overtime.objects.get(pk=id)
            from_time=  datetime.strptime(request.POST.get('from_time'),'%Y-%m-%d')
            to_time= datetime.strptime(request.POST.get('to_time'), '%Y-%m-%d')
            
                        
            form = OvertimeForm(request.POST, instance = overtime)  
            if form.is_valid():
               overtime.save()
               return redirect('ot_list')
            else:
               return HttpResponse("Invalid Form")
                
     else:   # GET
         if id == 0 : # to open a blank from
                     
            form = OvertimeForm(dep_id=request.user.department)
            context = {
               'form':form,             
            }
         
         else: # to populate the form with the data needed to be updated
            overtime = Overtime.objects.get(pk=id)
           
            form = OvertimeForm(instance=overtime)
            if request.user.id == getAppEmp(overtime):
               RejAcc = True
            else:
               RejAcc = False   
   
            context = {
               'form':form,
               'RejAcc': RejAcc,
               }    
      
         return render(request, 'overtime\\overtime.html', context)

def create_overtime(request):
    otForm = OvertimeForm()
    context = {
        "form ":otForm
    }
    return render(request,"overtime\\overtime.html", context )


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