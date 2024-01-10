from django.shortcuts import render,redirect,HttpResponse
from .forms import EmployeeAccountForm
from .models import Account,Department,Position
from django.contrib import messages
# import pagination stuff
from django.core.paginator import Paginator
# imports for pdf generator
import os
from django.template.loader import render_to_string
from weasyprint import HTML
from datetime import datetime

# Create your views here.
def profilesPDF(request):
  
  os.add_dll_directory(r"C:/Program Files/GTK3-Runtime Win64/bin")
  response = HttpResponse(content_type='application/pdf')
  response['Content-Disposition'] = 'inline; filename=Vacation'+ str(datetime.now) + '.pdf'
  response['Content-Transfer-Encoding'] = 'binary'


  accounts= Account.objects.all()
   
  context = {
      'accounts' : accounts ,      
   }
  
  html_string = render_to_string('profiles\\profilesPDF.html', context)
  html=HTML(string=html_string, base_url=request.build_absolute_uri())
  result= html.write_pdf(response , presentational_hints=True)
  return response  

   
def hierarchy(request):
   em = request.GET.get('employee')
   
   emps = Account.objects.all()
   team = Account.objects.filter(head_dep=em)
   context = { 
      'emps': emps,
      'team': team,

   }
   return render(request, 'profiles\\hierarchy.html',context)
def list_profiles(request):
 
   departments = Department.objects.all()
   positions = Position.objects.all()
   
   # set up pagination
   name_search = request.GET.get('name_search')
   PSno_search = request.GET.get('PSno_search')
   department_search  = request.GET.get('department_search')
   position_search = request.GET.get('position_search')
   
   sortby = request.GET.get('sortby')
   print(sortby)
   if sortby is not None:
    data = Account.objects.all().order_by(sortby)
   else:
    data = Account.objects.all()     


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
   p_profiles = p.get_page(page)
   

   context = { 'p_profiles':p_profiles, 'departments':departments,'positions':positions}
   return render(request,"profiles\profiles_list.html", context)


def profiles(request, id = 0):
 
 if request.method == "POST":
       if id == 0: # to create a new record and append it to the table  
            print("create new record")
            form = EmployeeAccountForm(request.POST, request.FILES)
            if form.is_valid():
                first_name= form.cleaned_data['first_name']
                middle_name= form.cleaned_data['middle_name']
                last_name= form.cleaned_data['last_name']
                phone_number = form.cleaned_data['phone_number']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                username = email.split('@')[0]
                ps_number =form.cleaned_data['ps_number']
                financial_number=form.cleaned_data['financial_number']
                nssf_number= form.cleaned_data['nssf_number']
                work_start_date= form.cleaned_data['work_start_date']
                work_finish_date= form.cleaned_data['work_finish_date']
                department= form.cleaned_data['department']
                position= form.cleaned_data['position']
                head_dep= form.cleaned_data['head_dep']
                remarks= form.cleaned_data['remarks']
                address= form.cleaned_data['address']
                profile_pic = form.cleaned_data['profile_pic']
             
                profile = Account.objects.create(first_name=first_name, middle_name=middle_name, last_name=last_name,
                                                 phone_number=phone_number,email=email, username=username, password = password,
                                                 ps_number=ps_number,financial_number=financial_number,nssf_number=nssf_number,
                                                 work_start_date=work_start_date,work_finish_date=work_finish_date,
                                                 department=department,position=position,head_dep=head_dep, remarks = remarks,
                                                 address= address, profile_pic=profile_pic)
                profile.save()
               #  messages.success(request, "New Employee Account saved successfully")
                return redirect('list_profiles')
            else:
                return HttpResponse('invalid form')
            
       else: # to update the edited record in the table
            print("the update submitted")
            profile = Account.objects.get(pk=id)
         
            form = EmployeeAccountForm(request.POST, request.FILES,instance = profile)  
            if form.is_valid():
               profile.save()
               # messages.success(request, "Employee Account updated successfully")
               return redirect('list_profiles')
            else:
                return redirect('list_profiles')
                
 else:   # GET
         if id == 0 : # to open a blank from
            form = EmployeeAccountForm()
            img = ""
         else: # to populate the form with the data needed to be updated
            profile = Account.objects.get(pk=id)           
            form = EmployeeAccountForm(instance=profile)
            if profile.profile_pic:
              img = profile.profile_pic.url
            else:
              img =""

         print(img)   
         context = {
                    'form':form,
                    'img': img,
               }
    
         return render(request, 'profiles\profiles.html', context)
 

def profile_delete(request, id):
      profile = Account.objects.get(id=id)
      if request.method == "POST":
         profile.delete()
         return redirect('list_profiles')
      
      return render(request,
                  'profiles/profile_delete.html',
                  {'profile': profile}) 
 
