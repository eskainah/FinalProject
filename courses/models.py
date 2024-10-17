from django.db import models
from django.conf import settings  # referencing custom User model
from django.core.exceptions import ValidationError
import re
from django.utils import timezone

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

    # Day and Time (Entered directly by the user)
    day_time = models.CharField(max_length=255, help_text="Enter the schedule (e.g., 'Mon & Wed 9-11 AM')")

    # Manually entered instructor custom_id (should correspond to a teacher)
    instructor_id_input = models.CharField(max_length=100, help_text="Enter the Instructor custom ID")

    # Foreign Key to the Custom User model for instructor
    instructor_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,  # Allow null until validation is done
        on_delete=models.CASCADE,
        related_name='courses_taught'
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
            instructor = settings.AUTH_USER_MODEL.objects.get(custom_id=self.instructor_id_input, role='teacher')
            self.instructor_id = instructor  # Set the ForeignKey relationship
            # Concatenate the instructor's name
            self.instructor_full_name = f"{instructor.first_name} {instructor.middle_name or ''} {instructor.last_name}".strip()
        except settings.AUTH_USER_MODEL.DoesNotExist:
            raise ValidationError("The entered Instructor custom ID does not correspond to a valid teacher.")

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

    # Foreign key to the Course model
    course_code = models.ForeignKey(Course, on_delete=models.CASCADE, help_text="Select a course")

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
            student = settings.AUTH_USER_MODEL.objects.get(custom_id=self.student_id_input, role='student')
            self.student_id = student  # Set the ForeignKey relationship
            # Concatenate the student's name
            self.student_name = f"{student.first_name} {student.middle_name or ''} {student.last_name}".strip()
        except settings.AUTH_USER_MODEL.DoesNotExist:
            raise ValidationError("The entered Student custom ID does not correspond to a valid student.")

        # Get the related course object and populate the fields
        course = self.course_code
        self.course_name = course.course_name
        self.credit_hours = course.credit_hours
        self.class_lab = course.class_lab
        self.day_time = course.day_time
        self.instructor_name = course.instructor_full_name
        self.semester = course.semester

        super(Enrollment, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.student_name} enrolled in {self.course_code} - {self.course_name} "
