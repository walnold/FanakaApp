from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from analytics.serializers import EnrollmentComparisonSerializer, EnrollmentPerClassSerializer, LessonsDailySerializer, PaymentsMonthlySerializer, PendingExamsSerializer
from .models import (
    ActiveEnrollmentView, EnrollmentPerClassView, PaymentsMonthlyView,
    LessonsDailyView, PendingExamsView, EnrollmentComparisonView
)

class AnalyticsViewSet(ViewSet):
    def list(self, request):
        branch_id = request.query_params.get("branch_id")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        # Role-based branch scope
        if not request.user.is_Manager:
            branch_id = request.user.branch_id

        # Query views with filters
        active_enrollments = ActiveEnrollmentView.objects.filter(
            branch_id=branch_id if branch_id else None
        ).count()

        enrollments_per_class = EnrollmentPerClassView.objects.filter(
            branch_id=branch_id if branch_id else None
        )

        payments_monthly = PaymentsMonthlyView.objects.filter(
            branch_id=branch_id if branch_id else None
        )

        lessons_daily = LessonsDailyView.objects.filter(
            branch_id=branch_id if branch_id else None,
            lesson_date__range=[start_date, end_date] if start_date and end_date else None
        )

        pending_exams = PendingExamsView.objects.filter(
            branch_id=branch_id if branch_id else None
        )

        enrollment_comparison = EnrollmentComparisonView.objects.filter(
            branch_id=branch_id if branch_id else None
        )

        return Response({
            "summary": {
                "active_enrollments": active_enrollments,
                "payments_monthly": PaymentsMonthlySerializer(payments_monthly, many=True).data,
            },
            "charts": {
                "enrollments_per_class": EnrollmentPerClassSerializer(enrollments_per_class, many=True).data,
                "lessons_daily": LessonsDailySerializer(lessons_daily, many=True).data,
                "enrollment_comparison": EnrollmentComparisonSerializer(enrollment_comparison, many=True).data,
            },
            "pending_exams": PendingExamsSerializer(pending_exams, many=True).data,
        })
