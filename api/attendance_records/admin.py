from django.contrib import admin
from .models import Attendance

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_name', 'instructor_name', 'date', 'semester', 'status')
    search_fields = ('course_code', 'instructor_name')
    list_filter = ('date', 'semester', 'status')

admin.site.register(Attendance, AttendanceAdmin)