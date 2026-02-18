from django.urls import path
from .views import register_view, ProfileView, account_verification_view, resend_account_verification_otp, forgot_password_view, otp_verification_view, set_new_password_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('account/verify-otp/', account_verification_view, name='account-verification'),
    path('account/resend-otp/', resend_account_verification_otp, name='resend-account-verification-otp'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password/forgot/', forgot_password_view, name='forgot-password'),
    path('password/verify-otp/', otp_verification_view, name='forgot-password-verification'),
    path('password/resend-otp/', forgot_password_view, name='resend-forgot-password-verification-otp'),
    path('password/reset/', set_new_password_view, name='set-new-password'),
]