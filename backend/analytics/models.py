from django.db import models
class ActiveEnrollmentView(models.Model):
    id = models.IntegerField(primary_key=True)
    course_id = models.IntegerField()
    learner_id = models.IntegerField()
    enrolled_on = models.DateField()
    branch_id = models.IntegerField()
    class Meta: managed = False; db_table = "v_active_enrollments"

class EnrollmentPerClassView(models.Model):
    course_name = models.CharField(max_length=100)
    enrollment_count = models.IntegerField()
    branch_id = models.IntegerField()
    month = models.CharField(max_length=7)
    class Meta: managed = False; db_table = "v_enrollments_per_class"

class PaymentsMonthlyView(models.Model):
    branch_id = models.IntegerField()
    branch_name = models.CharField(max_length=100)
    month = models.CharField(max_length=7)
    total_amount = models.IntegerField()
    class Meta: managed = False; db_table = "v_payments_monthly"

class LessonsDailyView(models.Model):
    lesson_date = models.DateField()
    lessons_count = models.IntegerField()
    branch_id = models.IntegerField()
    class Meta: managed = False; db_table = "v_lessons_daily"

class PendingExamsView(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    course_name = models.CharField(max_length=100)
    exam_date = models.DateField()
    status = models.CharField(max_length=20)
    branch_id = models.IntegerField()
    class Meta: managed = False; db_table = "v_pending_exams"

class EnrollmentComparisonView(models.Model):
    course_name = models.CharField(max_length=100)
    month = models.CharField(max_length=7)
    enrollment_count = models.IntegerField()
    branch_id = models.IntegerField()
    class Meta: managed = False; db_table = "v_enrollment_comparison"


