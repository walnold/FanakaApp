from rest_framework import serializers
from learner.models.learner import Learner, LearnerStatus

class LearnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Learner
        fields = ['id', 'first_name', 'last_name', 'idNumber', 'status', 'branch', 'created_by']
        read_only_fields = ['created_by']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class LearnerStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearnerStatus
        fields = '__all__'