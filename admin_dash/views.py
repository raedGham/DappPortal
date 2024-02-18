from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
@login_required(login_url='login')
def admindash(request):
   if request.user.username=="adminuser":
      labels1 = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
      data1 = [10, 20, 30, 40, 50]
      context = {"labels1": labels1, "data1": data1, }
      return  render(request, "admin_dash/admindash.html", context)
   else:
      return  HttpResponse("Access Denied")
