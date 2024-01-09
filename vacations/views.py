from django.shortcuts import render,redirect,HttpResponse
from vacations.models import Vacation, EmployeeLeaveStat
from django.core.paginator import Paginator
from .forms import VacationForm, EntitlementForm
from datetime import timedelta, datetime
from django.conf import settings
from pathlib import Path
from accounts.models import Account
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
   department_search  = request.GET.get('department_search')
   position_search = request.GET.get('position_search')
   
   sortby = request.GET.get('sortby')
   sortby = "-id"
   if sortby is not None:
    data = Vacation.objects.all().order_by(sortby)
   else:
    data = Vacation.objects.all()     


   if name_search !='' and name_search is not None:     
     if sortby is not None:
      data = data.filter(first_name__icontains= name_search).order_by(sortby)
     else:
      data = data.filter(first_name__icontains= name_search)   

   if PSno_search !='' and PSno_search is not None:
     if sortby is not None:
      data = data.filter(ps_number__icontains= PSno_search).order_by(sortby)
     else:
      data = data.filter(ps_number__icontains= PSno_search)   

   if department_search !='' and department_search !='Select Dep...' and department_search is not None:
     if sortby is not None:
      data = data.filter(department= department_search).order_by(sortby)
     else:
      data = data.filter(department= department_search)   

   
   if position_search !='' and position_search != 'Select Pos...'  and position_search is not None:
     if sortby is not None:
       data = data.filter(position = position_search).order_by(sortby)  
     else:
       data = data.filter(position = position_search)   

   
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
               
               vacation = Vacation.objects.create(employee=employee,vac_date=vac_date,from_date=from_date, to_date=to_date,
                                                  nodays=x,ampm=ampm, remarks=remarks)
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
               'balance': ''
            }

         else: # to populate the form with the data needed to be updated
            vacation = Vacation.objects.get(pk=id)
           
            form = VacationForm(instance=vacation)          
            els = EmployeeLeaveStat.objects.filter(employee = vacation.employee.id)                         
            idy = els[0].id
            updEls = EmployeeLeaveStat.objects.get(id= idy )        
           
   
            context = {
               'form':form,
               'updEls':updEls, 
               'annual': updEls.current_year + updEls.previous_year,
               'this': vacation.nodays,
               'balance': (updEls.current_year + updEls.previous_year)-(updEls.daystaken_current+vacation.nodays)
               }    
      
         return render(request, 'vacations\\vacations.html', context)


def vacation_delete(request,id):
      vac = Vacation.objects.get(id=id)
      if request.method == "POST":
         vac.delete()
         return redirect('list_vacations')
      
      return render(request,
                  'vacations/vacation_delete.html',
                  {'vac': vac}) 

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
  context = {
     'vac' : vac
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
               description= form.cleaned_data['description']
               current_year= form.cleaned_data['current_year']
               previous_year= form.cleaned_data['previous_year']
               daystaken_current = form.cleaned_data['daystaken_current']             
               total_annual = current_year + previous_year
               entitlement = EmployeeLeaveStat.objects.create(employee=employee , description = description , current_year = current_year, previous_year= previous_year,
                                                            daystaken_current=daystaken_current, total_annual = total_annual  )
               entitlement.save()
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
      
      if request.method == "POST":
         entitlement.delete()
         return redirect('entitlement', entitlement.employee.id)
      
      return render(request,
                  'vacations/entitlement_delete.html',
                  {'ent': entitlement}) 

   