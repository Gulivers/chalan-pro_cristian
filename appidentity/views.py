from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from .models import Identity
from rest_framework import viewsets, filters 
from .serializers import IdentitySerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions 
from rest_framework.pagination import PageNumberPagination

class IdentityPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

class IdentityViewSet(viewsets.ModelViewSet):
    serializer_class = IdentitySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    pagination_class = IdentityPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    
    def get_queryset(self):    
        user = self.request.user
        if user.is_staff:
            return Identity.objects.all()
    
    def perform_create(self, serializer):
        user = self.request.user
        if user.is_staff:
            serializer.save()
