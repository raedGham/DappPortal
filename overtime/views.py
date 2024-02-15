from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from .models import Overtime
from positions.models import Position
from accounts.models import Account
from datetime import datetime
from .forms import OvertimeForm, OtByDateForm
from dapp.utils import GetFilterDepList 
from decimal import Decimal
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date
from django.db.models import Q
import json
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
    # Pagination

      # set up pagination
   name_search = request.GET.get('name_search')
   PSno_search = request.GET.get('PSno_search')  
   S_fromdate = request.GET.get('S_fromdate')  
   S_todate = request.GET.get('S_todate') 

   FilterDepList = GetFilterDepList(request.user)
   # sortby = request.GET.get('sortby')
   sortby = "-id"

   if sortby is not None:
    data = Overtime.objects.filter(employee__department__name__in=FilterDepList).order_by(sortby)
   else:
    data = Overtime.objects.filter(employee__department__name__in=FilterDepList)     

   if name_search !='' and name_search is not None:     
     if sortby is not None:
      data = data.filter(employee__first_name__icontains= name_search).order_by(sortby)
     else:
      data = data.filter(employee__first_name__icontains= name_search)   

   if PSno_search !='' and PSno_search is not None:
     if sortby is not None:
      data = data.filter(employee__ps_number= PSno_search).order_by(sortby)
     else:
      data = data.filter(employee__ps_number= PSno_search)    

   if S_fromdate is not None and S_todate is not None and S_fromdate != '' and S_todate != '':
     if sortby is not None:    
      data = data.filter(ot_date__range=[parse_date(S_fromdate), parse_date(S_todate)])
     else:      
      data = data.filter(ot_date__range=[parse_date(S_fromdate), parse_date(S_todate)])   

   p = Paginator(data,20)
   page = request.GET.get('page')
   p_overtime = p.get_page(page)

    
    
   if request.GET.get('employee') is not None:
      selected_emp = request.GET.get('employee')
   else:
      selected_emp=-1 

   print(request.GET.get('otdate'))
   if request.GET.get('otdate') is not None:
      selected_date = request.GET.get('otdate')
   else:
      selected_date=datetime.now().strftime("%Y-%m-%d")
      print("selected Date=", selected_date) 
      print(type(selected_date))           
    
   FilterDepList= GetFilterDepList(request.user)
   emps = Account.objects.filter(department__name__in=FilterDepList).order_by("username")
  

   context={
      'p_ots':p_overtime,
      'emps' :emps,
      'selected_emp':int(selected_emp),
      'selected_date':selected_date,
    }
   return render(request, 'overtime/ot_list.html', context)

def create_ot_form(request):    
    form = OvertimeForm()
    context = {
        "form": form
    }
    return render(request, "overtime/ot_form.html", context)

def create_ot_By_date_form(request):      
    # dep_id=request.user.department_id
    form = OtByDateForm(dep_id=request.user.department_id)
    
    context = {
        "form": form,    
    }
    return render(request, "overtime/ot_form1.html", context)

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
       if employee.is_head :
          first_app = employee
       else:   
          first_app = employee.head_dep
                
       second_app = first_app.head_dep
       third_app = Account.objects.get(position = Position.objects.get(title="Admin Head"))
       fourth_app = Account.objects.get(position = Position.objects.get(title="Superintendent"))

       ot.employee = employee
       ot.total_hours = (TD.total_seconds()/60) /60
       ot.straight = Decimal(ot.total_hours) * ot.rate       
       ot.save()    
       upd_ot = Overtime.objects.get(id=ot.id)
       upd_ot.first_approval = first_app
       upd_ot.second_approval = second_app
       upd_ot.third_approval = third_app
       upd_ot.fourth_approval = fourth_app
       upd_ot.save()   
       
    else:
       return HttpResponse("Invalid")
    

 context = {  
      'form': form,    
      'overtime': overtime,
      'employee': employee,
   }       
      
 return render(request, 'overtime\\overtime.html', context)

def Getdoweek(date_str, format="%Y-%m-%d"):
   try:
        date_obj = datetime.strptime(date_str, format)

        # Get the number of the day (0-6, Monday-Sunday)
        day_of_week_num = date_obj.weekday()

        # Convert to character day of the week using a dictionary
        character_days = {0: "Mon", 1: "Tues", 2: "Wed", 3: "Thurs", 4: "Fri", 5: "Sat", 6: "Sun"}

        return character_days[day_of_week_num]

   except ValueError:
        raise ValueError("Invalid date string or format. Please use the correct format:", format)


@login_required(login_url='login')
def ot_by_date(request,otdate):
 
 overtime = Overtime.objects.filter(ot_date=otdate)
 form = OtByDateForm(request.POST or None)

 if request.method == "POST":
    
    if form.is_valid():
       
       employee=form.cleaned_data['employee']
       from_time= form.cleaned_data['from_time']
       to_time=  form.cleaned_data['to_time']
       ot_date = datetime.strptime(otdate, "%Y-%m-%d" )

       FT = datetime.combine(ot_date, from_time)
       TT = datetime.combine(ot_date, to_time)                            
       TD = TT -FT             
       ot = form.save(commit=False)
       if employee.is_head :
          first_app = employee
       else:   
          first_app = employee.head_dep
                
       second_app = first_app.head_dep
       third_app = Account.objects.get(position = Position.objects.get(title="Admin Head"))
       fourth_app = Account.objects.get(position = Position.objects.get(title="Superintendent"))
       ot.ot_date = otdate
       ot.employee = employee
       ot.total_hours = (TD.total_seconds()/60) /60
       ot.straight = Decimal(ot.total_hours) * ot.rate  
        
       ot.save()       
       upd_ot = Overtime.objects.get(id=ot.id)
       upd_ot.first_approval = first_app
       upd_ot.second_approval = second_app
       upd_ot.third_approval = third_app
       upd_ot.fourth_approval = fourth_app
       upd_ot.save()

       return HttpResponse("success")
    else:
       return HttpResponse("Invalid")
    
 doweek = Getdoweek(otdate)
 context = {  
      'form': form,    
      'overtime': overtime,
      'otdate': otdate,
      'doweek': doweek,
   }       
      
 return render(request, 'overtime\\ot_by_date.html', context)

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


def ots_approve(request):
   usr = request.user
   
   ots = Overtime.objects.filter(
                                       Q(first_app_status = 0) & Q(first_approval = usr)  |
                                       Q(second_app_status = 0) & Q(second_approval = usr)|
                                       Q(third_app_status = 0) & Q(third_approval = usr)  | 
                                       Q(fourth_app_status = 0) & Q(fourth_approval = usr) )
   print(request.method)
   
   if request.method == "POST":
        selected_items = json.loads(request.body)
        print(selected_items)
        # Process the selected_items list
        # For example, save them to a database or perform other actions
        return HttpResponse("Items processed successfully!")
   else:   
      context = {
         'ots':ots
         }
      return render(request,'overtime/ots_approve.html', context)

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


@login_required(login_url='login')
def workflow(request, id):
     ot = Overtime.objects.get(id=id)
     return render(request,'overtime/workflow.html',{'ot': ot}) 
