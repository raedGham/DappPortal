from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from dapp.utils import GetFilterDepList
from .forms import LogForm
from log.models import Log
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date
from accounts.models import Account
from datetime import datetime
# Create your views here.

 #--------------------------------------------------------------------------    L O G  L I S T
@login_required(login_url='login')
def log_list(request):
    # Pagination

      # set up pagination
   name_search = request.GET.get('name_search')
   PSno_search = request.GET.get('PSno_search')  
   S_fromdate = request.GET.get('S_fromdate')  
   S_todate = request.GET.get('S_todate') 
   request.session["name_search"] = name_search 
   request.session["PSno_search"] = PSno_search
   FilterDepList = GetFilterDepList(request.user)
   # sortby = request.GET.get('sortby')
   sortby = "-id"

   if sortby is not None:
    data = Log.objects.filter(employee__department__name__in=FilterDepList).order_by(sortby)
   else:
    data = Log.objects.filter(employee__department__name__in=FilterDepList)     

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
      data = data.filter(log_date__range=[parse_date(S_fromdate), parse_date(S_todate)])
     else:      
      data = data.filter(log_date__range=[parse_date(S_fromdate), parse_date(S_todate)])   

   p = Paginator(data,20)
   page = request.GET.get('page')
   p_log = p.get_page(page)

    
    
   if request.GET.get('employee') is not None:
      selected_emp = request.GET.get('employee')
   else:
      selected_emp=-1 

   
   if request.GET.get('otdate') is not None:
      selected_date = request.GET.get('otdate')
   else:
      selected_date=datetime.now().strftime("%Y-%m-%d")
      print("selected Date=", selected_date) 
      print(type(selected_date))           
    
   FilterDepList= GetFilterDepList(request.user)
   emps = Account.objects.filter(department__name__in=FilterDepList).order_by("username")
  

     

   
  




   context={
      'p_log':p_log,
      'emps' :emps,
      'selected_emp':int(selected_emp),
      'selected_date':selected_date,
      
    }
   return render(request, 'log/log_list.html', context)



#    -------------------------------------------     A D D / E D I T   L O G S
@login_required(login_url='login')
def logs(request, id=0):
     
     if request.method == "POST":
       if id == 0: # to create a new record and append it to the table            
            form = LogForm(request.POST, request.FILES)
            if form.is_valid():
               employee= form.cleaned_data['employee']
               log_date= form.cleaned_data['log_date']
               log_time= form.cleaned_data['logtime']                 
               description  = form.cleaned_data['description']
               log = Log.objects.create(employee=employee,log_date=log_date,log_time=log_time,description=description)      
               log.save()
               
               return redirect('list_log')
            else: 
               context = {
               'form':form,
               
            }
               return render(request, 'log\\log.html',context)
            
       else: # to update the edited record in the table
            print("the update submitted")
            log = Log.objects.get(pk=id)
             
                        
            form = LogForm(request.POST,request.FILES, instance = log)  
            if form.is_valid():
               log.save()
               return redirect('log_list')
            else:
                print('Invalid form')
                return redirect('list_medreps')
                
     else:   # GET request
         if id == 0 : # to open a blank from
            if request.user.username != "adminuser":         
              form = LogForm(dep_id=request.user.department)
            else: 
              form = LogForm()   
              
            context = {
               'form':form,
             
            }
         
         else: # to populate the form with the data needed to be updated
            log = Log.objects.get(pk=id)
           
            form = LogForm(instance=log)          
                            

            
            
   
            context = {
               'form':form,
              
               }    
      
         return render(request, 'log\\log.html', context)