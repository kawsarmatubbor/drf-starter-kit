import random
from django.forms import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, ProfileSerializer
from .models import User, Profile, Verification
from .send_mail import send_verification_otp, send_forgot_password_otp

def generate_otp():
        return random.randint(100000, 999999)


@api_view(["POST"])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        otp = generate_otp()

        Verification.objects.create(
            user = user,
            otp = otp
        )

        send_verification_otp(otp, user.email)

        return Response(
            {
                "user": serializer.data,
                "success": "Registration successful. OTP sent."
            }
        )
    return Response(serializer.errors)

@api_view(["POST"])
def account_verification_view(request):
    email = request.data.get('email')
    provided_otp = request.data.get('otp')

    if not email or not provided_otp:
        return Response(
            {
                "error": "Email and OTP are required."
            }
        )
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {
                "error": "User not found."
            }
        )
    
    if user.is_active:
        return Response(
            {
                "detail": "User already verified."
            }
        )
    
    try:
        verification = Verification.objects.get(user=user)
    except Verification.DoesNotExist:
        return Response(
            {
                "detail": "OTP not found."
            }
        )
    
    if str(verification.otp) != str(provided_otp):
        return Response(
            {
                "detail": "Invalid OTP."
            }
        )
    
    user.is_active = True
    user.save()

    verification.delete()

    return Response(
        {
            "message": "Account verified successfully."
        }
    )

@api_view(["POST"])
def resend_account_verification_otp(request):
    email = request.data.get("email")

    if not email:
        return Response(
            {
                "detail": "Email is required."
            }
        )

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {
                "detail": "User does not exist."
            }
        )
    
    if user.is_active:
        return Response(
            {
                "detail" : "Your are already verified"
            }
        )
        
    Verification.objects.filter(user = user).delete()
    
    otp = generate_otp()

    Verification.objects.create(
        user = user,
        otp = otp
    )

    send_verification_otp(otp, user.email)

    return Response(
        {"message": "OTP resent successfully."},
    )

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, created = Profile.objects.get_or_create(
            user=request.user,
        )
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    
    def put(self, request):
        profile, created = Profile.objects.get_or_create(
            user=request.user,
        )

        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

@api_view(["POST"])
def forgot_password_view(request):
    email = request.data.get('email')

    if not email:
        return Response(
            {
                "detail": "Email is required."
            }
        )
    
    try:
        user = User.objects.get(email=email, is_active = True)
    except User.DoesNotExist:
        return Response(
            {
                "detail": "User not found."
            }
        )
    
    Verification.objects.filter(user = user).delete()
    
    otp = generate_otp()

    Verification.objects.create(
        user = user,
        otp = otp
    )

    send_forgot_password_otp(otp, email)

    return Response(
        {
            "detail": "OTP sent successful."
        }
    )

@api_view(["POST"])
def otp_verification_view(request):
    email = request.data.get('email')
    provided_otp = request.data.get('otp')

    if not email or not provided_otp:
        return Response(
            {
                "detail": "Email and OTP are required."
            }
        )
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {
                "detail": "User not found."
            }
        )
    
    try:
        verification = Verification.objects.get(user=user)
    except Verification.DoesNotExist:
        return Response(
            {
                "detail": "OTP not found."
            }
        )
    
    if str(verification.otp) != str(provided_otp):
        return Response(
            {
                "detail": "Invalid OTP."
            }
        )
    
    if verification.is_verified:
        return Response(
            {
                "detail": "OTP already verified."
            }
        )
    
    verification.is_verified = True
    verification.save()

    return Response(
        {
            "message": "OTP verified successfully."
        }
    )

@api_view(["POST"])
def set_new_password_view(request):
    email = request.data.get("email")
    new_password = request.data.get("new_password")
    confirm_new_password = request.data.get("confirm_new_password")

    if not email or not new_password or not confirm_new_password:
        return Response(
            {
                "detail": "Email and passwords are required."
            }
        )

    if new_password != confirm_new_password:
        return Response(
            {
                "detail": "Passwords do not match."
            }
        )
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {
                "detail": "User not found."
            }
        )

    try:
        verification = Verification.objects.get(user=user)
    except Verification.DoesNotExist:
        return Response(
            {
                "detail": "OTP record not found."
            }
        )

    if not verification.is_verified:
        return Response(
            {
                "detail": "OTP is not verified yet."
            }
        )

    verification.delete()
    user.set_password(new_password)
    user.save()

    return Response(
        {
            "success": "Password updated successfully."
        }
    )