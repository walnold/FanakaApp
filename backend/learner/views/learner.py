from rest_framework import viewsets, permissions
from learner.models.learner import Learner
from learner.models.enrollement import Enrollement
from learner.models.payments import Payments
from learner.models.lessons import Lesson
from learner.serializers.enrollement import  EnrollmentSerializer
from learner.serializers.learner import LearnerSerializer
from learner.serializers.payment import PaymentSerializer
from learner.serializers.lessons import LessonSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication


class LearnerViewSet(viewsets.ModelViewSet):
    queryset = Learner.objects.all()
    serializer_class = LearnerSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication] 

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollement.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication] 

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication] 

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication] 
