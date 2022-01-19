import http
from http.client import HTTPResponse
from django.shortcuts import render

# Create your views here.

def front(request):
    return render(request, 'test.html')