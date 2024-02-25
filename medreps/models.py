from django.db import models
from accounts.models import Account
from datetime import datetime

# Create your models here.

class Medrep (models.Model):
    employee  = models.ForeignKey(Account, on_delete = models.CASCADE,  null=True )    
    medrep_date = models.DateField(default=datetime.now)
    description   = models.TextField(blank=True)
    from_date = models.DateField(blank=True, null=True )
    to_date   = models.DateField(blank=True, null=True )
    nodays    = models.IntegerField(blank=True)
      
    first_approval = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='first_approval_medreps')
    first_app_status = models.IntegerField(default=0)
    first_app_date = models.DateTimeField(auto_now_add=True , null=True)
    second_approval = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='second_approval_medreps')
    second_app_status = models.IntegerField(default=0)
    second_app_date = models.DateTimeField(auto_now_add=True, null=True)
    third_approval = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='third_approval_medreps')
    third_app_status = models.IntegerField(default=0)
    third_app_date = models.DateTimeField(auto_now_add=True, null=True)
    fourth_approval = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='fouth_approval_medreps')
    fourth_app_status = models.IntegerField(default=0)    
    fourth_app_date = models.DateTimeField(auto_now_add=True, null=True)
    status   = models.IntegerField(default=0)
    approval_position = models.IntegerField(default=1)
    
    def __str__(self) :
        if self.employee.last_name is not None:
          return self.employee.first_name+ " "+ self.employee.last_name
        else:  
          return self.employee.email 
         
    
   

class EmployeeMedLeaveStat (models.Model):
    employee = models.OneToOneField(Account, on_delete=models.CASCADE)
    description = models.CharField(max_length=50, default="")
    current_year = models.IntegerField()
 #   previous_year = models.IntegerField()
 #   total_annual= models.IntegerField()
    daystaken_current = models.IntegerField()
    
    def __str__(self) :
        return self.employee.first_name+" "+self.employee.last_name
    

