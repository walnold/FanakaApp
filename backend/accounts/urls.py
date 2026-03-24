from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import LoginView, LogoutView, RequestPasswordReset, ConfirmPasswordReset, StaffCreateView, StaffListView



urlpatterns = [
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('logout/', LogoutView.as_view(),),
        path('login/', LoginView.as_view(),),
        path('password-reset/', RequestPasswordReset.as_view(),),
        path('password-reset-confirm/<int:uid>/<str:token>/', ConfirmPasswordReset.as_view(),),
        path('staffs/create', StaffCreateView.as_view(), name='staff-create'),
        path('staffs/', StaffListView.as_view(), name='staff-list'),

    
]

