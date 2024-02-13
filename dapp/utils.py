from datetime import datetime

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
