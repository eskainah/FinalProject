from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from courses.models import Enrollment
from accounts.models import CustomUser  # Assuming the CustomUser model is in the accounts app

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
    course_code = models.CharField(max_length=20, editable=False)  # Populated from Enrollment
    course_name = models.CharField(max_length=255, editable=False)  # Populated from Enrollment
    student_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # ForeignKey to CustomUser
    student_name = models.CharField(max_length=255, editable=False)  # Auto-populated from Enrollment
    instructor_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='instructor_attendance')  # ForeignKey to CustomUser
    instructor_name = models.CharField(max_length=255, editable=False)  # Populated from Course via Enrollment
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    semester = models.CharField(max_length=20, editable=False)  # Populated from Enrollment

    def save(self, *args, **kwargs):
        """
        Generate attendance_id and populate fields from the Enrollment model.
        Ensure only one attendance record is created per day for a course.
        """
        # Check if an attendance record already exists for the course on this date
        if Attendance.objects.filter(course_code=self.course_code, date=self.date).exists():
            raise ValidationError(f"Attendance record for {self.course_code} already exists for {self.date}. Only one record can be created per day.")

        # Ensure attendance_id is generated
        if not self.attendance_id:
            last_attendance = Attendance.objects.filter(course_code=self.course_code).order_by('attendance_id').last()
            if last_attendance:
                last_num = int(last_attendance.attendance_id.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            self.attendance_id = f"{self.course_code}-{new_num:03d}"

        # Auto-populate data from Enrollment and save for each student
        try:
            # Fetch the enrollment records for the students in the course
            enrollments = Enrollment.objects.filter(course_code=self.course_code)
            for enrollment in enrollments:
                # Populate student data
                self.student_id = enrollment.student_id
                self.student_name = f"{enrollment.student_id.first_name} {enrollment.student_id.middle_name or ''} {enrollment.student_id.last_name}".strip()
                self.course_name = enrollment.course_name
                self.semester = enrollment.semester
                self.instructor_id = enrollment.course_code.instructor_id
                self.instructor_name = enrollment.course_code.instructor_full_name

                # Save the attendance for the student
                super().save(*args, **kwargs)

        except Exception as e:
            raise ValidationError(f"Error saving attendance: {e}")

    def __str__(self):
        return f"{self.attendance_id} - {self.course_code} - {self.date}"
