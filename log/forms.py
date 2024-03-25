from django import forms
from .models import Log
from accounts.models import Account
from datetime import datetime
from django.contrib import messages

#from calculation import FormulaInput

class LogForm(forms.ModelForm):

  employee  = forms.ModelChoiceField(queryset=Account.objects.all() )
  log_date = forms.DateField(initial=datetime.today , widget = forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))
  description   = forms.CharField(required=False,widget=forms.Textarea(attrs={'rows':'4'}))
  log_time = forms.TimeField()
  
        

  class Meta:
    model = Log
    fields = ['employee','log_date','description','log_time']
    
  def __init__(self,*args, **kwargs):
    dep_id = kwargs.pop('dep_id', None)
   
    super(LogForm, self).__init__(*args, **kwargs)
    print("Dep ID passed:", str(dep_id))
    if dep_id is not None:            
            self.fields['employee'].queryset = Account.objects.filter(department=dep_id)

    for field in self.fields:
        self.fields[field].widget.attrs['class']= "form-control"