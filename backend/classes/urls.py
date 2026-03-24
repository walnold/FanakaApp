from rest_framework.routers import DefaultRouter
from classes.views import CourseViewSet, ClassStatusViewSet
from django.urls import path, include


router = DefaultRouter()
router.register(r"courses", CourseViewSet)
router.register(r"class-status", ClassStatusViewSet)

# urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls))
]

