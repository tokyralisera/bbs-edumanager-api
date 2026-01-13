from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Créer les utilisateurs par défaut (Admin et Scolarité)'
    
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Création des utilisateurs par défaut...'))
        
        # Créer un administrateur
        if not User.objects.filter(email='admin@bbs.edu').exists():
            admin = User.objects.create_superuser(
                email='admin@bbs.edu',
                password='admin123',
                first_name='Administrateur',
                last_name='Principal',
                role='ADMIN'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Admin créé: {admin.email}')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Admin existe déjà: admin@bbs.edu')
            )
        
        # Créer un utilisateur scolarité
        if not User.objects.filter(email='scolarite@bbs.edu').exists():
            scolarite = User.objects.create_user(
                email='scolarite@bbs.edu',
                password='scolarite123',
                first_name='Service',
                last_name='Scolarité',
                role='SCOLARITE'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Scolarité créé: {scolarite.email}')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Scolarité existe déjà: scolarite@bbs.edu')
            )
        
        self.stdout.write(self.style.SUCCESS('Création des utilisateurs terminée!'))
        self.stdout.write(self.style.SUCCESS('\Comptes créés:'))
        self.stdout.write('   - Admin: admin@bbs.edu / admin123')
        self.stdout.write('   - Scolarité: scolarite@bbs.edu / scolarite123')