from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DocumentTypeViewSet, PartyTypeViewSet, PartyCategoryViewSet, PartyViewSet
)

router = DefaultRouter()
router.register(r'document-types', DocumentTypeViewSet)
router.register(r'party-types', PartyTypeViewSet)
router.register(r'party-categories', PartyCategoryViewSet)
router.register(r'parties', PartyViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]