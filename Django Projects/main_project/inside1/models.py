from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    perm = models.CharField(max_length=30)
    subs = models.CharField(max_length=10)

class Student(models.Model):
    rollno = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=30)
    initial = models.CharField(max_length=5)
    address = models.TextField()
    phone1 = models.CharField(max_length=12)
    phone2 = models.CharField(max_length=12)
    std = models.CharField(max_length=2)
    sec = models.CharField(max_length=1)
    bg = models.CharField(max_length=3)

class Subject(models.Model):
    sub_code = models.CharField(max_length=2, primary_key=True)
    sub_name = models.CharField(max_length=30)

class Test(models.Model):
    test_id = models.AutoField(primary_key=True)
    test_name = models.CharField(max_length=40)
    max_marks = models.CharField(max_length=50)
    test_subs = models.CharField(max_length=30)
    test_class = models.CharField(max_length=2)

class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    sub = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.CharField(max_length=4)