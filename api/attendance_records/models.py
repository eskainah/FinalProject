from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from accounts.models import CustomUser 

class Attendance(models.Model):
    # Choices for attendance status
    PRESENT = 'Present'
    ABSENT = 'Absent'
    EXCUSED = 'Excused'

    STATUS_CHOICES = [
        (PRESENT, 'Present'),
        (ABSENT, 'Absent'),
        (EXCUSED, 'Excused'),
    ]

    # Fields
    attendance_id = models.CharField(max_length=20, unique=True, primary_key=True)
    course_code = models.CharField(max_length=20)  # Populated from frontend
    course_name = models.CharField(max_length=255)  # Populated from frontend
    instructor_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='instructor_attendance')  # ForeignKey to CustomUser
    instructor_name = models.CharField(max_length=255)  # Populated from frontend
    date = models.DateField(default=timezone.now)
    students = models.ManyToManyField(CustomUser, through='AttendanceRecord', related_name='attendance_records')

    def save(self, *args, **kwargs):
        """Generate attendance_id and save the attendance record with the data passed during submission."""
        # Ensure only one attendance record is created per day for a course
        if Attendance.objects.filter(course_code=self.course_code, date=self.date).exists():
            raise ValidationError(f"Attendance record for {self.course_code} already exists for {self.date}. Only one record can be created per day.")

        # Generate attendance_id
        if not self.attendance_id:
            # Find all existing attendance_ids for the given course_code
            existing_ids = Attendance.objects.filter(course_code=self.course_code).values_list('attendance_id', flat=True)
            existing_numbers = sorted([int(id.split('-')[-1]) for id in existing_ids])

            # Find the first missing number in the sequence
            new_num = 1
            for num in existing_numbers:
                if num == new_num:
                    new_num += 1  # Continue to the next number if there's no gap
                else:
                    break  # Found the gap, use the missing number

            # Set the attendance_id with the smallest missing number
            self.attendance_id = f"{self.course_code}-{new_num:03d}"

        # Ensure required fields are provided
        if not self.course_code or not self.course_name or not self.instructor_id or not self.instructor_name:
            raise ValidationError("Course details (course_code, course_name, instructor) must be provided.")

        # Save the attendance record
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.attendance_id} - {self.course_code} - {self.date}"

class AttendanceRecord(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=Attendance.STATUS_CHOICES)

    class Meta:
        unique_together = ('attendance', 'student')  # Ensure no duplicate attendance for same student

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.status}"
