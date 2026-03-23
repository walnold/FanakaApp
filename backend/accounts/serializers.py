from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Staff

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'isManager', 'phoneNumber', 'idNumber', 'password',
                  'created_on', 'last_edit_on', 'last_edit_by', 'is_deleted']
        read_only_fields = ['created_on', 'last_edit_on', 'last_edit_by', 'is_deleted']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['last_edit_by'] = request.user
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['last_edit_by'] = request.user
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)

    def soft_delete(self, instance):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            instance.last_edit_by = request.user
        instance.is_deleted = True
        instance.save()
        return instance
