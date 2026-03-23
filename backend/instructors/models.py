from django.db import models

# Create your models here.
class InstructorStatus(models.Model):
    status  = models.CharField(max_length=20, unique=True, blank=False, null=False)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.status


class Instructor(models.Model):
    first_name = models.CharField(max_length=20, blank=False, null=False)
    last_name  = models.CharField(max_length=20, blank=False, null=False)
    phoneNumber  = models.CharField(max_length=15)
    idNumber = models.CharField(max_length=15)
    hire_date  = models.DateField(auto_now_add=True)
    status = models.ForeignKey(InstructorStatus, on_delete=models.SET_NULL, null=True, blank=True, related_name='instructors')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
