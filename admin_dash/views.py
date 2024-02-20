from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from  departments.models import Department
from vacations.models import Vacation
from overtime.models import Overtime
from django.db.models import Count,Sum
from collections import  namedtuple

# Create your views here.
@login_required(login_url='login')
def admindash(request):
   if request.user.username=="adminuser":
      
      # get vacations count
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
      print(OT_type_sum)
     
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
      print(OT_emp_sum)
     
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
