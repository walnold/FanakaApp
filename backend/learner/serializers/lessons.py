from rest_framework import serializers
from learner.models.lessons import Lesson
from learner.models.enrollement import Enrollement

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'Learner', 'instructor', 'vehicle', 'created_on', 'creted_by']
        read_only_fields = ['creted_by', 'created_on']

    def validate(self, data):
        learner = data['Learner']
        enrollement = Enrollement.objects.filter(learner=learner).first()
        if not enrollement:
            raise serializers.ValidationError("Learner must be enrolled in a course.")

        # 1. One lesson per day
        if Lesson.objects.filter(Learner=learner, created_on=data.get('created_on')).exists():
            raise serializers.ValidationError("Learner already has a lesson for this day.")

        # 2. Payment vs lessons constraint
        course_fee = enrollement.course.price
        discount = enrollement.discount or 0
        effective_fee = course_fee - discount

        total_paid = sum(p.amount for p in enrollement.payments.all())
        total_lessons = enrollement.lessons
        lessons_taken = Lesson.objects.filter(Learner=learner).count() + 1

        lessons_allowed = int((total_paid / effective_fee) * total_lessons)

        if lessons_taken > lessons_allowed:
            raise serializers.ValidationError(
                f"Insufficient payment. Allowed {lessons_allowed} lessons, "
                f"but trying to create lesson #{lessons_taken}."
            )

        return data

    def create(self, validated_data):
        validated_data['creted_by'] = self.context['request'].user
        return super().create(validated_data)
