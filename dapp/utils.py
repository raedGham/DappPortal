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