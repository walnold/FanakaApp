from rest_framework import serializers
from instructors.models import Instructor, InstructorStatus

class InstructorStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorStatus
        fields = "__all__"


class InstructorListSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Instructor
        fields = ["first_name", "last_name", "phoneNumber"]

    def get_status(self, obj):
        # Example: if you later link Instructor to InstructorStatus
        return getattr(obj, "status", None)


class InstructorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = "__all__"
