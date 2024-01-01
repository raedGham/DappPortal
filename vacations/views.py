from django.shortcuts import render,redirect,HttpResponse
from vacations.models import Vacation
from django.core.paginator import Paginator
from .forms import VacationForm

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
   print(sortby)
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
               vacation = Vacation.objects.create(employee=employee,vac_date=vac_date,from_date=from_date, to_date=to_date,
                                                  nodays=nodays,ampm=ampm, remarks=remarks  )
               vacation.save()
               return redirect('list_vacations')
            else:
                return HttpResponse('invalid form')
            
       else: # to update the edited record in the table
            print("the update submitted")
            vacation = Vacation.objects.get(pk=id)
         
            form = VacationForm(request.POST, instance = vacation)  
            if form.is_valid():
               vacation.save()
               return redirect('list_vacations')
            else:
                return redirect('list_vacations')
                
     else:   # GET
         if id == 0 : # to open a blank from
          
            form = VacationForm()
         else: # to populate the form with the data needed to be updated
            vacation = Vacation.objects.get(pk=id)
           
            form = VacationForm(instance=vacation)

         context = {
                    'form':form,
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