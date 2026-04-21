from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import CreateAPIView
from accounts.models import Staff
from accounts.serializers import StaffSerializer
from accounts.customPermissions import IsSuperUserOrManager
from rest_framework.generics import ListAPIView


from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings





# Create your views here.

# Login Endpoint
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        

        user = authenticate(username=username, password=password)
       

        if user is not None:
            refresh = RefreshToken.for_user(user)

            return Response({
                "access":str(refresh.access_token),
                "refresh":str(refresh),
                "user":{
                    "username":user.username,
                    "is_Manager":user.is_Manager,
                    "user_id":user.id,
                }}, status=HTTP_200_OK
            )
        
                
        return Response({"error":"Invalid Credentials"}, status=HTTP_401_UNAUTHORIZED)
    


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
            token = default_token_generator.make_token(user)
            uid = user.pk

            reset_link = f"http://[f.endlink]/reset-password/{uid}/{token}/"

            send_mail(
                "password Reset",
                f"Click link: {reset_link}",
                settings.Email_Host_user,
                [email],
            )

        return Response({"message":"If email exists, reset Link sent"})
    
#confirm password reset
class ConfirmPasswordReset(APIView):
    def post(self, request, uid, token):
        from accounts.models import Staff

        password = request.data.get("password")

        try:
            user = Staff.objects.get(pk=uid)
        except Staff.DoesNotExist:
            return Response({"error":"Invalid User"}, status=400)
        

        if default_token_generator.check_token(user, token):
            user.set_password(password)
            user.save()
            return Response({"message":"Password reset successful"})
        
        return Response({"error":"Invalid or expired token"}, status=400)
    

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

        