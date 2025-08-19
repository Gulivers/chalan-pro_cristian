from rest_framework import serializers
from .models import DocumentType, PartyType

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = '__all__'
        
class PartyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartyType
        fields = '__all__'