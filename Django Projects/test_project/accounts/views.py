from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth

# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['pass']
        user = auth.authenticate(username=username, password=password)
        if user != None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Wrong Username or Password')
            return redirect('login')

    else:
        return render(request, 'login.html')

def register(request):

    if request.method == 'POST':
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password0 = request.POST['password0']
        password1 = request.POST['password1']

        if password0 != password1:
            print('Password Mismatch')
            messages.info(request, 'Password Mismatch')
            return redirect('register')
        elif User.objects.filter(username=username).exists():
            print('Username Exists')
            messages.info(request, 'Username Exists')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            print('Email Exists')
            messages.info(request, 'Email Exists')
            return redirect('register')
        else:
            user = User.objects.create_user(username=username, first_name=fname, last_name=lname, email=email, password=password0)
            user.save()
            print('User Created')
            return redirect('login')
            
    else:
        return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('/')