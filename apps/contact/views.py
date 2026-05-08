from rest_framework.views import APIView
from utils.helpers import success, error
from .models import Contact
from .serializers import ContactSerializer

# Contact create view
class ContactCreateView(APIView):
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success(
                status_code=201,
                message="Contact created successfully",
                data=serializer.data
            )
        return error(
            status_code=400,
            message="Invalid data",
            errors=serializer.errors
        )