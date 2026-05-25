from rest_framework import serializers
from .models import Identity, SocialMedia

# Identity serializer
class IdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Identity
        fields = ['id', 'title', 'description', 'phone', 'email', 'address', 'logo', 'fav_icon']

# Social media serializer
class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = ['id', 'name', 'url', 'icon']