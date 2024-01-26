from django import forms
from .models import Vacation,EmployeeLeaveStat
from accounts.models import Account
from datetime import datetime
from django.contrib import messages

#from calculation import FormulaInput

class VacationForm(forms.ModelForm):

  employee  = forms.ModelChoiceField(queryset=Account.objects.filter(has_vac_ent=True) )
  vac_date = forms.DateField(initial=datetime.today , widget = forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))
  from_date = forms.DateField(widget = forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))
  to_date   = forms.DateField(widget = forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}) )
  nodays    = forms.DecimalField(decimal_places=1, max_digits=3,required=False, disabled=True)
  ampm      = forms.ChoiceField(required=False, choices=(('','--'),('am','AM'),('pm','PM')))
  remarks   = forms.CharField(required=False,widget=forms.Textarea(attrs={'rows':'4'}))
  
  def clean(self):
     cleaned_data = super(VacationForm, self).clean()
     from_d = cleaned_data.get("from_date")
     to_d = cleaned_data.get("to_date")
     ap = cleaned_data.get("ampm")
     
     
     
        

     if from_d > to_d:                
        raise forms.ValidationError("From Date Should be less than or equal to To Date")
       
        

  class Meta:
    model = Vacation
    fields = ['employee','vac_date','from_date', 'to_date','nodays', 'ampm','remarks']
    
  def __init__(self,*args, **kwargs):
    dep_id = kwargs.pop('dep_id', None)
    print(dep_id)
    super(VacationForm, self).__init__(*args, **kwargs)
    
    if dep_id is not None:            
            self.fields['employee'].queryset = Account.objects.filter(has_vac_ent=True, department=dep_id)

    for field in self.fields:
        self.fields[field].widget.attrs['class']= "form-control"


class EntitlementForm(forms.ModelForm):
   description = forms.CharField(max_length=250)
   current_year = forms.NumberInput()
   previous_year = forms.NumberInput()
   daytaken_current = forms.NumberInput()
   
   class Meta:
    model = EmployeeLeaveStat
    fields = ['description','current_year','previous_year','daystaken_current']

   def __init__(self,*args, **kwargs):
      super(EntitlementForm, self).__init__(*args, **kwargs)
      for field in self.fields:
          self.fields[field].widget.attrs['class']= "form-control"