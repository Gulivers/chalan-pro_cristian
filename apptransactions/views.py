from django.shortcuts import render
from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from .models import (
    DocumentType, PartyType, PartyCategory, Party
)
from .serializers import (
    DocumentTypeSerializer,PartyTypeSerializer,PartyCategorySerializer,PartySerializer
)
from rest_framework.authentication import TokenAuthentication


class DocumentTypeViewSet(viewsets.ModelViewSet):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    
class PartyTypeViewSet(viewsets.ModelViewSet):
    queryset = PartyType.objects.all()
    serializer_class = PartyTypeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    
class PartyCategoryViewSet(viewsets.ModelViewSet):
    queryset = PartyCategory.objects.all()
    serializer_class = PartyCategorySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

class PartyViewSet(viewsets.ModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer

    # Filtros / búsqueda / orden
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'category', 'types', 'customer_rank', 'supplier_rank']
    search_fields = ['name', 'rfc', 'email', 'phone', 'city', 'state']
    ordering_fields = ['name', 'customer_rank', 'supplier_rank', 'id']
    ordering = ['name']