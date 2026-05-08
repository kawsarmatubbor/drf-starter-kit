from rest_framework import serializers
from .models import Contact

# Contact serializer
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["id", "email", "phone", "message", "is_replied"]
        read_only_fields = ["id", "is_replied"]