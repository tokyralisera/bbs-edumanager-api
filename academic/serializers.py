from rest_framework import serializers
from .models import AnneeUniversitaire, Vague, Filiere, Niveau

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
        #? Valider que le nom de la vague est unique pour cette année universitaire
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
    class Meta:
        model = Vague
        fields = ['nom', 'annee_universitaire']
    
    def validate_annee_universitaire(self, value):
        #? Vérifier que l'année universitaire existe"""
        if not value:
            raise serializers.ValidationError(
                "L'année universitaire est obligatoire"
            )
        return value
    
class FiliereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filiere
        fields = [
            'id',
            'libelle',
            'code',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        
    def validate_code(self, value):
        value = value.strip().upper()
        if len(value) < 2 :
            raise serializers.ValidationError('Le code doit contenir au moins 2 caracteres')
        if len(value)> 10:
            raise serializers.ValidationError('Le code ne doit pas depasser 10 caracteres')
        
        existing = Filiere.objects.filter(code__iexact=value)

        if self.instance:
            existing = existing.exclude(pk=self.instance.pk)
            
        if existing.exists():
            raise serializers.ValidationError('Une Filiere avec ce libelle existe deja')
    
        return value
    
class FiliereListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filiere
        fields = ['id', 'code', 'libelle']

class NiveauSerializer(serializers.ModelSerializer):
    class Meta:
        model = Niveau
        fields = [
            'id',
            'libelle',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_libelle(self, value):
        value = value.strip()
        
        if len(value) < 2:
            raise serializers.ValidationError(
                'Le libellé doit contenir au moins 2 caractères'
            )
        
        existing = Niveau.objects.filter(libelle__iexact=value)
        
        if self.instance:
            existing = existing.exclude(pk=self.instance.pk)
        
        if existing.exists():
            raise serializers.ValidationError(
                'Un niveau avec ce libellé existe déjà'
            )
        
        return value

class NiveauListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Niveau
        fields = ['id', 'libelle']