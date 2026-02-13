import random
from django.forms import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, ProfileSerializer, VerificationSerializer
from .models import User, Profile, Verification
from .send_mail import send_verification_otp, send_forgot_password_otp

@api_view(["POST"])
def register_view(request):
    register_serializer = RegisterSerializer(data=request.data)

    if register_serializer.is_valid():
        user = register_serializer.save()

        otp = random.randint(100000, 999999)

        verification_serializer = VerificationSerializer(
            data={
                "user": user.id,
                "otp": otp
            }
        )

        if not verification_serializer.is_valid():
            return Response(verification_serializer.errors)

        verification_serializer.save()

        send_verification_otp(otp, user.email)

        return Response(
            {
                "user": register_serializer.data,
                "message": "Registration successful. OTP sent."
            },
        )

    return Response(register_serializer.errors)


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
def account_verification_view(request):
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
    
    user.is_active = True
    user.save()

    verification.delete()

    return Response(
        {
            "message": "Account verified successfully."
        }
    )

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
    
    otp = random.randint(100000, 999999)

    verification_serializer = VerificationSerializer(
        data={
            "user": user.id,
            "otp": otp
        }
    )

    if verification_serializer.is_valid():
        verification_serializer.save()

        send_forgot_password_otp(otp, email)

        return Response(
            {
                "detail": "OTP sent successful."
            }
        )
    return Response(verification_serializer.errors)

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
            },
        )

    if new_password != confirm_new_password:
        return Response(
            {
                "detail": "Passwords do not match."
            },
        )
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {
                "detail": "User not found."
            },
        )

    try:
        verification = Verification.objects.get(user=user)
    except Verification.DoesNotExist:
        return Response(
            {
                "detail": "OTP record not found."
            },
        )

    if not verification.is_verified:
        return Response(
            {
                "detail": "OTP is not verified yet."
            },
        )

    verification.delete()
    user.set_password(new_password)
    user.save()

    return Response(
        {
            "success": "Password updated successfully."
        },
    )