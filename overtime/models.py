from django.db import models
from accounts.models import Account
from datetime import datetime

# Create your models here.

class Overtime (models.Model):
    employee  = models.ForeignKey(Account, on_delete = models.CASCADE,  null=True )
    ot_date = models.DateField(default=datetime.now)
    from_time = models.TimeField(blank=True, null=True )
    to_time   = models.TimeField(blank=True, null=True )
    total_hours  = models.DecimalField(decimal_places=1, max_digits=3, blank=True, null=True)
    rate  = models.DecimalField(decimal_places=1, max_digits=3, blank=True, null=True)
    description   = models.TextField(blank=True)
    first_approval = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='first_approval_ot')
    first_app_status = models.IntegerField(default=0)
    second_approval = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='second_approval_ot')
    second_app_status = models.IntegerField(default=0)
    third_approval = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='third_approval_ot')
    third_app_status = models.IntegerField(default=0)
    fourth_approval = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='fouth_approval_ot')
    fourth_app_status = models.IntegerField(default=0)    
    status   = models.IntegerField(default=0)
    approval_position = models.IntegerField(default=1)
    
    def __str__(self) :
        if self.employee.last_name is not None:
          return self.employee.first_name+ " "+ self.employee.last_name
        else:  
          return self.employee.email 
        
        