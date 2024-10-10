from itertools import count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Timetable, Attendance, Student, Subject
from .serializers import TimetableSerializer, AttendanceSerializer, AttendanceSummarySerializer

class TimetableView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        timetable = Timetable.objects.all()
        serializer = TimetableSerializer(timetable, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TimetableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class AttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        student = request.user.student.reg_number
        subject_id = request.data.get('subject_id')

        subject = Subject.objects.get(id=subject_id)
        attendance, created = Attendance.objects.get_or_create(
            student=student, subject=subject, date=timezone.now().date()
        )
        attendance.present = True
        attendance.save()

        return Response({'detail': 'Attendance marked successfully'}, status=200)

    def get(self, request):
        attendance = Attendance.objects.all()
        serializer = AttendanceSerializer(attendance, many=True)
        return Response(serializer.data)

class CurrentClassView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_time = timezone.now().time()
        current_day = timezone.now().strftime('%A')  # Get the current day name

        # Find the current class based on time and day
        current_class = Timetable.objects.filter(
            start_time__lte=current_time, 
            end_time__gte=current_time, 
            day=current_day
        ).first()

        # if current_class:
        #     return Response({
        #         'subject': {
        #             'id': current_class.subject.id,
        #             'name': current_class.subject.name,
        #         },
        #         'start_time': current_class.start_time,
        #         'end_time': current_class.end_time,
        #     }, status=200)
        # else:
        #     return Response({'detail': 'No current class found'}, status=404)
        if current_class:
            serializer = TimetableSerializer(current_class)
            return Response(serializer.data)
        else:
            return Response({'detail': 'No current class found'}, status=404)

# class AttendanceSummaryView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         subject_id = request.query_params.get('subject_id')
#         if subject_id:
#             attendance_summary = Attendance.objects.filter(subject_id=subject_id).values('student').annotate(
#                 total_classes=count('id'),
#                 attended_classes=sum('present')
#             )
#         else:
#             attendance_summary = Attendance.objects.values('student').annotate(
#                 total_classes=count('id'),
#                 attended_classes=sum('present')
#             )
        
#         serializer = AttendanceSummarySerializer(attendance_summary, many=True)
#         return Response(serializer.data)
class AttendanceSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subject_id = request.query_params.get('subject_id')
        if subject_id:
            attendance_summary = Attendance.objects.filter(subject_id=subject_id).values(
                'student__name', 'student__reg_number'
            ).annotate(
                total_classes=count('id'),
                attended_classes=sum('present')
            )
        else:
            attendance_summary = Attendance.objects.values(
                'student__name', 'student__reg_number'
            ).annotate(
                total_classes=count('id'),
                attended_classes=sum('present')
            )
        
        # Prepare the response data for each student
        response_data = [
            {
                'student_name': entry['student__name'],
                'student_reg_number': entry['student__reg_number'],
                'total_classes': entry['total_classes'],
                'attended_classes': entry['attended_classes']
            }
            for entry in attendance_summary
        ]

        return Response(response_data)
