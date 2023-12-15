from django.shortcuts import render,HttpResponse, redirect
from .forms import PositionForm
from .models import Position
# Create your views here.
from django.contrib.auth.models import User

def list_positions(request):
   positions = Position.objects.all()
   context = { 'positions': positions}
   return render(request,'positions\positions_list.html', context)

def positions(request):  
     
    if request.method == "POST":
       
        form = PositionForm(request.POST)
        if form.is_valid():
           
            title= form.cleaned_data['title']
            description = form.cleaned_data['description']
            pos = Position.objects.create(title=title, description = description)
            pos.save()
            return redirect('list_positions')
    else:   
         form = PositionForm()
         context = {
                    'form':form,
               }
         return render(request, "positions\positions.html", context)
   