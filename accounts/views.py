from django.shortcuts import render
from .forms import EmployeeAccountForm
# Create your views here.

def profiles(request):
    form = EmployeeAccountForm()
    context = {
                    'form':form,
              }
    
    return render(request, 'profiles\profiles.html', context)