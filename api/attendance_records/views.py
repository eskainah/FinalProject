from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Attendance, Course
from serializers import AttendanceSerializer
from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404

class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Attendance.objects.all()
        elif user.role == 'teacher':
            return Attendance.objects.filter(instructor_id=user.custom_id)
        elif user.role == 'student':
            return Attendance.objects.filter(students_data__contains=user.custom_id)
        return Attendance.objects.none()

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated], url_path='create-attendance')
    def create_attendance(self, request):
        """Endpoint to create attendance records."""
        user = request.user
        if user.role != 'teacher':
            return Response({"error": "Only teachers can create attendance records."}, status=403)

        course_code = request.data.get('course_code')
        course = get_object_or_404(Course, course_code=course_code)

        if course.instructor_id.custom_id != user.custom_id:
            return Response({"error": "You are not assigned to this course."}, status=403)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='teacher-view')
    def view_attendance_by_course_teacher(self, request, pk=None):
        user = request.user
        course = get_object_or_404(Course, pk=pk, instructor_id=user.custom_id)
        attendances = Attendance.objects.filter(course_code=course.course_code)
        serializer = self.get_serializer(attendances, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='student-view')
    def view_attendance_by_course_student(self, request, pk=None):
        user = request.user
        course = get_object_or_404(Course, pk=pk)
        if user.custom_id not in [student.student_id for student in course.students.all()]:
            return Response({"error": "You are not enrolled in this course."}, status=403)
        attendances = Attendance.objects.filter(course_code=course.course_code)
        serializer = self.get_serializer(attendances, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='admin-view')
    def view_attendance_by_course_admin(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        attendances = Attendance.objects.filter(course_code=course.course_code)
        serializer = self.get_serializer(attendances, many=True)
        return Response(serializer.data)
