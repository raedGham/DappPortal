from django.shortcuts import render

# Create your views here.

from django.shortcuts import render,HttpResponse, redirect
from .forms import departmentForm
from .models import Department
# Create your views here.
from django.contrib.auth.models import User

def list_departments(request):
   departments = Department.objects.all()
   context = { 'departments': departments}
   return render(request,'departments\departments_list.html', context)

def departments(request, id = 0):  
     
    if request.method == "POST":
       if id == 0: # to create a new record and append it to the table  
            print("create new record")
            form = departmentForm(request.POST)
            if form.is_valid():
                name= form.cleaned_data['name']
                description = form.cleaned_data['description']
                dep = Department.objects.create(name=name, description = description)
                dep.save()
                return redirect('list_departments')
            
       else: # to update the edited record in the table
            print("the update submitted")
            department = Department.objects.get(pk=id)
            form = departmentForm(request.POST, instance = department)  
            if form.is_valid():
               department.save()
               return redirect('list_departments')
            
    else:   # GET
         if id == 0 : # to open a blank from
            form = departmentForm()
         else: # to populate the form with the data needed to be updated
            department = Department.objects.get(pk=id)
            form = departmentForm(instance=department)

         context = {
                    'form':form,
               }
         return render(request, "departments\departments.html", context)
    

   


def department_delete(request, id):
    department = Department.objects.get(id=id)
    if request.method == "POST":
       department.delete()
       return redirect('list_departments')
    
    return render(request,
                'departments/department_delete.html',
                {'department': department})