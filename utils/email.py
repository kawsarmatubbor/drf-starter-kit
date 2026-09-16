from smtplib import SMTPException
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime


class EmailDeliveryError(Exception):
    """Raised when an OTP email cannot reach the configured mail server."""


def _send_otp_email(*, subject, message, email, html_message):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )
    except (OSError, SMTPException) as exc:
        raise EmailDeliveryError from exc


def send_signup_otp_email(email, otp):
    subject = "Account Activation OTP"
    message = f"Your OTP for account activation is: {otp}. It is valid for 5 minutes."
    context = {
        "otp": otp,
        "year": datetime.now().year,
    }
    html_message = render_to_string("emails/signup_otp.html", context)

    _send_otp_email(
        subject=subject,
        message=message,
        email=email,
        html_message=html_message,
    )


def send_password_reset_otp_email(email, otp):
    subject = "Password Reset OTP"
    message = f"Your OTP for password reset is: {otp}. It is valid for 5 minutes."
    context = {
        "otp": otp,
        "year": datetime.now().year,
    }
    html_message = render_to_string("emails/forgot_password_otp.html", context)

    _send_otp_email(
        subject=subject,
        message=message,
        email=email,
        html_message=html_message,
    )
