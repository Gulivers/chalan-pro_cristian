from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DashboardView, WarehouseViewSet, ProductCategoryViewSet,
    ProductBrandViewSet, ProductViewSet,
    UnitOfMeasureViewSet, ProductListAPIView, UnitOfMeasureListAPIView,
    UnitCategoryListAPIView, UnitCategoryViewSet, PriceTypeViewSet,
    ProductDataTableAPIView
)

from .views_validation import validate_units_of_measure

from .views_schema import (
    ProductCategorySchemaView, ProductBrandSchemaView,
    UnitOfMeasureSchemaView, UnitCategorySchemaView,
    PriceTypeSchemaView
)

# Router para ViewSets
router = DefaultRouter()
router.register(r'warehouses', WarehouseViewSet, basename='warehouse')
router.register(r'productcategory', ProductCategoryViewSet)
router.register(r'productbrand', ProductBrandViewSet)
router.register(r'products', ProductViewSet, basename='product')
router.register(r'unitsofmeasure', UnitOfMeasureViewSet, basename='unitofmeasure')
router.register(r'unitcategory', UnitCategoryViewSet)
router.register(r'pricetypes', PriceTypeViewSet)

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='inventory-dashboard'),
    path('api/validate-units-measure/', validate_units_of_measure, name='validate-units-measure'),
    
    # Schema endpoints
    path('api/schema/product-category/', ProductCategorySchemaView.as_view(), name='product-category-schema'),
    path('api/schema/productcategory/', ProductCategorySchemaView.as_view()),  # alias alternativo
    path('api/schema/productbrand/', ProductBrandSchemaView.as_view(), name='productbrand-schema'),
    path('api/schema/unitofmeasure/', UnitOfMeasureSchemaView.as_view(), name='unitofmeasure-schema'),
    path('api/unitcategories/', UnitCategoryListAPIView.as_view(), name='unitcategory-list'),
    path('api/schema/unitcategory/', UnitCategorySchemaView.as_view(), name='unitcategory-schema'),
    path('api/schema/pricetype/', PriceTypeSchemaView.as_view(), name='pricetype-schema'),
    
    # List endpoints
    path('api/products/options/', ProductListAPIView.as_view(), name='product-list-options'),
    path('api/unitsofmeasure-options/', UnitOfMeasureListAPIView.as_view(), name='unitofmeasure-options'),
    path('api/datatable-products/', ProductDataTableAPIView.as_view(), name='datatable-products'),
    
    # CRUD API routes
    path('api/', include(router.urls)),
]
