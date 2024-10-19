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
    list_display = ('student_name', 'course_code', 'course_name', 'credit_hours', 'semester', 'instructor_name')
    fields = ('course_code_input', 'student_id_input')
    search_fields = ('course_code', 'student_name', 'course_name', 'instructor_name')
    list_filter = ('semester', 'credit_hours')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # If an object is being edited
            return ['course_code_input']  # Make the input field readonly
        return []

# Register the Enrollment model with the EnrollmentAdmin class
admin.site.register(Enrollment, EnrollmentAdmin)

