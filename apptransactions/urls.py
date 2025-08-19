from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DocumentTypeViewSet, PartyTypeViewSet
)

router = DefaultRouter()
router.register(r'document-types', DocumentTypeViewSet)
router.register(r'party-types', PartyTypeViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
]