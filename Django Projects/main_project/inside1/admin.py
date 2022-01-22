from django.contrib import admin
from .models import Teacher, Student, Test, Subject

# Register your models here.

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Test)
admin.site.register(Subject)