
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.db import transaction
from .models import DocumentType, PartyType, PartyCategory, Party

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = '__all__'
        
class PartyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartyType
        fields = '__all__'
        
class PartyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PartyCategory
        fields = '__all__'
        

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.db import transaction
from .models import Party, PartyType, PartyCategory, PriceType

class PartySerializer(serializers.ModelSerializer):
    # IDs de relaciones (simple y performante para list/create/update)
    types = serializers.PrimaryKeyRelatedField(
        queryset=PartyType.objects.all(), many=True
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=PartyCategory.objects.all(), allow_null=True, required=False
    )
    default_price_type = serializers.PrimaryKeyRelatedField(
        queryset=PriceType.objects.all(), allow_null=True, required=False
    )

    # Unicidad por nombre (case-insensitive)
    name = serializers.CharField(
        max_length=255,
        validators=[
            UniqueValidator(
                queryset=Party.objects.all(),
                lookup='iexact',
                message='A party with this name already exists.'
            )
        ]
    )

    class Meta:
        model = Party
        fields = [
            'id', 'name', 'rfc', 'street', 'floor_office', 'city', 'state',
            'zipcode', 'country', 'phone', 'email',
            'types', 'category', 'default_price_type',
            'customer_rank', 'supplier_rank', 'is_active'
        ]

    # Validaciones y normalización
    def validate(self, attrs):
        # trim strings
        for k in ['name','rfc','street','floor_office','city','state','zipcode','country','phone','email']:
            if k in attrs and isinstance(attrs[k], str):
                attrs[k] = attrs[k].strip()

        # email en minúsculas
        if attrs.get('email'):
            attrs['email'] = attrs['email'].lower()

        # (Opcional) política: al menos un rol cliente/proveedor
        # if attrs.get('customer_rank', 0) == 0 and attrs.get('supplier_rank', 0) == 0:
        #     raise serializers.ValidationError({'customer_rank': 'Must be > 0 if not supplier.', 'supplier_rank': 'Must be > 0 if not customer.'})

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        types = validated_data.pop('types', [])
        instance = Party.objects.create(**validated_data)
        if types:
            instance.types.set(types)
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        types = validated_data.pop('types', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if types is not None:
            instance.types.set(types)
        return instance
