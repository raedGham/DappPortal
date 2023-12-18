from django.shortcuts import render,HttpResponse, redirect
from .forms import PositionForm
from .models import Position
# Create your views here.
from django.contrib.auth.models import User

def list_positions(request):
   positions = Position.objects.all()
   context = { 'positions': positions}
   return render(request,'positions\positions_list.html', context)

def positions(request, id = 0):  
     
    if request.method == "POST":
       if id == 0: # to create a new record and append it to the table  
            print("create new record")
            form = PositionForm(request.POST)
            if form.is_valid():
                title= form.cleaned_data['title']
                description = form.cleaned_data['description']
                pos = Position.objects.create(title=title, description = description)
                pos.save()
                return redirect('list_positions')
            
       else: # to update the edited record in the table
            print("the update submitted")
            position = Position.objects.get(pk=id)
            form = PositionForm(request.POST, instance = position)  
            if form.is_valid():
               position.save()
               return redirect('list_positions')
            
    else:   # GET
         if id == 0 : # to open a blank from
            form = PositionForm()
         else: # to populate the form with the data needed to be updated
            position = Position.objects.get(pk=id)
            form = PositionForm(instance=position)

         context = {
                    'form':form,
               }
         return render(request, "positions\positions.html", context)
    

   


def position_delete(request, id):
    position = Position.objects.get(id=id)
    if request.method == "POST":
       position.delete()
       return redirect('list_positions')
    
    return render(request,
                'positions/position_delete.html',
                {'position': position})