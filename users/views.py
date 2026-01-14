from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import IsAdmin
from .serializers import (UserCreateSerializer, UserDetailSerializer, UserListSerializer, UserUpdateSerializer)
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q


User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        elif self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserDetailSerializer
    
    def get_queryset(self):
        queryset = User.objects.all()
        
        role = self.request.query_params.get('role', None)
        if role:
            queryset = queryset.filter(role=role)
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower()=='true')
            
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
    
        return queryset.order_by('-date_joined')

    @action(detail=True, methods=['patch'])
    def activate(self, request, _pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()
        
        serializer = UserDetailSerializer(user)
        return Response({
            'message': 'Utilisateur activé avec succès',
            'user': serializer.data
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['patch'])
    def deactivate(self, request, _pk=None):
        """Désactiver un utilisateur"""
        user = self.get_object()
        user.is_active = False
        user.save()
        
        serializer = UserDetailSerializer(user)
        return Response({
            'message': 'Utilisateur désactivé avec succès',
            'user': serializer.data
        }, status=status.HTTP_200_OK)
