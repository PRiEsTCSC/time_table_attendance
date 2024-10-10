from django.urls import path
from .views import TimetableView, AttendanceView, AttendanceSummaryView, CurrentClassView

urlpatterns = [
    path('timetable/', TimetableView.as_view(), name='timetable'),
    path('attendance/', AttendanceView.as_view(), name='attendance'),
    path('attendance-summary/', AttendanceSummaryView.as_view(), name='attendance-summary'),
    path('students/current-class/', CurrentClassView.as_view(), name='current-class'),
]
