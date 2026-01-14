from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnneeUniversitaireViewSet, VagueViewSet

app_name = 'academic'

router = DefaultRouter()
router.register(r'annees-universitaires', AnneeUniversitaireViewSet, basename='annee-universitaire')
router.register(r'vagues', VagueViewSet, basename='vague')

urlpatterns = [
    path('', include(router.urls)),
]