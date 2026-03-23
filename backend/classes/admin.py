from django.contrib import admin
from classes.models import ClassStatus, Course

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    list_display=["name", "price", "num_of_lessons"]


admin.site.register(ClassStatus)
admin.site.register(Course, CourseAdmin)

