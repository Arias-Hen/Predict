from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_created = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created']

    def _str_(self):
        return self.title

class Users(models.Model):
    uniqueid = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100, default='Mi Empresa')
    nombre = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    estado = models.BooleanField(default=True) 
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'data"."users'

    def __str__(self):
        return self.usuario

    # Establecer una contraseña cifrada
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    # Verificar la contraseña
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    # Marcar el usuario como autenticado
    @property
    def is_authenticated(self):
        return True if self.is_active else False
    uniqueid = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100, default='Mi Empresa')
    nombre = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    estado = models.BooleanField(default=True) 
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = 'data"."users'
