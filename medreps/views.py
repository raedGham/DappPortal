from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from medreps.models import Medrep, EmployeeMedLeaveStat
from django.core.paginator import Paginator
from .forms import MedrepForm, EntitlementMedForm
from datetime import timedelta, datetime
from django.conf import settings
from pathlib import Path
from accounts.models import Account
from positions.models import Position
from django.utils.dateparse import parse_date
from dapp.utils import GetFilterDepList, SetWorkflow
from django.http import FileResponse, Http404
# imports for pdf generator
import os
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from  django.db.models import Sum

#--------------------------------------------------------------------------    P D F  M E D R E P  L I S T   
@login_required(login_url='login')
def medrepListPDF(request):
  os.add_dll_directory(r"C:/Program Files/GTK3-Runtime Win64/bin")
  response = HttpResponse(content_type='application/pdf')
  response['Content-Disposition'] = 'inline; filename=Vacation'+ str(datetime.now) + '.pdf'
  response['Content-Transfer-Encoding'] = 'binary'
  name_search = request.session["name_search"]
  PSno_search = request.session["PSno_search"]
  
  data = Medrep.objects.all()
  if name_search !='' and name_search is not None:
    data = Medrep.objects.filter(employee__first_name__icontains=name_search )
  if PSno_search !='' and PSno_search is not None:
    data = Medrep.objects.filter(employee__ps_number__icontains= PSno_search)
  context = {
      'medreps' : data ,      
   }
  
  html_string = render_to_string('medreps\\medrepListPDF.html', context)
  html=HTML(string=html_string, base_url=request.build_absolute_uri())
  result= html.write_pdf(response , presentational_hints=True)
  return response     


#    -------------------------------------------     M E D R E P S   L I S T
@login_required(login_url='login')
def list_medreps(request):
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
    data = Medrep.objects.filter(employee__department__name__in=FilterDepList).order_by(sortby)
   else:
    data = Medrep.objects.filter(employee__department__name__in=FilterDepList)     


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
      data = data.filter(medrep_date__range=[parse_date(S_fromdate), parse_date(S_todate)]).order_by(sortby)
     else:      
      data = data.filter(medrep_date__range=[parse_date(S_fromdate), parse_date(S_todate)])   
 

   
   p = Paginator(data,20)
   page = request.GET.get('page')
   p_medreps = p.get_page(page)

 # calculate canDel

   canDelete=[]
  
   for medrep in data:

       if  request.user.username == 'adminuser' and medrep.status not in [1,2]:
         canDelete.append(medrep.id)

       if       (medrep.approval_position == 1 and medrep.first_approval==request.user) or (
                 medrep.approval_position == 2 and medrep.second_approval==request.user) or(
                 medrep.approval_position == 3 and medrep.third_approval==request.user) or ( 
                 medrep.approval_position == 4 and medrep.fourth_approval==request.user): 
          
          canDelete.append(medrep.id)


   context = { 
               'p_medreps':p_medreps, 
               'canDelete':canDelete,              
               }
   return render(request,"medreps\\medreps_list.html", context)

