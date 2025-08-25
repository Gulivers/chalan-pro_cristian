from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from .models import (
    Party, PartyType, PartyCategory,
    DocumentType, Document, DocumentLine
)

@admin.register(PartyType)
class PartyTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(PartyCategory)
class PartyCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'default_price_type', 'customer_rank', 'supplier_rank', 'is_active')
    list_filter = ('is_active', 'category')
    search_fields = ('name', 'rfc', 'email', 'phone')
    autocomplete_fields = ('category', 'default_price_type', 'types')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate()

    def get_list_filter(self, request):
        filters = list(super().get_list_filter(request))
        filters.append(('customer_rank', admin.BooleanFieldListFilter))
        filters.append(('supplier_rank', admin.BooleanFieldListFilter))
        return filters


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_code', 'description', 'stock_movement', 'is_active')
    search_fields = ('type_code', 'description')
    list_filter = ('is_active', 'stock_movement')

# Validación que aplica a cada línea del inline
class DocumentLineInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                quantity = form.cleaned_data.get('quantity')
                product = form.cleaned_data.get('product')
                if quantity is None or product is None:
                    raise ValidationError("Todas las líneas deben tener producto y cantidad.")

class DocumentLineInline(admin.TabularInline):
    model = DocumentLine
    extra = 1
    formset = DocumentLineInlineFormSet

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        for field in ['quantity', 'product']:
            if field in formset.form.base_fields:
                formset.form.base_fields[field].required = True  # Campos obligatorios
        return formset

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('document_type', 'date', 'party', 'warehouse', 'is_active')
    search_fields = ('job', 'lot', 'notes')
    list_filter = ('document_type', 'warehouse', 'is_active')
    autocomplete_fields = ('party', 'warehouse', 'document_type', 'created_by')
    inlines = [DocumentLineInline]

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        for field in ['quantity', 'product']:
            if field in formset.form.base_fields:
                formset.form.base_fields[field].required = True
        return formset