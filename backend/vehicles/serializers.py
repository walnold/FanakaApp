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

    status = serializers.PrimaryKeyRelatedField(read_only=True)
    transmission = serializers.PrimaryKeyRelatedField(read_only=True)

    status_display = serializers.CharField(source="status.status", read_only=True)
    transmission_display = serializers.CharField(source="transmission.type", read_only=True)

    class Meta:
        model = Vehicle
        fields = ["id", "number_plate", "status", "status_display", "transmission", "transmission_display", "yom"]

    def get_status(self, obj):
        if obj.status:
            return obj.status.status
        return None

    def get_transmission(self, obj):
        if obj.transmission:
            return obj.transmission.type
        return None

class VehicleDetailSerializer(serializers.ModelSerializer):
    status = serializers.PrimaryKeyRelatedField(queryset=VehicleStatus.objects.all())
    transmission = serializers.PrimaryKeyRelatedField(queryset=TransmissionType.objects.all())

    status_display = serializers.CharField(source="status.status", read_only=True)
    transmission_display = serializers.CharField(source="transmission.type", read_only=True)

    class Meta:
        model = Vehicle
        fields = "__all__"
