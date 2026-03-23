from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from vehicles.models import Vehicle, VehicleStatus, TransmissionType
from vehicles.serializers import (
    VehicleSerializer, VehicleStatusSerializer, TransmissionTypeSerializer,
    VehicleListSerializer, VehicleDetailSerializer
)
from accounts.customPermissions import IsAdminOrReadOnly


class VehicleViewSet(ModelViewSet):
    queryset = Vehicle.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return VehicleListSerializer
        return VehicleDetailSerializer

    # Custom action: filter by status
    @action(detail=False, methods=["get"])
    def by_status(self, request):
        status_param = request.query_params.get("status")
        if not status_param:
            return Response({"error": "status query param required"}, status=status.HTTP_400_BAD_REQUEST)
        vehicles = Vehicle.objects.filter(status__status=status_param)
        serializer = self.get_serializer(vehicles, many=True)
        return Response(serializer.data)

    # Custom action: filter by transmission type
    @action(detail=False, methods=["get"])
    def by_transmission(self, request):
        transmission_param = request.query_params.get("transmission")
        if not transmission_param:
            return Response({"error": "transmission query param required"}, status=status.HTTP_400_BAD_REQUEST)
        vehicles = Vehicle.objects.filter(transmission__type=transmission_param)
        serializer = self.get_serializer(vehicles, many=True)
        return Response(serializer.data)


class VehicleStatusViewSet(ModelViewSet):
    queryset = VehicleStatus.objects.all()
    serializer_class = VehicleStatusSerializer
    permission_classes = [IsAdminOrReadOnly]


class TransmissionTypeViewSet(ModelViewSet):
    queryset = TransmissionType.objects.all()
    serializer_class = TransmissionTypeSerializer
    permission_classes = [IsAdminOrReadOnly]
