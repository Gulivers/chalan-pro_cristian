from rest_framework import serializers
from appinventory.models import (
    Warehouse, ProductCategory, ProductBrand, Product, UnitOfMeasure, 
    UnitCategory, PriceType, ProductPrice
)
from django.db import transaction

# Serializador para almacenes
class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'

# Serializador para categorías de productos
class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'

# Serializador para categorías de unidades
class UnitCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitCategory
        fields = '__all__'

# Serializador para marcas de productos
class ProductBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBrand
        fields = '__all__'

# Serializador para precios de productos
class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        exclude = ['product']

# Serializador principal para productos, incluye relación con precios y unidades
class ProductSerializer(serializers.ModelSerializer):
    prices = ProductPriceSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = '__all__'
        
    def validate_prices(self, value):
        seen = set()
        for item in value:
            key = (item.get('price_type'), item.get('unit'), item.get('valid_from'), item.get('valid_until'))
            if key in seen:
                raise serializers.ValidationError(f"Duplicate price for type/unit/period: {key}")
            seen.add(key)
        return value

    def create(self, validated_data):
        prices_data = validated_data.pop('prices', [])

        with transaction.atomic():
            product = super().create(validated_data)

            for price_data in prices_data:
                ProductPrice.objects.create(product=product, **price_data)

        return product

    def update(self, instance, validated_data):
        prices_data = validated_data.pop('prices', [])


        # Actualiza campos del producto
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Elimina precios anteriores y guarda nuevos
        instance.prices.all().delete()
        for price_data in prices_data:
            ProductPrice.objects.create(product=instance, **price_data)

        return instance

# Serializador para unidades de medida
class UnitOfMeasureSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = UnitOfMeasure
        fields = [
            'id', 'name', 'code', 'category', 'category_name',
            'reference_unit', 'conversion_sign', 'conversion_factor', 'is_active'
        ]

# Serializador para tipos de precio
class PriceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceType
        fields = ['id', 'name', 'description', 'is_active']

# Serializador compacto para listados
class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', default='', read_only=True)
    brand_name = serializers.CharField(source='brand.name', default='', read_only=True)
    unit_name = serializers.CharField(source='unit_default.name', default='', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'sku', 'category_name', 'brand_name',
            'reorder_level', 'unit_name', 'is_active'
        ]

# Serializador para detalle completo de producto (usado en modo edición o vista)
class ProductDetailSerializer(ProductSerializer):
    prices = ProductPriceSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        extra_fields = ['prices']
