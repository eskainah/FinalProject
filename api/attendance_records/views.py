from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Attendance, AttendanceRecord
from courses.models import Course
from django.utils import timezone
from accounts.models import CustomUser
from .serializers import AttendanceSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer

    class StandardResultsSetPagination(PageNumberPagination):
        page_size = 10
        page_size_query_param = 'page_size'
        max_page_size = 100

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Attendance.objects.all()
        elif user.role == 'teacher':
            return Attendance.objects.filter(instructor_id=user.custom_id)
        elif user.role == 'student':
            return Attendance.objects.filter(students=user.custom_id)
        return Attendance.objects.none()

    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated], url_path='upsert-attendance')
    def upsert_attendance(self, request):
        """Unified endpoint to create or update attendance records."""
        user = request.user

        if user.role != 'teacher':
            return Response({"error": "Only teachers can create or update attendance records."}, status=403)

        course_code = request.data.get('course_code')
        course = get_object_or_404(Course, course_code=course_code)

        # Ensure the teacher is assigned to the course
        if course.instructor_id.custom_id != user.custom_id:
            return Response({"error": "You are not assigned to this course."}, status=403)

        # Retrieve or create an attendance record
        date = request.data.get('date', timezone.now().date())
        attendance, created = Attendance.objects.get_or_create(
            course_code=course_code,
            date=date,
            defaults={
                'course_name': course.course_name,
                'instructor_id': user,
                'instructor_name': user.get_full_name(),
            }
        )

        # Add or update students in the attendance record
        students_data = request.data.get('students', [])
        if not students_data:
            return Response({"error": "At least one student must be included."}, status=400)

        existing_records = {record.student.custom_id: record for record in attendance.attendancerecord_set.all()}

        for student_data in students_data:
            student = get_object_or_404(CustomUser, custom_id=student_data.get('student_id'))
            status = student_data.get('status')

            # Update existing records or create new ones
            if student.custom_id in existing_records:
                record = existing_records[student.custom_id]
                record.status = status
                record.save()
            else:
                AttendanceRecord.objects.create(
                    attendance=attendance,
                    student=student,
                    status=status
                )

        return Response({
            "message": "Attendance record successfully " + ("created" if created else "updated"),
            "attendance": AttendanceSerializer(attendance).data
        })
        
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='teacher-view')
    def teacher_view(self, request, course_code=None):
        """Teacher views attendance by course using course_code as pk."""
        user = request.user
        course = get_object_or_404(Course, course_code=course_code, instructor_id=user.custom_id)

        attendances = Attendance.objects.filter(course_code=course.course_code)
        serializer = self.get_serializer(attendances, many=True)
        return Response(serializer.data)
