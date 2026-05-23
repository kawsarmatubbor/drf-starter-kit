from rest_framework.views import APIView
from utils.helpers import success, error
from .models import HeroSection
from .serializers import HeroSectionSerializer

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
