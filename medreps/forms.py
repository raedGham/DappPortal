from django import forms
from .models import Medrep,EmployeeMedLeaveStat
from accounts.models import Account
from datetime import datetime
from django.contrib import messages

#from calculation import FormulaInput

class MedrepForm(forms.ModelForm):

  employee  = forms.ModelChoiceField(queryset=Account.objects.filter(has_med_ent=True) )
  medrep_date = forms.DateField(initial=datetime.today , widget = forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))
  description   = forms.CharField(required=False,widget=forms.Textarea(attrs={'rows':'4'}))
  from_date = forms.DateField(widget = forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))
  to_date   = forms.DateField(widget = forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}) )
  nodays    = forms.DecimalField(decimal_places=1, max_digits=3,required=False, disabled=True)
  
 
  
  def clean(self):
     cleaned_data = super(MedrepForm, self).clean()
     from_d = cleaned_data.get("from_date")
     to_d = cleaned_data.get("to_date")
     if from_d > to_d:                
        raise forms.ValidationError("From Date Should be less than or equal to To Date")
       
        

  class Meta:
    model = Medrep
    fields = ['employee','medrep_date','description','from_date', 'to_date','nodays']
    
  def __init__(self,*args, **kwargs):
    dep_id = kwargs.pop('dep_id', None)
   
    super(MedrepForm, self).__init__(*args, **kwargs)
    print("Dep ID passed:", str(dep_id))
    if dep_id is not None:            
            self.fields['employee'].queryset = Account.objects.filter(has_vac_ent=True, department=dep_id)

    for field in self.fields:
        self.fields[field].widget.attrs['class']= "form-control"


class EntitlementMedForm(forms.ModelForm):
   description = forms.CharField(max_length=250)
   current_year = forms.NumberInput()  
   daytaken_current = forms.NumberInput()
   
   class Meta:
    model = EmployeeMedLeaveStat
    fields = ['description','current_year','daystaken_current']

   def __init__(self,*args, **kwargs):
      super(EntitlementMedForm, self).__init__(*args, **kwargs)
      for field in self.fields:
          self.fields[field].widget.attrs['class']= "form-control"