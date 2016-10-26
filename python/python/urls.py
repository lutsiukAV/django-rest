"""python URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from testdj import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = i18n_patterns(
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^register/', views.register),
    url(r'^login/', views.regok),
    url(r'^out/', views.out),
    url(r'^menu/', views.menu),
    url(r'^userslist/', views.showAllUsers),
    url(r'^addTeacher/', views.addTeacher),
    url(r'^deleteUser/', views.deleteUser),
    url(r'^adminMenu/', views.adminMenu),
    url(r'^changePass/', views.changePass),
    url(r'^addCourse/', views.addCourse),
    url(r'^showInfoCourses/', views.showInfoCourses),
    url(r'^courseDetails/', views.courseDetails),
    url(r'^showAllCourses/', views.showAllCourses),
    url(r'^followCourse/', views.followCourse),
    url(r'^idStudentEstimate/', views.idStudentEstimate),
    url(r'^estimate/', views.estimate),
    url(r'^viewGrades/', views.viewGrades),
    url(r'^teacherMenu', views.teacherMenu),
    url(r'^studentMenu/', views.studentMenu),
    url(r'^lang/', views.changeLang),
    url(r'checkAttendance/', views.checkAttendance),
)

api_urls = [
    url(r'^students/$', views.StudentList.as_view()),
    url(r'^students/(?P<pk>[0-9]+)/$', views.StudentDetail.as_view()),
    url(r'^teachers/$', views.TeacherList.as_view()),
    url(r'^teachers/(?P<pk>[0-9]+)/$', views.TeacherDetail.as_view()),
    url(r'^courses/$', views.CourseList.as_view()),
    url(r'^courses/(?P<pk>[0-9]+)/$', views.CourseDetail.as_view()),
    url(r'^grades/$', views.GradesList.as_view()),
    url(r'^grades/(?P<pk>[0-9]+)/$', views.GradesDetail.as_view()),
]

api_urls = format_suffix_patterns(api_urls)

urlpatterns += api_urls