from django.contrib import admin
from .models import Enrollment, Course
class CourseAdmin(admin.ModelAdmin):

    list_display = ('course_code', 'course_name', 'credit_hours', 'class_lab', 'day_time', 'display_instructor_full_name', 'semester')
    fields = ('course_code', 'course_name', 'credit_hours','day', 'start_time', 'end_time', 'class_lab', 'instructor_id_input', 'semester')

    # Custom method to display instructor's full name in the list view
    def display_instructor_full_name(self, obj):
        return obj.instructor_full_name
    # Change the header of the instructor's full name in the admin view
    display_instructor_full_name.short_description = 'Instructor Full Name'

admin.site.register(Course, CourseAdmin)

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('get_student_id', 'student_name', 'course_code', 'course_name', 'credit_hours', 'semester', 'instructor_name')
    fields = ('course_code', 'student_id')
    search_fields = ('course_code', 'student_id__custom_id', 'student_name', 'course_name', 'instructor_name')
    list_filter = ('semester', 'credit_hours')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # If an object is being edited
            return ['course_code']  # Make the course_code field readonly
        return []

    def get_student_id(self, obj):
        """Display the actual student_id (custom_id) instead of the username."""
        return obj.student_id.custom_id
    get_student_id.short_description = "Student ID"  # Header for the column

# Register the Enrollment model with the EnrollmentAdmin class
admin.site.register(Enrollment, EnrollmentAdmin)
