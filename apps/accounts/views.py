from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RegisterSerializer

@api_view(["POST"])
def register_view(request):
    serializer = RegisterSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)