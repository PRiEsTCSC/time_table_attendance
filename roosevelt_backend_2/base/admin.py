from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Student, Subject, Timetable, Attendance

# Custom admin for the User model
class UserAdmin(BaseUserAdmin):
    list_display = ('name', 'role', 'is_active', 'is_admin')  # Display fields for the User model
    list_filter = ('role', 'is_active', 'is_admin')  # Filter options in the admin panel

    fieldsets = (
        (None, {'fields': ('name', 'password')}),  # Basic fields for the User model
        ('Role Information', {'fields': ('role',)}),  # Role-specific information
        ('Permissions', {'fields': ('is_active', 'is_admin')}),  # Permissions for the User model
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'password1', 'password2', 'role', 'is_active', 'is_admin'),
        }),
    )
    
    search_fields = ('name',)  # Allow searching by the user's name
    ordering = ('name',)  # Order the users by name
    filter_horizontal = ()  # No horizontal filters needed here

# Register the custom User model with the custom UserAdmin
admin.site.register(User, UserAdmin)

# Register the Student model
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'reg_number')  # Show the student's name and reg_number
    search_fields = ('name', 'reg_number')  # Search by the student's name and registration number
    list_filter = ('user__role',)  # Filter students by role (although all should be students)

# Register the Subject model
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher')  # Show the subject name and teacher in the admin list
    search_fields = ('name', 'teacher__name')  # Allow searching subjects by name and teacher's name
    list_filter = ('teacher',)  # Filter subjects by their teacher

# Register the Timetable model
@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('subject', 'day', 'start_time', 'end_time')  # Show subject, day, start time, and end time
    search_fields = ('subject__name', 'day')  # Search timetables by subject name and day
    list_filter = ('day',)  # Filter timetables by the day of the week

# Register the Attendance model
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'date', 'present', 'missed')  # Show attendance details
    search_fields = ('student__name', 'student__reg_number', 'subject__name')  # Search attendance by student and subject
    list_filter = ('present', 'missed', 'date')  # Filter attendance by presence status and date
