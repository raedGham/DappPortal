from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from  departments.models import Department
from vacations.models import Vacation
from django.db.models import Count
from collections import defaultdict

# Create your views here.
@login_required(login_url='login')
def admindash(request):
   if request.user.username=="adminuser":
      department_list = []
      count_list = []  

      vacation_type_counts = Vacation.objects.values("employee__department__name").annotate(
      count=Count("id"))

      
      print(vacation_type_counts)
      for vac in vacation_type_counts:
          print(vac.employee__department__name)
          #department_list.append(vac.employee__department__name)
         # count_list.append(vac.count)
      
      labels1 = department_list
      data1 = count_list
      context = {"labels1": labels1, "data1": data1, }
      return  render(request, "admin_dash/admindash.html", context)
   else:
      return  HttpResponse("Access Denied")
