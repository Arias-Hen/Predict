from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_created = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created']

    def _str_(self):
        return self.title

class UsersManager(BaseUserManager):
    def create_user(self, usuario, password=None, **extra_fields):
        if not usuario:
            raise ValueError("El nombre de usuario debe ser proporcionado")
        user = self.model(usuario=usuario, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, usuario, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(usuario, password, **extra_fields)


class Users(AbstractBaseUser, PermissionsMixin):
    uniqueid = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=100, unique=True)
    empresa = models.CharField(max_length=100, default='Mi Empresa')
    nombre = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Nombre único para evitar conflictos
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Nombre único para evitar conflictos
        blank=True,
    )

    objects = UsersManager()

    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'data"."users'

    def __str__(self):
        return self.usuario
    
class Valoracion(models.Model):
    idv = models.AutoField(primary_key=True)
    iduser = models.IntegerField()
    modo = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=100)
    distrito = models.CharField(max_length=100)
    barrio = models.CharField(max_length=100)
    calle = models.CharField(max_length=100)
    tipo_vivienda = models.CharField(max_length=100)
    metros_cuadrados = models.FloatField()
    num_habitaciones = models.IntegerField()
    num_banos = models.IntegerField()
    planta = models.IntegerField()
    terraza = models.BooleanField()
    balcon = models.BooleanField()
    ascensor = models.BooleanField()
    estado_inmueble = models.CharField(max_length=50)
    fecha_guardado = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'data"."ventas'