from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnneeUniversitaireViewSet, VagueViewSet, FiliereViewSet, NiveauViewSet

app_name = 'academic'

router = DefaultRouter()
router.register(r'annees-universitaires', AnneeUniversitaireViewSet, basename='annee-universitaire')
router.register(r'vagues', VagueViewSet, basename='vague'),
router.register(r'filieres', FiliereViewSet, basename='filiere'),
router.register(r'niveaux', NiveauViewSet, basename='niveaux'),

urlpatterns = [
    path('', include(router.urls)),
]