from django.contrib import admin
from .models import AnneeUniversitaire, Vague

@admin.register(AnneeUniversitaire)
class AnneeUniversitaireAdmin(admin.ModelAdmin):
    """Configuration de l'interface admin pour AnneeUniversitaire"""
    
    list_display = ['libelle', 'date_debut', 'date_fin', 'is_active', 'created_at']
    list_filter = ['is_active', 'date_debut']
    search_fields = ['date_debut', 'date_fin']
    ordering = ['-date_debut']
    
    fieldsets = (
        ('Période', {
            'fields': ('date_debut', 'date_fin')
        }),
        ('Statut', {
            'fields': ('is_active',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def libelle(self, obj):
        return obj.libelle
    libelle.short_description = 'Année Universitaire'


@admin.register(Vague)
class VagueAdmin(admin.ModelAdmin):
    """Configuration de l'interface admin pour Vague"""
    
    list_display = ['nom', 'annee_universitaire', 'created_at']
    list_filter = ['annee_universitaire']
    search_fields = ['nom']
    ordering = ['-annee_universitaire', 'nom']
    
    fieldsets = (
        (None, {
            'fields': ('nom', 'annee_universitaire')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']