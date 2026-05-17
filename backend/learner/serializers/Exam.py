from rest_framework import serializers
from learner.models.Exam import Exam, ExamStatus

class ExamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'enrollment', 'exam_date', 'exam_status']

    def validate(self, data):
        enrollment = data['enrollment']
        course_fee = enrollment.course.price
        discount = enrollment.discount or 0
        effective_fee = course_fee - discount

        total_paid = sum(p.amount for p in enrollment.payments.all())
        if total_paid < effective_fee:
            raise serializers.ValidationError(
                "Exam cannot be scheduled until full payment is complete."
            )
        return data

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
    



class ExamListSerializer(serializers.ModelSerializer):
    learner_name = serializers.CharField(source="enrollment.learner.first_name", read_only=True)
    course_name = serializers.CharField(source="enrollment.course.name", read_only=True)
    exam_status = serializers.CharField(source="exam_status.status", read_only=True)

    class Meta:
        model = Exam
        fields = ['id', 'exam_date', 'exam_status', 'learner_name', 'course_name']



from learner.serializers.enrollement import EnrollmentDetailSerializer

class ExamDetailSerializer(serializers.ModelSerializer):
    enrollment = EnrollmentDetailSerializer(read_only=True)
    exam_status = serializers.CharField(source="exam_status.status", read_only=True)

    class Meta:
        model = Exam
        fields = [
            'id', 'exam_date', 'exam_status',
            'enrollment', 'created_by',
            'created_on', 'edited_on'
        ]


class ExamStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamStatus
        fields = "__all__"

