from django.core.mail import send_mail
from django.conf import settings

def send_verification_otp(otp, email):
    sub = 'Verification OTP'
    message = f'Your verification code is: {otp}. Please do not share this with anyone.'
    
    send_mail(
        subject=sub,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL, 
        recipient_list=[email],
        fail_silently=False,
    )

def send_forgot_password_otp(otp, email):
    sub = 'Forgot password OTP'
    message = f'Your verification code is: {otp}. Please do not share this with anyone.'
    
    send_mail(
        subject=sub,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL, 
        recipient_list=[email],
        fail_silently=False,
    )