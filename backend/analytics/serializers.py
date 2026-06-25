from rest_framework import serializers
from analytics.models import ActiveEnrollmentView, EnrollmentComparisonView, EnrollmentPerClassView, LessonsDailyView, PaymentsMonthlyView, PendingExamsView
# from learner.models.enrollement import Enrollement
# from learner.models.lessons import Lesson
# from learner.models.Exam import Exam
# from learner.models.payments import Payments
# from django.db.models import Count, Sum
# from datetime import date

# class SummarySerializer(serializers.Serializer):
#     active_enrollments = serializers.IntegerField()
#     new_enrollments = serializers.IntegerField()
#     payments_this_month = serializers.IntegerField()
#     pending_exams = serializers.IntegerField()

# class LessonsDailySerializer(serializers.Serializer):
#     date = serializers.DateField()
#     count = serializers.IntegerField()

# class EnrollmentsPerClassSerializer(serializers.Serializer):
#     course = serializers.CharField()
#     count = serializers.IntegerField()

# class EnrollmentOverviewSerializer(serializers.Serializer):
#     active = serializers.IntegerField()
#     new = serializers.IntegerField()
#     inactive = serializers.IntegerField()

# class PendingExamSerializer(serializers.Serializer):
#     student = serializers.CharField()
#     course = serializers.CharField()
#     exam = serializers.CharField()
#     status = serializers.CharField()

# class AnalyticsSerializer(serializers.Serializer):
#     summary = SummarySerializer()
#     charts = serializers.DictField()
#     pending_exams = PendingExamSerializer(many=True)

class ActiveEnrollmentSerializer(serializers.ModelSerializer):
    class Meta: model = ActiveEnrollmentView; fields = "__all__"

class EnrollmentPerClassSerializer(serializers.ModelSerializer):
    class Meta: model = EnrollmentPerClassView; fields = "__all__"

class PaymentsMonthlySerializer(serializers.ModelSerializer):
    class Meta: model = PaymentsMonthlyView; fields = "__all__"

class LessonsDailySerializer(serializers.ModelSerializer):
    class Meta: model = LessonsDailyView; fields = "__all__"

class PendingExamsSerializer(serializers.ModelSerializer):
    class Meta: model = PendingExamsView; fields = "__all__"

class EnrollmentComparisonSerializer(serializers.ModelSerializer):
    class Meta: model = EnrollmentComparisonView; fields = "__all__"
