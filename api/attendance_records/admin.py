from django.contrib import admin
from .models import Attendance, AttendanceRecord

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('attendance_id', 'course_code', 'course_name', 'instructor_name', 'date')
    list_filter = ('course_code', 'date')
    search_fields = ('attendance_id', 'course_code', 'course_name', 'instructor_name')
    date_hierarchy = 'date'
    ordering = ('-date',)

    # Customize the form to show related records
    def get_readonly_fields(self, request, obj=None):
        """Make certain fields read-only after creation."""
        if obj:
            return ['attendance_id', 'course_code', 'course_name', 'instructor_name', 'date']
        return []

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('attendance', 'student', 'status')
    list_filter = ('status',)
    search_fields = ('attendance__course_code', 'student__custom_id', 'student__first_name', 'student__last_name')
    ordering = ('attendance', 'student')
