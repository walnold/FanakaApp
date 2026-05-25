from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainSlidingView, TokenRefreshSlidingView
from accounts.views import ChangePasswordView, LoginView, LogoutView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView, RequestPasswordReset, ConfirmPasswordReset, StaffActivationView, StaffCreateView, StaffListView,StaffUpdateView, StaffDetailView



urlpatterns = [
        path('token/',TokenObtainSlidingView.as_view()),
        path('token/refresh/', TokenRefreshSlidingView.as_view()),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('logout/', LogoutView.as_view(),),
        path('login/', LoginView.as_view(),),
        path('password-reset/', RequestPasswordReset.as_view(),),
        path(
        "password-reset-confirm/<uidb64>/<token>/",
        ConfirmPasswordReset.as_view(),
        name="password_reset_confirm",
    ),
        path('staffs/create/', StaffCreateView.as_view(), name='staff-create'),
        path('staffs/<int:pk>/', StaffUpdateView.as_view(), name='staff-update'),
        path('staffs/', StaffListView.as_view(), name='staff-list'),
        path('staffs/profile/<int:pk>/', StaffDetailView.as_view(), name='staff-detail'),
         path("staffs/<int:pk>/activate/", StaffActivationView.as_view(), name="staff-activate"),
         path("password-change/", ChangePasswordView.as_view(), name="password-change"),
         path("password-reset/", PasswordResetView.as_view(), name="password-reset"),
    path("password-reset-confirm/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    path("password-change/", PasswordChangeView.as_view(), name="password-change"),

    
]

