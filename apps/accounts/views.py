import random
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, ProfileSerializer, VerificationSerializer
from .models import User, Profile, Verification
from .send_mail import send_verification_otp

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