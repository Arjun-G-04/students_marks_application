from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth

# Create your views here.

def home(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        uname = request.POST['username']
        pswd = request.POST['pswd']

        user = auth.authenticate(username=uname, password=pswd)

        if user != None:
            auth.login(request, user)
            return redirect('app1/front')
        else:
            messages.info(request, 'Wrong Password or Username!!')
            return redirect('/')
    else:
        return render(request, 'index.html')