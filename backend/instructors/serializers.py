from rest_framework import serializers
from instructors.models import Instructor, InstructorStatus

class InstructorStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorStatus
        fields = "__all__"


class InstructorListSerializer(serializers.ModelSerializer):
    # Nest the status serializer so you get full JSON object
    status = InstructorStatusSerializer(read_only=True)

    class Meta:
        model = Instructor
        fields = ["id", "first_name", "last_name", "phoneNumber", "status"]


class InstructorDetailSerializer(serializers.ModelSerializer):
    # Same adjustment here for consistency
    status = InstructorStatusSerializer(read_only=True)

    class Meta:
        model = Instructor
        fields = "__all__"
