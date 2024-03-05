from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from vacations.models import Vacation, EmployeeLeaveStat
from django.core.paginator import Paginator
from .forms import VacationForm, EntitlementForm
from datetime import timedelta, datetime
from django.conf import settings
from pathlib import Path
from accounts.models import Account
from positions.models import Position
from django.utils.dateparse import parse_date
from dapp.utils import GetFilterDepList, SetWorkflow
from decimal import Decimal
from django.contrib import messages
# imports for pdf generator
import os
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from  django.db.models import Sum

#--------------------------------------------------------------------------    P D F  V A C A T I O N  L I S T   
@login_required(login_url='login')
def vacListPDF(request):
  os.add_dll_directory(r"C:/Program Files/GTK3-Runtime Win64/bin")
  response = HttpResponse(content_type='application/pdf')
  response['Content-Disposition'] = 'inline; filename=Vacation'+ str(datetime.now) + '.pdf'
  response['Content-Transfer-Encoding'] = 'binary'
  name_search = request.session["name_search"]
  PSno_search = request.session["PSno_search"]
  print("name search:", name_search)
  data = Vacation.objects.all()
  if name_search !='' and name_search is not None:
    data = Vacation.objects.filter(employee__first_name__icontains=name_search )
  if PSno_search !='' and PSno_search is not None:
    data = Vacation.objects.filter(employee__ps_number__icontains= PSno_search)
  context = {
      'vacs' : data ,      
   }
  
  html_string = render_to_string('vacations\\vacListPDF.html', context)
  html=HTML(string=html_string, base_url=request.build_absolute_uri())
  result= html.write_pdf(response , presentational_hints=True)
  return response     


#    -------------------------------------------     V A C A T I O N S  L I S T
@login_required(login_url='login')
def list_vacations(request):
#    departments = Department.objects.all()
#    positions = Position.objects.all()
   
   # set up pagination
   name_search = request.GET.get('name_search')
   PSno_search = request.GET.get('PSno_search')
   S_fromdate = request.GET.get('S_fromdate')  
   S_todate = request.GET.get('S_todate') 

   request.session["name_search"]= name_search
   request.session["PSno_search"]= PSno_search
   FilterDepList = GetFilterDepList(request.user)
   # sortby = request.GET.get('sortby')
   sortby = "-id"

   if sortby is not None:
    data = Vacation.objects.filter(employee__department__name__in=FilterDepList).order_by(sortby)
   else:
    data = Vacation.objects.filter(employee__department__name__in=FilterDepList)     


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
      data = data.filter(vac_date__range=[parse_date(S_fromdate), parse_date(S_todate)]).order_by(sortby)
     else:      
      data = data.filter(vac_date__range=[parse_date(S_fromdate), parse_date(S_todate)])   
 

   
   p = Paginator(data,20)
   page = request.GET.get('page')
   p_vacations = p.get_page(page)
   
   # calculate canDel

   canDelete=[]
  
   for vac in data:
       print(request.user.username)
       if  request.user.username == 'adminuser' and vac.status not in [1,2]:
         canDelete.append(vac.id)

       if       (vac.approval_position == 1 and vac.first_approval==request.user) or (
                 vac.approval_position == 2 and vac.second_approval==request.user) or(
                 vac.approval_position == 3 and vac.third_approval==request.user) or ( 
                 vac.approval_position == 4 and vac.fourth_approval==request.user): 
          canDelete.append(vac.id)

   
   context = { 
               'p_vacations':p_vacations, 
               'canDelete': canDelete,
                           
               }
   return render(request,"vacations\\vacations_list.html", context)

