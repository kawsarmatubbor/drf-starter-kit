from django.urls import path
from .views import (
    SignupView,
    OtpVerifyView,
    SigninView,
    SignoutView,
    ProfileView,
    PasswordChangeView,
    ForgotPasswordView,
    RefreshTokenView,
    TokenVerifyView,
)

urlpatterns = [
    # Authentication
    path('signup/', SignupView.as_view(), name='signup'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('signout/', SignoutView.as_view(), name='signout'),

    # Profile
    path('profile/', ProfileView.as_view(), name='profile'),

    # OTP
    path('otp/verify/', OtpVerifyView.as_view(), name='otp_verify'),
    # path('otp/resend/', , name='otp_resend'),

    # Password
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('password/forgot/', ForgotPasswordView.as_view(), name='password_forgot'),
    # path('password/reset/', , name='password_reset'),

    # Token
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
