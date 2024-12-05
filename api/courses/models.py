from django.db import models
from django.conf import settings  # referencing custom User model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
import re
from django.utils import timezone
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser

# Function to generate semester choices dynamically
def current_year():
    return timezone.now().year

SEMESTER_CHOICES = [
    ('Fall', _('Fall')),
    ('Spring', _('Spring')),
    ('Summer', _('Summer')),
]

# Custom validator to ensure semester is not created in the past or future
def validate_semester(value):
    current_semester = SEMESTER_CHOICES()
    valid_semesters = [choice[0] for choice in current_semester]
    
    if value not in valid_semesters:
        raise ValidationError(f'{value} is not a valid semester. Choose one from the current semesters.')

# Validator for course code (3-4 uppercase letters followed by 3 digits)
def validate_course_code(value):
    if not re.match(r'^[A-Z]{3,4}\d{3}$', value):
        raise ValidationError(
            'Course code must consist of 3 or 4 uppercase letters followed by 3 digits (e.g., CSC101).'
        )

class Course(models.Model):
    semester = models.CharField(
        max_length=50,
        choices=[(f"{season} {current_year}", f"{season} {current_year}") for season in dict(SEMESTER_CHOICES).keys()],
        validators=[validate_semester]
    )
    course_code = models.CharField(
        max_length=20,
        primary_key=True,
        unique=True,
        validators=[validate_course_code],
        help_text="Enter 3-4 uppercase letters followed by 3 digits (e.g., CSC101)"
    )
    course_name = models.CharField(max_length=255)
    CREDIT_HOURS_CHOICES = [(i, str(i)) for i in range(1, 5)]
    credit_hours = models.PositiveIntegerField(choices=CREDIT_HOURS_CHOICES)
    class_lab = models.CharField(max_length=10, help_text="Enter the lab number, CL- will be prefixed automatically.")
    day = models.CharField(max_length=10, help_text="Select a day (Monday to Friday).")
    start_time = models.TimeField(help_text="Select start time (between 9 AM and 6 PM).")
    end_time = models.TimeField(help_text="Select end time (between 9 AM and 6 PM).")
    day_time = models.CharField(max_length=255, editable=False)
    instructor_id = models.ForeignKey(
       CustomUser,
        null=True,
        on_delete=models.CASCADE,
        related_name='courses_taught'
    )
    instructor_full_name = models.CharField(max_length=255, editable=False)

    class Meta:
        indexes = [
            models.Index(fields=['course_code']),  # Index on course_code for faster lookups
        ]

    def clean(self):
        """Perform model validation."""
        # Validate instructor
        if self.instructor_id:
            if self.instructor_id.role != 'teacher':
                raise ValidationError("The assigned instructor must have the role of 'teacher'.")

            # Set instructor's full name
            self.instructor_full_name = f"{self.instructor_id.first_name} {self.instructor_id.middle_name or ''} {self.instructor_id.last_name}".strip()

        # Validate time and duration
        def validate_duration(start_time, end_time, credit_hours):
            duration = (datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)).seconds / 3600
            if duration != credit_hours:
                raise ValidationError(f"The duration ({duration} hours) must match credit hours ({credit_hours}).")


        # Ensure class_lab has correct prefix
        if not self.class_lab.startswith("CL-"):
            self.class_lab = f"CL-{self.class_lab}"

    def save(self, *args, **kwargs):
        # Concatenate day and time
        self.day_time = f"{self.day} {self.start_time.strftime('%I:%M %p')} to {self.end_time.strftime('%I:%M %p')}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.course_code


class Enrollment(models.Model):
    student_id = models.ForeignKey(
        CustomUser,
        null=True,
        on_delete=models.CASCADE,
        related_name='enrollments',
        to_field='custom_id'  # Explicitly reference the `custom_id` field in the CustomUser model
    )
    course_code = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    course_name = models.CharField(max_length=255, editable=False)
    credit_hours = models.PositiveIntegerField(editable=False)
    class_lab = models.CharField(max_length=10, editable=False)
    day_time = models.CharField(max_length=255, editable=False)
    instructor_name = models.CharField(max_length=255, editable=False)
    semester = models.CharField(max_length=20, editable=False)
    student_name = models.CharField(max_length=255, editable=False)

    class Meta:
        indexes = [
            models.Index(fields=['student_id']),  # Index on student_id for faster lookups
            models.Index(fields=['course_code']),  # Index on course_code for faster lookups
        ]

    def clean(self):
        """Perform model validation."""
        # Validate student
        if self.student_id.role != 'student':
            raise ValidationError("The assigned user must have the role of 'student'.")

        # Set student name
        self.student_name = f"{self.student_id.first_name} {self.student_id.middle_name or ''} {self.student_id.last_name}".strip()

        # Validate course and populate related fields
        if self.course_code:
            self.course_name = self.course_code.course_name
            self.credit_hours = self.course_code.credit_hours
            self.class_lab = self.course_code.class_lab
            self.day_time = self.course_code.day_time
            self.instructor_name = self.course_code.instructor_full_name
            self.semester = self.course_code.semester

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure `clean()` is called before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student_name} enrolled in {self.course_code} - {self.course_name}"