#    -------------------------------------------     A D D / E D I T   V A C A T I O N
@login_required(login_url='login')
def vacations(request, id=0):
     
   if request.method == "POST":
      if id == 0: # to create a new record and append it to the table      
            

            form = VacationForm(request.POST)
            if form.is_valid():
                  employee= form.cleaned_data['employee']
                  vac_date= form.cleaned_data['vac_date']
                  from_date= form.cleaned_data['from_date']
                  to_date= form.cleaned_data['to_date']
                  nodays= form.cleaned_data['nodays']
                  ampm  = form.cleaned_data['ampm']
                  remarks  = form.cleaned_data['remarks']
                 
                  els = EmployeeLeaveStat.objects.filter(employee = employee)               
                  idy = els[0].id
                  updEls = EmployeeLeaveStat.objects.get(id= idy ) 
                  drem = updEls.current_year + updEls.previous_year - updEls.daystaken_current
                  if ampm.lower() == 'am' or ampm.lower() =='pm':
                     if to_date>from_date:
                        to_date = from_date
                     x = 0.5
                  else:      
                     x = RequestedVac(from_date, to_date)
                  if x> drem :
                     messages.error(request, str(drem)+  " days remaining only")
                     return redirect('list_vacations')
                  # set Vacation Approval Workflow
                  first_app, second_app, third_app, fourth_app = SetWorkflow(employee)                               
                                 
                  vacation = Vacation.objects.create(employee=employee,vac_date=vac_date,from_date=from_date, to_date=to_date,
                                                      nodays=x,ampm=ampm, remarks=remarks)      
                  vacation.save()
                  if first_app is not None:
                     vacation.first_approval = first_app
                     vacation.approval_position = 1
                  else:  
                     vacation.first_app_status=1
                     vacation.approval_position = 2
                  
                  if second_app is not None:
                     vacation.second_approval = second_app                  
                  else:
                     vacation.first_app_status=1
                     vacation.second_app_status=1
                     vacation.approval_position = 3

                  if third_app is not None:
                     vacation.third_approval = third_app
                  if fourth_app is not None:
                     vacation.fourth_approval = fourth_app   
                  
                  # update EmployeeLeaveStat 
               
                  els = EmployeeLeaveStat.objects.filter(employee = employee)               
                  idy = els[0].id
                  updEls = EmployeeLeaveStat.objects.get(id= idy ) 
                  vacation.sofar = updEls.daystaken_current 
                  vacation.leave_stat_id = updEls          
                  updEls.daystaken_current = updEls.daystaken_current + Decimal(vacation.nodays)
                  updEls.save()         
                  vacation.save()
                  return redirect('list_vacations')
            else: 
                  context = {
                  'form':form,
                  'updEls':{}, 
                  'annual': '',
                  'this': '',
                  'balance': '',
                  'RejAcc': False,
               }
            return render(request, 'vacations\\vacations.html',context)
            
      else: # to update the edited record in the table 
            print("the update submitted")
            print("session previousnodays:", request.session['prevnodays'])
 
            vacation = Vacation.objects.get(pk=id)
            from_date=  datetime.strptime(request.POST.get('from_date'),'%Y-%m-%d')
            to_date= datetime.strptime(request.POST.get('to_date'), '%Y-%m-%d')
            vacation.nodays = RequestedVac(from_date,to_date)              
            form = VacationForm(request.POST, instance = vacation)  
            if form.is_valid():
               if Decimal(request.session["prevnodays"] != vacation.nodays):                
                  els = EmployeeLeaveStat.objects.filter(employee = vacation.employee)               
                  idy = els[0].id
                  updEls = EmployeeLeaveStat.objects.get(id= idy )                                
                  updEls.daystaken_current += (vacation.nodays - Decimal(request.session["prevnodays"]))
                  updEls.save()             

               vacation.save()               
               return redirect('list_vacations')
            else:
                print('Invalid form')
                return redirect('list_vacations')
                
   else:   # GET request
         print("GET")
         if id == 0 : # to open a blank from
            if request.user.username != "adminuser":         
              form = VacationForm(dep_id=request.user.department)
            else: 
              form = VacationForm()   
              
            context = {
               'form':form,
               'updEls':{}, 
               'annual': '',
               'this': '',
               'balance': '',
               'RejAcc': False,
            }
         
         else: # to populate the form with the data needed to be updated

            vacation = Vacation.objects.get(pk=id)
            request.session['prevnodays'] = str(vacation.nodays)
            if (vacation.approval_position == 1 and vacation.first_approval==request.user) or (
                 vacation.approval_position == 2 and vacation.second_approval==request.user) or(
                 vacation.approval_position == 3 and vacation.third_approval==request.user) or ( 
                 vacation.approval_position == 4 and vacation.fourth_approval==request.user) or request.user.username=="adminuser" : 

            
               form = VacationForm(instance=vacation)          
               els = EmployeeLeaveStat.objects.filter(employee = vacation.employee.id)                         
               idy = els[0].id
               updEls = EmployeeLeaveStat.objects.get(id= idy )                    

                     
               if request.user.id == getAppEmp(vacation):
                  RejAcc = True
               else:
                  RejAcc = False   

               context = {
                        'form':form,
                        'updEls':updEls, 
                        'annual': updEls.total_annual,
                        'this': vacation.nodays,
                        'sofar':vacation.sofar,
                        'balance': updEls.total_annual -(vacation.sofar)-(vacation.nodays),
                        'vac' : vacation,
                        'RejAcc': RejAcc,
                        }    
            else:
                messages.warning(request, 'Not Allowed to edit ...')
                return redirect('list_vacations')
                           
   return render(request, 'vacations\\vacations.html', context)

