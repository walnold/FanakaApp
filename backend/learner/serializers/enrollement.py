from rest_framework import serializers
from learner.models.enrollement import Enrollement

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollement
        fields = ['id', 'course', 'learner', 'discount', 'lessons', 'enrolled_on', 'created_by']
        read_only_fields = ['created_by', 'enrolled_on']
        optional_fileds=["status"]

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        if 'discount' not in validated_data:
            validated_data['discount'] = 0
        return super().create(validated_data)
