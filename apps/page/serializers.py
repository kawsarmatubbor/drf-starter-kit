from rest_framework import serializers
from .models import HeroSection, ContactSection, ContactMessage

# Hero section serializer
class HeroSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroSection
        fields = ['id', 'title', 'description', 'image']


# Contact section serializer
class ContactSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSection
        fields = ['id', 'title', 'description', 'email', 'phone_number', 'address']

# Contact message serializer
class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'subject', 'message']