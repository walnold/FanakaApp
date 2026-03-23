from django.contrib import admin
from accounts.models import Staff

class StaffAdmin(admin.ModelAdmin):
    # fields=["__all__"]
    list_display = ['first_name', 'last_name', 'email', 'phoneNumber']

# Register your models here.
admin.site.register(Staff, StaffAdmin)
