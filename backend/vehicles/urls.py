from rest_framework.routers import DefaultRouter
from vehicles.views import VehicleViewSet, VehicleStatusViewSet, TransmissionTypeViewSet

router = DefaultRouter()
router.register(r"vehicles", VehicleViewSet)
router.register(r"vehicle-status", VehicleStatusViewSet)
router.register(r"transmission-types", TransmissionTypeViewSet)

urlpatterns = router.urls
