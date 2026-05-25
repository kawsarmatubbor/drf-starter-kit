from rest_framework import serializers
from .models import HeroSection, ContactSection, ContactMessage, FAQSection, FAQQuestion, OtherPage
from django.utils import timezone

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


# Faq question serializer
class FAQQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQQuestion
        fields = ['id', 'question', 'answer']

# Faq section serializer
class FAQSectionSerializer(serializers.ModelSerializer):
    questions = FAQQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = FAQSection
        fields = ['id', 'title', 'description', 'image', 'questions']

# Other page serializer
class OtherPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherPage
        fields = ['id', 'title', 'slug', 'content']