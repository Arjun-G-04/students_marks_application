from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth

# Create your views here.

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
        elif User.objects.filter(username=username).exists():
            print('Username Exists')
        elif User.objects.filter(email=email).exists():
            print('Email Exists')
        else:
            user = User.objects.create_user(username=username, first_name=fname, last_name=lname, email=email, password=password0)
            user.save()
            print('User Created')
        
        return redirect('/')
            
    else:
        return render(request, 'register.html')