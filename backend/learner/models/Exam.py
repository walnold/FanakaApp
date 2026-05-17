from django.db import models
from accounts.models import Staff
from learner.models.enrollement import Enrollement

class ExamStatus(models.Model):
    status = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.status


class Exam(models.Model):
    enrollment = models.ForeignKey(
        Enrollement,
        related_name='exams',
        on_delete=models.CASCADE
    )
    exam_date = models.DateField()
    created_by = models.ForeignKey(
        Staff,
        related_name='created_exams',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    exam_status = models.ForeignKey(
        ExamStatus,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    created_on = models.DateTimeField(auto_now_add=True)
    edited_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Exam for {self.enrollment.learner} on {self.exam_date}"
