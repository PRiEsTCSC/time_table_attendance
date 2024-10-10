from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime, timedelta
from django.utils import timezone

# Custom user manager
class UserManager(BaseUserManager):
    def create_user(self, name, password=None, role='student', reg_number=None):
        if not name:
            raise ValueError('Users must have a name')
        
        if role == 'student' and not reg_number:
            raise ValueError('Students must have a registration number')
        
        user = self.model(name=name, role=role)
        
        if role == 'student':
            user.reg_number = reg_number  # Set registration number only for students
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password=None):
        user = self.create_user(name=name, password=password, role='admin')
        user.is_admin = True
        user.save(using=self._db)
        return user

# Custom User model
class User(AbstractBaseUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )
    name = models.CharField(max_length=100)  # Name field for all users
    reg_number = models.CharField(max_length=10, unique=True, null=True, blank=True)  # Optional for non-students
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'name'  # Identify users by name
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reg_number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name} - {self.reg_number}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name



class Timetable(models.Model):
    DAYS_OF_THE_WEEK = (
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day = models.CharField(choices=DAYS_OF_THE_WEEK, max_length=10)  # e.g., "Monday"
    start_time = models.TimeField()
    end_time = models.TimeField()

    @property
    def next_class_datetime(self):
        now = timezone.now()
        weekday_map = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}
        next_class_day = weekday_map[self.day]
        days_ahead = (next_class_day - now.weekday()) % 7
        next_class_date = now + timedelta(days=days_ahead)
        return timezone.make_aware(datetime.combine(next_class_date, self.start_time))

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    present = models.BooleanField(default=False)
    missed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.present:
            self.missed = True
        super().save(*args, **kwargs)
