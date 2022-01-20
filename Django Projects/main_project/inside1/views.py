import http
from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth

# Create your views here.

class Class():
    name : str

def front(request):
    if request.user.is_authenticated:
        u = User.objects.get(username=request.user.username)
        perms = u.teacher.perm
        l = perms.split('-')
        grade = {'0':'9', '1':'10', '2':'11', '3':'12'}
        sec = {'0':'A', '1':'B', '2':'C', '3':'D', '4':'E'}
        classes = []
        for i in l:
            c = Class()
            c.name = 'Class ' + grade[i[0]] + ' ' + sec[i[1]]
            classes.append(c)
        return render(request, 'front.html', {'classes':classes})
    else:
        return render(request, 'oops.html')

def logout(request):
    auth.logout(request)
    return redirect('/')