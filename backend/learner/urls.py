from django.urls import path, include
from rest_framework.routers import DefaultRouter
from learner.views.learner import  LearnerViewSet, EnrollmentViewSet, PaymentViewSet, LessonViewSet

router = DefaultRouter()
router.register(r'learners', LearnerViewSet, basename='learner')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'lessons', LessonViewSet, basename='lesson')

urlpatterns = [
    path('', include(router.urls)),
]
