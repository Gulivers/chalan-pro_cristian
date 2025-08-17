# App: transactions (documentos, detalles, clientes, proveedores)

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from appinventory.models import Product, UnitOfMeasure, Warehouse, PriceType, ProductBrand

User = get_user_model()

class PartyType(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class PartyCategory(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Party(models.Model):
    name = models.CharField(max_length=255)
    rfc = models.CharField(max_length=50, blank=True)
    street = models.CharField(max_length=100, blank=True)
    floor_office = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    types = models.ManyToManyField(PartyType)
    category = models.ForeignKey(PartyCategory, on_delete=models.SET_NULL, null=True)
    default_price_type = models.ForeignKey(PriceType, on_delete=models.SET_NULL, null=True, blank=True)
    customer_rank = models.PositiveIntegerField(default=0)
    supplier_rank = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def is_customer(self):
        return self.customer_rank > 0

    def is_supplier(self):
        return self.supplier_rank > 0

    def is_both(self):
        return self.customer_rank > 0 and self.supplier_rank > 0

    def __str__(self):
        return self.name

class DocumentType(models.Model):
    type_code = models.CharField(max_length=20, unique=True) # Ej: INCOME, ADJUSTMENT_OUT, PICK
    description = models.CharField(max_length=255)
    affects_physical = models.BooleanField(default=True)  # INVFIS
    affects_logical = models.BooleanField(default=True)   # INVLOG
    affects_accounting = models.BooleanField(default=False)  # INVCON
    is_taxable = models.BooleanField(default=False)       # IVA
    is_purchase = models.BooleanField(default=False)      # LIBCOM
    is_sales = models.BooleanField(default=False)         # LIBVTA
    warehouse_required = models.BooleanField(default=True)  # ALMACE
    stock_movement = models.SmallIntegerField(
        choices=[(1, "+1 Entrada"), (-1, "-1 Salida"), (0, "0 Neutro")],
        default=0
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.type_code} - {self.description}"

class Document(models.Model):
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True)
    party = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True)
    builder = models.CharField(max_length=100, blank=True, null=True)
    job = models.CharField(max_length=100, blank=True, null=True)
    lot = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    total_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    def clean(self):
        if not hasattr(self, "document_type") or self.document_type is None:
            return  # Detener validación si no se ha asignado aún

        if self.document_type and self.document_type.is_sales and not self.party.is_customer():
            raise ValidationError("Selected party is not a customer.")
        if self.document_type and self.document_type.is_purchase and not self.party.is_supplier():
            raise ValidationError("Selected party is not a supplier.")

    def calculate_totals(self):
        total = 0
        total_discount = 0
        for line in self.lines.all():
            total += line.final_price or 0
            discount = line.unit_price * line.quantity * (line.discount_percentage / 100)
            total_discount += discount
        self.total_amount = total
        self.total_discount = total_discount
        self.save()

def __str__(self):
    if getattr(self, "document_type", None) and self.date:
        return f"{self.document_type.type_code} - {self.date}"
    return "Document"

class DocumentLine(models.Model):
    document = models.ForeignKey(Document, related_name="lines", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.ForeignKey(UnitOfMeasure, on_delete=models.SET_NULL, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True)
    price_type = models.ForeignKey(PriceType, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(ProductBrand, on_delete=models.SET_NULL, null=True, blank=True)  # Marca específica usada en esta línea, útil para trazabilidad

    def clean(self):
        errors = {}
        if self.quantity is None:
            errors['quantity'] = 'La cantidad no puede estar vacía.'
        if self.product is None:
            errors['product'] = 'Debe seleccionar un producto.'
        if errors:
            raise ValidationError(errors)
        
    def save(self, *args, **kwargs):
        print(" 1 🧼 apptransactions\models.py -> DocumentLine: def save(self, *args, **kwargs).")
        
        discount = self.discount_percentage / 100
        adjusted_price = self.unit_price

        # El precio se mantiene tal cual viene del formulario (por unidad seleccionada)
        # No se aplica conversión aquí — solo se usa la unidad seleccionada

        self.final_price = adjusted_price * self.quantity * (1 - discount)

        # Si el usuario no seleccionó el tipo de precio, se usa el default del cliente o proveedor.
        if not self.price_type and self.document and self.document.party and self.document.party.default_price_type:
            self.price_type = self.document.party.default_price_type

        super().save(*args, **kwargs)

        # Recalcular totales del documento
        if self.document:
            self.document.calculate_totals()

    def __str__(self):
        unit_code = self.unit.code if self.unit else "unit"
        return f"{self.product.name} x {self.quantity} {unit_code}" if self.product else "Detail"
    
    
