from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError
from .models import User, Profile

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

        return user

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
