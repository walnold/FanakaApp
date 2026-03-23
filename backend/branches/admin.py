from django.contrib import admin
from branches.models import Branch

class BranchAdmin(admin.ModelAdmin):
    list_display=['id','name','description', 'created_on','created_by']

# Register your models here.
admin.site.register(Branch, BranchAdmin)
