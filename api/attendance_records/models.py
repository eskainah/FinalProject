from django.db import models
from accounts.models import CustomUser
from courses.models import Course
from django.utils import timezone
import json

class Attendance(models.Model):
    PRESENT = 'Present'
    ABSENT = 'Absent'
    EXCUSED = 'Excused'

    STATUS_CHOICES = [
        (PRESENT, 'Present'),
        (ABSENT, 'Absent'),
        (EXCUSED, 'Excused'),
    ]

    attendance_id = models.CharField(max_length=20, unique=True, primary_key=True)
    course_code = models.CharField(max_length=10)  # Teacher-entered course code
    course_name = models.CharField(max_length=100, blank=True)  # Auto-populated course name
    instructor_id = models.CharField(max_length=10, blank=True)  # Auto-populated instructor ID
    instructor_name = models.CharField(max_length=100, blank=True)  # Concatenated instructor name
    students_data = models.JSONField(default=dict)  # Stores student IDs and concatenated names
    date = models.DateField(default=timezone.now)
    semester = models.CharField(max_length=10)
    status = models.JSONField(default=dict)  # Stores student IDs and statuses as a JSON

    def __str__(self):
        return f"{self.attendance_id} - {self.course_code} - {self.date}"

    def save(self, *args, **kwargs):
        if not self.attendance_id:
            # Get the last attendance record for the same course code
            last_attendance = Attendance.objects.filter(course_code=self.course_code).order_by('attendance_id').last()
            if last_attendance:
                last_num = int(last_attendance.attendance_id.split('-')[1])
                new_num = last_num + 1
            else:
                new_num = 1
            self.attendance_id = f"{self.course_code}-{new_num:03d}"  # e.g., CSC100-001

        # Auto-populate instructor name and ID if available
        if self.instructor_id and not self.instructor_name:
            instructor = CustomUser.objects.get(custom_id=self.instructor_id)
            self.instructor_name = f"{instructor.first_name} {instructor.middle_name or ''} {instructor.last_name}"

        super().save(*args, **kwargs)
