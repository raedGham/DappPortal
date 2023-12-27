from django.shortcuts import render,redirect,HttpResponse
from .forms import EmployeeAccountForm
from .models import Account,Department,Position
# import pagination stuff
from django.core.paginator import Paginator

# Create your views here.

def list_profiles(request):
   

   departments = Department.objects.all()
   positions = Position.objects.all()
   
   # set up pagination
   name_search = request.GET.get('name_search')
   PSno_search = request.GET.get('PSno_search')
   department_search  = request.GET.get('department_search')
   position_search = request.GET.get('position_search')

   data = Account.objects.all().order_by('ps_number')
     
   if name_search !='' and name_search is not None:
     data = data.filter(first_name__icontains= name_search)

   if PSno_search !='' and PSno_search is not None:
     data = data.filter(ps_number__icontains= PSno_search)

   if department_search !='' and department_search !='Select Dep...' and department_search is not None:
     data = data.filter(department= department_search)
   
   if position_search !='' and position_search != 'Select Pos...'  and position_search is not None:
     data = data.filter(position = position_search)  

   for d in data:
       print(d.first_name)

   p = Paginator(data,20)
   page = request.GET.get('page')
   p_profiles = p.get_page(page)
   

   context = { 'p_profiles':p_profiles, 'departments':departments,'positions':positions}
   return render(request,"profiles\profiles_list.html", context)


def profiles(request, id = 0):
 
 if request.method == "POST":
       if id == 0: # to create a new record and append it to the table  
            print("create new record")
            form = EmployeeAccountForm(request.POST)
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
               # profile_pic = form.cleaned_data['profile_pic']
             
                profile = Account.objects.create(first_name=first_name, middle_name=middle_name, last_name=last_name,
                                                 phone_number=phone_number,email=email, username=username, password = password,
                                                 ps_number=ps_number,financial_number=financial_number,nssf_number=nssf_number,
                                                 work_start_date=work_start_date,work_finish_date=work_finish_date,
                                                 department=department,position=position,head_dep=head_dep, remarks = remarks,
                                                 address= address)
                profile.save()
                return redirect('list_profiles')
            else:
                return HttpResponse('invalid form')
            
       else: # to update the edited record in the table
            print("the update submitted")
            profile = Account.objects.get(pk=id)
         
            form = EmployeeAccountForm(request.POST, instance = profile)  
            if form.is_valid():
               profile.save()
               return redirect('list_profiles')
            else:
                return redirect('list_profiles')
                
 else:   # GET
         if id == 0 : # to open a blank from
            form = EmployeeAccountForm()
         else: # to populate the form with the data needed to be updated
            profile = Account.objects.get(pk=id)
           
            form = EmployeeAccountForm(instance=profile)

         context = {
                    'form':form,
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
 
