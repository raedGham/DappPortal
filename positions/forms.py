from django import forms
from .models import Position

class PositionForm(forms.ModelForm):
  title = forms.CharField()
  description = forms.Textarea()

  class Meta:
    model = Position
    fields = ['title','description']

  def __init__(self,*args, **kwargs):
    super(PositionForm, self).__init__(*args, **kwargs)
    self.fields['title'].widget.attrs['placeholder']= "Enter a title"
    self.fields['title'].widget.attrs['class']= "form-control"
    self.fields['description'].widget.attrs['placeholder']= "Enter job description"
    self.fields['description'].widget.attrs['class']= "form-control"
