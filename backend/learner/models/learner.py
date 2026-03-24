from django.db import models
from branches.models import Branch

class LearnerStatus(models.Model):
    status = models.CharField(blank=False, null=False, max_length=10, unique=True, db_index=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.status


# Create your models here.
class Learner(models.Model):
    first_name = models.CharField(max_length=20, blank=False, null=False)
    last_name = models.CharField(max_length=20, blank=False, null=False)
    idNumber = models.CharField(max_length=20, null=False, blank=False, unique=True, db_index=True)
    status = models.ForeignKey(LearnerStatus, related_name='learners', on_delete=models.SET_NULL)
    branch = models.ForeignKey(Branch, related_name="learners", on_delete=models.SET_NULL)



    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    


