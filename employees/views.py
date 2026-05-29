from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def employees(request):
    return HttpResponse('This is employees page')