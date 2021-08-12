from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, User
from django.utils.safestring  import mark_safe
from django.utils import timezone

genero = [
    ('Hombre', 'Hombre'),
    ('Mujer', 'Mujer'),
]
ocupacion = [
    ('Odontologo', 'Odontologo'),
    ('Odontologa', 'Odontologa'),
]
tiempo = [
    ('8:00 am/8:30 am', '8:00 am/8:30 am'),
    ('8:30 am/9:00 am', '8:30 am/9:00 am'),
    ('9:00 am/9:30 am', '9:00 am/9:30 am'),
    ('9:30 am/10:00 am', '9:30 am/10:00 am'),
    ('10:00 am/10:30 am', '10:00 am/10:30 am'),
    ('10:30 am/11:00 am', '10:30 am/11:00 am'),
    ('11:00 am/11:30 am', '11:00 am/11:30 am'),
    ('11:30 am/12:00 pm', '11:30 am/12:00 pm'),
    ('13:00 pm/13:30 pm', '13:00 pm/13:30 pm'),
    ('13:30 pm/14:00 pm', '13:30 pm/14:00 pm'),
    ('14:00 pm/14:30 pm', '14:00 pm/14:30 pm'),
    ('14:30 pm/15:00 pm', '14:30 pm/:15:00 pm'),
    ('15:00 pm/15:30 pm', '15:00 pm/15:30 pm'),
    ('15:30 pm/16:00 pm', '15:30 pm/16:00 pm'),
    ('16:00 pm/16:30 pm', '16:00 pm/16:30 pm'),
    ('16:30 am/17:00 am', '16:30 am/17:00 am'),
  
]
class Tratamiento(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=False, null=False)
    descripcion = models.CharField(max_length=255, blank=False, null=False)
    precio = models.DecimalField(max_digits=5, decimal_places=2)
   
    class Meta:
        ordering = ["nombre"]
        verbose_name = 'Tratamiento'
        verbose_name_plural = 'Tratamientos'

    def __str__(self):
        return self.nombre

class Paciente(models.Model):
    id = models.AutoField(primary_key=True)
    cedula = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=225, blank=False, null=False)
    apellido = models.CharField( max_length=225, blank=False, null=False)
    direccion = models.TextField(max_length=225,blank=False, null=False)
    fecha = models.DateField()
    observacion= models.TextField( max_length=225,blank=False, null=False)
    sexo = models.CharField(max_length=30,choices=genero, default='available')
    correo = models.EmailField()
    celular = models.CharField( max_length=10)
            
    class Meta:
        ordering = ["apellido","nombre"]
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
    
    def __str__(self):
        return self.nombre + " " + self.apellido

class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    cedula = models.CharField(max_length=10, unique=True)
    nombre = models.CharField( max_length=225, blank=False, null=False)
    apellido = models.CharField( max_length=225, blank=False, null=False)
    especialidad = models.CharField( max_length=60, choices=ocupacion, default='available')
    sexo = models.CharField(max_length=30 ,choices=genero, default='available')
    direccion = models.TextField( max_length=225,blank=False, null=False)
    correo = models.EmailField()
    celular = models.CharField( max_length=10)
    # fecha_entrega = models.DateTimeField(default=timezone.now)
  
    class Meta:
        ordering = ["apellido", "nombre"]
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctores'
    
    def __str__(self):
        return self.nombre + " " + self.apellido

class Cita(models.Model):
    id = models.AutoField(primary_key=True)
    paciente = models.ForeignKey( Paciente , on_delete=models.CASCADE, default='available')
    doctor = models.ForeignKey( Doctor, on_delete=models.CASCADE, default='available')
    tratamiento = models.ForeignKey(Tratamiento,  on_delete=models.CASCADE, default='available' )
    fecha = models.DateField()
    hora =  models.CharField( max_length=60, choices=tiempo, default='available')
    estado = models.BooleanField(default = True)
    
    class Meta:
        ordering = ["doctor","fecha"]
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'

    def __str__ (self):
        return self.paciente.nombre + " " + self.paciente.apellido


class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return self.usuario.username

