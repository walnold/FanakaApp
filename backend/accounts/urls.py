from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import LoginView, LogoutView, RequestPasswordReset, ConfirmPasswordReset, StaffCreateView, StaffListView



urlpatterns = [
        path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('api/logout/', LogoutView.as_view(),),
        path('api/login/', LoginView.as_view(),),
        path('api/password-reset/', RequestPasswordReset.as_view(),),
        path('api/password-reset-confirm/<int:uid>/<str:token>/', ConfirmPasswordReset.as_view(),),
        path('api/staffs/create', StaffCreateView.as_view(), name='staff-create'),
        path('api/staffs/', StaffListView.as_view(), name='staff-list'),

    
]

