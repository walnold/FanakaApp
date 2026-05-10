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
from django.db.models import Q


class LearnerStatusViewSet(viewsets.ModelViewSet):
    queryset = LearnerStatus.objects.all()
    serializer_class = LearnerStatusSerializer



class LearnerViewSet(viewsets.ModelViewSet):
    queryset = Learner.objects.all()
    serializer_class = LearnerSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication] 

    def get_queryset(self):
        qs = Learner.objects.all()

        # If user is not a manager or superuser, restrict to their branch
        user = self.request.user
        if not getattr(user, "is_Manager", False) and not user.is_superuser:
            if user.branch_id:
                qs = qs.filter(branch_id=user.branch_id)
            else:
                qs = qs.none()  # no branch assigned → no learners visible

        return qs

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
            .prefetch_related("payments", "lesson_items")
            .annotate(
                total_payments=Coalesce(Sum("payments__amount"), 0),
                lessons_taken=Coalesce(Count("lesson_items"), 0),
                balance=F("course__price") - F("discount") - Coalesce(Sum("payments__amount"), 0),
                lessons_remaining=F("num_of_lessons") - Coalesce(Count("lesson_items"), 0),
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
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        qs = (
            Lesson.objects
            .select_related("enrollment", "instructor", "vehicle")
            .all()
        )

        enrollment_id = self.request.query_params.get("enrollment")
        learner_id = self.request.query_params.get("learner")
        location = self.request.query_params.get("location")

        # 🔹 filter by enrollment
        if enrollment_id:
            qs = qs.filter(enrollment_id=enrollment_id)

        # 🔹 filter by learner (through enrollment)
        if learner_id:
            qs = qs.filter(enrollment__learner_id=learner_id)

        # 🔹 filter by location (only if your model has it or related model does)
        if location:
            qs = qs.filter(
                Q(vehicle__number_plate__icontains=location) |
                Q(instructor__first_name__icontains=location) |
                Q(instructor__last_name__icontains=location)
            )

        return qs