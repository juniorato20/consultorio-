from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.safestring  import mark_safe
from django.db import models

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
    apellido = models.CharField( max_length=225, unique=True, blank=False, null=False)
    direccion = models.TextField(max_length=225,blank=False, null=False)
    fecha = models.DateField()
    sexo = models.CharField(max_length=30,choices=genero, default='available')
    correo = models.EmailField()
    celular = models.CharField( max_length=10)
            
    class Meta:
        ordering = ["nombre","apellido"]
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
    direccion = models.TextField( max_length=225,blank=True, null=False)
    correo = models.EmailField()
    celular = models.CharField( max_length=10)

  
    class Meta:
        ordering = ["nombre", "apellido"]
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctores'
    
    def __str__(self):
        return self.nombre + " " + self.apellido

tiempo = [
    ('8:00/8:30 AM', '8:00/8:30 AM'),
    ('8:30/9:00 AM', '8:30/9:00 AM'),
    ('9:00/9:30 AM', '9:00/9:30 AM'),
    ('9:30/10:00 AM', '9:30/10:00 AM'),
    ('10:00/10:30 AM', '10:00/10:30 AM'),
    ('10:30/11:00 AM', '10:30/11:00 AM'),
    ('11:00/11:30 AM', '11:00/11:30 AM'),
    ('11:30/12:00 AM', '11:30/12:00 AM'),
    ('13:00/13:30 PM', '13:00/13:30 PA'),
    ('13:30/14:00 PM', '13:30/14:00 PM'),
    ('14:00/14:30 PM', '14:00/14:30 PM'),
    ('14:30/15:00 PM', '14:30/15:00 PM'),
    ('15:00/15:30 PM', '15:00/15:30 PM'),
    ('15:30/16:00 PM', '15:30/16:00 PM'),
    ('16:00/16:30 PM', '14:00/16:30 PM'),
    ('16:30/17:00 PM', '16:30/17:00 PM'),
]

class Cita(models.Model):
    id = models.AutoField(primary_key=True)
    paciente = models.ForeignKey( Paciente , on_delete=models.CASCADE, default='available')
    doctor = models.ForeignKey( Doctor, on_delete=models.CASCADE, default='available')
    tratamiento = models.ForeignKey(Tratamiento,  on_delete=models.CASCADE, default='available' )
    fecha = models.DateField()
    hora = models.CharField( max_length=50,choices=tiempo, default='available')
    estado = models.BooleanField(default = True)

    class Meta:
        ordering = ["doctor","id"]
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'

def str (self):
    return self.paciente.nombre

class Reporte(models.Model):
    id = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, default='available')
    observacion= models.TextField( max_length=225,blank=True, null=False)
    fecha = models.DateField()

    class Meta:
        ordering = ["id"]
        verbose_name = 'Reporte'
        verbose_name_plural = 'Reportes'

def str (self):
    return self.id

def url_perfil(self, filename):
    ruta = "static/Perfiles/%s/%s" % (self.usuario, str(filename))
    return ruta

class Perfil(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, default='available')
    celular = models.CharField('Celular', max_length=10)
    direccion = models.TextField('Direccion')
    cedula = models.CharField('Cedula', max_length=10)
    correo = models.EmailField()
    foto = models.ImageField('Foto', upload_to=url_perfil)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

def foto_perfil(self):
    return mark_safe('<a href="/%s" target="blank"><img src"/%s" hight="50px" widht="50px"/></a>' % (self.foto, self.foto))

foto_perfil.allow_tags = True

def __str__(self):
    return self.usuario.username
