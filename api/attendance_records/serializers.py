from django.utils import timezone 
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Attendance, Course

import json

User = get_user_model()

class AttendanceSerializer(serializers.ModelSerializer):
    # Auto-populated fields
    course_name = serializers.ReadOnlyField()  # Course name is read-only
    instructor_name = serializers.SerializerMethodField()  # Concatenating instructor's name
    student_list = serializers.SerializerMethodField()  # List of students in the course
    students_data = serializers.JSONField(write_only=True)  # Auto-populated field to store in JSON format

    class Meta:
        model = Attendance
        fields = ['attendance_id', 'course_code', 'course_name', 'instructor_id', 'instructor_name', 'student_list', 'date', 'semester', 'students_data', 'status']

    def get_instructor_name(self, obj):
        """Return the concatenated full name of the instructor."""
        return f"{obj.instructor.first_name} {obj.instructor.middle_name or ''} {obj.instructor.last_name}"

    def get_student_list(self, obj):
        """Retrieve and format the list of students for the course."""
        course = Course.objects.get(course_code=obj.course_code)
        students = course.students.all()  # Assuming course has a ManyToMany field with students
        return [{"student_id": student.custom_id, "name": f"{student.first_name} {student.middle_name or ''} {student.last_name}"} for student in students]

    def validate(self, data):
        """Validate the course code and populate relevant fields."""
        course_code = data.get('course_code')
        try:
            # Check if course exists
            course = Course.objects.get(course_code=course_code)
            data['course_name'] = course.course_name  # Populate course name
            data['semester'] = course.semester  # Populate semester

            # Populate students_data as a JSON of student_id: full_name
            students_data = {}
            for student in course.students.all():
                full_name = f"{student.first_name} {student.middle_name or ''} {student.last_name}"
                students_data[student.custom_id] = full_name  # Using custom_id for students
            data['students_data'] = json.dumps(students_data)  # Store as JSON

            # Populate instructor_id and instructor_name
            instructor = self.context['request'].user  # Assuming the instructor is the logged-in user
            data['instructor_id'] = instructor.custom_id  # Using custom_id for instructor
            data['instructor_name'] = f"{instructor.first_name} {instructor.middle_name or ''} {instructor.last_name}"

        except Course.DoesNotExist:
            raise serializers.ValidationError("Invalid course code.")
        return data

    def create(self, validated_data):
        """Override the create method to handle attendance creation."""
        students_data = json.loads(validated_data.pop('students_data'))  # Deserialize JSON data
        status_data = validated_data.get('status')  # Status remains as is (JSON)

        # Create the Attendance record with all necessary fields
        attendance = Attendance.objects.create(
            attendance_id=validated_data['attendance_id'],
            course_code=validated_data['course_code'],
            course_name=validated_data['course_name'],
            instructor_id=validated_data['instructor_id'],
            instructor_name=validated_data['instructor_name'],
            date=timezone.now(),  # Automatically set the date to now
            semester=validated_data['semester'],  # Use the semester from validation
            students_data=students_data,  # Stored as JSON
            status=status_data  # JSON field
        )
        return attendance
