from rest_framework.views import APIView
from utils.helpers import success
from .models import Identity, SocialMedia
from .serializers import IdentitySerializer, SocialMediaSerializer

# system setting view
class SystemSettingView(APIView):
    def get(self, request):
        identity = Identity.objects.filter(is_active=True).last()
        identity_serializer = IdentitySerializer(identity)

        social_media = SocialMedia.objects.filter(is_active=True)
        social_media_serializer = SocialMediaSerializer(social_media, many=True)

        data = {
            'identity': identity_serializer.data,
            'social_media': social_media_serializer.data
        }
        return success(
            status_code=200,
            message='System setting retrieved successfully',
            data=data
        )