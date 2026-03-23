from rest_framework.routers import DefaultRouter
from classes.views import CourseViewSet, ClassStatusViewSet

router = DefaultRouter()
router.register(r"courses", CourseViewSet)
router.register(r"class-status", ClassStatusViewSet)

urlpatterns = router.urls
