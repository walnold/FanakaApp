from rest_framework import serializers
from learner.models.learner import Learner, LearnerStatus

class LearnerSerializer(serializers.ModelSerializer):

    status_name = serializers.CharField(
        source="status.status",
        read_only=True
    )

    branch_name = serializers.CharField(
        source="branch.name",
        read_only=True
    )

    created_by_name = serializers.StringRelatedField(
        source="created_by",
        read_only=True
    )


    class Meta:
        model = Learner
        fields = ['id', 'first_name', 'last_name', 'idNumber', 'status','phoneNumber', 'branch', 'created_by', 'status_name' ,'branch_name', 'created_by_name']
        read_only_fields = ['created_by']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class LearnerStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearnerStatus
        fields = '__all__'