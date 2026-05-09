from rest_framework import serializers
from instructors.models import Instructor
from learner.models.lessons import Lesson
from learner.models.enrollement import Enrollement
from vehicles.models import Vehicle
from django.db.models import Sum

# class LessonSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Lesson
#         fields = ['id', 'learner','enrollment', 'instructor','lesson_time', 'vehicle', 'created_on', 'creted_by']
#         read_only_fields = ['creted_by', 'created_on']

#     def validate(self, data):

#         print("VALIDATED DATA:", data)

#         learner = data.get('Learner')
#         enrollment = data.get('enrollment')


       

#         if not learner:
#             raise serializers.ValidationError({
#                 "Learner": "Learner is required."
#             })

#         if not enrollment:
#             raise serializers.ValidationError({
#                 "enrollment": "Enrollment is required."
#             })


#         if enrollment.learner_id != learner.id:
#             raise serializers.ValidationError(
#                 "Selected enrollment does not belong to learner."
#             )


#         # 1. One lesson per day
#         if Lesson.objects.filter(Learner=learner, lesson_time=data.get('lesson_time')).exists():
#             raise serializers.ValidationError("Learner already has a lesson for this day.")

#         # 2. Payment vs lessons constraint
#         course_fee = enrollment.course.price
#         discount = enrollment.discount or 0
#         effective_fee = course_fee - discount

#         total_paid = sum(p.amount for p in enrollment.payments.all())
#         total_lessons = enrollment.num_of_lessons
#         lessons_taken = Lesson.objects.filter(Learner=learner).count() + 1

#         lessons_allowed = int((total_paid / effective_fee) * total_lessons)

#         if lessons_taken > lessons_allowed:
#             raise serializers.ValidationError(
#                 f"Insufficient payment. Allowed {lessons_allowed} lessons, "
#                 f"but trying to create lesson #{lessons_taken}."
#             )

#         return data

#     def create(self, validated_data):
#         validated_data['creted_by'] = self.context['request'].user
#         return super().create(validated_data)


class LessonSerializer(serializers.ModelSerializer):

    # =========================
    # Writable fields (POST/PUT)
    # =========================
    enrollment = serializers.PrimaryKeyRelatedField(
        queryset=Enrollement.objects.select_related("course", "learner")
    )

    instructor = serializers.PrimaryKeyRelatedField(
        queryset=Instructor.objects.all()
    )

    vehicle = serializers.PrimaryKeyRelatedField(
        queryset=Vehicle.objects.all()
    )

    # =========================
    # Human-readable fields
    # =========================
    learner_name = serializers.CharField(
        source="enrollment.learner",
        read_only=True
    )

    course_name = serializers.CharField(
        source="enrollment.course.name",
        read_only=True
    )

    instructor_name = serializers.StringRelatedField(
        source="instructor",
        read_only=True
    )

    vehicle_name = serializers.CharField(
        source="vehicle.number_plate",
        read_only=True
    )

    created_by_name = serializers.StringRelatedField(
        source="created_by",
        read_only=True
    )

    class Meta:
        model = Lesson
        fields = [
            "id",

            # IDs
            "enrollment",
            "instructor",
            "vehicle",

            # Human-readable
            "learner_name",
            "course_name",
            "instructor_name",
            "vehicle_name",
            "created_by_name",

            # Dates
            "lesson_time",
            "created_on",

            # metadata
            "created_by",
        ]

        read_only_fields = [
            "created_by",
            "created_on",
        ]

    def validate(self, attrs):

        print("VALIDATED DATA:", attrs)

        enrollment = attrs.get("enrollment")
        lesson_time = attrs.get("lesson_time")

        if not enrollment:
            raise serializers.ValidationError({
                "enrollment": "Enrollment is required."
            })

        if not lesson_time:
            raise serializers.ValidationError({
                "lesson_time": "Lesson time is required."
            })

        learner = enrollment.learner
        lesson_date = lesson_time.date()

        # ======================================
        # 1. One lesson per learner per day
        # ======================================
        lesson_exists = Lesson.objects.filter(
            enrollment__learner=learner,
            lesson_time__date=lesson_date
        ).exists()

        if lesson_exists:
            raise serializers.ValidationError({
                "lesson_time": "Learner already has a lesson for this day."
            })

        # ======================================
        # 2. Payment validation
        # ======================================
        course_fee = enrollment.course.price or 0
        discount = enrollment.discount or 0

        effective_fee = course_fee - discount

        if effective_fee <= 0:
            raise serializers.ValidationError({
                "payment": "Invalid course fee or discount configuration."
            })

        total_paid = enrollment.payments.aggregate(
            total=Sum("amount")
        ).get("total") or 0

        total_lessons = enrollment.num_of_lessons or 0

        if total_lessons <= 0:
            raise serializers.ValidationError({
                "num_of_lessons": "Enrollment has invalid number of lessons."
            })

        lessons_taken = Lesson.objects.filter(
            enrollment=enrollment
        ).count() + 1

        lessons_allowed = int(
            (total_paid / effective_fee) * total_lessons
        )

        if lessons_taken > lessons_allowed:
            raise serializers.ValidationError({
                "payment": (
                    f"Insufficient payment. "
                    f"Allowed {lessons_allowed}, "
                    f"trying lesson #{lessons_taken}"
                )
            })

        return attrs

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)