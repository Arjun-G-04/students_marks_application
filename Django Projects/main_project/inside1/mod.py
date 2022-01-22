from django.contrib.auth.models import User

def classes(request):
    u = User.objects.get(username=request.user.username)
    perms = u.teacher.perm
    l = perms.split('-')
    grade = {'0':'9', '1':'10', '2':'11', '3':'12'}
    sec = {'0':'A', '1':'B', '2':'C', '3':'D', '4':'E'}
    classes = []
    for i in l:
        c = (grade[i[0]], sec[i[1]], i)
        classes.append(c)
    return classes

def code_to_class(code):
    grade = {'0':'9', '1':'10', '2':'11', '3':'12'}
    sec = {'0':'A', '1':'B', '2':'C', '3':'D', '4':'E'}
    c = (grade[code[0]], sec[code[1]])
    return c

def class_alone(request):
    u = User.objects.get(username=request.user.username)
    perms = u.teacher.perm
    l = perms.split('-')
    grade = {'0':'9', '1':'10', '2':'11', '3':'12'}
    classes = []
    for i in l:
        c = grade[i[0]]
        if c not in classes:
            classes.append(c)
    return classes