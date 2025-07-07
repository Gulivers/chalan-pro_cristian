from rest_framework import serializers
from .models import Identity

class IdentitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Identity
        fields = ['id', 'name', 'logo', 'last_update']
