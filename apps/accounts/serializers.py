from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User, Profile

# Profile serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio', 'gender', 'address', 'phone_number', 'avatar']

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