def getAppEmp(vac):
   if vac.approval_position == 1 :
      return vac.first_approval.id
   elif vac.approval_position == 2:
      return vac.second_approval.id
   elif vac.approval_position == 3:
      return vac.third_approval.id
   elif vac.approval_position == 4:
      return vac.fourth_approval.id

#    -------------------------------------------     D E L E T E   V A C A T I O N    
@login_required(login_url='login')
def vacation_delete(request,id):
   vac = Vacation.objects.get(id=id)
   if (vac.approval_position == 1 and vac.first_approval==request.user) or (
                 vac.approval_position == 2 and vac.second_approval==request.user) or(
                 vac.approval_position == 3 and vac.third_approval==request.user) or ( 
                 vac.approval_position == 4 and vac.fourth_approval==request.user) or request.user.username=="adminuser": 
         
        if request.method == "POST":
        
         no_of_days = vac.nodays
         leaveId = vac.leave_stat_id
         vacid  = vac.id
         updEls = EmployeeLeaveStat.objects.get(id= vac.leave_stat_id.id )               
         updEls.daystaken_current -= vac.nodays
         updEls.save()               
         vac.delete()
           
         UpdVac = Vacation.objects.filter(leave_stat_id = leaveId)
            
         for updvac in UpdVac:
               if updvac.id > vacid:
      #          print(updvac.id)
                  updvac.sofar -= no_of_days 
                  updvac.save()
         return redirect('list_vacations')      
      
   else:
     print("CANNOT DELETE")
     messages.warning(request, 'Not Allowed to Delete ...')
     return redirect('list_vacations')
        
         
   return render(request,'vacations/vacation_delete.html',{'vac': vac}) 

@login_required(login_url='login')
def workflow(request, id):
     vac = Vacation.objects.get(id=id)
     return render(request,
                  'vacations/workflow.html',
                  {'vac': vac}) 

#    -------------------------------------------      A P P R O V E    V A C A T I O N 
@login_required(login_url='login')
def vacation_approve(request, id):   
   vac = Vacation.objects.get(id=id) 

   if vac.approval_position == 1 :
      vac.first_app_status = 1
      vac.approval_position = 2
      vac.first_app_date = datetime.now()
   elif  vac.approval_position == 2 : 
      vac.second_app_status = 1
      vac.approval_position = 3
      vac.second_app_date = datetime.now()
   elif  vac.approval_position == 3 : 
      vac.third_app_status = 1
      vac.approval_position = 4
      vac.third_app_date = datetime.now()
   elif  vac.approval_position == 4 :     
      vac.fourth_app_status = 1
      vac.fourth_app_date = datetime.now()
      vac.status = 1       
   vac.save()
   return redirect('list_vacations') 

#    -------------------------------------------      R E J E C T    V A C A T I O N 
@login_required(login_url='login')
def vacation_reject(request, id):   
   vac = Vacation.objects.get(id=id) 
   vac.status = 2 
   no_of_days = vac.nodays
   vacid = vac.id
  
   ELS = EmployeeLeaveStat.objects.get(id = vac.leave_stat_id.id)   
   ELS.daystaken_current -= vac.nodays
   ELS.save()
   vac.save()

   UpdVac = Vacation.objects.filter(leave_stat_id = vac.leave_stat_id.id)
   for updvac in UpdVac:
            if updvac.id > vacid:     
               updvac.sofar -= no_of_days 
               updvac.save()

   return redirect('list_vacations') 



def RequestedVac( from_date , to_date):
 
   excluded = (6, 7)
   days = 0
   while from_date <= to_date:
            if from_date.isoweekday() not in excluded: #if you want to get only weekdays
                days += 1
            from_date+= timedelta(days=1)
   return days

#    -------------------------------------------    NOT USED
@login_required(login_url='login')
def single_vacation(request, id):
  vac = Vacation.objects.get(id=id)
  context = {
     'vac' : vac
  }
  return render(request, 'vacations\\single_vacationPDF.html',context)

