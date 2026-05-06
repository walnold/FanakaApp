from rest_framework import viewsets, permissions
from learner.models.learner import Learner, LearnerStatus
from learner.models.enrollement import Enrollement
from learner.models.payments import Payments
from learner.models.lessons import Lesson
from learner.serializers.enrollement import  EnrollmentCreateSerializer, EnrollmentDetailSerializer, EnrollmentOverviewSerializer
from learner.serializers.learner import LearnerSerializer, LearnerStatusSerializer
from learner.serializers.payment import PaymentSerializer
from learner.serializers.lessons import LessonSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from django.db.models import Sum, Count, F
from django.db.models.functions import Coalesce
from django.db.models import Prefetch
from rest_framework.response import Response


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
    # serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication] 

    def get_queryset(self):
        learner_id = self.request.query_params.get("learner")
        qs = (
            Enrollement.objects
            .select_related("course", "learner")
            .prefetch_related("payments", "lessons__set()")
            .annotate(
                total_payments=Coalesce(Sum("payments__amount"), 0),
                lessons_taken=Coalesce(Count("lessons"), 0),
                balance=F("course__price") - F("discount") - Coalesce(Sum("payments__amount"), 0),
                lessons_remaining=F("lessons") - Coalesce(Count("lessons"), 0),
            )
        )
        if learner_id:
            qs = qs.filter(learner_id=learner_id)
        return qs

    def get_serializer_class(self):
        if self.action == "list":
            return EnrollmentOverviewSerializer
        elif self.action == "retrieve":
            return EnrollmentDetailSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return EnrollmentCreateSerializer
        return EnrollmentOverviewSerializer
    
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

    @action(detail=False, methods=["get"], url_path="by-enrollment/(?P<enrollment_id>[^/.]+)")
    def by_enrollment(self, request, enrollment_id=None):
        payments = Payments.objects.filter(enrollement_id=enrollment_id)
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication] 
