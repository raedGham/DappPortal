from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from  departments.models import Department
from vacations.models import Vacation
from overtime.models import Overtime
from django.db.models import Count,Sum
from collections import  namedtuple
from datetime import datetime
from django.db.models import Q

# Create your views here.
def GetFromDate(dat):
   y = int(dat[:4])
   m = int(dat[-2:])
   return datetime(year=y, month=m, day=1)

def GetToDate(dat):
   y = int(dat[:4])
   m = int(dat[-2:])
   if m in [1,3,5,7,8,10,12]:      
     e=31
   elif m in [4,6,9,11]:
     e=30
   elif m == 2:
      if (y % 4)==0 :
         e = 29 
      else: 
         e = 28
   return datetime(year=y, month=m , day =e)

@login_required(login_url='login')
def admindash(request):
 if request.user.username=="adminuser":
      if request.GET.get('dat') is not None:
            dat = request.GET.get('dat')
            from_date = GetFromDate(dat)
            to_date = GetToDate(dat)
      else:
           from_date=""
           ro_date=""      
      # get vacations count
      if from_date !="":       
         vacation_type_counts = Vacation.objects.values("employee__department__name").annotate(
         count=Count("id")).filter(Q(vac_date__gte =from_date) & Q(vac_date__lte =to_date) )
      else:
         vacation_type_counts = Vacation.objects.values("employee__department__name").annotate(
         count=Count("id"))   

      # Define a namedtuple to represent the data structure
      DepartmentCount = namedtuple('DepartmentCount', ['department_name', 'count'])

     # Convert the data to DepartmentCount objects
      department_counts = [
         DepartmentCount(item['employee__department__name'], item['count']) for item in vacation_type_counts
      ]

      # Extract department and count lists
      departments = [department_count.department_name for department_count in department_counts]
      counts = [department_count.count for department_count in department_counts] 
           
     # get OT hours
      OT_type_sum = Overtime.objects.values("employee__department__name").annotate(
      sum=Sum("straight"))
    
     
     # Define a namedtuple to represent the data structure
      DepartmentSum = namedtuple('DepartmentSum', ['department_name', 'total_sum'])

      # Convert the data to DepartmentSum objects
      department_sums = [
         DepartmentSum(item['employee__department__name'], item['sum']) for item in OT_type_sum
      ]

      # Extract department and sum lists
      departments1 = [department_sum.department_name for department_sum in department_sums]
      sums = [str(department_sum.total_sum) for department_sum in department_sums]

   # get employee OT
      
      OT_emp_sum = Overtime.objects.values("employee__first_name","employee__last_name").annotate(
      sum=Sum("straight")).order_by('-sum')[:5]
  
     
     # Define a namedtuple to represent the data structure
      EmpSum = namedtuple('EmpSum', ['emp_name', 'total_sum'])

      # Convert the data to DepartmentSum objects
      emp_sums = [
         EmpSum(item['employee__first_name']+" "+item['employee__last_name'], item['sum']) for item in OT_emp_sum
      ]

      # Extract department and sum lists
      emps = [emp_sum.emp_name for emp_sum in emp_sums]
      empOT = [str(emp_sum.total_sum) for emp_sum in emp_sums]
    
      context = {
         "labels1": departments, 
         "data1": counts, 
         "labels2": departments1, 
         "data2": sums, 
         "labels3": emps,
         "data3": empOT,
         
         }
      return  render(request, "admin_dash/admindash.html", context)
 else:
     return  HttpResponse("Access Denied")
