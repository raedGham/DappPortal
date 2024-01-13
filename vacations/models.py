from django.db import models
from accounts.models import Account
from datetime import datetime

# Create your models here.

class Vacation (models.Model):
    employee  = models.ForeignKey(Account, on_delete = models.CASCADE,  null=True )
    vac_date = models.DateField(default=datetime.now)
    from_date = models.DateField(blank=True, null=True )
    to_date   = models.DateField(blank=True, null=True )
    nodays    = models.DecimalField(decimal_places=1, max_digits=3, blank=True, null=True)
    ampm      = models.CharField(max_length =2, blank=True, null=True)
    remarks   = models.TextField(blank=True)
    first_approval = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='first_approval_vacations')
    first_app_status = models.IntegerField(default=0)
    second_approval = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='second_approval_vacations')
    second_app_status = models.IntegerField(default=0)
    third_approval = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='third_approval_vacations')
    third_app_status = models.IntegerField(default=0)
    fourth_approval = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='fouth_approval_vacations')
    fourth_app_status = models.IntegerField(default=0) 

    def __str__(self) :
        if self.employee.last_name is not None:
          return self.employee.first_name+ " "+ self.employee.last_name
        else:  
          return self.employee.email 
         
    
   

class EmployeeLeaveStat (models.Model):
    employee = models.OneToOneField(Account, on_delete=models.CASCADE)
    description = models.CharField(max_length=50, default="")
    current_year = models.IntegerField()
    previous_year = models.IntegerField()
    total_annual= models.IntegerField()
    daystaken_current = models.IntegerField()
    
    def __str__(self) :
        return self.employee.first_name+" "+self.employee.last_name
    

