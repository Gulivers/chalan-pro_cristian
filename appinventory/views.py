# Django core
from django.views.generic import TemplateView
from django.db.models import F, Sum, OuterRef, Subquery
# Django REST Framework (DRF)
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, action
from rest_framework.permissions import (
    IsAuthenticated,
    DjangoModelPermissions,
    AllowAny,
    IsAuthenticatedOrReadOnly
    )
from utils.datatable import handle_datatable_query
# App Models
from appinventory.models import (
    Product, Stock, Warehouse, ProductCategory,
    ProductBrand, UnitOfMeasure, UnitCategory, PriceType
    )
from apptransactions.models import Document, DocumentLine
# Serializers
from appinventory.serializers import (
    WarehouseSerializer, ProductCategorySerializer, ProductBrandSerializer,
    ProductSerializer, UnitOfMeasureSerializer, UnitCategorySerializer,
    PriceTypeSerializer, ProductListSerializer,ProductDetailSerializer
    )


class DashboardView(TemplateView):
    template_name = "inventory/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Productos con stock bajo el reorder_level
        low_stock_products = (
            Product.objects.filter(is_active=True)
            .annotate(
                total_stock=Subquery(
                    Stock.objects.filter(product=OuterRef('pk'))
                    .values('product')
                    .annotate(qty=Sum('quantity'))
                    .values('qty')[:1]
                )
            )
            .filter(total_stock__lt=F('reorder_level'))
        )

        # Top 5 productos más bajos en stock
        lowest_stock_products = (
            Product.objects.filter(is_active=True)
            .annotate(
                total_stock=Subquery(
                    Stock.objects.filter(product=OuterRef('pk'))
                    .values('product')
                    .annotate(qty=Sum('quantity'))
                    .values('qty')[:1]
                )
            )
            .order_by('total_stock')[:5]
        )

        # Últimos movimientos (últimos 10 documentos con líneas)
        recent_documents = (
            Document.objects.filter(is_active=True)
            .select_related('document_type', 'warehouse', 'party')
            .prefetch_related('lines')
            .order_by('-date')[:10]
        )

        # Totales generales
        total_warehouses = Warehouse.objects.filter(is_active=True).count()
        total_products = Product.objects.filter(is_active=True).count()
        total_stock_units = Stock.objects.aggregate(total=Sum('quantity'))['total'] or 0

        context.update({
            'low_stock_products': low_stock_products,
            'lowest_stock_products': lowest_stock_products,
            'recent_documents': recent_documents,
            'total_warehouses': total_warehouses,
            'total_products': total_products,
            'total_stock_units': total_stock_units,
            'page_title': "Inventory Dashboard"
        })

        return context

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

class UnitCategoryViewSet(viewsets.ModelViewSet):
    queryset = UnitCategory.objects.all()
    serializer_class = UnitCategorySerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    authentication_classes = [TokenAuthentication]

class UnitCategoryListAPIView(ListAPIView):
    queryset = UnitCategory.objects.all()
    serializer_class = UnitCategorySerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

class ProductBrandViewSet(viewsets.ModelViewSet):
    queryset = ProductBrand.objects.all()
    serializer_class = ProductBrandSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    
class PriceTypeViewSet(viewsets.ModelViewSet):
    queryset = PriceType.objects.all()
    serializer_class = PriceTypeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer  # Para vistas tipo tabla
        elif self.action == 'retrieve':
            return ProductDetailSerializer  # Para vista detalle o edición
        return ProductSerializer  # Para create, update, partial_update

@permission_classes([AllowAny])
class ProductListAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        return Response([
            {"value": p.id, "label": p.name} for p in products
        ])

class UnitOfMeasureViewSet(viewsets.ModelViewSet):
    queryset = UnitOfMeasure.objects.all()
    serializer_class = UnitOfMeasureSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

@permission_classes([AllowAny])
class UnitOfMeasureListAPIView(APIView):
    def get(self, request):
        units = UnitOfMeasure.objects.all()
        return Response([
            {"value": u.id, "label": u.name} for u in units
        ])

class ProductDataTableAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Product.objects.select_related('category', 'brand', 'unit_default')
        return handle_datatable_query(
            request,
            queryset,
            ProductListSerializer,
            search_fields=['name', 'sku']
        )
