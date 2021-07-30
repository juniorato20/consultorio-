from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.utils.safestring  import mark_safe


genero = [
    ('Hombre', 'Hombre'),
    ('Mujer', 'Mujer'),
]
ocupacion = [
    ('Odontologo', 'Odontologo'),
    ('Odontologa', 'Odontologa'),
]
class Tratamiento(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=False, null=False,unique=True )
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
    hora = models.TimeField()
    estado = models.BooleanField(default = True)

    class Meta:
        ordering = ["doctor","id"]
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'

    def __str__ (self):
        return self.paciente.nombre + " " + self.paciente.apellido

class Reporte(models.Model):
    id = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, default='available')
    observacion= models.TextField( max_length=225,blank=False, null=False)
    fecha = models.DateField()

    class Meta:
        ordering = ["id"]
        verbose_name = 'Reporte'
        verbose_name_plural = 'Reportes'

    def __str__ (self):
        return self.paciente.nombre + " " + self.paciente.apellido
 

# class CustomUser(AbstractUser):
     
#     token = models.UUIDField(primary_key=False, editable=False, null=True, blank=True)
#     class Meta: 
#         verbose_name  = 'User'
#         verbose_name_plural = 'Users'
    
#     def __str__(self):
#         return self.username
