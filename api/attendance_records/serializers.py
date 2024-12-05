from rest_framework import serializers
from .models import Attendance, AttendanceRecord
from accounts.models import CustomUser

class StudentAttendanceSerializer(serializers.ModelSerializer):
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role=CustomUser.STUDENT),
        source='student'
    )
    student_name = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceRecord
        fields = ['student_id', 'student_name', 'status']

    def get_student_name(self, obj):
        """Retrieve the full name of the student from the related CustomUser model."""
        return obj.student.get_full_name()

class AttendanceSerializer(serializers.ModelSerializer):
    instructor_name = serializers.SerializerMethodField()
    students = StudentAttendanceSerializer(source='attendancerecord_set', many=True)

    class Meta:
        model = Attendance
        fields = ['attendance_id', 'course_code', 'course_name', 'students', 'instructor_id', 'instructor_name']
        read_only_fields = ['attendance_id']  # attendance_id is auto-generated

    def get_instructor_name(self, obj):
        """Retrieve the name of the instructor from the related CustomUser model."""
        return obj.instructor_id.get_full_name()

    def validate(self, data):
        """
        Custom validation to ensure that course details (course_code, course_name, and instructor_id) are provided.
        """
        if not data.get('course_code') or not data.get('course_name') or not data.get('instructor_id'):
            raise serializers.ValidationError("Course details (course_code, course_name, instructor) must be provided.")
        return data

    def create(self, validated_data):
        """Override the create method to handle the creation of the attendance record."""
        students_data = validated_data.pop('students', [])
        course_code = validated_data.get('course_code')
        course_name = validated_data.get('course_name')
        instructor_id = validated_data.get('instructor_id')

        # Create attendance record
        attendance = Attendance.objects.create(
            course_code=course_code,
            course_name=course_name,
            instructor_id=instructor_id,
        )

        # Create AttendanceRecord for each student
        for student_data in students_data:
            student = student_data['student']
            status = student_data['status']
            AttendanceRecord.objects.create(
                attendance=attendance,
                student=student,
                status=status
            )

        return attendance
