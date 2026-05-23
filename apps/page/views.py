from rest_framework.views import APIView
from utils.helpers import success, error
from .models import HeroSection, ContactSection
from .serializers import HeroSectionSerializer, ContactSectionSerializer, ContactMessageSerializer

# Landing page views
class LandingPageView(APIView):
    def get(self, request):
        hero_section = HeroSection.objects.filter(is_active=True)
        hero_serializer = HeroSectionSerializer(hero_section, many=True)

        data = {
            'hero_section': hero_serializer.data
        }

        return success(
            status_code=200,
            message='Landing page retrieved successfully',
            data=data
        )

# Contact page view
class ContactPageView(APIView):
    def get(self, request):
        contact_section = ContactSection.objects.filter(is_active=True)
        contact_serializer = ContactSectionSerializer(contact_section, many=True)

        data = {
            'contact_section': contact_serializer.data
        }

        return success(
            status_code=200,
            message='Contact page retrieved successfully',
            data=data
        )
    
# Contact message create view
class ContactMessageCreateView(APIView):
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return success(
                status_code=201,
                message='Contact message created successfully',
                data=serializer.data
            )
        
        return error(
            status_code=400,
            message='Invalid data',
            errors=serializer.errors
        )