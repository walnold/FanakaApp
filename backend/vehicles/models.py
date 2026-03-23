from django.db import models

# Create your models here.
class TransmissionType(models.Model):
    type = models.CharField(max_length=15, null=False, blank=False)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.type



class VehicleStatus(models.Model):
    status = models.CharField(unique=True, 
                              max_length=15,
                              blank=False, 
                              null=False)
    description= models.CharField(max_length=200)

    def __str__(self):
        return self.status



class Vehicle(models.Model):
    number_plate = models.CharField(unique=True, max_length=9, blank=False, null=False)
    transmission = models.ForeignKey(TransmissionType, 
                                     on_delete=models.SET_NULL,
                                     blank=True, null=True, 
                                     related_name='vehicles')
    status = models.ForeignKey(VehicleStatus, 
                               on_delete=models.SET_NULL, 
                               blank=True, null=True, related_name='vehicles')
    
    yom= models.IntegerField()


    def __str__(self):
        return self.number_plate




