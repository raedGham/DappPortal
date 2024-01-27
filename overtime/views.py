from django.shortcuts import render,HttpResponse
from .models import Overtime

# Create your views here.

def ot_list(request):
    p_ots = Overtime.objects.all()
    return render(request, 'overtime/ot_list.html', {'p_ots':p_ots})