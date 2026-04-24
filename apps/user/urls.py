from django.urls import path
from .views import (
    SignupView,
    SigninView,
    SignoutView,
    RefreshTokenView,
    TokenVerifyView,
)

urlpatterns = [
    # Authentication
    path('signup/', SignupView.as_view(), name='signup'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('signout/', SignoutView.as_view(), name='signout'),

    # Profile
    # path('profile/', , name='profile'),

    # OTP
    # path('otp/verify/', , name='otp_verify'),
    # path('otp/resend/', , name='otp_resend'),

    # Password
    # path('password/change/', , name='password_change'),
    # path('password/forgot/', , name='password_forgot'),
    # path('password/reset/', , name='password_reset'),

    # Token
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]