from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from .models import Identity
from rest_framework import viewsets, filters, serializers
from .serializers import IdentitySerializer, UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend

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
        else:
            return Identity.objects.filter(user=user)
    
    def perform_create(self, serializer):
        user = self.request.user

        user_id = self.request.data.get('user_id', None)
        
        if user.is_staff and user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise serializers.ValidationError("El usuario especificado no existe.")
        
            if Identity.objects.filter(user=user).exists() and self.request.method in ['POST', 'PUT']:
                raise serializers.ValidationError("Ya hay una empresa registrada para este usuario.")

        serializer.save(user=user)
            
    @action(detail=False, methods=['get'], url_path='me')
    def get_or_create_my_identity(self, request):
        identity, created = Identity.objects.get_or_create(user=self.request.user)
        if created:
            # If the identity was created, you might want to set some default values
            identity.name = "Company of "+ self.request.user.username
            identity.save()
        serializer = self.get_serializer(identity)
        return Response(serializer.data)
    
    # @action(detail=False, methods=['get'], url_path='all', permission_classes=[IsAdminUser])
    # def list_all_identities(self, request):
    #     """Solo accesible para administradores"""
    #     queryset = Identity.objects.all()
        
    #     # Aplica paginación
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)

    #     # Sin paginación
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
