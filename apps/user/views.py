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
                status_code=201,
                message="Signup successful.",
                data=serializer.data,
            )
        return error(
            status_code=400,
            message="Signup failed.",
            errors=serializer.errors,
        )