from django.db import models
from accounts.models import Account
from datetime import datetime

# Create your models here.

class Log (models.Model):
    employee  = models.ForeignKey(Account, on_delete = models.CASCADE,  null=True )
    log_date = models.DateField(default=datetime.now)
    log_time = models.TimeField(blank=True, null=True )   
    description   = models.TextField(blank=True)       
    section  = models.IntegerField()
    log_type =  models.IntegerField(blank=True, null=True)
   
    
    def __str__(self) :
         
          return self.description
    