from django.db import models
from learner.models.enrollement import Enrollement
from accounts.models import Staff




class Payments(models.Model):
    amount = models.IntegerField()
    transaction_code = models.CharField(max_length=20, unique=True)
    paymentMode = models.CharField(max_length=30)
    enrollement = models.ForeignKey(Enrollement, related_name='payments', on_delete=models.SET_NULL, blank=True, null=True)
    payed_on = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, related_name='created_payemnts')