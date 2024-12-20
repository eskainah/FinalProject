from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Attendance, AttendanceRecord
from courses.models import Course
from django.utils import timezone
from datetime import timedelta
from accounts.models import CustomUser
from .serializers import AttendanceSerializer
from django.db.models import Count, F, Q

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
        # Initialize lists for storing the percentages
        weekly_present_percentage, weekly_absent_percentage, weekly_excused_percentage = [], [], []
        monthly_present_percentage, monthly_absent_percentage, monthly_excused_percentage = [], [], []

        # Fetch all attendance records ordered by attendance_id
        attendance_records = Attendance.objects.order_by('attendance_id')

        # Map attendance records to weeks
        weekly_groups = {}  # {week_number: [Attendance, ...]}
        for attendance in attendance_records:
            # Extract the week number from attendance_id
            week_number = int(attendance.attendance_id.split('-')[-1])
            if week_number not in weekly_groups:
                weekly_groups[week_number] = []
            weekly_groups[week_number].append(attendance)

        # Process weekly data: Each week corresponds to a specific week_number
        for week_number in range(1, 17):  # Limit to 16 weeks
            if week_number in weekly_groups:
                # Fetch all records for the given week
                weekly_attendances = weekly_groups[week_number]
                weekly_records = AttendanceRecord.objects.filter(attendance__in=weekly_attendances)

                total_students = weekly_records.count()

                if total_students > 0:
                    weekly_present_percentage.append(round((weekly_records.filter(status='Present').count() / total_students) * 100, 2))
                    weekly_absent_percentage.append(round((weekly_records.filter(status='Absent').count() / total_students) * 100, 2))
                    weekly_excused_percentage.append(round((weekly_records.filter(status='Excused').count() / total_students) * 100, 2))
                else:
                    weekly_present_percentage.append(0)
                    weekly_absent_percentage.append(0)
                    weekly_excused_percentage.append(0)
            else:
                # No data for this week
                weekly_present_percentage.append(0)
                weekly_absent_percentage.append(0)
                weekly_excused_percentage.append(0)

        # Process monthly data: Aggregate every 4 weeks as one month
        for month_id in range(1, 5):  # 4 months = 16 weeks
            start_week = (month_id - 1) * 4 + 1
            end_week = start_week + 4
            monthly_attendances = []

            # Collect all attendance records within the month range
            for week_number in range(start_week, end_week):
                if week_number in weekly_groups:
                    monthly_attendances.extend(weekly_groups[week_number])

            # Aggregate monthly data
            monthly_records = AttendanceRecord.objects.filter(attendance__in=monthly_attendances)
            total_students = monthly_records.count()

            if total_students > 0:
                monthly_present_percentage.append(round((monthly_records.filter(status='Present').count() / total_students) * 100, 2))
                monthly_absent_percentage.append(round((monthly_records.filter(status='Absent').count() / total_students) * 100, 2))
                monthly_excused_percentage.append(round((monthly_records.filter(status='Excused').count() / total_students) * 100, 2))
            else:
                monthly_present_percentage.append(0)
                monthly_absent_percentage.append(0)
                monthly_excused_percentage.append(0)

        # Compile trends
        trends = {
            "weekly_present_percentage": weekly_present_percentage,
            "weekly_absent_percentage": weekly_absent_percentage,
            "weekly_excused_percentage": weekly_excused_percentage,
            "monthly_present_percentage": monthly_present_percentage,
            "monthly_absent_percentage": monthly_absent_percentage,
            "monthly_excused_percentage": monthly_excused_percentage,
        }

        return Response(trends)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='std-attendance-ave')
    def student_attendance_averages(self, request):
        """Calculate the average percentages of Present, Absent, and Excused for each student in a course."""
        user = request.user

        if user.role != 'teacher':
            return Response({"error": "Only teachers can access this view."}, status=403)

        course_code = request.query_params.get('course_code')
        if not course_code:
            return Response({"error": "Course code is required."}, status=400)

        # Fetch all attendance records for the given course code
        attendance_records = AttendanceRecord.objects.filter(attendance__course_code=course_code)

        if not attendance_records.exists():
            return Response({"error": "No attendance records found for this course."}, status=404)

        # Calculate the total number of attendance records and status counts per student
        student_stats = (
            attendance_records
            .values("student__custom_id", "student__first_name", "student__last_name")
            .annotate(
                total_records=Count("id"),
                present_count=Count("id", filter=Q(status='Present')),
                absent_count=Count("id", filter=Q(status='Absent')),
                excused_count=Count("id", filter=Q(status='Excused'))
            )
        )

        # Calculate percentages for each student
        data = []
        for stats in student_stats:
            total_records = stats["total_records"]
            data.append({
                "Student ID": stats["student__custom_id"],
                "Student Name": f"{stats['student__first_name']} {stats['student__last_name']}",
                "Present Percentage": round((stats["present_count"] / total_records) * 100, 2) if total_records > 0 else 0,
                "Absent Percentage": round((stats["absent_count"] / total_records) * 100, 2) if total_records > 0 else 0,
                "Excused Percentage": round((stats["excused_count"] / total_records) * 100, 2) if total_records > 0 else 0,
            })

        return Response(data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='weekly-overview')
    def weekly_overview(self, request):
        """Returns weekly attendance details for a specific course."""
        user = request.user

        if user.role != 'teacher':
            return Response({"error": "Only teachers can access this view."}, status=403)

        course_code = request.query_params.get('course_code')
        if not course_code:
            return Response({"error": "Course code is required."}, status=400)

        # Initialize data structure for students
        students_data = {}

        # Fetch all attendance records for the given course code
        attendance_records = Attendance.objects.filter(course_code=course_code).order_by('attendance_id')

        if not attendance_records.exists():
            return Response({"error": "No attendance records found for this course."}, status=404)

        # Define a total of 16 weeks, initializing as 'null' for all weeks
        total_weeks = 16

        # Loop through each attendance record (each represents a different week)
        for attendance in attendance_records:
            # Fetch the associated attendance records for the students
            week_number = int(attendance.attendance_id.split('-')[-1])  # Extract the week number from the attendance_id
            if week_number > total_weeks:
                continue  # If the week number exceeds 16 weeks, skip

            for record in attendance.attendancerecord_set.all():
                student_id = record.student.custom_id

                # If student not in data, initialize their data
                if student_id not in students_data:
                    students_data[student_id] = {
                        "Student ID": student_id,
                        "Student Name": record.student.get_full_name(),
                        **{f"Week {i}": "null" for i in range(1, total_weeks + 1)}  # Default to 'null' for all weeks
                    }

                # Set the attendance status for the correct week
                students_data[student_id][f"Week {week_number}"] = record.status

        # Prepare the final data in the desired format
        data = []
        for student_data in students_data.values():
            row = {
                "Student ID": student_data["Student ID"],
                "Student Name": student_data["Student Name"]
            }
            # Populate the attendance data for each week (Week 1 to Week 16)
            for week in range(1, total_weeks + 1):
                row[f"Week {week}"] = student_data[f"Week {week}"]

            data.append(row)

        return Response(data)




