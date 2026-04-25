from datetime import timedelta
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError
from utils.helpers import generate_otp
from utils.email_sender import send_password_reset_otp_email, send_signup_otp_email
from .models import User, Profile, Verification

# Profile serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio', 'gender', 'address', 'phone_number', 'avatar']

# User serializer
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'email', 'profile']

# Signup serializer
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_2 = serializers.CharField(write_only=True, required=True)
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'password_2', 'profile']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_2']:
            raise serializers.ValidationError("Passwords don't match.")
        

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_2')
        profile_data = validated_data.pop('profile', None)

        user = User.objects.create_user(**validated_data)

        if profile_data:
            Profile.objects.create(user=user, **profile_data)
        else:
            Profile.objects.create(user=user)

        verification = Verification.objects.create(
            user=user,
            otp=generate_otp(),
            purpose="account_activation",
        )

        send_signup_otp_email(email=user.email, otp=verification.otp)

        return user

# OTP verify serializer
class OtpVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True, max_length=6)
    purpose = serializers.ChoiceField(
        required=True,
        choices=Verification.PURPOSE_CHOICES,
    )

    def validate(self, attrs):
        email = attrs.get("email")
        otp = attrs.get("otp")
        purpose = attrs.get("purpose")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": ["User with this email does not exist."]})

        verification = Verification.objects.filter(
            user=user,
            purpose=purpose,
            is_verified=False,
        ).last()

        if not verification:
            raise serializers.ValidationError(f"No pending OTP found.")

        if verification.created_at + timedelta(minutes=5) <= timezone.now():
            raise serializers.ValidationError("OTP has expired. Please request a new one.")

        if verification.otp != otp:
            raise serializers.ValidationError({"otp": ["Invalid OTP."]})

        attrs["user"] = user
        attrs["verification"] = verification
        return attrs

    @transaction.atomic
    def save(self, **kwargs):
        user = self.validated_data["user"]
        verification = self.validated_data["verification"]
        purpose = self.validated_data["purpose"]

        verification.is_verified = True
        verification.save(update_fields=["is_verified"])

        if purpose == "account_activation":
            user.is_active = True
            user.save(update_fields=["is_active"])
            verification.delete()

        return user

# OTP resend serializer
class OtpResendSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    purpose = serializers.ChoiceField(
        required=True,
        choices=Verification.PURPOSE_CHOICES,
    )

    def validate(self, attrs):
        email = attrs.get("email")
        purpose = attrs.get("purpose")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": ["User with this email does not exist."]})

        if purpose == "account_activation" and user.is_active:
            raise serializers.ValidationError("This account is already active.")

        existing_otp = Verification.objects.filter(
            user=user,
            purpose=purpose,
            is_verified=False,
        ).last()

        if existing_otp and existing_otp.created_at + timedelta(minutes=5) > timezone.now():
            raise serializers.ValidationError("OTP already sent. Please wait 5 minutes.")

        Verification.objects.filter(
            user=user,
            purpose=purpose,
            is_verified=False,
        ).delete()

        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        user = validated_data["user"]
        purpose = validated_data["purpose"]

        verification = Verification.objects.create(
            user=user,
            otp=generate_otp(),
            purpose=purpose,
        )

        if purpose == "account_activation":
            send_signup_otp_email(email=user.email, otp=verification.otp)
        else:
            send_password_reset_otp_email(email=user.email, otp=verification.otp)

        return verification

# Signin serializer
class SigninSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            email=email,
            password=password,
        )

        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        if not user.is_active:
            raise serializers.ValidationError("Your account is inactive.")

        refresh = RefreshToken.for_user(user)

        attrs["user"] = user
        attrs["tokens"] = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return attrs

# Signout serializer
class SignoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        refresh_token = attrs.get("refresh")

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            raise serializers.ValidationError("Invalid or expired token.")

        return attrs

# Password change serializer
class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    new_password_2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        user = self.context["request"].user
        current_password = attrs.get("current_password")
        new_password = attrs.get("new_password")
        new_password_2 = attrs.get("new_password_2")

        if not user.check_password(current_password):
            raise serializers.ValidationError(
                {"current_password": ["Current password is incorrect."]}
            )

        if new_password != new_password_2:
            raise serializers.ValidationError(
                {"new_password_2": ["New passwords do not match."]}
            )

        validate_password(new_password, user=user)
        return attrs

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save(update_fields=["password"])
        return user

# Forgot password serializer
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        
        ex_otp = Verification.objects.filter(user=user, purpose="password_reset").last()
        
        if ex_otp:
            if ex_otp.created_at + timedelta(minutes=5) > timezone.now():
                raise serializers.ValidationError("Password reset OTP already sent. Please wait 5 minutes.")

        Verification.objects.filter(user=user, purpose="password_reset").delete()
                
        attrs["user"] = user
        return attrs
    
    def create(self, validated_data):
        user = validated_data.get("user")

        verification = Verification.objects.create(user=user, otp=generate_otp(), purpose="password_reset")

        send_password_reset_otp_email(email=user.email, otp=verification.otp)

        return verification

# Password reset serializer
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    new_password_2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        new_password = attrs.get("new_password")
        new_password_2 = attrs.get("new_password_2")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": ["User with this email does not exist."]})

        if new_password != new_password_2:
            raise serializers.ValidationError(
                {"new_password_2": ["New passwords do not match."]}
            )

        verification = Verification.objects.filter(
            user=user,
            purpose="password_reset",
            is_verified=True,
        ).last()

        if not verification:
            raise serializers.ValidationError(
                "Password reset OTP verification is required before resetting the password."
            )

        if verification.created_at + timedelta(minutes=5) <= timezone.now():
            verification.delete()
            raise serializers.ValidationError("Verified password reset OTP has expired. Please request a new one.")

        validate_password(new_password, user=user)

        attrs["user"] = user
        attrs["verification"] = verification
        return attrs

    @transaction.atomic
    def save(self, **kwargs):
        user = self.validated_data["user"]
        verification = self.validated_data["verification"]

        user.set_password(self.validated_data["new_password"])
        user.save(update_fields=["password"])
        verification.delete()

        return user


# Refresh token serializer
class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        refresh_token = attrs.get("refresh")

        try:
            token = RefreshToken(refresh_token)
            new_access = str(token.access_token)

            attrs["access"] = new_access
        except TokenError:
            raise serializers.ValidationError("Invalid or expired refresh token.")

        return attrs

# Access token verify serializer
class TokenVerifySerializer(serializers.Serializer):
    access = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        access_token = attrs.get("access")

        try:
            AccessToken(access_token)
        except TokenError:
            raise serializers.ValidationError("Invalid or expired access token.")

        return attrs