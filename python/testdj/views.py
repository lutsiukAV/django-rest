from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics
from django.contrib.auth.models import User, Group
from testdj.models import Teacher, Student, Course, Grades, Record
from serializers import StudentSerializer, TeacherSerializer, CourseSerializer, GradesSerializer
from testdj.Singleton import SystemLog
import logging


def index(request):
    return HttpResponse(render(request, 'index.html', context={'message': ''}))


def register(request):
    return HttpResponse(render(request, 'register.html'))

@ensure_csrf_cookie
def regok(request):
    user = User.objects.create_user(username=request.POST['login'], password=request.POST['password'])
    user.save()
    s = Student(name=user)
    s.save()
    g = Group.objects.get(name='Student')
    user.groups.add(g)
    return HttpResponse(render(request, 'index.html', context={'message': 'Registraton ok'}))

def teacherMenu(request):
    return HttpResponse(render(request, 'teacher.html'))

def studentMenu(request):
    return HttpResponse(render(request, 'student.html'))


@ensure_csrf_cookie
def menu(request):
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger(None)
    user = authenticate(username=request.POST['login'], password=request.POST['password'])
    if user is not None:
        login(request, user)
        u = User.objects.get(username=request.POST['login'])
        if u.is_superuser:
            log.info('Admin ' + u.username + ' logged in')
            SystemLog(u)
            return HttpResponse(render(request, 'admin.html'))
        else:
            if u.groups.filter(name='Teacher').exists():
                SystemLog(u)
                log.info('Teacher ' + u.username + ' logged in')
                return HttpResponse(render(request, 'teacher.html'))
            elif u.groups.filter(name='Student').exists():
                SystemLog(u)
                log.info('Student ' + u.username + ' logged in')
                return HttpResponse(render(request, 'student.html'))
            else:
                log.info('Unknown user tried to logged in')
                return HttpResponse(render(request, 'index.html', context={'message': 'Login fail'}))
    else:
        return HttpResponse(render(request, 'index.html', context={'message': 'Login fail'}))


def out(request):
    logout(request)
    return HttpResponse(render(request, 'index.html'))

@ensure_csrf_cookie
def addTeacher(request):
    user = User.objects.create_user(username=request.POST['tname'], password='123')
    g = Group.objects.get(name='Teacher')
    user.groups.add(g)
    user.save()
    t = Teacher(name=user)
    t.save()
    return HttpResponse(render(request, 'admin.html'))


def showAllUsers(request):
    res = []
    users = User.objects.all()
    for u in users:
        type = 'None'
        if u.groups.filter(name='Teacher').exists():
            type = 'Teacher'
        elif u.groups.filter(name='Student').exists():
            type = 'Student'
        res.append({'user': u, 'type': type})
    return HttpResponse(render(request, 'userslist.html', {'users': res}))


def deleteUser(request):
    User.objects.get(username=request.GET['login']).delete()
    res = []
    users = User.objects.all()
    for u in users:
        type = 'None'
        if u.groups.filter(name='Teacher').exists():
            type = 'Teacher'
        elif u.groups.filter(name='Student').exists():
            type = 'Student'
        res.append({'user': u, 'type': type})
    return HttpResponse(render(request, 'userslist.html', {'users': res}))


def adminMenu(request):
    return HttpResponse(render(request, 'admin.html'))

def checkAttendance(request):
    r = Record.objects.all()
    return HttpResponse(render(request, 'attendance.html', {"records": r}))

@ensure_csrf_cookie
def changePass(request):
    u = request.user
    u.set_password(request.POST['newpass'])
    u.save()
    return HttpResponse(render(request, 'teacher.html'))

@ensure_csrf_cookie
def addCourse(request):
    u = request.user
    t = Teacher.objects.filter(name=u)
    c = Course.objects.create(name=request.POST['course'], hours=request.POST['hours'], teacher=t[0])
    c.save()
    return HttpResponse(render(request, 'teacher.html'))

def showInfoCourses(request):
    c = Course.objects.filter(teacher__name__username=request.user)
    return HttpResponse(render(request, 'coursesInfo.html', {'courses': c}))


def courseDetails(request):
    g = Grades.objects.filter(course_id=request.GET['id'])
    return HttpResponse(render(request, 'courseDetails.html', {'info': g}))

def showAllCourses(request):
    c = Course.objects.all()
    return HttpResponse(render(request, 'allCourses.html', {'allCourses': c}))

def followCourse(request):
    s = Student.objects.filter(name=request.user)
    c = Course.objects.filter(id=request.GET['id'])
    g = Grades(student=s[0], course=c[0], mark=0, comment="")
    g.save()
    return HttpResponse(render(request, 'allCourses.html'))

def idStudentEstimate(request):
    id = request.GET['id']
    cID = request.GET['cID']
    return HttpResponse(render(request, 'estimation.html', {'id': id, 'cID': cID}))

@ensure_csrf_cookie
def estimate(request):
    g = Grades.objects.filter(student_id=request.POST['sID'], course_id=request.POST['cID'])
    g = g[0]
    g.mark = request.POST['mark']
    g.comment = request.POST['comment']
    g.save()
    return HttpResponse(render(request, 'estimation.html'))

def viewGrades(request):
    u = request.user
    g = Grades.objects.filter(student__name=u)
    return HttpResponse(render(request, 'myGrades.html', {'grades': g}))


def changeLang(request):
    return HttpResponse(render(request, request.GET['template'] + '.html', context={'message': ''}))


#serializers views

class StudentList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class TeacherList(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class GradesList(generics.ListCreateAPIView):
    queryset = Grades.objects.all()
    serializer_class = GradesSerializer

class GradesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grades.objects.all()
    serializer_class = GradesSerializer