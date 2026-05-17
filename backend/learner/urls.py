from django.urls import path, include
from rest_framework.routers import DefaultRouter
from learner.views.exam import ExamStatusViewSet, ExamViewSet
from learner.views.learner import  LearnerViewSet, EnrollmentViewSet, PaymentViewSet, LessonViewSet, LearnerStatusViewSet

router = DefaultRouter()
router.register(r'learners', LearnerViewSet, basename='learner')
router.register(r'learner-status', LearnerStatusViewSet, basename='learner-status')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'exams', ExamViewSet, basename='exam')
router.register(r'exam-status', ExamStatusViewSet, basename='exam-status')

urlpatterns = [
    path('', include(router.urls)),
]
