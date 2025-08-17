from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentTypeViewSet

router = DefaultRouter()
router.register('document-types', DocumentTypeViewSet, basename='document-types')


urlpatterns = [
    path('api/', include(router.urls)),
]