#    -------------------------------------------     V A C A T I O N    R E P O R T   P D F
@login_required(login_url='login')
def single_vacationPDF(request, id):
  os.add_dll_directory(r"C:/Program Files/GTK3-Runtime Win64/bin")

  response = HttpResponse(content_type='application/pdf')
  response['Content-Disposition'] = 'inline; filename=Vacation'+ str(datetime.now) + '.pdf'
  response['Content-Transfer-Encoding'] = 'binary'


  vac = Vacation.objects.get(id=id)
  els = EmployeeLeaveStat.objects.filter(employee = vac.employee.id)
 
  if els.exists():                         
   idy = els[0].id  
   updEls = EmployeeLeaveStat.objects.get(id= idy )  
   # if updEls.daystaken_current == 0:
   #     y = 0
   # else:
   #    y=vac.nodays 

   # sofar =   updEls.daystaken_current - y    

   context = {
      'vac' : vac,
      'updEls':updEls, 
      'annual': updEls.total_annual,
      'this': vac.nodays,
      'sofar':vac.sofar,
      'balance': (updEls.total_annual)-(vac.sofar)-(vac.nodays)
   }
  else:
        context = {
               'vac':vac,
               'updEls':{}, 
               'annual': '',
               'this': '',
               'balance': ''
            }   
  html_string = render_to_string('vacations\\single_vacationPDF.html', context)
  html=HTML(string=html_string, base_url=request.build_absolute_uri())
  result= html.write_pdf(response , presentational_hints=True)
  return response  

  with tempfile.NamedTemporaryFile(delete=True) as output:
     output.write(result)
     output.flush()
     print(output.name)
     output.seek(0)
     response.write(output.read())

  return response  
#    -------------------------------------------      E N T I T L E M E N T  M A I N  F O R M 
@login_required(login_url='login')  
def entitlement(request, em=0):
  
   if request.GET.get('employee') is not None:
    em = request.GET.get('employee')
   FilterDepList= GetFilterDepList(request.user)
   emps = Account.objects.filter(department__name__in=FilterDepList).order_by("username")
   entitlement = EmployeeLeaveStat.objects.filter(employee=em)
   context = { 
      'selected_emp':int(em),
      'emps': emps,
      'entitlement': entitlement
   }       
   return render(request, 'vacations\\entitlement.html', context)

#    -------------------------------------------      E N T I T L E M E N T  S U B   F O R M 
@login_required(login_url='login')
@permission_required("NormalUser", raise_exception=True)
def entform(request, id, empl):
    if request.method == "POST":
       if id == 0: # to create a new record and append it to the table  
            print("create new record")
            form = EntitlementForm(request.POST)
            if form.is_valid():   
               employee = Account.objects.get(id=empl)  
               employee.has_vac_ent = True               
               description= form.cleaned_data['description']
               current_year= form.cleaned_data['current_year']
               previous_year= form.cleaned_data['previous_year']
               daystaken_current = form.cleaned_data['daystaken_current']             
               total_annual = current_year + previous_year
               entitlement = EmployeeLeaveStat.objects.create(employee=employee , description = description , current_year = current_year, previous_year= previous_year,
                                                            daystaken_current=daystaken_current, total_annual = total_annual  )
               entitlement.save()               
               employee.save()
               return redirect('entitlement', employee.id)
            else:
                return HttpResponse('invalid form')
            
       else: # to update the edited record in the table
            print("the update submitted")
            employee = Account.objects.get(id=empl)  
            entitlement = EmployeeLeaveStat.objects.get(pk=id)
            form = EntitlementForm(request.POST, instance = entitlement)  
            if form.is_valid():
               form.save()
               return redirect('entitlement', employee.id)
            else:
                print('Invalid form')
                return redirect('entitlement', employee.id)
                
    else:   # GET
         if id == 0 : # to open a blank from          
            form = EntitlementForm()
            context = {
                     'form':form,
                     'employee':'', 
                  }
            
         else: # to populate the form with the data needed to be updated
            entitlement = EmployeeLeaveStat.objects.get(pk=id)
            form = EntitlementForm(instance=entitlement)
            employee = Account.objects.get(id=empl)
         
            context = {
                     'form':form,
                     'employee':employee, 
                  }
    
         return render(request, 'vacations\\ent_form.html', context)

   
#    -------------------------------------------     D E L E T E   E N T I T L E M E N T 
@login_required(login_url='login')
@permission_required("NormalUser", raise_exception=True)
def ent_delete(request, id):
      entitlement = EmployeeLeaveStat.objects.get(id=id)
      emp = Account.objects.get(id=entitlement.employee.id)      
      emp.has_vac_ent = False
      emp.save()
      if request.method == "POST":
         entitlement.delete()
         return redirect('entitlement', entitlement.employee.id)
      
      return render(request,
                  'vacations/entitlement_delete.html',
                  {'ent': entitlement}) 

   