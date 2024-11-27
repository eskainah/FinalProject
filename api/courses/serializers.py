from rest_framework import serializers
from .models import Course, Enrollment

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_code', 'course_name', 'credit_hours', 'class_lab', 'day_time', 'instructor_full_name', 'semester']

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['student_id_input', 'course_code']

    def validate(self, attrs):
        # Ensure that student_id_input and course_code are provided
        if not attrs.get('student_id_input') or not attrs.get('course_code'):
            raise serializers.ValidationError("Both student ID and course code must be provided.")
        return attrs