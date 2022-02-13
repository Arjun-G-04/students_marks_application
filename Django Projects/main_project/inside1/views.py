import http
from http.client import HTTPResponse
from msilib import type_string
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

class sub_view():
    pass_per : int
    fail_per : int
    avg_per : int
    passno : int
    failno : int
    avg : int
    highest : int
    total : int
    marks : list 

def front(request):
    if request.user.is_authenticated:
        l = classes(request)
        classes_class = []
        grades = []
        for i in l:
            c = Class()
            c.std, c.sec, c.code = i
            if c.std not in grades:
                grades.append(c.std)
            classes_class.append(c) 
        
        return render(request, 'front.html', {'classes':classes_class, 'grades':grades}) 
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
        sub = Subject.objects.get(sub_code=User.objects.get(username=request.user.username).teacher.subs)
        for i in tests1:
            marks = Marks.objects.all().filter(test=i)
            req_marks = []
            for m in marks:
                if m.student.std == std and m.student.sec == sec and m.sub == sub:
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
        sub = Subject.objects.get(sub_code=User.objects.get(username=request.user.username).teacher.subs)
        return render(request, 'add_test.html', {'test':test, 'students':students, 'code':code, 'subject':sub})
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
    else:
        return render(request, 'oops.html')

def edit_marks(request, test_id, marks_id, code):
    if request.user.is_authenticated and (code in User.objects.get(username=request.user.username).teacher.perm):
        mark = Marks.objects.get(id=int(marks_id))
        mark.marks = request.POST[mark.student.name]
        mark.save()
        return redirect('/app1/front/' + code + '/view/' + test_id)
    else:
        return render(request, 'oops.html')

def tests_home(request, grade):
    if request.user.is_authenticated and (grade in class_alone(request)):
        tests = Test.objects.all().filter(test_class=grade)
        n = 1
        List = []
        for i in tests:
            marks = Marks.objects.all().filter(test=i)
            sec = []
            for m in marks:
                if m.student.sec not in sec:
                    sec.append(m.student.sec)
            List.append((str(n), i, sec))
            n += 1
        return render(request, 'tests_home.html', {'tests':List, 'grade':grade, 'sec':sec})
    else:
        return render(request, 'oops.html')

def test_report(request, grade, test_id, sec):
    if sec != 'all':
        test = Test.objects.get(test_id = test_id)
        marks_raw = Marks.objects.all().filter(test_id=test_id)
        marks_req = []
        for m in marks_raw:
            if m.student.sec == sec:
                marks_req.append(m)
        
        max_marks = eval(test.max_marks)
        sub_codes = eval(test.test_subs)
        
        # Final Table 
        subs = []
        for i in sub_codes:
            s = Subject.objects.get(sub_code=str(i))
            subs.append(s)

        head = ('Roll No.', 'Name')

        for sub in subs:
            s1 = sub.sub_name
            s2 = f'({max_marks[int(sub.sub_code)]})'
            head += (s1+s2,)

        rows = []
        students = Student.objects.all().filter(std = grade, sec = sec)
        for s in students:
            row = (s.rollno, s.name)
            total = 0
            total_max = 0
            for sub in subs:
                try:
                    m = Marks.objects.get(test=test,sub=sub,student=s)
                    total += round((float(m.marks)/max_marks[int(sub.sub_code)])*100, 0)
                    total_max += 100
                    row += (m.marks,)
                except:
                    row += ('-',)
            row += (str(total),)
            rows.append(row)
        head += (f'Total({total_max})', 'Rank', 'Percentile')

        for t in rows:
            status = 'Pass'
            for sub in subs:
                search = sub.sub_name + f'({max_marks[int(sub.sub_code)]})'
                if t[head.index(search)]  != '-':
                    if float(t[head.index(search)]) < (0.33*max_marks[int(sub.sub_code)]):
                        status = 'Fail'
            rows[rows.index(t)] = t + (status,)
        
        # Calc. Overall Stats
        no_pass = 0
        no_fail = 0
        no_abv_90 = 0
        no_blw_50 = 0
        total_marks = []
        total_sum = 0
        for r in rows:
            total_marks.append(float(r[head.index(f'Total({total_max})')]))
            total_sum += float(r[head.index(f'Total({total_max})')])
            if r[-1] == 'Pass':
                no_pass += 1
            else:
                no_fail += 1
            if float(r[-2]) >= (0.90*total_max):
                no_abv_90 += 1
            if float(r[-2]) < (0.50*total_max):
                no_blw_50 += 1
        avg_mark = round((total_sum / len(rows)), 0)
        highest_mark = max(total_marks)

        # Subwise stats
        return render(
            request, 'report.html', 
            {
                'test':test, 
                'sec':sec,
                'pass_per':int(round((no_pass/len(rows))*100, 0)),
                'fail_per':int(round((no_fail/len(rows))*100, 0)),
                'avg_per':int(round((avg_mark/total_max)*100, 0)),
                'abv90_per':int(round((no_abv_90/len(rows))*100, 0)),
                'blw50_per':int(round((no_blw_50/len(rows))*100, 0)),
                'passno':no_pass,
                'failno':no_fail,
                'avg':int(avg_mark),
                'highest':int(highest_mark),
                'total':int(total_max),
                'abv90':no_abv_90,
                'blw50':no_blw_50
            }
        )

def logout(request):
    auth.logout(request)
    return redirect('/')