from rest_framework import serializers
from learner.models.enrollement import Enrollement
from learner.models.lessons import Lesson
from learner.models.payments import Payments
from rest_framework import serializers
from learner.models.enrollement import Enrollement






# from classes.models import Course

# class EnrollmentSerializer(serializers.ModelSerializer):
#     course_name = serializers.CharField(source="course.name", read_only=True)
#     enrollment_status = serializers.CharField(source='EnrollementStatus.status')


#     #aggregated fields 
#     total_payments = serializers.SerializerMethodField()
#     balance = serializers.SerializerMethodField()
#     lessons_taken = serializers.SerializerMethodField()
#     lessons_remaining = serializers.SerializerMethodField()


#     class Meta:
#         model = Enrollement
#         fields = ['id', 'course','course_name',
#                    'learner', 
#                   'discount', 'lessons',
#                     'enrolled_on', 'created_by'
#                     'total_payments',
#                     'balance',
#                     'lessons_taken',
#                     'lessons_remaining'
#                     'enrollment_status'
#                     ]
#         read_only_fields = ['created_by', 'enrolled_on']
#         optional_fileds=["status"]

#     def create(self, validated_data):
#         validated_data['created_by'] = self.context['request'].user
#         if 'discount' not in validated_data:
#             validated_data['discount'] = 0
#         return super().create(validated_data)
    
#     def get_total_payments(self, obj):
#         return Payments.objects.filter(enrollment=obj).aggregate(total=sum("amount"))
    
#     def get_balance(self, obj):
#         total_fee = obj.course.price
#         discount  = obj.discount or 0
#         total_payments = self.get_total_payments(obj)
#         return total_fee - discount - total_payments
    
#     def get_lessons_taken(self, obj):
#         return Lesson.objects.filter(enrollment=obj).count()
    
#     def get_lessons_remaining(self, obj):
#         return obj.lessons - self.get_lessons_taken(obj)




class EnrollmentOverviewSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source="course.name", read_only=True)
    enrollment_status = serializers.CharField(source="EnrollementStatus.status", read_only=True)

    total_payments = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    lessons_taken = serializers.IntegerField(read_only=True)
    lessons_remaining = serializers.IntegerField(read_only=True)

    class Meta:
        model = Enrollement
        fields = [
            "id", "course", "course_name", "learner",
            "discount", "lessons", "enrolled_on", "created_by",
            "enrollment_status", "total_payments", "balance",
            "lessons_taken", "lessons_remaining"
        ]
        read_only_fields = ["created_by", "enrolled_on"]




class EnrollmentDetailSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source="course.name", read_only=True)
    enrollment_status = serializers.CharField(source="EnrollementStatus.status", read_only=True)

    total_payments = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    lessons_taken = serializers.IntegerField(read_only=True)
    lessons_remaining = serializers.IntegerField(read_only=True)

    payments = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Enrollement
        fields = [
            "id", "course", "course_name", "learner",
            "discount", "lessons", "enrolled_on", "created_by",
            "enrollment_status", "total_payments", "balance",
            "lessons_taken", "lessons_remaining",
            "payments", "lessons"
        ]
        read_only_fields = ["created_by", "enrolled_on"]

    def get_payments(self, obj):
        return [{"id": p.id, "amount": p.amount, "paid_on": p.paid_on} for p in obj.payment_set.all()]

    def get_lessons(self, obj):
        return [{"id": l.id, "topic": l.topic, "date": l.date} for l in obj.lesson_set.all()]





class EnrollmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollement
        fields = [
            "course",
            "learner",
            "discount",
            "lessons",
        ]

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        if "discount" not in validated_data:
            validated_data["discount"] = 0
        return super().create(validated_data)

