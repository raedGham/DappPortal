from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from departments.models import Department
from positions.models import Position


# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, username, email, password):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have an username')
        user = self.model(
            email = self.normalize_email(email),
            username= username,   
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email,password):
        user = self.create_user(
           email = self.normalize_email(email),
            username= username,
            password = password, 
            
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user



class Account(AbstractBaseUser):
    first_name      = models.CharField(max_length=50)
    middle_name     = models.CharField(max_length=50,null=True,blank=True )
    last_name       = models.CharField(max_length=50, null=True)
    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(max_length=100, unique=True)
    phone_number    = models.CharField(max_length=50, null=True,blank=True )
    ps_number       = models.CharField(max_length=50, null=True)
    financial_number= models.CharField(max_length=50, null=True,blank=True )
    nssf_number     = models.CharField(max_length=50,null=True,blank=True )
    work_start_date  = models.DateField(blank=True, null=True )
    work_finish_date = models.DateField(blank=True, null=True )
    department    = models.ForeignKey(Department, on_delete = models.CASCADE,  null=True ) 
    position       = models.ForeignKey(Position, on_delete = models.CASCADE,  null=True )
    head_dep       = models.ForeignKey('self', on_delete = models.RESTRICT, null=True )
    # user_group
    remarks        = models.TextField(blank=True, null=True)
    address        = models.TextField(blank=True, null=True)
    profile_pic     = models.ImageField(null=True, blank=True, upload_to = 'images/photos/employee')
    #required field

    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=False)
    is_superadmin   = models.BooleanField(default=False)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username'] 

    objects = MyAccountManager()

    def __str__(self):
      if self.last_name is not None:
        return self.first_name+" "+self.last_name
      else:
        return self.email  
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True
