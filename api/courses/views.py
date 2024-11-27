from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
from .permissions import IsAdmin, IsTeacher, IsStudent
from django.contrib.auth import get_user_model

User = get_user_model()

class CourseViewSet(viewsets.ModelViewSet):
    """
    Viewset for handling Courses with role-based access control.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Custom permission check based on user role.
        - Admins: Full CRUD permissions.
        - Teachers and Students: Only retrieve (view) permissions.
        """
        if self.action in ['create_course', 'update_course', 'delete_course']:
            return [IsAdmin()]
        elif self.action in ['list', 'retrieve_course', 'students_count', 'enrolled_students']:
            if self.request.user.role == 'admin':
                return [IsAdmin()]
            elif self.request.user.role == 'teacher':
                return [IsTeacher()]
            elif self.request.user.role == 'student':
                return [IsStudent()]
        return super(CourseViewSet, self).get_permissions()

    def get_queryset(self):
        """
        Return filtered queryset based on the user's role.
        - Admins: See all courses.
        - Teachers: See only their assigned courses.
        - Students: See only their enrolled courses.
        """
        user = self.request.user

        if user.role == 'admin':
            return Course.objects.all()
        elif user.role == 'teacher':
            return Course.objects.filter(instructor_id=user)
        elif user.role == 'student':
            return Course.objects.filter(enrollment__student_id=user)
        return Course.objects.none()
    
    @action(detail=False, methods=['get'], url_path='search', permission_classes=[IsAuthenticated])
    def search_course(self, request):
        """
        Search courses based on course_code, course_name, or instructor_name.
        """
        course_code = request.query_params.get('course_code', None)
        course_name = request.query_params.get('course_name', None)
        instructor_name = request.query_params.get('instructor_name', None)

        # Start with all courses
        courses = self.get_queryset()

        # Filter by course_code if provided
        if course_code:
            courses = courses.filter(course_code__icontains=course_code)

        # Filter by course_name if provided
        if course_name:
            courses = courses.filter(course_name__icontains=course_name)

        # Filter by instructor's full name if provided
        if instructor_name:
            courses = courses.filter(instructor_full_name__icontains=instructor_name)

        # Serialize the filtered courses
        serializer = self.get_serializer(courses, many=True)

        # Return the filtered courses
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

    @action(detail=True, methods=['get'], url_path='enrolled_students', permission_classes=[IsStudent | IsTeacher | IsAdmin])
    def enrolled_students(self, request, pk=None):
        """
        Custom action to get the list of students enrolled in a specific course.
        - Admins and Teachers can view all enrolled students in a course.
        """
        course = self.get_object()
        enrolled_students = Enrollment.objects.filter(course_code=course).values('student_name')
        return Response({'course': course.course_name, 'enrolled_students': enrolled_students}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='enroll-student')
    def enroll_student(self, request):
        """
        Admin can enroll a student in multiple courses.
        Expects a student custom ID and a list of course codes.
        Example payload:
        {
            "student_id": "STU001",
            "course_codes": ["CSC100", "CSC101"]
        }
        """
        student_id = request.data.get("student_id")
        course_codes = request.data.get("course_codes")

        if not student_id or not course_codes:
            return Response({"error": "Both student_id and course_codes are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the student using the provided student_id
            student = User.objects.get(custom_id=student_id, role='student')
        except User.DoesNotExist:
            return Response({"error": f"Student with custom ID {student_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Enroll the student in each specified course
        for course_code in course_codes:
            try:
                course = Course.objects.get(course_code=course_code)

                # Validate using the Enrollment serializer
                enrollment_data = {
                    'student_id_input': student_id,
                    'course_code': course
                }
                enrollment_serializer = EnrollmentSerializer(data=enrollment_data)
                enrollment_serializer.is_valid(raise_exception=True)  # This will raise an error if validation fails
                Enrollment.objects.create(student_id=student, course_code=course)
            except Course.DoesNotExist:
                return Response({"error": f"Course with course code {course_code} does not exist."}, status=status.HTTP_400_BAD_REQUEST)
            except serializers.ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": "Student enrolled in specified courses successfully."}, status=status.HTTP_201_CREATED)

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
        except User.DoesNotExist:
            return Response({"error": f"Student with custom ID {student_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        except Enrollment.DoesNotExist:
            return Response({"error": "No enrollment found for this student in the specified course."}, status=status.HTTP_404_NOT_FOUND)

def update_enrollment(self, request, pk=None):
        """
        Admin can update a student's enrollment in a course.
        """
        course = self.get_object()
        student_id = request.data.get("student_id")

        if not student_id:
            return Response({"error": "student_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = User.objects.get(custom_id=student_id, role='student')
            enrollment = Enrollment.objects.get(student_id=student, course_code=course)
            # You can add any additional fields to update as needed
            enrollment.save()  # Assuming you want to just update some fields of the existing enrollment
            return Response({"success": "Enrollment updated successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": f"Student with custom ID {student_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        except Enrollment.DoesNotExist:
            return Response({"error": "No enrollment found for this student in the specified course."}, status=status.HTTP_404_NOT_FOUND)