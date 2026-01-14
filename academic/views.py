from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from authentication.permissions import IsAdminOrScolarite
from .models import AnneeUniversitaire, Vague
from .serializers import (
    AnneeUniversitaireSerializer,
    AnneeUniversitaireCreateSerializer,
    VagueSerializer,
    VagueListSerializer,
    VagueCreateSerializer
)


class AnneeUniversitaireViewSet(viewsets.ModelViewSet):    
    queryset = AnneeUniversitaire.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrScolarite]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AnneeUniversitaireCreateSerializer
        return AnneeUniversitaireSerializer
    
    def get_queryset(self):
        queryset = AnneeUniversitaire.objects.all()
        
        #? Filtrer par statut actif
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        #? Filtrer par année
        year = self.request.query_params.get('year', None)
        if year:
            queryset = queryset.filter(
                Q(date_debut__year=year) | Q(date_fin__year=year)
            )
        
        return queryset.order_by('-date_debut')
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        active_year = AnneeUniversitaire.get_active_year()
        
        if not active_year:
            return Response({
                'message': 'Aucune année universitaire active'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AnneeUniversitaireSerializer(active_year)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        #? Activer une année universitaire
        annee = self.get_object()
        
        #? Désactiver toutes les autres années
        AnneeUniversitaire.objects.exclude(pk=annee.pk).update(is_active=False)
        
        #? Activer cette année
        annee.is_active = True
        annee.save()
        
        serializer = AnneeUniversitaireSerializer(annee)
        return Response({
            'message': 'Année universitaire activée avec succès',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        #? Désactiver une année universitaire
        annee = self.get_object()
        annee.is_active = False
        annee.save()
        
        serializer = AnneeUniversitaireSerializer(annee)
        return Response({
            'message': 'Année universitaire désactivée avec succès',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class VagueViewSet(viewsets.ModelViewSet):
    
    queryset = Vague.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrScolarite]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return VagueListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return VagueCreateSerializer
        return VagueSerializer
    
    def get_queryset(self):
        queryset = Vague.objects.select_related('annee_universitaire').all()
        
        #? Filtrer par année universitaire
        annee_id = self.request.query_params.get('annee_universitaire', None)
        if annee_id:
            queryset = queryset.filter(annee_universitaire_id=annee_id)
        
        #? Filtrer par année universitaire active
        active_year = self.request.query_params.get('active_year', None)
        if active_year and active_year.lower() == 'true':
            queryset = queryset.filter(annee_universitaire__is_active=True)
        
        #? Recherche par nom
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(nom__icontains=search)
        
        return queryset.order_by('annee_universitaire__date_debut', 'nom')
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        #? Retourner avec le serializer complet
        instance = serializer.instance
        response_serializer = VagueSerializer(instance)
        
        return Response({
            'message': 'Vague créée avec succès',
            'data': response_serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        #? Retourner avec le serializer complet
        response_serializer = VagueSerializer(instance)
        
        return Response({
            'message': 'Vague mise à jour avec succès',
            'data': response_serializer.data
        }, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        #? Supprimer une vague
        instance = self.get_object()
        
        #! Vérifier qu'aucune inscription n'utilise cette vague
        if instance.inscriptions.exists():
             return Response({
                'error': 'Impossible de supprimer cette vague car elle est utilisée'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_destroy(instance)
        
        return Response({
            'message': 'Vague supprimée avec succès'
        }, status=status.HTTP_200_OK)