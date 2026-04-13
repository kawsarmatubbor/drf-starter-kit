from django.urls import path
from .views import (
    SignupView
)

urlpatterns = [
    # Authentication
    path('signup/', SignupView.as_view(), name='register'),

    # Profile
    # path('profile/', , name='profile'),

    # OTP
    # path('otp/verify/', , name='otp_verify'),

    # Password
    # path('password/change/', , name='password_change'),
    # path('password/forgot/', , name='password_forgot'),
    # path('password/reset/', , name='password_reset'),
]