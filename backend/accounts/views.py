from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken
from rest_framework.generics import CreateAPIView, GenericAPIView, UpdateAPIView, RetrieveAPIView
from accounts.models import Staff
from accounts.serializers import PasswordChangeSerializer, PasswordResetConfirmSerializer, PasswordResetSerializer, StaffActivationSerializer, StaffSerializer
from accounts.customPermissions import IsSuperUserOrManager
from rest_framework.generics import ListAPIView
from rest_framework.authtoken.models import Token
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode 
from django.utils.encoding import force_bytes, force_str
# from rest_framework.authtoken.models import Token



from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

from accounts.utils import logout_user_sessions





# Create your views here.

# Login Endpoint
class LoginView(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:

            token = SlidingToken.for_user(user)

            return Response({
                "token": str(token),
                "user": {
                    "username": user.username,
                    "is_Manager": user.is_Manager,
                    "user_id": user.id,
                    "is_superuser": user.is_superuser,
                    "branch": user.branch.id if user.branch else None
                }
            }, status=HTTP_200_OK)

        return Response(
            {"error": "Invalid Credentials"},
            status=HTTP_401_UNAUTHORIZED
        )

#Logout Endpoint
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()


            return Response({"message": "Logged out succesfully"})
        except Exception:
            return Response({'error':"Invalid token"}, status=400)
        


#Reset Password via email

class RequestPasswordReset(APIView):
    def post(self, request):
        email = request.data.get('email')

        from accounts.models import Staff
        user = Staff.objects.filter(email=email).first()


        if user:
            # token = default_token_generator.make_token(user)
            # uid = user.pk

            # reset_link = f"http://{settings.FRONTEND_LINK}/reset-password/{uid}/{token}/"
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_link = f"http://{settings.FRONTEND_LINK}/reset-password/{uidb64}/{token}/"

            send_mail(
                "password Reset",
                f"Click link: {reset_link}",
                settings.EMAIL_HOST_USER,
                [email],
            )

        return Response({"message":"If email exists, reset Link sent"})
    
#confirm password reset
# class ConfirmPasswordReset(APIView):
#     def post(self, request, uid, token):
#         from accounts.models import Staff

#         password = request.data.get("password")

#         try:
#             user = Staff.objects.get(pk=uid)
#         except Staff.DoesNotExist:
#             return Response({"error":"Invalid User"}, status=400)
        

#         if default_token_generator.check_token(user, token):
#             user.set_password(password)
#             user.save()
#             return Response({"message":"Password reset successful"})
        
#         return Response({"error":"Invalid or expired token"}, status=400)


class ConfirmPasswordReset(APIView):
    def post(self, request, uidb64, token):
        password = request.data.get("new_password")

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Staff.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Staff.DoesNotExist):
            return Response({"error": "Invalid user"}, status=400)

        if default_token_generator.check_token(user, token):
            user.set_password(password)
            user.save()

            # ✅ For JWT: just let old tokens expire naturally.
            # Optionally, you can force logout by rotating signing key or using blacklist.

            return Response({"message": "Password reset successful"})
        
        return Response({"error": "Invalid or expired token"}, status=400)
    

class StaffCreateView(CreateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    def perform_update(self, serializer):
        serializer.save(last_edit_by=self.request.user)

class StaffListView(ListAPIView):
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated]


    

    def get_queryset(self):
        # Only return staff who are not deleted
        return Staff.objects.filter(is_deleted=False)
    

class StaffSoftDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            staff = Staff.objects.get(pk=pk, is_deleted=False)
        except Staff.DoesNotExist:
            return Response({"error": "Staff not found or already deleted"}, status=HTTP_404_NOT_FOUND)

        serializer = StaffSerializer(context={'request': request})
        serializer.soft_delete(staff)
        return Response({"message": "Staff soft-deleted successfully"}, status=HTTP_200_OK)
    

class StaffUpdateView(UpdateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated]


class StaffDetailView(RetrieveAPIView):
    queryset = Staff.objects.filter(is_deleted=False)
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated]



class StaffActivationView(UpdateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffActivationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only superadmins can activate staff
        if self.request.user.is_superuser:
            return Staff.objects.all()
        return Staff.objects.none()



class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect"}, status=HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Password changed successfully"})
    

class PasswordResetView(GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Reset link sent if email exists"})


class PasswordResetConfirmView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # ✅ For JWT: no Token.objects deletion
        # Clear Django sessions if you’re using session auth
        logout(request)

        # On the frontend, clear JWTs from localStorage/session
        return Response({"message": "Password reset successful. Please log in again."})


class PasswordChangeView(GenericAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        Token.objects.filter(user=user).delete()
        logout_user_sessions(user)  # force logout
        return Response({"message": "Password changed successfully. Please log in again."})