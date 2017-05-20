from django.db import models

# Create your models here.
class Usuario(models.Model):
    nombre = models.CharField(max_length=32)
    tituloPag = models.CharField(max_length=32)
    letra = models.IntegerField(default=0)
    color = models.CharField(max_length=10)

class Direccion(models.Model):
    claseVia = models.CharField(max_length=10)
    nombreVia = models.TextField()
    numero = models.CharField(max_length=8)
    localidad = models.CharField(max_length=20)
    provincia = models.CharField(max_length=20)
    cp = models.IntegerField()

class DatosContacto(models.Model):
    telefono = models.CharField(max_length=11)
    email = models.EmailField()

class Aparcamiento(models.Model):
    nombre = models.CharField(max_length=60)
    direccion = models.ForeignKey(Direccion)
    latitud = models.FloatField()
    longitud = models.FloatField()
    descripcion = models.TextField()
    accesible = models.IntegerField()
    barrio = models.CharField(max_length=20)
    distrito = models.CharField(max_length=20)
    datosContacto = models.ForeignKey(DatosContacto)
    url = models.TextField()
    numComents = models.IntegerField(default=0)

class Seleccionado(models.Model):
    usuario = models.ForeignKey(Usuario)
    fecha = models.DateTimeField(auto_now_add=True)
    aparcamiento = models.ForeignKey(Aparcamiento)

class Comentarios(models.Model):
    aparcamiento = models.ForeignKey(Aparcamiento)
    texto = models.TextField()
