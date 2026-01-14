from django.core.management.base import BaseCommand
from academic.models import AnneeUniversitaire, Vague
from datetime import date

class Command(BaseCommand):
    help = 'Créer des années universitaires et vagues de test'
    
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Création des données académiques...'))
        
        #? Créer des années universitaires
        annees = [
            {
                'date_debut': date(2023, 9, 1),
                'date_fin': date(2024, 7, 31),
                'is_active': False
            },
            {
                'date_debut': date(2024, 9, 1),
                'date_fin': date(2025, 7, 31),
                'is_active': True
            },
            {
                'date_debut': date(2025, 9, 1),
                'date_fin': date(2026, 7, 31),
                'is_active': False
            },
        ]
        
        for annee_data in annees:
            annee, created = AnneeUniversitaire.objects.get_or_create(
                date_debut=annee_data['date_debut'],
                date_fin=annee_data['date_fin'],
                defaults={'is_active': annee_data['is_active']}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Année universitaire créée: {annee.libelle}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Année universitaire existe déjà: {annee.libelle}')
                )
        
        #? Créer des vagues liées aux années universitaires
        annee_2024 = AnneeUniversitaire.objects.get(date_debut=date(2024, 9, 1))
        annee_2025 = AnneeUniversitaire.objects.get(date_debut=date(2025, 9, 1))
        
        vagues_data = [
            {'nom': 'Vague 1', 'annee': annee_2024},
            {'nom': 'Vague 2', 'annee': annee_2024},
            {'nom': 'Vague Exceptionnelle', 'annee': annee_2024},
            {'nom': 'Vague 1', 'annee': annee_2025},
            {'nom': 'Vague 2', 'annee': annee_2025},
        ]
        
        for vague_data in vagues_data:
            vague, created = Vague.objects.get_or_create(
                nom=vague_data['nom'],
                annee_universitaire=vague_data['annee']
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Vague créée: {vague.nom} - {vague.annee_universitaire.libelle}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Vague existe déjà: {vague.nom} - {vague.annee_universitaire.libelle}'
                    )
                )
        
        self.stdout.write(self.style.SUCCESS('\nDonnées académiques créées avec succès!'))