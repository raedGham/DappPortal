from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from  departments.models import Department
from vacations.models import Vacation
from overtime.models import Overtime
from medreps.models import Medrep
from django.db.models import Count,Sum
from collections import  namedtuple
from datetime import datetime
from django.db.models import Q

# Create your views here.
def GetFromDate(dat):
  if dat != "":
   y = int(dat[:4])
   m = int(dat[-2:])
   return datetime(year=y, month=m, day=1)

def GetToDate(dat):
   if dat != "":
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
           dat = None
           from_date=None
           to_date=None      
      # ------------------------------------get vacations count
      if from_date is not None:       
         vacation_type_counts = Vacation.objects.values("employee__department__name").annotate(
         count=Count("id")).filter(Q(vac_date__gte =from_date) & Q(vac_date__lte =to_date) )

         # count total vacations
         vacation_total_count = Vacation.objects.annotate(
         count=Count("id")).filter(Q(vac_date__gte =from_date) & Q(vac_date__lte =to_date) )

      else:
         vacation_type_counts = Vacation.objects.values("employee__department__name").annotate(
         count=Count("id"))  
         
         # count total vacations 
         vacation_total_count = Vacation.objects.annotate(count=Count("id")) 
         
      # Define a namedtuple to represent the data structure
      DepartmentCount = namedtuple('DepartmentCount', ['department_name', 'count'])

     # Convert the data to DepartmentCount objects
      department_counts = [
         DepartmentCount(item['employee__department__name'], item['count']) for item in vacation_type_counts
      ]

      # Extract department and count lists
      departments = [department_count.department_name for department_count in department_counts]
      counts = [department_count.count for department_count in department_counts] 
           
     # -------------------------------get OT hours
      if from_date is not None:  
         OT_type_sum = Overtime.objects.values("employee__department__name").annotate(
         sum=Sum("straight")).filter(Q(ot_date__gte =from_date) & Q(ot_date__lte =to_date) )
         ot_total_sum = Overtime.objects.filter(Q(ot_date__gte =from_date) & Q(ot_date__lte =to_date) ).aggregate(Sum('straight'))['straight__sum']
      else:
         OT_type_sum = Overtime.objects.values("employee__department__name").annotate(
         sum=Sum("straight"))
         ot_total_sum = Overtime.objects.aggregate(Sum('straight'))['straight__sum']
     
     # Define a namedtuple to represent the data structure
      DepartmentSum = namedtuple('DepartmentSum', ['department_name', 'total_sum'])

      # Convert the data to DepartmentSum objects
      department_sums = [
         DepartmentSum(item['employee__department__name'], item['sum']) for item in OT_type_sum
      ]

      # Extract department and sum lists
      departments1 = [department_sum.department_name for department_sum in department_sums]
      sums = [str(department_sum.total_sum) for department_sum in department_sums]

   # ----------------------------------------get employee OT
      if from_date is not None:
         OT_emp_sum = Overtime.objects.values("employee__first_name","employee__last_name").annotate(
         sum=Sum("straight")).filter(Q(ot_date__gte =from_date) & Q(ot_date__lte =to_date) ).order_by('-sum')[:5]
     
      else:
         OT_emp_sum = Overtime.objects.values("employee__first_name","employee__last_name").annotate(
         sum=Sum("straight")).order_by('-sum')[:5] 
  

      
      ot_top_sum = 0
      for over in OT_emp_sum: 
       print(over['sum'])      
       ot_top_sum += over['sum']

     # Define a namedtuple to represent the data structure
      EmpSum = namedtuple('EmpSum', ['emp_name', 'total_sum'])

      # Convert the data to DepartmentSum objects
      emp_sums = [
         EmpSum(item['employee__first_name']+" "+item['employee__last_name'], item['sum']) for item in OT_emp_sum
      ]

      # Extract department and sum lists
      emps = [emp_sum.emp_name for emp_sum in emp_sums]
      empOT = [str(emp_sum.total_sum) for emp_sum in emp_sums]

     # ----------------------------------------get employee Medreps
      if from_date is not None:
         med_emp_sum = Medrep.objects.values("employee__first_name","employee__last_name").annotate(
         sum=Sum("nodays")).filter(Q(ot_date__gte =from_date) & Q(ot_date__lte =to_date) ).order_by('-sum')[:5]
     
      else:
         med_emp_sum = Medrep.objects.values("employee__first_name","employee__last_name").annotate(
         sum=Sum("nodays")).order_by('-sum')[:5] 
  

      
      med_top_sum = 0
      for over in med_emp_sum: 
        
       med_top_sum += over['sum']

     # Define a namedtuple to represent the data structure
      EmpSum1 = namedtuple('EmpSum1', ['emp_name', 'total_sum'])

      # Convert the data to DepartmentSum objects
      emp_sums1 = [
         EmpSum1(item['employee__first_name']+" "+item['employee__last_name'], item['sum']) for item in med_emp_sum
      ]

      # Extract department and sum lists
      emps1 = [emp_sum.emp_name for emp_sum in emp_sums1]
      empMed = [str(emp_sum.total_sum) for emp_sum in emp_sums1]  
      print(emps1)
      print(empMed)

      context = {
         "labels1": departments, 
         "data1": counts, 
         "labels2": departments1, 
         "data2": sums, 
         "labels3": emps,
         "data3": empOT,
         "labels4":emps1,
         "data4":empMed,
         "sel_date": dat,
         "vacation_total_count":vacation_total_count.count(),
         'ot_total_sum':ot_total_sum,
         'ot_top_sum': ot_top_sum,
         'med_top_sum':med_top_sum,
         }
      return  render(request, "admin_dash/admindash.html", context)
 else:
     return  HttpResponse("Access Denied")
