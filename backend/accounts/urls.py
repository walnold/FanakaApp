from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainSlidingView, TokenRefreshSlidingView
from accounts.views import LoginView, LogoutView, RequestPasswordReset, ConfirmPasswordReset, StaffActivationView, StaffCreateView, StaffListView,StaffUpdateView, StaffDetailView



urlpatterns = [
        path('token/',TokenObtainSlidingView.as_view()),
        path('token/refresh/', TokenRefreshSlidingView.as_view()),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('logout/', LogoutView.as_view(),),
        path('login/', LoginView.as_view(),),
        path('password-reset/', RequestPasswordReset.as_view(),),
        path('password-reset-confirm/<int:uid>/<str:token>/', ConfirmPasswordReset.as_view(),),
        path('staffs/create/', StaffCreateView.as_view(), name='staff-create'),
        path('staffs/<int:pk>/', StaffUpdateView.as_view(), name='staff-update'),
        path('staffs/', StaffListView.as_view(), name='staff-list'),
        path('staffs/profile/<int:pk>/', StaffDetailView.as_view(), name='staff-detail'),
         path("staff/<int:pk>/activate/", StaffActivationView.as_view(), name="staff-activate"),

    
]

