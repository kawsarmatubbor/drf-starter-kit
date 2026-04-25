from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    SignupSerializer,
    SigninSerializer,
    SignoutSerializer,
    UserSerializer,
    ProfileSerializer,
    PasswordChangeSerializer,
    RefreshTokenSerializer,
    TokenVerifySerializer,
)
from utils.helpers import success, error

# Signup view
class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return success(
                status_code=201,
                message="Signup successful.",
                data=serializer.data,
            )
        return error(
            status_code=400,
            message="Signup failed.",
            errors=serializer.errors,
        )
    
# Signin view
class SigninView(APIView):
    def post(self, request):
        serializer = SigninSerializer(data=request.data)

        if serializer.is_valid():
            tokens = serializer.validated_data["tokens"]

            return success(
                status_code=200,
                message="Signin successful.",
                data=tokens,
            )
        return error(
            status_code=400,
            message="Signin failed.",
            errors=serializer.errors,
        )

# Signout view
class SignoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SignoutSerializer(data=request.data)

        if serializer.is_valid():
            return success(
                status_code=200,
                message="Signout successful.",
            )
        return error(
            status_code=400,
            message="Signout failed.",
            errors=serializer.errors,
        )

# Profile view
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return success(
            status_code=200,
            message="Profile retrieved successfully.",
            data=serializer.data,
        )

    def put(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return success(
                status_code=200,
                message="Profile updated successfully.",
                data=serializer.data,
            )
        return error(
            status_code=400,
            message="Profile update failed.",
            errors=serializer.errors,
        )
    
# Refresh token view
class RefreshTokenView(APIView):
    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)

        if serializer.is_valid():
            return success(
                status_code=200,
                message="Token refresh successful.",
                data={
                    "access": serializer.validated_data["access"],
                },
            )
        return error(
            status_code=400,
            message="Token refresh failed.",
            errors=serializer.errors,
        )

# Verify token view
class TokenVerifyView(APIView):
    def post(self, request):
        serializer = TokenVerifySerializer(data=request.data)

        if serializer.is_valid():
            return success(
                status_code=200,
                message="Token is valid.",
                data={
                    "valid": True,
                },
            )
        return error(
            status_code=400,
            message="Token verification failed.",
            errors=serializer.errors,
        )

# Password change view
class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return success(
                status_code=200,
                message="Password changed successfully.",
            )
        return error(
            status_code=400,
            message="Password change failed.",
            errors=serializer.errors,
        )
