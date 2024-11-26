from django.db import models
from django.conf import settings  # referencing custom User model
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
import re
from django.utils import timezone
from datetime import datetime

  # Get the CustomUser model
User = get_user_model()
# Function to generate semester choices dynamically
def current_year():
    return timezone.now().year

def semester_choices():
    current_year = timezone.now().year
    return [
        (f'Fall {current_year}', f'Fall {current_year}'),
        (f'Spring {current_year}', f'Spring {current_year}'),
        (f'Summer {current_year}', f'Summer {current_year}'),
    ]

# Custom validator to ensure semester is not created in the past or future
def validate_semester(value):
    current_semester = semester_choices()
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
    # Course Code (Primary Key) with custom validator
    course_code = models.CharField(
        max_length=20, 
        primary_key=True, 
        unique=True, 
        validators=[validate_course_code],
        help_text="Enter 3-4 uppercase letters followed by 3 digits (e.g., CSC101)"
    )

    course_name = models.CharField(max_length=255)

    # Credit Hours (Choices: 1, 2, 3, 4)
    CREDIT_HOURS_CHOICES = [(i, str(i)) for i in range(1, 5)]
    credit_hours = models.PositiveIntegerField(choices=CREDIT_HOURS_CHOICES)

    # Class-Lab with CL- prefix added automatically
    class_lab = models.CharField(max_length=10, help_text="Enter the lab number, CL- will be prefixed automatically.")

    # Day and Time fields
    day = models.CharField(max_length=10, help_text="Select a day (Monday to Friday).")
    start_time = models.TimeField(help_text="Select start time (between 9 AM and 6 PM).")
    end_time = models.TimeField(help_text="Select end time (between 9 AM and 6 PM).")

    # Day and Time concatenated field
    day_time = models.CharField(max_length=255, editable=False, help_text="Automatically generated schedule (e.g., 'Monday 9:00 AM to 12:00 PM').")

    # Manually entered instructor custom_id (should correspond to a teacher)
    instructor_id_input = models.CharField(max_length=100, help_text="Enter the Instructor custom ID")

    # Foreign Key to the Custom User model for instructor
    instructor_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,  # Allow null until validation is done
        on_delete=models.CASCADE,
        related_name='courses_taught',
        editable=False
    )

    # Instructor's full name (Concatenated first, middle, and last names)
    instructor_full_name = models.CharField(max_length=255, editable=False)  # Auto-populated

    # Semester (Fall, Spring, Summer of the current year)
    semester = models.CharField(
        max_length=20, 
        choices=semester_choices(), 
        validators=[validate_semester],
        help_text="Choose from the current semesters (e.g., 'Fall 2024')."
    )

    # Overriding the save method to ensure CL- prefix for class_lab and to validate instructor custom_id
    def save(self, *args, **kwargs):
        # Add CL- prefix to class_lab if not already present
        if not self.class_lab.startswith("CL-"):
            self.class_lab = f"CL-{self.class_lab}"

        # Validate and fetch instructor custom_id based on input
        try:
            instructor = User.objects.get(custom_id=self.instructor_id_input, role='teacher')
            self.instructor_id = instructor  # Set the ForeignKey relationship to the instructor
            # Concatenate the instructor's name
            self.instructor_full_name = f"{instructor.first_name} {instructor.middle_name or ''} {instructor.last_name}".strip()
        except User.DoesNotExist:
            raise ValidationError("The entered Instructor custom ID does not correspond to a valid teacher.")

        # Check if the end time is greater than the start time
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be greater than start time.")

        # Calculate duration in hours
        duration = (datetime.combine(datetime.today(), self.end_time) - datetime.combine(datetime.today(), self.start_time)).seconds / 3600
        
        # Validate duration against credit hours
        if duration != self.credit_hours:
            raise ValidationError(f"The duration must be exactly {self.credit_hours} hour(s).")

        # Attempt to save the course, handle IntegrityError
        try:
            super(Course, self).save(*args, **kwargs)
        except IntegrityError:
            raise ValidationError(f"A course with the course code '{self.course_code}' already exists. Please use a different course code.")

        # Concatenate day and time for the day_time field
        self.day_time = f"{self.day} {self.start_time.strftime('%I:%M %p')} to {self.end_time.strftime('%I:%M %p')}"
        
        # Call the parent save method to finalize the save
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.course_name} ({self.course_code})"

class Enrollment(models.Model):
    # Manually entered student custom_id (should correspond to a student)
    student_id_input = models.CharField(max_length=100, help_text="Enter the Student custom ID")

    # Foreign Key to the Custom User model for student
    student_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,  # Allow null until validation is done
        on_delete=models.CASCADE,
        related_name='enrollments'
    )

    # Editable field for user to input course code
    course_code_input = models.CharField(max_length=20, help_text="Enter the Course Code (e.g., CSC101)")

    # Foreign key to the Course model (non-editable)
    course_code = models.ForeignKey(Course, on_delete=models.CASCADE, help_text="Select a course", editable=False)

    # Automatically populated fields from the Course model
    course_name = models.CharField(max_length=255, editable=False)  # Auto-populated
    credit_hours = models.PositiveIntegerField(editable=False)  # Auto-populated
    class_lab = models.CharField(max_length=10, editable=False)  # Auto-populated
    day_time = models.CharField(max_length=255, editable=False)  # Auto-populated
    instructor_name = models.CharField(max_length=255, editable=False)  # Auto-populated
    semester = models.CharField(max_length=20, editable=False)  # Auto-populated
    student_name = models.CharField(max_length=255, editable=False)  # Concatenated student name

    def save(self, *args, **kwargs):
        """
        Validate student custom_id and automatically populate the fields from the selected course.
        """
        # Validate and fetch student custom_id based on input
        try:
            student = User.objects.get(custom_id=self.student_id_input, role='student')
            self.student_id = student  # Set the ForeignKey relationship
            # Concatenate the student's name
            self.student_name = f"{student.first_name} {student.middle_name or ''} {student.last_name}".strip()
        except settings.AUTH_USER_MODEL.DoesNotExist:
            raise ValidationError("The entered Student custom ID does not correspond to a valid student.")

        # Validate course_code_input and fetch the corresponding Course
        try:
            course = Course.objects.get(course_code=self.course_code_input)
            self.course_code = course  # Set the ForeignKey relationship
            # Populate fields from the Course model
            self.course_name = course.course_name
            self.credit_hours = course.credit_hours
            self.class_lab = course.class_lab
            self.day_time = course.day_time
            self.instructor_name = course.instructor_full_name
            self.semester = course.semester
        except Course.DoesNotExist:
            raise ValidationError(f"The course code '{self.course_code_input}' does not exist. Please enter a valid course code.")

        # Call the parent save method to finalize the save
        super(Enrollment, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.student_name} enrolled in {self.course_code} - {self.course_name}"