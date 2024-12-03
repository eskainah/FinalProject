from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
from .permissions import IsAdmin, IsTeacher, IsStudent
from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework.authentication import TokenAuthentication

User = get_user_model()

class CourseViewSet(viewsets.ModelViewSet):
    """
    Viewset for handling Courses with role-based access control.
    """
    queryset = Course.objects.all().select_related('instructor')  # Use select_related for optimization
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        """
        Custom permission check based on user role.
        - Admins: Full CRUD permissions.
        - Teachers and Students: Only retrieve (view) permissions.
        """
        if not self.request.user.is_authenticated:
            return [IsAuthenticated()]
        
        if self.action in ['create_course', 'update_course', 'delete_course']:
            return [IsAdmin()] if self.request.user.role == 'admin' else [IsAuthenticated()]

        if self.action in ['list', 'retrieve_course', 'students_count', 'enrolled_students']:
            if self.request.user.role == 'admin':
                return [IsAdmin()]
            elif self.request.user.role == 'teacher':
                return [IsTeacher()]
            elif self.request.user.role == 'student':
                return [IsStudent()]

        return super().get_permissions()

    def get_queryset(self):
        """
        Return filtered queryset based on the user's role.
        - Admins: See all courses.
        - Teachers: See only their assigned courses.
        - Students: See only their enrolled courses.
        """
        user = self.request.user

        if user.role == 'admin':
            return self.queryset
        elif user.role == 'teacher':
            return self.queryset.filter(instructor_id=user)
        elif user.role == 'student':
            return self.queryset.filter(enrollment__student_id=user)
        return Course.objects.none()
    
    @action(detail=False, methods=['get'], url_path='search', permission_classes=[IsAuthenticated])
    def search_course(self, request):
        """
        Search courses based on course_code, course_name, or instructor_name.
        """
        filters = {
            'course_code__icontains': request.query_params.get('course_code', ''),
            'course_name__icontains': request.query_params.get('course_name', ''),
            'instructor__full_name__icontains': request.query_params.get('instructor_name', '')
        }
        courses = self.get_queryset().filter(**{key: value for key, value in filters.items() if value})
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='create_course', permission_classes=[IsAdmin])
    def create_course(self, request):
        """
        Custom action to create a new course. Only accessible to admins.
        """
        return self.create(request)

    @action(detail=True, methods=['get'], url_path='retrieve_course', permission_classes=[IsAdmin | IsTeacher | IsStudent])
    def retrieve_course(self, request, pk=None):
        """
        Custom action to retrieve a course. 
        - Admins: Retrieve any course.
        - Teachers: Retrieve courses they teach.
        - Students: Retrieve courses they are enrolled in.
        """
        return self.retrieve(request, pk=pk)

    @action(detail=True, methods=['put', 'patch'], url_path='update_course', permission_classes=[IsAdmin])
    def update_course(self, request, pk=None):
        """
        Custom action to update a course. Only accessible to admins.
        """
        return self.update(request, pk=pk)

    @action(detail=True, methods=['delete'], url_path='delete_course', permission_classes=[IsAdmin])
    def delete_course(self, request, pk=None):
        """
        Custom action to delete a course. Only accessible to admins.
        """
        return self.destroy(request, pk=pk)

    @action(detail=True, methods=['get'], url_path='students_count', permission_classes=[IsTeacher | IsAdmin])
    def students_count(self, request, pk=None):
        """
        Custom action to get the number of students enrolled in a specific course.
        - Admins and Teachers can see the student count for their assigned courses.
        """
        course = self.get_object()
        student_count = Enrollment.objects.filter(course_code=course).count()
        return Response({'course': course.course_name, 'student_count': student_count}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='teacher_courses', permission_classes=[IsTeacher])
    def teacher_courses(self, request):
        """
        Fetch all courses assigned to the teacher and annotate with student count.
        """
        user = request.user
        if user.role != 'teacher':
            return Response({"error": "Only teachers can access this endpoint."}, status=status.HTTP_403_FORBIDDEN)

        courses = self.queryset.filter(instructor_id=user).annotate(student_count=Count('enrollment'))
        total_courses = courses.count()
        total_students = sum(course.student_count for course in courses)

        data = {
            "total_courses": total_courses,
            "total_students": total_students,
            "courses": [
                {
                    "course_name": course.course_name,
                    "student_count": course.student_count,
                }
                for course in courses
            ]
        }

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='enrolled_students', permission_classes=[IsStudent | IsTeacher | IsAdmin])
    def enrolled_students(self, request, pk=None):
        """
        Custom action to get the list of students enrolled in a specific course.
        """
        course = self.get_object()
        enrolled_students = Enrollment.objects.filter(course_code=course).values('student_name')
        return Response({'course': course.course_name, 'enrolled_students': enrolled_students}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='enroll-student', permission_classes=[IsAdmin])
    def enroll_student(self, request):
        """
        Admin can enroll a student in a single course.
        Expects a student custom ID and a course code.
        """
        student_id = request.data.get("student_id")
        course_code = request.data.get("course_code")

        if not student_id or not course_code:
            return Response({"error": "Both student_id and course_code are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = User.objects.get(custom_id=student_id, role='student')
            course = Course.objects.get(course_code=course_code)
        except (User.DoesNotExist, Course.DoesNotExist):
            return Response({"error": "Invalid student ID or course code."}, status=status.HTTP_400_BAD_REQUEST)

        if Enrollment.objects.filter(student_id=student.id, course_code=course.course_code).exists():
            return Response({"error": "Student is already enrolled."}, status=status.HTTP_400_BAD_REQUEST)

        enrollment_data = {
            'student_id': student.id,
            'course_code': course.course_code
        }

        enrollment_serializer = EnrollmentSerializer(data=enrollment_data)
        if enrollment_serializer.is_valid():
            enrollment_serializer.save()
            return Response({"success": "Student enrolled successfully."}, status=status.HTTP_201_CREATED)

        return Response(enrollment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='delete-enrollment', permission_classes=[IsAdmin])
    def delete_enrollment(self, request, pk=None):
        """
        Admin can delete a specific enrollment for a student in a course.
        """
        course = self.get_object()
        student_id = request.data.get("student_id")

        if not student_id:
            return Response({"error": "student_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = User.objects.get(custom_id=student_id, role='student')
            enrollment = Enrollment.objects.get(student_id=student, course_code=course)
            enrollment.delete()
            return Response({"success": "Enrollment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except (User.DoesNotExist, Enrollment.DoesNotExist):
            return Response({"error": "Invalid student ID or enrollment not found."}, status=status.HTTP_400_BAD_REQUEST)
