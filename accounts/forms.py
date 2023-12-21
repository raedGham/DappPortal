from django import forms
from .models import Account, Department, Position

class EmployeeAccountForm(forms.ModelForm):
  email = forms.EmailField(max_length=100)
  first_name =  forms.CharField(max_length=50)
  last_name =  forms.CharField(max_length=50)
  middle_name =  forms.CharField(max_length=50)
  password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password','class':'form-control'}))
  confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))
  ps_number       = forms.CharField(max_length=50)
  financial_number= forms.CharField(max_length=50)
  nssf_number     = forms.CharField(max_length=50)
  work_start_date  = forms.DateTimeField(widget = forms.DateInput(format="%d-%m-%Y", attrs={"type": "date"}))
  work_finish_date = forms.DateTimeField(widget = forms.DateInput(format="%d-%m-%Y", attrs={"type": "date"}))
  phone_number    = forms.CharField(max_length=50)
  remarks        = forms.CharField(widget=forms.Textarea(attrs={'rows':'4'}))
  address        = forms.CharField(widget=forms.Textarea(attrs={'rows':'4'}))
  department    = forms.ModelChoiceField(queryset=Department.objects.all())
  position       = forms.ModelChoiceField(queryset=Position.objects.all())
  head_dep       = forms.ModelChoiceField(queryset=Account.objects.all())
  
  class Meta:
    model = Account
    fields = ['email','first_name','middle_name', 'last_name','password', 'confirm_password','ps_number',
              'financial_number','nssf_number','work_start_date','work_finish_date','phone_number','remarks','address','department','position','head_dep']
    
    # ,'departrment','position','head_dep'


  def __init__(self,*args, **kwargs):
    super(EmployeeAccountForm, self).__init__(*args, **kwargs)
    for field in self.fields:
        self.fields[field].widget.attrs['class']= "form-control"