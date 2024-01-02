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

    def __str__(self) :
        if self.employee.last_name is not None:
          return self.employee.first_name+ " "+ self.employee.last_name
        else:  
          return self.employee.email 
         
    @property
    def getnod(self):
       return 41
    
      #  if self.from_date is not None and self.to_date is not None:
      #   return self.to_date - self.from_date
      #  else:
      #   return 0  

class EmployeeLeaveStat (models.Model):
    employee = models.OneToOneField(Account, on_delete=models.CASCADE)
    current_year = models.IntegerField()
    previous_year = models.IntegerField()
    total_annual= models.IntegerField()
    daystaken_current = models.IntegerField()
    
    def __str__(self) :
        return self.employee
    