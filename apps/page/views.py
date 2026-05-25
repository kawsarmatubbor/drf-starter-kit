from rest_framework.views import APIView
from utils.helpers import success, error
from .models import HeroSection, ContactSection, FAQSection, OtherPage 
from .serializers import HeroSectionSerializer, ContactSectionSerializer, ContactMessageSerializer, FAQSectionSerializer, OtherPageSerializer

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
        serializer = ContactSectionSerializer(contact_section, many=True)

        return success(
            status_code=200,
            message='Contact page retrieved successfully',
            data=serializer.data
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
    
# Faq page view
class FAQPageView(APIView):
    def get(self, request):
        faq_section = FAQSection.objects.filter(is_active=True).last()
        serializer = FAQSectionSerializer(faq_section)

        return success(
            status_code=200,
            message='FAQ page retrieved successfully',
            data=serializer.data
        )
    
# Other page list view
class OtherPageListView(APIView):
    def get(self, request):
        other_pages = OtherPage.objects.filter(is_active=True)
        serializer = OtherPageSerializer(other_pages, many=True)

        return success(
            status_code=200,
            message='Other pages retrieved successfully',
            data=serializer.data
        )
    
# Other page detail view
class OtherPageDetailView(APIView):
    def get(self, request, slug):
        try:
            other_page = OtherPage.objects.get(slug = slug, is_active=True)
        except OtherPage.DoesNotExist:
            return error(
                status_code=404,
                message='Other page not found'
            )

        serializer = OtherPageSerializer(other_page)

        return success(
            status_code=200,
            message='Other page retrieved successfully',
            data=serializer.data
        )