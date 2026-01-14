from rest_framework import serializers
from .models import AnneeUniversitaire, Vague
from datetime import datetime


class VagueListSerializer(serializers.ModelSerializer):
    annee_universitaire_libelle = serializers.CharField(source='annee_universitaire.libelle', read_only=True)
    
    class Meta:
        model = Vague
        fields = [
            'id',
            'nom',
            'annee_universitaire_libelle',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'annee_universitaire_libelle']


class AnneeUniversitaireSerializer(serializers.ModelSerializer):
    libelle = serializers.CharField(read_only=True)
    vagues = VagueListSerializer(many=True, read_only=True)
    vagues_count= serializers.SerializerMethodField()
    
    class Meta:
        model = AnneeUniversitaire
        fields = [
            'id',
            'date_debut',
            'date_fin',
            'libelle',
            'is_active',
            'vagues',
            'vagues_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'libelle', 'created_at', 'updated_at', 'vagues', 'vagues_count']
        
    def get_vagues_count(self, obj):
        return obj.vagues.count()
    
    def validate(self, data):
        date_debut = data.get('date_debut', None)
        date_fin = data.get('date_fin', None)
        
        if date_debut and date_fin:
            if date_debut >= date_fin:
                raise serializers.ValidationError("La date de début doit être antérieure à la date de fin.")
        
        return data

    def validate_date_debut(self, value):
        #? Valider que la date de début n'est pas trop ancienne
        if value.year < 2000:
            raise serializers.ValidationError(
                "L'année de début ne peut pas être antérieure à 2000"
            )
        return value
    
class AnneeUniversitaireCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnneeUniversitaire
        fields = ['date_debut', 'date_fin', 'is_active']
        
    def validate(self, data):
        date_debut = data.get('date_debut')
        date_fin = data.get('date_fin')
        
        if date_fin <= date_debut:
            raise serializers.ValidationError("La date de fin doit être postérieure à la date de début.")
        
        existing = AnneeUniversitaire.objects.filter(
            date_debut=date_debut,
            date_fin=date_fin
        )
        
        if self.instance:
            existing = existing.exclude(pk=self.instance.pk)
        
        if existing.exists():
            raise serializers.ValidationError("Une année universitaire avec ces dates existe déjà.")
    
        return data
    
class VagueSerializer(serializers.ModelSerializer):
    annee_universitaire_libelle = serializers.CharField(source='annee_universitaire.libelle', read_only=True)
    
    class Meta:
        model = Vague
        fields = [
            'id',
            'nom',
            'annee_universitaire',
            'annee_universitaire_libelle',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'annee_universitaire_libelle']
        
    def validate(self, data):
        """Valider que le nom de la vague est unique pour cette année universitaire"""
        nom = data.get('nom', '').strip()
        annee_universitaire = data.get('annee_universitaire')
        
        if len(nom) < 3:
            raise serializers.ValidationError({
                'nom': 'Le nom de la vague doit contenir au moins 3 caractères'
            })
        
        #? Vérifier si l'annee universitaire est unique
        existing = Vague.objects.filter(
            nom__iexact=nom,
            annee_universitaire=annee_universitaire
        )
        
        if self.instance:
            existing = existing.exclude(pk=self.instance.pk)
        
        if existing.exists():
            raise serializers.ValidationError({
                'nom': 'Une vague avec ce nom existe déjà pour cette année universitaire'
            })
        
        return data

class VagueCreateSerializer(serializers.ModelSerializer):
    """Serializer pour créer une vague"""
    
    class Meta:
        model = Vague
        fields = ['nom', 'annee_universitaire']
    
    def validate_annee_universitaire(self, value):
        """Vérifier que l'année universitaire existe"""
        if not value:
            raise serializers.ValidationError(
                "L'année universitaire est obligatoire"
            )
        return value