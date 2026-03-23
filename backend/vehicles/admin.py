from django.contrib import admin
from vehicles.models  import TransmissionType, Vehicle, VehicleStatus

# Register your models here.

admin.site.register(TransmissionType)
admin.site.register(VehicleStatus)
admin.site.register(Vehicle)
