from django import forms
from .models import Vacation,EmployeeLeaveStat
from accounts.models import Account
from datetime import datetime
#from calculation import FormulaInput

class VacationForm(forms.ModelForm):

  employee  = forms.ModelChoiceField(queryset=Account.objects.all() )
  vac_date = forms.DateField(initial=datetime.today , widget = forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))
  from_date = forms.DateField(widget = forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))
  to_date   = forms.DateField(widget = forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}) )
  nodays    = forms.DecimalField(decimal_places=1, max_digits=3,required=False, disabled=True)
  ampm      = forms.ChoiceField(required=False, choices=(('','--'),('am','AM'),('pm','PM')))
  
  remarks   = forms.Textarea()
  
  class Meta:
    model = Vacation
    fields = ['employee','vac_date','from_date', 'to_date','nodays', 'ampm','remarks']
    
  def __init__(self,*args, **kwargs):
    super(VacationForm, self).__init__(*args, **kwargs)
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