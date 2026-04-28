from rest_framework import viewsets, permissions
from learner.models.learner import Learner, LearnerStatus
from learner.models.enrollement import Enrollement
from learner.models.payments import Payments
from learner.models.lessons import Lesson
from learner.serializers.enrollement import  EnrollmentSerializer
from learner.serializers.learner import LearnerSerializer, LearnerStatusSerializer
from learner.serializers.payment import PaymentSerializer
from learner.serializers.lessons import LessonSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action


class LearnerStatusViewSet(viewsets.ModelViewSet):
    queryset = LearnerStatus.objects.all()
    serializer_class = LearnerStatusSerializer



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

    def get_queryset(self):
        queryset = Enrollement.objects.all()
        learner_id = self.request.query_params.get("learner")
        if learner_id:
            queryset = queryset.filter(learner_id=learner_id)
        return queryset
    
    @action(detail=False, methods=["get"], url_path="by-learner/(?P<learner_id>[^/.]+)")
    def by_learner(self, request, learner_id=None):
        enrollments = Enrollement.objects.filter(learner_id=learner_id)
        serializer = self.get_serializer(enrollments, many=True)
        return Response(serializer.data)


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
