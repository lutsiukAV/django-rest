from rest_framework import serializers

from testdj.models import Student, Teacher, Course, Grades

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'name')

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('id', 'name')

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        field = ('id', 'name', 'teacher', 'hours')

class GradesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grades
        field = ('id', 'course', 'student', 'mark', 'comment')