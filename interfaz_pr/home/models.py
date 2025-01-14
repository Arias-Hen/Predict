from django.db import models

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
    class Meta:
        db_table = 'data"."users'
