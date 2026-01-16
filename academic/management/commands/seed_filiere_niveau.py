from django.core.management.base import BaseCommand
from academic.models import Filiere, Niveau

class Command(BaseCommand):
    help = 'Créer des filières et niveaux de test'
    
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Création des filières et niveaux...'))
        
        # Créer des filières
        filieres_data = [
            {'code': 'MARKET', 'libelle': 'Marketing'},
            {'code': 'COMPTA', 'libelle': 'Comptabilité'},
            {'code': 'BANK', 'libelle': 'Banque et Finance'},
        ]
        
        for filiere_data in filieres_data:
            filiere, created = Filiere.objects.get_or_create(
                code=filiere_data['code'],
                defaults={'libelle': filiere_data['libelle']}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Filière créée: {filiere.code} - {filiere.libelle}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Filière existe déjà: {filiere.code}')
                )
        
        # Créer des niveaux
        niveaux_data = [
            'Licence 1',
            'Licence 2',
            'Licence 3',
        ]
        
        for niveau_libelle in niveaux_data:
            niveau, created = Niveau.objects.get_or_create(libelle=niveau_libelle)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Niveau créé: {niveau.libelle}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Niveau existe déjà: {niveau.libelle}')
                )
        
        self.stdout.write(self.style.SUCCESS('\nFilières et niveaux créés avec succès!'))
