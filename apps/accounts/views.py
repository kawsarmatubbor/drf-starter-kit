import random
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import NotificationSerializer, RegisterSerializer, ProfileSerializer
from .models import Notification, User, Profile, Verification
from .send_mail import send_verification_otp, send_forgot_password_otp


OTP_EXPIRY_MINUTES = 3
OTP_COOLDOWN_SECONDS = 30


def generate_otp():
    return random.randint(100000, 999999)


def send_otp(email, purpose):
    if not email:
        return Response({"error": "Email is required."}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=404)

    if purpose == "account_verification" and user.is_active:
        return Response({"error": "User already verified."}, status=400)

    existing = Verification.objects.filter(
        user=user,
        purpose=purpose
    ).first()

    if existing and timezone.now() < existing.created_at + timedelta(seconds=OTP_COOLDOWN_SECONDS):
        return Response(
            {"error": "Please wait before requesting another OTP."},
            status=429
        )

    Verification.objects.filter(user=user, purpose=purpose).delete()

    otp = generate_otp()

    Verification.objects.create(
        user=user,
        otp=otp,
        purpose=purpose
    )

    if purpose == "account_verification":
        send_verification_otp(otp, user.email)
    elif purpose == "password_reset":
        send_forgot_password_otp(otp, user.email)

    return Response({"success": "OTP sent successfully."}, status=200)


@api_view(["POST"])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        otp = generate_otp()

        Verification.objects.create(
            user=user,
            otp=otp,
            purpose="account_verification"
        )

        send_verification_otp(otp, user.email)

        return Response(
            {
                "user": serializer.data,
                "success": "Registration successful. OTP sent."
            },
            status=201
        )

    return Response(serializer.errors, status=400)


@api_view(["POST"])
def otp_verification_view(request):
    email = request.data.get("email")
    provided_otp = request.data.get("otp")
    purpose = request.data.get("purpose")

    if not email or not provided_otp or not purpose:
        return Response(
            {"error": "Email, OTP and purpose are required."},
            status=400
        )

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=404)

    if purpose == "account_verification" and user.is_active:
        return Response({"error": "User already verified."}, status=400)

    try:
        verification = Verification.objects.get(user=user, purpose=purpose)
    except Verification.DoesNotExist:
        return Response({"error": "OTP not found."}, status=404)

    if timezone.now() > verification.created_at + timedelta(minutes=OTP_EXPIRY_MINUTES):
        verification.delete()
        return Response({"error": "OTP expired."}, status=400)

    if str(verification.otp) != str(provided_otp):
        return Response({"error": "Invalid OTP."}, status=400)

    if purpose == "account_verification":
        user.is_active = True
        user.save()
        verification.delete()

    elif purpose == "password_reset":
        verification.is_verified = True
        verification.save()

    return Response({"success": "OTP verified successfully."}, status=200)


@api_view(["POST"])
def resend_account_verification_otp(request):
    email = request.data.get("email")
    return send_otp(email=email, purpose="account_verification")


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)

        serializer = ProfileSerializer(
            profile,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


@api_view(["POST"])
def forgot_password_view(request):
    email = request.data.get("email")
    return send_otp(email=email, purpose="password_reset")


@api_view(["POST"])
def set_new_password_view(request):
    email = request.data.get("email")
    new_password = request.data.get("new_password")
    confirm_new_password = request.data.get("confirm_new_password")

    if not email or not new_password or not confirm_new_password:
        return Response(
            {"error": "Email and passwords are required."},
            status=400
        )

    if new_password != confirm_new_password:
        return Response({"error": "Passwords do not match."}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=404)

    try:
        verification = Verification.objects.get(
            user=user,
            purpose="password_reset"
        )
    except Verification.DoesNotExist:
        return Response({"error": "OTP record not found."}, status=404)

    if timezone.now() > verification.created_at + timedelta(minutes=OTP_EXPIRY_MINUTES):
        verification.delete()
        return Response({"error": "OTP expired."}, status=400)

    if not verification.is_verified:
        return Response({"error": "OTP is not verified yet."}, status=400)

    verification.delete()
    user.set_password(new_password)
    user.save()

    return Response(
        {"success": "Password updated successfully."},
        status=200
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    user = request.user

    old_password = request.data.get("old_password")
    new_password = request.data.get("new_password")
    confirm_new_password = request.data.get("confirm_new_password")

    if not old_password or not new_password or not confirm_new_password:
        return Response(
            {"error": "All password fields are required."},
            status=400
        )

    if not user.check_password(old_password):
        return Response(
            {"error": "Old password is incorrect."},
            status=400
        )

    if new_password != confirm_new_password:
        return Response(
            {"error": "Passwords do not match."},
            status=400
        )

    if user.check_password(new_password):
        return Response(
            {"error": "New password must be different from old password."},
            status=400
        )

    user.set_password(new_password)
    user.save()

    return Response(
        {"success": "Password updated successfully."},
        status=200
    )

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def notification_view(request):
    user = request.user

    notifications = Notification.objects.filter(user = user, is_read = False)
    serializer = NotificationSerializer(notifications, many = True)

    return Response(serializer.data)