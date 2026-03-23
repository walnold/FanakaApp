from rest_framework.serializers import ModelSerializer
from branches.models import Branch

class BranchSerializer(ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name', 'description', 'created_by', 'created_on', 'last_edit_on', 'last_edit_by', 'is_deleted']
        read_only_fields = ['created_by', 'created_on', 'last_edit_on', 'last_edit_by', 'is_deleted']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
            validated_data['last_edit_by'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['last_edit_by'] = request.user
        return super().update(instance, validated_data)

    def soft_delete(self, instance):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            instance.last_edit_by = request.user
        instance.is_deleted = True
        instance.save()
        return instance