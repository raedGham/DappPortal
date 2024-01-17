from django.shortcuts import render,redirect,HttpResponse
from vacations.models import Vacation, EmployeeLeaveStat
from django.core.paginator import Paginator
from .forms import VacationForm, EntitlementForm
from datetime import timedelta, datetime
from django.conf import settings
from pathlib import Path
from accounts.models import Account
from positions.models import Position
from django.utils.dateparse import parse_date

# imports for pdf generator
import os
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from  django.db.models import Sum

# Create your views here.
def list_vacations(request):
#    departments = Department.objects.all()
#    positions = Position.objects.all()
   
   # set up pagination
   name_search = request.GET.get('name_search')
   PSno_search = request.GET.get('PSno_search')
   S_fromdate = request.GET.get('S_fromdate')  
   S_todate = request.GET.get('S_todate') 

  

   # sortby = request.GET.get('sortby')
   sortby = "-id"

   if sortby is not None:
    data = Vacation.objects.all().order_by(sortby)
   else:
    data = Vacation.objects.all()     


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

   print(S_fromdate)
   print(type(S_fromdate))

   if S_fromdate is not None and S_todate is not None and S_fromdate != '' and S_todate != '':
     if sortby is not None:    
      data = data.filter(vac_date__range=[parse_date(S_fromdate), parse_date(S_todate)]).order_by(sortby)
     else:      
      data = data.filter(vac_date__range=[parse_date(S_fromdate), parse_date(S_todate)])   
 

   
   p = Paginator(data,20)
   page = request.GET.get('page')
   p_vacations = p.get_page(page)
   

   context = { 'p_vacations':p_vacations,}
   return render(request,"vacations\\vacations_list.html", context)



def vacations(request, id=0):
     
     if request.method == "POST":
       if id == 0: # to create a new record and append it to the table  
            print("create new record")
            form = VacationForm(request.POST)
            if form.is_valid():
               employee= form.cleaned_data['employee']
               vac_date= form.cleaned_data['vac_date']
               from_date= form.cleaned_data['from_date']
               to_date= form.cleaned_data['to_date']
               nodays= form.cleaned_data['nodays']
               ampm  = form.cleaned_data['ampm']
               remarks  = form.cleaned_data['remarks']
               
               x = RequestedVac(from_date, to_date)
               print("create:"+ str(x))
               # set Vacation Approval Workflow
               if employee.is_head :
                     first_app = employee
               else:   
                     first_app = employee.head_dep
                
               second_app = first_app.head_dep
               third_app = Account.objects.get(position = Position.objects.get(title="Admin Head"))
               fourth_app = Account.objects.get(position = Position.objects.get(title="Superintendent"))
               
               
               vacation = Vacation.objects.create(employee=employee,vac_date=vac_date,from_date=from_date, to_date=to_date,
                                                  nodays=x,ampm=ampm, remarks=remarks, first_approval= first_app, 
                                                  second_approval= second_app,third_approval = third_app, fourth_approval = fourth_app)
              
               vacation.save()

               # update EmployeeLeaveStat 
             
               els = EmployeeLeaveStat.objects.filter(employee = employee)               
               idy = els[0].id
               updEls = EmployeeLeaveStat.objects.get(id= idy )               
               updEls.daystaken_current += x
               updEls.save()            
               return redirect('list_vacations')
            else:
                return HttpResponse('invalid form')
            
       else: # to update the edited record in the table
            print("the update submitted")
            vacation = Vacation.objects.get(pk=id)
            from_date=  datetime.strptime(request.POST.get('from_date'),'%Y-%m-%d')
            to_date= datetime.strptime(request.POST.get('to_date'), '%Y-%m-%d')
            vacation.nodays = RequestedVac(from_date,to_date)     
                        
            form = VacationForm(request.POST, instance = vacation)  
            if form.is_valid():
               vacation.save()
               return redirect('list_vacations')
            else:
                print('Invalid form')
                return redirect('list_vacations')
                
     else:   # GET
         if id == 0 : # to open a blank from
          
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
               'annual': updEls.current_year + updEls.previous_year,
               'this': vacation.nodays,
               'balance': (updEls.current_year + updEls.previous_year)-(updEls.daystaken_current+vacation.nodays),
               'vac' : vacation,
               'RejAcc': RejAcc,
               }    
      
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
   

def vacation_delete(request,id):
      vac = Vacation.objects.get(id=id)
      if request.method == "POST":                
         vac.delete()
         return redirect('list_vacations')
      
      return render(request,
                  'vacations/vacation_delete.html',
                  {'vac': vac}) 

def workflow(request, id):
     vac = Vacation.objects.get(id=id)
     return render(request,
                  'vacations/workflow.html',
                  {'vac': vac}) 



def vacation_approve(request, id):   
   vac = Vacation.objects.get(id=id) 

   if vac.approval_position == 1 :
      vac.first_app_status = 1
      vac.approval_position = 2
   elif  vac.approval_position == 2 : 
      vac.second_app_status = 1
      vac.approval_position = 3
   elif  vac.approval_position == 3 : 
      vac.third_app_status = 1
      vac.approval_position = 4
   elif  vac.approval_position == 4 : 
      print("Approval position = 4")
      vac.fourth_app_status = 1
      vac.status = 1
      

   
   vac.save()
   return redirect('list_vacations') 

def vacation_reject(request, id):   
   vac = Vacation.objects.get(id=id) 
   vac.status = 2 
   vac.save()
   return redirect('list_vacations') 

def test(request):
  vac = Vacation.objects.get(id=2)

  return HttpResponse(vac.getnod)


def RequestedVac( from_date , to_date):
 
   excluded = (6, 7)
   days = 0
   while from_date <= to_date:
            if from_date.isoweekday() not in excluded: #if you want to get only weekdays
                days += 1
            from_date+= timedelta(days=1)
   return days

 
def single_vacation(request, id):
  vac = Vacation.objects.get(id=id)
  context = {
     'vac' : vac
  }
  return render(request, 'vacations\\single_vacationPDF.html',context)

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
   context = {
      'vac' : vac,
      'updEls':updEls, 
      'annual': updEls.current_year + updEls.previous_year,
      'this': vac.nodays,
      'balance': (updEls.current_year + updEls.previous_year)-(updEls.daystaken_current+vac.nodays)
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

  
def entitlement(request, em=0):
  
   if request.GET.get('employee') is not None:
    em = request.GET.get('employee')
   
   emps = Account.objects.all()
   entitlement = EmployeeLeaveStat.objects.filter(employee=em)
   context = { 
      'selected_emp':int(em),
      'emps': emps,
      'entitlement': entitlement
   }       
   return render(request, 'vacations\\entitlement.html', context)


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
         else: # to populate the form with the data needed to be updated
            entitlement = EmployeeLeaveStat.objects.get(pk=id)
           
            form = EntitlementForm(instance=entitlement)


         employee = Account.objects.get(id=empl)
         
         context = {
                    'form':form,
                    'employee':employee, 
               }
    
         return render(request, 'vacations\\ent_form.html', context)

   


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

   