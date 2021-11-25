from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'home.html', {'name':'AAAA'})

def add(request):
    n1 = request.POST['num1']
    n2 = request.POST['num2']
    res = float(n1) + float(n2)
    return render(request, 'results.html', {'res':res})