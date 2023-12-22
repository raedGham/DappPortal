from django.shortcuts import render,redirect
from .forms import EmployeeAccountForm
from .models import Account
# Create your views here.

def list_profiles(request):
   profiles = Account.objects.all()
   context = { 'profiles': profiles}
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
                profile_pic = form.cleaned_data['profile_pic']
             
                profile = Account.objects.create(first_name=first_name, middle_name=middle_name, last_name=last_name,
                                                 phone_number=phone_number,email=email, username=username, password = password,
                                                 ps_number=ps_number,financial_number=financial_number,nssf_number=nssf_number,
                                                 work_start_date=work_start_date,work_finish_date=work_finish_date,
                                                 department=department,position=position,head_dep=head_dep, remarks = remarks,
                                                 address= address, profile_pic= profile_pic)
                profile.save()
                return redirect('list_profiles')
            
       else: # to update the edited record in the table
            print("the update submitted")
            profile = Account.objects.get(pk=id)
            form = EmployeeAccountForm(request.POST, instance = profile)  
            if form.is_valid():
               profile.save()
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