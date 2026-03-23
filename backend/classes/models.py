from django.db import models

# Create your models here.
class ClassStatus(models.Model):
    status = models.CharField(max_length=20, blank=False, null=False, unique =True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.status



class Course(models.Model):
    name = models.CharField(max_length=15, blank=True, null=True)
    description = models.CharField(max_length=300)
    num_of_lessons = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=2)



    def __str__(self):
        return f"{self.name}"