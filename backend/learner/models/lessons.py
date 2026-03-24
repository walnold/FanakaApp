from django.db import models
from learner.models.learner import Learner
from vehicles.models import Vehicle
from instructors.models import Instructor
from accounts.models import Staff

class Lesson(models.Model):
   
    Learner = models.ForeignKey(Learner, related_name='lessons', on_delete=models.SET_NULL, null=True, blank=True)
    instructor = models.ForeignKey(Instructor, related_name='lessons', on_delete=models.SET_NULL, null=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, related_name='lessons', on_delete=models.SET_NULL, null=True, blank=True)
    created_on = models.DateField(auto_now_add=True)
    creted_by = models.ForeignKey(Staff, related_name='createdlessons', on_delete=models.SET_NULL, null=True, blank=True)
   


    def __str__(self):
       return f"{self.Learner.name} {self.vehicle.number_plate} {self.created_on}"
   