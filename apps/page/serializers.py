from rest_framework import serializers
from .models import HeroSection

# Hero section serializer
class HeroSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroSection
        fields = ['id', 'title', 'description', 'image']
