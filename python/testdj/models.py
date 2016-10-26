from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Student(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)

class Teacher(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)

class Course(models.Model):
    name = models.CharField(max_length=20)
    hours = models.IntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

class Grades(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    mark = models.IntegerField()
    comment = models.CharField(max_length=100)

class Record(models.Model):
    username = models.ForeignKey(User)
    time = models.DateTimeField()