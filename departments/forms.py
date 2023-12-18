from django import forms
from .models import Department

class departmentForm(forms.ModelForm):
  name = forms.CharField()
  description = forms.Textarea()

  class Meta:
    model = Department
    fields = ['name','description']

  def __init__(self,*args, **kwargs):
    super(departmentForm, self).__init__(*args, **kwargs)
    self.fields['name'].widget.attrs['placeholder']= "Enter department name"
    self.fields['name'].widget.attrs['class']= "form-control"
    self.fields['description'].widget.attrs['placeholder']= "Enter job description"
    self.fields['description'].widget.attrs['class']= "form-control"
