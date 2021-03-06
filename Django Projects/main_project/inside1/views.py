import http
from http.client import HTTPResponse
import re
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from inside1.mod import classes, code_to_class, class_alone
from inside1.models import Test, Marks, Student, Subject

# Create your views here.

class Class():
    std : str
    sec : str
    code : str

def front(request):
    if request.user.is_authenticated:
        l = classes(request)
        classes_class = []
        for i in l:
            c = Class()
            c.std, c.sec, c.code = i
            classes_class.append(c)
        return render(request, 'front.html', {'classes':classes_class})
    else:
        return render(request, 'oops.html')

def class_view(request, code):
    if request.user.is_authenticated and (code in User.objects.get(username=request.user.username).teacher.perm):
        std, sec = code_to_class(code)
        tests = Test.objects.all()
        teacher_subs = User.objects.get(username=request.user.username).teacher.subs
        teacher_subs = teacher_subs.split('-')
        tests1 = []
        for i in teacher_subs:
            for j in tests:
                if int(i) in eval(j.test_subs) and (j.test_class == std):
                    tests1.append(j)
        pending_tests = []
        comp_tests = []
        for i in tests1:
            marks = Marks.objects.all().filter(test=i)
            req_marks = []
            for m in marks:
                if m.student.std == std and m.student.sec == sec:
                    req_marks.append(m)
            if not req_marks:
                pending_tests.append(i)
            else:
                comp_tests.append(i)
        return render(request, 'class.html', {'std':std, 'sec':sec, 'code':code, 'pending':pending_tests, 'comp':comp_tests})
    else:
        return render(request, 'oops.html')

def add_test(request, code, test_id):
    if request.user.is_authenticated and (code in User.objects.get(username=request.user.username).teacher.perm):
        test = Test.objects.get(test_id = test_id)
        students = Student.objects.all().filter(std=code_to_class(code)[0], sec=code_to_class(code)[1])
        return render(request, 'add_test.html', {'test':test, 'students':students, 'code':code})
    else:
        return render(request, 'oops.html')

def submit_test(request, code, test_id): 
    if request.user.is_authenticated and (code in User.objects.get(username=request.user.username).teacher.perm):
        test = Test.objects.get(test_id = test_id)
        students = Student.objects.all().filter(std=code_to_class(code)[0], sec=code_to_class(code)[1])
        c = 0
        for s in students:
            m = Marks()
            m.student = s
            m.test = test
            m.sub = Subject.objects.get(sub_code=User.objects.get(username=request.user.username).teacher.subs)
            m.marks = request.POST[s.name]
            m.save()
            c += 1
        return render(request, 'success.html', {'c':c, 'code':code})
    else:
        return render(request, 'oops.html')

def view_test(request, code, test_id):
    if request.user.is_authenticated and (code in User.objects.get(username=request.user.username).teacher.perm):
        std, sec = code_to_class(code)
        test = Test.objects.get(test_id=test_id)
        marks = Marks.objects.all().filter(test=test)
        req_marks = []
        students = Student.objects.all().filter(std=std, sec=sec)
        sub = Subject.objects.all().filter(sub_code=User.objects.get(username=request.user.username).teacher.subs)
        for m in marks:
            if (m.student in students) and (m.sub in sub):
                req_marks.append(m)
        return render(request, 'view_test.html', {'test':test, 'marks':req_marks, 'code':code})

def logout(request):
    auth.logout(request)
    return redirect('/')