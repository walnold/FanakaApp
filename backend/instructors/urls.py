from rest_framework.routers import DefaultRouter
from instructors.views import InstructorViewSet, InstructorStatusViewSet

router = DefaultRouter()
router.register(r"instructors", InstructorViewSet)
router.register(r"instructor-status", InstructorStatusViewSet)

urlpatterns = router.urls
