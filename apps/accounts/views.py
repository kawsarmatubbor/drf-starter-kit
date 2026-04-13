from rest_framework.views import APIView
from .serializers import SignupSerializer
from utils.helpers import success, error

# Signup view
class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return success(
                message="Signup successful.",
                data=serializer.data,
                status_code=201
            )
        return error(
            message="Signup failed.",
            status_code=400,
            errors=serializer.errors
        )