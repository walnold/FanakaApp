from rest_framework import serializers
from vehicles.models import Vehicle, VehicleStatus, TransmissionType

# Full serializers
class VehicleStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleStatus
        fields = "__all__"

class TransmissionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransmissionType
        fields = "__all__"

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"


# Custom serializers for different contexts
class VehicleListSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="status.status")
    transmission = serializers.CharField(source="transmission.type")

    class Meta:
        model = Vehicle
        fields = ["number_plate", "status", "transmission"]

class VehicleDetailSerializer(serializers.ModelSerializer):
    status = serializers.StringRelatedField()
    transmission = serializers.StringRelatedField()

    class Meta:
        model = Vehicle
        fields = "__all__"
