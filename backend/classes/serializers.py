from rest_framework import serializers
from classes.models import Course, ClassStatus

class ClassStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassStatus
        fields = "__all__"


class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["name", "price"]


class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
