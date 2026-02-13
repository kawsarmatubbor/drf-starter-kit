from django.urls import path
from .views import register_view, ProfileView, account_verification_view, forgot_password_view, otp_verification_view, set_new_password_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('account-verification/', account_verification_view, name='account-verification'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('forgot-password/', forgot_password_view, name='forgot-password'),
    path('otp-verification/', otp_verification_view, name='otp-verification'),
    path('set-new-password/', set_new_password_view, name='set-new-password'),
]