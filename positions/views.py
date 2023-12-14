from django.shortcuts import render,HttpResponse

# Create your views here.

def list_positions(request):
   return HttpResponse("list poisitions")