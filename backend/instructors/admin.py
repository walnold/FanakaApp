from django.contrib import admin
from instructors.models import InstructorStatus, Instructor

# Register your models here.
admin.site.register(InstructorStatus)
admin.site.register(Instructor)
