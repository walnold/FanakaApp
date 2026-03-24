from django.db import models
from accounts.models import Staff
from branches.models import Branch
from classes.models import Course
from learner.models.learner import Learner


class EnrollementStatus(models.Model):
    status = models.CharField(max_length=10, unique=True)
    description = models.CharField(200)

    def __str__(self):
        return self.status



class Enrollement(models.Model):
    course  = models.ForeignKey(Course, related_name='enrollements', on_delete=models.SET_NULL, blank=True, null=True)
    learner = models.ForeignKey(Learner, related_name='enrollements', on_delete=models.SET_NULL, blank=True, null=True)
    discount = models.IntegerField()
    lessons = models.IntegerField()
    status = models.ForeignKey(EnrollementStatus, related_name='enrollements', on_delete=models.SET_NULL, null=True, blank=True)
    enrolled_on = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, related_name='created_enrollements')


    def __str__(self):
        return f"{self.course.name} {self.learner.first_name} on {self.enrolled_on}"
