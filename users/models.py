from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
import uuid

# Create your models here.
class UserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email obligatoire")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'ADMIN')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser doit avoir is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser doit avoir is_superuser=True')
        
        return self.create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrateur'),
        ('SCOLARITE', 'Service Scolarite'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=150, verbose_name="Prenom")
    last_name = models.CharField(max_length=150, verbose_name="Nom")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='SCOLARITE', verbose_name='Role')
    is_active = models.BooleanField(default=True, verbose_name='Actif')
    is_staff = models.BooleanField(default=False, verbose_name='Staff')
    is_superuser = models.BooleanField(default=False, verbose_name='Superuser')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="Date de l'inscription")
    last_login = models.DateTimeField(null=True, blank=True, verbose_name="Date de derniere connexion")
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
        ordering = ['-date_joined']
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_short_name(self):
        return self.first_name