#    -------------------------------------------     A D D / E D I T   M E D R E P
@login_required(login_url='login')
def medreps(request, id=0):
     
     if request.method == "POST":
       if id == 0: # to create a new record and append it to the table            
            form = MedrepForm(request.POST, request.FILES)
            if form.is_valid():
               employee= form.cleaned_data['employee']
               medrep_date= form.cleaned_data['medrep_date']
               from_date= form.cleaned_data['from_date']
               to_date= form.cleaned_data['to_date']
               nodays= form.cleaned_data['nodays'] 
               pdf_attachment=form.cleaned_data['pdf_attachment']         
               description  = form.cleaned_data['description']
               
               x = RequestedVac(from_date, to_date)
           
               # set medrep Approval Workflow
               first_app, second_app, third_app, fourth_app = SetWorkflow(employee)                               
                              
               medrep = Medrep.objects.create(employee=employee,medrep_date=medrep_date,from_date=from_date, to_date=to_date,
                                                   nodays=x,description=description, pdf_attachment=pdf_attachment)      
               medrep.save()
               if first_app is not None:
                 medrep.first_approval = first_app
                 medrep.approval_position = 1
               else:  
                 medrep.first_app_status=1
                 medrep.approval_position = 2
                 
               if second_app is not None:
                 medrep.second_approval = second_app                  
               else:
                 medrep.first_app_status=1
                 medrep.second_app_status=1
                 medrep.approval_position = 3

               if third_app is not None:
                 medrep.third_approval = third_app
               if fourth_app is not None:
                 medrep.fourth_approval = fourth_app   
               medrep.save()  
               # update EmployeeLeaveStat 
             
               els = EmployeeMedLeaveStat.objects.filter(employee = employee)               
               idy = els[0].id
               updEls = EmployeeMedLeaveStat.objects.get(id= idy )               
               updEls.daystaken_current += x
               updEls.save()            
               return redirect('list_medreps')
            else: 
               context = {
               'form':form,
               'updEls':{}, 
               'annual': '',
               'this': '',
               'balance': '',
               'RejAcc': False,
            }
               return render(request, 'medreps\\medreps.html',context)
            
       else: # to update the edited record in the table
            print("the update submitted")
            medrep = Medrep.objects.get(pk=id)
            from_date=  datetime.strptime(request.POST.get('from_date'),'%Y-%m-%d')
            to_date= datetime.strptime(request.POST.get('to_date'), '%Y-%m-%d')
            medrep.nodays = RequestedVac(from_date,to_date)     
                        
            form = MedrepForm(request.POST,request.FILES, instance = medrep)  
            if form.is_valid():
               medrep.save()
               return redirect('list_medreps')
            else:
                print('Invalid form')
                return redirect('list_medreps')
                
     else:   # GET request
         if id == 0 : # to open a blank from
            if request.user.username != "adminuser":         
              form = MedrepForm(dep_id=request.user.department)
            else: 
              form = MedrepForm()   
              
            context = {
               'form':form,
               'updEls':{}, 
               'annual': '',
               'this': '',
               'balance': '',
               'RejAcc': False,
            }
         
         else: # to populate the form with the data needed to be updated
            medrep = Medrep.objects.get(pk=id)
           
            form = MedrepForm(instance=medrep)          
            els = EmployeeMedLeaveStat.objects.filter(employee = medrep.employee.id)                         
            idy = els[0].id
            updEls = EmployeeMedLeaveStat.objects.get(id= idy )                    

            
            if request.user.id == getAppEmp(medrep):
               RejAcc = True
            else:
               RejAcc = False   
   
            context = {
               'form':form,
               'updEls':updEls, 
               'annual': updEls.current_year,
               'this': medrep.nodays,
               'balance': (updEls.current_year)-(updEls.daystaken_current+medrep.nodays),
               'medrep' : medrep,
               'RejAcc': RejAcc,
               }    
      
         return render(request, 'medreps\\medreps.html', context)
     
def pdf_view(request,id):
    medrep = Medrep.objects.get(pk=id)
   # return HttpResponse(medrep.pdf_attachment.name)
    if medrep.pdf_attachment.name is not None and  medrep.pdf_attachment.name !="":
      return FileResponse(open("media/"+ str(medrep.pdf_attachment), 'rb'), content_type='application/pdf')
    else:
      return HttpResponse("No Attachment...")
       
 

def getAppEmp(med):
   if med.approval_position == 1 :
      return med.first_approval.id
   elif med.approval_position == 2:
      return med.second_approval.id
   elif med.approval_position == 3:
      return med.third_approval.id
   elif med.approval_position == 4:
      return med.fourth_approval.id

#    -------------------------------------------     D E L E T E   M E D R E P   
@login_required(login_url='login')
def medrep_delete(request,id):
      medrep = Medrep.objects.get(id=id)
      if request.method == "POST":                
         medrep.delete()
         return redirect('list_medreps')
      
      return render(request,
                  'medreps/medrep_delete.html',
                  {'medrep': medrep}) 

@login_required(login_url='login')
def workflow(request, id):
     medrep = Medrep.objects.get(id=id)
     return render(request,
                  'medreps/workflow.html',
                  {'medrep': medrep}) 

#    -------------------------------------------      A P P R O V E    M E D R E P
@login_required(login_url='login')
def medrep_approve(request, id):   
   med = Medrep.objects.get(id=id) 

   if med.approval_position == 1 :
      med.first_app_status = 1
      med.approval_position = 2
      med.first_app_date = datetime.now()
   elif  med.approval_position == 2 : 
      med.second_app_status = 1
      med.approval_position = 3
      med.second_app_date = datetime.now()
   elif  med.approval_position == 3 : 
      med.third_app_status = 1
      med.approval_position = 4
      med.third_app_date = datetime.now()
   elif  med.approval_position == 4 :     
      med.fourth_app_status = 1
      med.fourth_app_date = datetime.now()
      med.status = 1       
   med.save()
   return redirect('list_medreps') 

#    -------------------------------------------      R E J E C T     M E D R E P 
@login_required(login_url='login')
def medrep_reject(request, id):   
   med = Medrep.objects.get(id=id) 
   med.status = 2 
   emplleavestatList = EmployeeMedLeaveStat.objects.filter(employee=med.employee)
   ide = emplleavestatList[0].id
   ELS = EmployeeMedLeaveStat.objects.get(id=ide)
   ELS.daystaken_current -= med.nodays
   ELS.save()
   med.save()
   return redirect('list_medreps') 



