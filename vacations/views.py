from django.shortcuts import render
from vacations.models import Vacation
from django.core.paginator import Paginator

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


def vacations():
    pass


def vacation_delete():
    pass