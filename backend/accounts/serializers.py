from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from .models import Staff

class StaffSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source="branch.name", read_only=True)

    class Meta:
        model = Staff
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'is_Manager', 'phoneNumber', 'idNumber', 'password',
                  'created_on', 'last_edit_on', 'last_edit_by', 'branch',
                  'branch_name', 'is_deleted','is_active']
        read_only_fields = ['created_on', 'last_edit_on', 'last_edit_by', 'is_deleted', ]
        extra_kwargs = {
            'password': {'write_only': True,'required': False},

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
    


# # accounts/serializers.py
# from rest_framework import serializers
# from .models import Staff

class StaffActivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ["id", "is_active"]

    def update(self, instance, validated_data):
        # Only superadmins should be able to activate
        request = self.context.get("request")
        if not request.user.is_superuser:
            raise serializers.ValidationError("Only superadmins can activate staff.")
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.is_staff=validated_data.get("is_active", instance.is_staff)
        instance.save()
        return instance


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = Staff.objects.get(email=value)
        except Staff.DoesNotExist:
            raise serializers.ValidationError("No user with this email")
        self.context["user"] = user
        return value

    def save(self):
        user = self.context["user"]
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"http://frontend/reset-password/{uid}/{token}/"

        send_mail(
            "Password Reset",
            f"Click link: {reset_link}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )
        return reset_link


# class PasswordResetConfirmSerializer(serializers.Serializer):
#     uid = serializers.CharField()
#     token = serializers.CharField()
#     new_password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         try:
#             uid = force_str(urlsafe_base64_decode(data["uidb64"]))
#             user = Staff.objects.get(pk=uidb64)
#         except (Staff.DoesNotExist, ValueError):
#             raise serializers.ValidationError("Invalid user")

#         if not default_token_generator.check_token(user, data["token"]):
#             raise serializers.ValidationError("Invalid or expired token")

#         data["user"] = user
#         return data

#     def save(self):
#         user = self.validated_data["user"]
#         user.set_password(self.validated_data["new_password"])
#         user.save()
#         return user

class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()   # <-- match the URL param
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            # Decode the base64 UID
            uid = force_str(urlsafe_base64_decode(data["uidb64"]))
            user = Staff.objects.get(pk=uid)
        except (Staff.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError({"non_field_errors": ["Invalid user"]})

        # Validate the token
        if not default_token_generator.check_token(user, data["token"]):
            raise serializers.ValidationError({"non_field_errors": ["Invalid or expired token"]})

        data["user"] = user
        return data

    def save(self):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value

    def save(self):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user