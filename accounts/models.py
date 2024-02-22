from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from departments.models import Department
from positions.models import Position
from django.utils import timezone

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, username, email, password, first_name , last_name, middle_name , phone_number,ps_number,financial_number,nssf_number,work_start_date,
                    work_finish_date, department, position, head_dep, remarks, address,profile_pic, is_head,is_engineer,is_deputy, is_guard, is_AdminNoHead,is_OMwithHead,is_OMnoHead,has_vac_ent) :       
                                                     
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have an username')
        
        user = self.model(
            email           = self.normalize_email(email),
            username        =username, 
            first_name      =first_name,
            last_name       =last_name,
            middle_name     =middle_name,
            phone_number    =phone_number,            
            ps_number       =ps_number,
            financial_number=financial_number,
            nssf_number     =nssf_number,
            work_start_date =work_start_date,
            work_finish_date=work_finish_date,
            department      =department,
            position        =position,
            head_dep        =head_dep, 
            remarks         = remarks,
            address         = address,
            profile_pic     =profile_pic,
            is_head         =is_head,
            is_engineer     = is_engineer,
            is_deputy       = is_deputy,      
            is_guard       = is_guard,    
            is_AdminNoHead  = is_AdminNoHead,
            is_OMwithHead   = is_OMwithHead,
            is_OMnoHead     = is_OMnoHead,
            has_vac_ent     = has_vac_ent,
            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email,password):
        user = self.create_user(
           email = self.normalize_email(email),
            username= username,          
            
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user



class Account(AbstractBaseUser,PermissionsMixin):
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
    department      = models.ForeignKey(Department, on_delete = models.CASCADE,  null=True ) 
    position        = models.ForeignKey(Position, on_delete = models.CASCADE,  null=True )
    head_dep        = models.ForeignKey('self', on_delete = models.RESTRICT, null=True )
    remarks         = models.TextField(blank=True, null=True)
    address         = models.TextField(blank=True, null=True)
    profile_pic     = models.ImageField(null=True, blank=True, upload_to = 'images/photos/employee') 
    date_joined     = models.DateTimeField(default=timezone.now)
    last_login      = models.DateTimeField(default=timezone.now)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    is_head         = models.BooleanField(default=False)
    is_engineer     = models.BooleanField(default=False)
    is_deputy       = models.BooleanField(default=False)
    is_guard        = models.BooleanField(default=False)
    is_AdminNoHead  = models.BooleanField(default=False)
    is_OMwithHead   = models.BooleanField(default=False)  
    is_OMnoHead     = models.BooleanField(default=False)  
    has_vac_ent     = models.BooleanField(default=False)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username'] 

    objects = MyAccountManager()

    def __str__(self):
      if self.last_name is not None:
        return self.first_name+" "+self.last_name
      else:
        return self.email
    
    # def has_perm(self, perm, obj=None):
    #     return self.is_admin
    
    # def has_add_perm(self, perm, obj=None):
    #     return self.is_admin
    

