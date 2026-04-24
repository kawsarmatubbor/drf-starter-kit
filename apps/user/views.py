from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import SignupSerializer, SigninSerializer, SignoutSerializer
from utils.helpers import success, error

# Signup view
class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data = request.data)

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
        serializer = SigninSerializer(data=request.data, context={"request": request})

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