def RequestedVac( from_date , to_date):
 
 #  excluded = (6, 7)
   days = 0
   while from_date <= to_date:
      #      if from_date.isoweekday() not in excluded: #if you want to get only weekdays
            days += 1
            from_date+= timedelta(days=1)
   return days

#    -------------------------------------------    NOT USED
@login_required(login_url='login')
def single_medrep(request, id):
  med = Medrep.objects.get(id=id)
  context = {
     'med' : med
  }
  return render(request, 'medreps\\single_medrepPDF.html',context)

#    -------------------------------------------     M E D    R E P O R T   P D F
@login_required(login_url='login')
def single_medrepPDF(request, id):
  os.add_dll_directory(r"C:/Program Files/GTK3-Runtime Win64/bin")

  response = HttpResponse(content_type='application/pdf')
  response['Content-Disposition'] = 'inline; filename=medrep'+ str(datetime.now) + '.pdf'
  response['Content-Transfer-Encoding'] = 'binary'


  med = Medrep.objects.get(id=id)
  els = EmployeeMedLeaveStat.objects.filter(employee = med.employee.id)
 
  if els.exists():                         
   idy = els[0].id  
   updEls = EmployeeMedLeaveStat.objects.get(id= idy )  
   context = {
      'med' : med,
      'updEls':updEls, 
      'annual': updEls.current_year,
      'this': med.nodays,
      'balance': (updEls.current_year )-(updEls.daystaken_current+med.nodays)
   }
  else:
        context = {
               'med':med,
               'updEls':{}, 
               'annual': '',
               'this': '',
               'balance': ''
            }   
  html_string = render_to_string('medreps\\single_medrepPDF.html', context)
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
def med_entitlement(request, em=0):
  
   if request.GET.get('employee') is not None:
    em = request.GET.get('employee')
   FilterDepList= GetFilterDepList(request.user)
   emps = Account.objects.filter(department__name__in=FilterDepList).order_by("username")
   entitlement = EmployeeMedLeaveStat.objects.filter(employee=em)
   context = { 
      'selected_emp':int(em),
      'emps': emps,
      'entitlement': entitlement
   }       
   return render(request, 'medreps\\med_entitlement.html', context)

#    -------------------------------------------      E N T I T L E M E N T  S U B   F O R M 
@login_required(login_url='login')
@permission_required("NormalUser", raise_exception=True)
def med_entform(request, id, empl):
    if request.method == "POST":
       if id == 0: # to create a new record and append it to the table  
            print("create new record")
            form = EntitlementMedForm(request.POST)
            if form.is_valid():   
               employee = Account.objects.get(id=empl)  
               employee.has_med_ent = True               
               description= form.cleaned_data['description']
               current_year= form.cleaned_data['current_year']               
               daystaken_current = form.cleaned_data['daystaken_current']             
            
               entitlement = EmployeeMedLeaveStat.objects.create(employee=employee , description = description , current_year = current_year,
                                                            daystaken_current=daystaken_current )
               entitlement.save()               
               employee.save()
               return redirect('med_entitlement', empl)
            else:
                return HttpResponse('invalid form')
            
       else: # to update the edited record in the table
            print("the update submitted")
            employee = Account.objects.get(id=empl)  
            entitlement = EmployeeMedLeaveStat.objects.get(pk=id)
            form = EntitlementMedForm(request.POST, instance = entitlement)  
            if form.is_valid():
               form.save()
               return redirect('med_entitlement', employee.id)
            else:
                print('Invalid form')
                return redirect('med_entitlement', employee.id)
                
    else:   # GET
         if id == 0 : # to open a blank from          
            form = EntitlementMedForm()
            context = {
                     'form':form,
                     'employee':'',
                     'empl':empl 
                  }
            
         else: # to populate the form with the data needed to be updated
            entitlement = EmployeeMedLeaveStat.objects.get(pk=id)
            form = EntitlementMedForm(instance=entitlement)
            employee = Account.objects.get(id=empl)
         
            context = {
                     'form':form,
                     'employee':employee, 
                  }
    
         return render(request, 'medreps\\med_ent_form.html', context)

   
#    -------------------------------------------     D E L E T E   E N T I T L E M E N T 
@login_required(login_url='login')
@permission_required("NormalUser", raise_exception=True)
def med_ent_delete(request, id):
      entitlement = EmployeeMedLeaveStat.objects.get(id=id)
      emp = Account.objects.get(id=entitlement.employee.id)      
      emp.has_med_ent = False
      emp.save()
      if request.method == "POST":
         entitlement.delete()
         return redirect('med_entitlement', entitlement.employee.id)
      
      return render(request,
                  'medreps/med_entitlement_delete.html',
                  {'ent': entitlement}) 

   