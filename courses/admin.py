from django.contrib import admin
from .models import Enrollment, Course

admin.site.register(Enrollment)
admin.site.register(Course)