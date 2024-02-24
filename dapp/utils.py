from datetime import datetime
from accounts.models import Account 
from positions.models import Position
def SetWorkflow(QS):
     
               Tarek = Account.objects.get(position = Position.objects.get(title="Admin Head"))
               Mustafa = Account.objects.get(position = Position.objects.get(title="Superintendent"))
               Issam = Account.objects.get(position = Position.objects.get(title="Head of Security"))                  
               first_app = None
               second_app = None
               third_app = None
               fourth_app = None                                 
               if QS.is_head:
                     if QS.is_engineer:
                           first_app = QS
                           second_app = QS.head_dep 
                           third_app = Tarek
                           fourth_app = Mustafa
                     elif QS.is_deputy:
                           first_app = None
                           second_app = QS
                           third_app = Tarek
                           fourth_app = Mustafa
                     elif QS.position.title == "Head of Security":
                           first_app = None
                           second_app = QS 
                           third_app =  Tarek 
                           fourth_app = Mustafa
                     elif QS.position.title == "Admin Head":
                          first_app= None
                          second_app= None
                          third_app =  Tarek 
                          fourth_app = Mustafa
               else:
                     if QS.is_guard:
                          first_app = None
                          second_app = Issam
                          third_app = Tarek
                          fourth_app = Mustafa  
                     elif QS.is_AdminNoHead:
                          first_app = None
                          second_app = None
                          third_app = Tarek
                          fourth_app = Mustafa                        
                     elif QS.is_OMwithHead:
                          first_app = QS.head_dep
                          second_app = first_app.head_dep
                          third_app = Tarek
                          fourth_app = Mustafa                        
                     elif QS.is_OMnoHead:
                          first_app = None
                          second_app= QS.dep_head
                          third_app = Tarek
                          fourth_app = Mustafa  

               return first_app, second_app, third_app, fourth_app                               

def  GetFilterDepList(u):
   if u.email == "admin@live.com":
        return ['MAINT','MEC','ELE','INS','GSR','IT','OPER','ADMIN']
      
   if u.position.title == "Maintenance Head" or u.position.title == "Deputy Maintenance Head" :
         return ['MAINT','MEC','ELE','INS','GSR','IT']
       
   elif u.position.title == "Admin Head" or u.position.title =="Superintendent":
         return ['MAINT','MEC','ELE','INS','GSR','IT','OPER']
       
   else:
      if u.department.name == "MEC" :
         return ['MEC']
      elif u.department.name == "ELE" :
         return ['ELE']
      elif u.department.name == "INS" :
         return ['INS']
      elif u.department.name == "GSR" :
         return ['GSR']
      elif u.department.name == "OPER" :
         return ['OPER']
      elif u.department.name == "IT" :
         return ['IT']
      elif u.department.name == "MAINT" :
         return ['MAINT']
      

def GetCurrentMonthStart():
   m = datetime.now().month
   y = datetime.now().year     
   return datetime(year=y, month=m, day=1)   

def GetCurrentMonthEnd():
   m = datetime.now().month
   y = datetime.now().year     
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

def GetPreviousMonthStart():
   m = datetime.now().month
   y = datetime.now().year     
   
   if m == 1:
      y = y-1
      m = 12
   else:   
      m = m-1
   
   return datetime(year=y, month=m, day=1) 

def GetPreviousMonthEnd():
   m = datetime.now().month
   y = datetime.now().year     
   if m == 1:
      y = y-1
      m = 12
   else:  
      m = m-1

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
