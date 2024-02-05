from django import forms
from .models import Overtime
from accounts.models import Account
from datetime import datetime
from django.contrib import messages


#from calculation import FormulaInput

class OvertimeForm(forms.ModelForm):

  # employee  = forms.ModelChoiceField(queryset=Account.objects.filter() )
  ot_date = forms.DateField(initial=datetime.today , widget = forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))
  from_time = forms.TimeField(widget = forms.TimeInput(format='%H:%M', attrs={"type": "time"}))
  to_time   = forms.TimeField(widget = forms.TimeInput(format='%H:%M', attrs={"type": "time"}) ) 
  rate      = forms.ChoiceField(required=False, choices=(('','--'),('1.5','1.5'),('2.0','2.0')))
  reason   = forms.CharField(required=False,widget=forms.Textarea(attrs={'rows':'1'}))
 
  
        

  class Meta:
    model = Overtime
    fields = ['ot_date','from_time', 'to_time', 'reason']
    
  def __init__(self,*args, **kwargs):
   # dep_id = kwargs.pop('dep_id', None)
   
    super(OvertimeForm, self).__init__(*args, **kwargs)
    
    # if dep_id is not None:            
    #         self.fields['employee'].queryset = Account.objects.filter(department=dep_id)

    for field in self.fields:
        self.fields[field].widget.attrs['class']= "form-control"


