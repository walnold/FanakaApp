from django.db import models
from learner.models.learner import Learner
from vehicles.models import Vehicle
from instructors.models import Instructor
from accounts.models import Staff
from datetime import datetime
from learner.models.enrollement import Enrollement

class Lesson(models.Model):
   
    # learner = models.ForeignKey(Learner, related_name='lessons', on_delete=models.SET_NULL, null=True, blank=True)
    instructor = models.ForeignKey(Instructor, related_name='lessons', on_delete=models.SET_NULL, null=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, related_name='lessons', on_delete=models.SET_NULL, null=True, blank=True)
    enrollment = models.ForeignKey(Enrollement, related_name='lesson_items', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    lesson_time = models.DateTimeField(null=False, blank=False, default=datetime.now)
    created_on = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(Staff, related_name='createdlessons', on_delete=models.SET_NULL, null=True, blank=True)

   


    def __str__(self):
       return f"{self.enrollment} {self.vehicle.number_plate} {self.created_on}"
   