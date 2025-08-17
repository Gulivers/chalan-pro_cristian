from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from appinventory.helpers import convert_to_reference_unit

# Categorías de Unidades de Medida (Longitud, Peso, Volumen...)
class UnitCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class UnitOfMeasure(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, unique=True)
    category = models.ForeignKey(UnitCategory, on_delete=models.CASCADE)
    reference_unit = models.BooleanField(default=False, help_text="Unidad base para conversiones")

    SIGN_CHOICES = [
        ('ref', 'Reference Unit'),
        ('*', 'Smaller than reference (*)'),
        ('/', 'Greater than reference (/)'),
    ]
    conversion_sign = models.CharField(max_length=4, choices=SIGN_CHOICES, default='ref')
    conversion_factor = models.DecimalField(max_digits=10, decimal_places=4, default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    def clean(self):
        if self.conversion_sign == 'ref':
            existing_ref = UnitOfMeasure.objects.filter(
                category=self.category,
                conversion_sign='ref'
            )
            if self.pk:
                existing_ref = existing_ref.exclude(pk=self.pk)
            if existing_ref.exists():
                raise ValidationError(
                    "There is already a reference unit for this category.")


class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    location = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ProductBrand(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(ProductBrand, on_delete=models.SET_NULL, null=True, blank=True)
    reorder_level = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit_default = models.ForeignKey(UnitOfMeasure, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class PriceType(models.Model):
    name = models.CharField(max_length=15, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, related_name="prices", on_delete=models.CASCADE)
    price_type = models.ForeignKey(PriceType, on_delete=models.CASCADE)
    unit = models.ForeignKey(UnitOfMeasure, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_default = models.BooleanField(default=False)
    is_sale = models.BooleanField(default=False)
    is_purchase = models.BooleanField(default=False)
    valid_from = models.DateField(null=True, blank=True)
    valid_until = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("product", "price_type", "unit", "valid_from", "valid_until")
        
    def clean(self):
        if not self.is_purchase and not self.is_sale:
            raise ValidationError(
                "You must indicate whether this unit is for purchasing, selling, or both.")


    def __str__(self):
        return f"{self.product} | {self.price_type} | {self.unit} → ${self.price}"
    

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("product", "warehouse")


class InventoryMovement(models.Model):
    MOVEMENT_TYPE_CHOICES = [
        (1, 'Entrada'),
        (-1, 'Salida'),
        (0, 'Ajuste')
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    movement_type = models.SmallIntegerField(choices=MOVEMENT_TYPE_CHOICES)
    reason = models.CharField(max_length=255, blank=True, null=True)
    unit = models.ForeignKey(UnitOfMeasure, on_delete=models.SET_NULL, null=True, blank=True)
    document = models.CharField(max_length=100, blank=True, null=True)
    line_id = models.PositiveIntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.product} ({self.quantity}) en {self.warehouse}"

    def get_converted_quantity(self):
        print("self.quantity: ",self.quantity)
        return convert_to_reference_unit(self.product, self.unit, self.quantity)

    def save(self, *args, **kwargs):
        if not self.product or not self.warehouse:
            raise ValueError("❌ No se puede guardar InventoryMovement sin producto o almacén.")

        print(f"💾 Salvando movimiento: product={self.product}, quantity={self.quantity}, unit={self.unit}, warehouse={self.warehouse}")

        # Calcular cantidad convertida
        try:
            converted_qty = self.get_converted_quantity() if self.unit else self.quantity
        except Exception as e:
            print(f"❌ Error al convertir cantidad: {e}")
            converted_qty = self.quantity

        if converted_qty is None:
            raise ValueError("🔥 Error: cantidad convertida terminó en None")

        # Guardar la cantidad convertida en el mismo campo
        self.quantity = converted_qty

        # Guardar el movimiento
        print(f"🏁 Guardando en DB → quantity={self.quantity} (tipo: {type(self.quantity)})")
        super().save(force_insert=not self.pk, *args, **kwargs)

        # Ajustar el stock
        stock, _ = Stock.objects.get_or_create(product=self.product, warehouse=self.warehouse)
        old_qty = stock.quantity
        stock.quantity += self.quantity * self.movement_type
        stock.save()

        print(f"📊 Stock actualizado: {old_qty} → {stock.quantity} (producto: {self.product}, almacén: {self.warehouse})")

    def delete(self, *args, **kwargs):
        from .models import Stock
        converted_qty = self.get_converted_quantity()
        stock, _ = Stock.objects.get_or_create(product=self.product, warehouse=self.warehouse)
        stock.quantity -= converted_qty * self.movement_type
        stock.save()
        super().delete(*args, **kwargs)
