from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Attendance, AttendanceRecord
from courses.models import Course
from django.utils import timezone
from datetime import timedelta
from accounts.models import CustomUser
from .serializers import AttendanceSerializer
from django.db.models import Count, Q

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


    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='attendance-summary')
    def attendance_summary(self, request):
        user = request.user

        # Get the relevant courses for the user
        if user.role == 'admin':
            courses = Course.objects.all()
        elif user.role == 'teacher':
            courses = Course.objects.filter(instructor_id=user.custom_id)
        elif user.role == 'student':
            courses = Course.objects.filter(students__custom_id=user.custom_id)
        else:
            return Response({"error": "You do not have permission to view this data."}, status=403)

        data = []
        total_present_percentage = 0
        total_absent_percentage = 0
        total_excused_percentage = 0
        total_courses = 0

        # Calculate averages for all courses
        for course in courses:
            attendance_records = AttendanceRecord.objects.filter(attendance__course_code=course.course_code)

            total_students = attendance_records.count()
            if total_students == 0:
                continue

            present_count = attendance_records.filter(status='Present').count()
            absent_count = attendance_records.filter(status='Absent').count()
            excused_count = attendance_records.filter(status='Excused').count()

            present_percentage = (present_count / total_students) * 100
            absent_percentage = (absent_count / total_students) * 100
            excused_percentage = (excused_count / total_students) * 100

            total_present_percentage += present_percentage
            total_absent_percentage += absent_percentage
            total_excused_percentage += excused_percentage
            total_courses += 1

            data.append({
                "course_name": course.course_name,
                "students_present_percentage": present_percentage,
                "students_absent_percentage": absent_percentage,
                "students_excused_percentage": excused_percentage,
            })

        if total_courses > 0:
            average_present_percentage = total_present_percentage / total_courses
            average_absent_percentage = total_absent_percentage / total_courses
            average_excused_percentage = total_excused_percentage / total_courses
        else:
            average_present_percentage = 0
            average_absent_percentage = 0
            average_excused_percentage = 0

        summary = {
            "attendance_summary": data,
            "total_present_percentage": average_present_percentage,
            "total_absent_percentage": average_absent_percentage,
            "total_excused_percentage": average_excused_percentage,
        }

        return Response(summary)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='attendance-trends')
    def attendance_trends(self, request):
        today = timezone.now().date()

        # Define date ranges for the last week and last month
        last_week = [today - timedelta(days=i) for i in range(7)]
        last_month = [today - timedelta(days=i) for i in range(30)]

        # Initialize lists for storing the percentages
        daily_present_percentage, daily_absent_percentage, daily_excused_percentage = [], [], []
        weekly_present_percentage, weekly_absent_percentage, weekly_excused_percentage = [], [], []
        monthly_present_percentage, monthly_absent_percentage, monthly_excused_percentage = [], [], []

        # Process daily data
        for day in last_week:
            daily_records = AttendanceRecord.objects.filter(attendance__date=day).order_by('attendance__date')
            total_students = daily_records.count()
            if total_students > 0:
                daily_present_percentage.append(round((daily_records.filter(status='Present').count() / total_students) * 100, 2))
                daily_absent_percentage.append(round((daily_records.filter(status='Absent').count() / total_students) * 100, 2))
                daily_excused_percentage.append(round((daily_records.filter(status='Excused').count() / total_students) * 100, 2))
            else:
                daily_present_percentage.append(0)
                daily_absent_percentage.append(0)
                daily_excused_percentage.append(0)

        # Process weekly data
        for week in range(1, 5):
            start_of_week = today - timedelta(days=7 * week)
            end_of_week = start_of_week + timedelta(days=7)
            weekly_records = AttendanceRecord.objects.filter(attendance__date__gte=start_of_week, attendance__date__lt=end_of_week).order_by('attendance__date')
            total_students = weekly_records.count()
            if total_students > 0:
                weekly_present_percentage.append(round((weekly_records.filter(status='Present').count() / total_students) * 100, 2))
                weekly_absent_percentage.append(round((weekly_records.filter(status='Absent').count() / total_students) * 100, 2))
                weekly_excused_percentage.append(round((weekly_records.filter(status='Excused').count() / total_students) * 100, 2))
            else:
                weekly_present_percentage.append(0)
                weekly_absent_percentage.append(0)
                weekly_excused_percentage.append(0)

        # Process monthly data
        for day in last_month:
            monthly_records = AttendanceRecord.objects.filter(attendance__date=day).order_by('attendance__date')
            total_students = monthly_records.count()
            if total_students > 0:
                monthly_present_percentage.append(round((monthly_records.filter(status='Present').count() / total_students) * 100, 2))
                monthly_absent_percentage.append(round((monthly_records.filter(status='Absent').count() / total_students) * 100, 2))
                monthly_excused_percentage.append(round((monthly_records.filter(status='Excused').count() / total_students) * 100, 2))
            else:
                monthly_present_percentage.append(0)
                monthly_absent_percentage.append(0)
                monthly_excused_percentage.append(0)

        trends = {
            "daily_present_percentage": daily_present_percentage,
            "daily_absent_percentage": daily_absent_percentage,
            "daily_excused_percentage": daily_excused_percentage,
            "weekly_present_percentage": weekly_present_percentage,
            "weekly_absent_percentage": weekly_absent_percentage,
            "weekly_excused_percentage": weekly_excused_percentage,
            "monthly_present_percentage": monthly_present_percentage,
            "monthly_absent_percentage": monthly_absent_percentage,
            "monthly_excused_percentage": monthly_excused_percentage,
        }

        return Response(trends)


  

    
    
   