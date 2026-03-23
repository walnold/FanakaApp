from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class Branch(models.Model):
    name = models.CharField(max_length=10)
    description = models.CharField(null=True, blank=True, max_length=200)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='created_branches'
    )
    created_on = models.DateTimeField(auto_now_add=True)

    last_edit_on = models.DateTimeField(auto_now=True)
    last_edit_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='edited_branches',
        null=True,
        blank=True
    )

    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"
