from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class AnneeUniversitaire(models.Model):
    """Modèle pour l'année universitaire"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin = models.DateField(verbose_name="Date de fin")
    is_active = models.BooleanField(default=False, verbose_name="Année active")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    
    class Meta:
        db_table = 'annees_universitaires'
        verbose_name = 'Année Universitaire'
        verbose_name_plural = 'Années Universitaires'
        ordering = ['-date_debut']
        constraints = [
            models.CheckConstraint(
                condition=models.Q(date_fin__gt=models.F('date_debut')),
                name='date_fin_after_date_debut'
            )
        ]
    
    def __str__(self):
        return f"{self.date_debut.year}-{self.date_fin.year}"
    
    @property
    def libelle(self):
        """Retourne le libellé formaté de l'année universitaire"""
        return f"{self.date_debut.year}/{self.date_fin.year}"
    
    def save(self, *args, **kwargs):
        #? Si cette année est activée, désactiver toutes les autres
        if self.is_active:
            AnneeUniversitaire.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)
    
    @classmethod
    def get_active_year(cls):
        """Retourne l'année universitaire active"""
        return cls.objects.filter(is_active=True).first()


class Vague(models.Model):
    """Modèle pour les vagues d'inscription"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100, verbose_name="Nom de la vague")
    annee_universitaire = models.ForeignKey(
        AnneeUniversitaire,
        on_delete=models.CASCADE,
        related_name='vagues',
        verbose_name="Année universitaire"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    
    class Meta:
        db_table = 'vagues'
        verbose_name = 'Vague'
        verbose_name_plural = 'Vagues'
        ordering = ['annee_universitaire', 'nom']
        #? Contrainte une vague unique par année universitaire
        constraints = [
            models.UniqueConstraint(
                fields=['nom', 'annee_universitaire'],
                name='unique_vague_per_year'
            )
        ]
    
    def __str__(self):
        return f"{self.nom} - {self.annee_universitaire.libelle}"
