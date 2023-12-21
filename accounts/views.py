from django.shortcuts import render
from .forms import EmployeeAccountForm
from .models import Account
# Create your views here.

def list_profiles(request):
   profiles = Account.objects.all()
   context = { 'profiles': profiles}
   return render(request,"profiles\profiles_list.html", context)


def profiles(request):

    form = EmployeeAccountForm()
    context = {
                    'form':form,
              }
    
    return render(request, 'profiles\profiles.html', context)