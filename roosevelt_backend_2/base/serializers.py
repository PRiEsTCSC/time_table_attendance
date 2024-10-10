from rest_framework import serializers
from .models import User, Student, Subject, Timetable, Attendance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['reg_number', 'role']

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ['reg_number', 'user', 'name']

class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['student', 'subject', 'date', 'present', 'missed']

class AttendanceSummarySerializer(serializers.ModelSerializer):
    total_classes = serializers.IntegerField()
    attended_classes = serializers.IntegerField()

    class Meta:
        model = Student
        fields = ['name', 'reg_number', 'total_classes', 'attended_classes']

class SubjectSerializer(serializers.ModelSerializer):
    teacher = serializers.CharField(source='teacher.name', read_only=True)  # Return the teacher's name

    class Meta:
        model = Subject
        fields = ['name', 'teacher']  # Return the subject's name and the teacher's name
