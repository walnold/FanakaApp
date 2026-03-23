from django.db import models
from django.contrib.auth.models import AbstractUser

class Staff(AbstractUser):
    email = models.EmailField(unique=True, db_index=True)
    phoneNumber = models.CharField(max_length=15, unique=True)
    idNumber = models.CharField(max_length=20, unique=True)
    is_Manager = models.BooleanField(default=False)
    

    branch = models.ForeignKey(
        'branches.Branch',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='users'
    )

    is_deleted = models.BooleanField(default=False)

    # objects = models.Manager()

    # class ActiveStaffManager(models.Manager):
    #     def get_queryset(self):
    #         return super().get_queryset().filter(is_deleted=False)

    # active = ActiveStaffManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



# class Manager(models.Model):
    # staff = models.OneToOneField(
    #     Staff,
    #     on_delete=models.CASCADE,
    #     related_name='manager_profile'
    # )
    # department = models.CharField(max_length=100, null=True, blank=True)

    # def __str__(self):
    #     return f"Manager: {self.staff.username}"


# class GeneralStaff(models.Model):
#     staff = models.OneToOneField(
#         Staff,
#         on_delete=models.CASCADE,
#         related_name='general_profile'
#     )
#     role_description = models.CharField(max_length=200, null=True, blank=True)

#     def __str__(self):
#         return f"General Staff: {self.staff.username}"



