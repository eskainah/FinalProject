from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from .models import Attendance
from courses.models import Course, Enrollment
from .serializers import AttendanceSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer

    # Pagination class for listing attendance records
    class StandardResultsSetPagination(PageNumberPagination):
        page_size = 10  # Items per page
        page_size_query_param = 'page_size'
        max_page_size = 100

    # Define queryset with optimized queries using select_related/prefetch_related
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            # For admin, return all attendance records
            return Attendance.objects.all()
        elif user.role == 'teacher':
            # For teacher, filter by instructor and use prefetch for related students
            return Attendance.objects.filter(instructor_id=user.custom_id).select_related('instructor')
        elif user.role == 'student':
            # For student, filter based on student enrollment
            return Attendance.objects.filter(students_data__contains=user.custom_id).select_related('course_code')
        return Attendance.objects.none()

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated], url_path='create-attendance')
    def create_attendance(self, request):
        """Endpoint to create attendance records for teachers."""
        user = request.user
        if user.role != 'teacher':
            return Response({"error": "Only teachers can create attendance records."}, status=403)

        course_code = request.data.get('course_code')
        course = get_object_or_404(Course, course_code=course_code)

        # Ensure the teacher is assigned to the course
        if course.instructor_id.custom_id != user.custom_id:
            return Response({"error": "You are not assigned to this course."}, status=403)

        # Create attendance record
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='teacher-view')
    def view_attendance_by_course_teacher(self, request, pk=None):
        """Teacher views attendance by course."""
        user = request.user
        course = get_object_or_404(Course, pk=pk, instructor_id=user.custom_id)

        # Prefetch related students who are enrolled in the course for better performance
        students_prefetch = Prefetch('students', queryset=course.students.all(), to_attr='enrolled_students')

        # Get attendances for the course and prefetch the related students
        attendances = Attendance.objects.filter(course_code=course.course_code).prefetch_related(students_prefetch)
        serializer = self.get_serializer(attendances, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='student-view')
    def view_attendance_by_course_student(self, request, pk=None):
        """Student views attendance by course."""
        user = request.user
        course = get_object_or_404(Course, pk=pk)

        # Check if the student is enrolled in the course using Enrollment model
        enrollment = get_object_or_404(Enrollment, student_id=user.custom_id, course=course)
        
        # If the student is not enrolled, return an error
        if not enrollment:
            return Response({"error": "You are not enrolled in this course."}, status=403)

        # Prefetch related students who are enrolled in the course for better performance
        students_prefetch = Prefetch('students', queryset=course.students.all(), to_attr='enrolled_students')

        # Get attendances for the course and prefetch the related students
        attendances = Attendance.objects.filter(course_code=course.course_code).prefetch_related(students_prefetch)
        serializer = self.get_serializer(attendances, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='admin-view')
    def view_attendance_by_course_admin(self, request, pk=None):
        """Admin views attendance by course."""
        course = get_object_or_404(Course, pk=pk)

        # Prefetch related students who are enrolled in the course for better performance
        students_prefetch = Prefetch('students', queryset=course.students.all(), to_attr='enrolled_students')

        # Get attendances for the course and prefetch the related students
        attendances = Attendance.objects.filter(course_code=course.course_code).prefetch_related(students_prefetch)
        serializer = self.get_serializer(attendances, many=True)
        return Response(serializer.data)
