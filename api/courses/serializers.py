from rest_framework import serializers
from .models import Course, Enrollment
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone  # Import timezone

User = get_user_model()

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_code', 'course_name', 'credit_hours', 'class_lab', 'day_time', 'instructor_full_name', 'semester']

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['student_id', 'course_code']

    def validate(self, attrs):
        student = attrs.get('student_id')
        course = attrs.get('course_code')

        if not student or not course:
            raise serializers.ValidationError("Both student ID and course code must be provided.")
        
        # Validate that the student exists and has the role of 'student'
        if student.role != 'student':
            raise serializers.ValidationError("The provided user must have the role of 'student'.")
        
        # Ensure that the course exists
        try:
            course = Course.objects.get(course_code=course.course_code)
        except Course.DoesNotExist:
            raise serializers.ValidationError("The provided course code does not exist.")
        
        # Ensure the course is part of the current semester
        current_year = timezone.now().year
        current_semester = timezone.now().strftime(f'Spring {current_year}, Summer {current_year}, Fall {current_year}') 
        # Adjust this logic if your semester logic is different (use `semester_choices()` or similar)
        if course.semester != current_semester:
            raise serializers.ValidationError(f"The course {course.course_code} is not available in the current semester.")

        # Ensure the student is not already enrolled in the course
        if Enrollment.objects.filter(student_id=student, course_code=course).exists():
            raise serializers.ValidationError("This student is already enrolled in the course.")
        
        # Ensure the instructor is valid and assigned
        if course.instructor_id and course.instructor_id.role != 'teacher':
            raise serializers.ValidationError(f"The course {course.course_code} does not have a valid instructor assigned.")
        
        return attrs

    def create(self, validated_data):
        # Create Enrollment
        enrollment = Enrollment.objects.create(**validated_data)
        return enrollment
