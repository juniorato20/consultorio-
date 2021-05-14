from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring  import mark_safe
genero = [
    ('Hombre', 'Hombre'),
    ('Mujer', 'Mujer'),
]
ocupacion = [
    ('Odontologo', 'Odontologo'),
    ('Odontologa', 'Odontologa'),
]

class Doctor(models.Model):
    nombre = models.CharField( max_length=225, blank=False, null=False)
    apellido = models.CharField( max_length=225, blank=False, null=False)
    especialidad = models.CharField( max_length=100, choices=ocupacion, default='available')
    sexo = models.CharField(max_length=30,choices=genero, default='available')
    direccion = models.TextField( max_length=225,blank=True, null=False)
    celular = models.CharField( max_length=10)

    class Meta:
        ordering = ["nombre"]
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctores'
    

def __str__(self):
        return self.nombre

class Paciente(models.Model):
    nombre = models.CharField(max_length=225, blank=False, null=False)
    apellido = models.CharField( max_length=225, blank=False, null=False)
    direccion = models.TextField(max_length=225,blank=False, null=False)
    sexo = models.CharField(max_length=30,choices=genero, default='available')
    correo = models.EmailField()
    fecha_nacimiento = models.DateField()
    celular = models.CharField( max_length=10)
    estado = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

    def __str__(self):
        return self.nombre

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
    paciente = models.ForeignKey( Paciente, on_delete=models.CASCADE, default='available')
    doctor = models.ForeignKey( Doctor, on_delete=models.CASCADE, default='available')
    fecha = models.DateField()
    hora = models.CharField( max_length=50,choices=tiempo, default='available')
    descripcion = models.CharField(max_length=225, blank=True, null=False)
    estado = models.BooleanField(default=True)

    class Meta:
        ordering = ["fecha","doctor"]
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'

def __str__(self):
    return self.fecha

class Reporte(models.Model):
    paciente = models.ForeignKey( Paciente, on_delete=models.CASCADE, default='available')
    fecha = models.DateField()
    descripcion = models.CharField(max_length=225, blank=True, null=False)
    estado = models.BooleanField( default=True)
    
    class Meta:
        ordering = ["fecha"]
        verbose_name = 'Reporte'
        verbose_name_plural = 'Reportes'

def __str__(self):
    return self.paciente

def url_perfil(self, filename):
    ruta = "static/Perfiles/%s/%s" % (self.usuario, str(filename))
    return ruta

class Perfil(models.Model):
    usuario = models.OneToOneField( User, on_delete=models.CASCADE, default='available')
    celular = models.CharField('Celular', max_length=10)
    direccion = models.TextField('Direccion')
    cedula = models.CharField('Cedula', max_length=10)
    foto = models.ImageField('Foto', upload_to=url_perfil)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

def foto_perfil(self):
    return mark_safe('<a href="/%s" target="blank"><img src"/%s" hight="50px" widht="50px"/></a>' % (self.foto, self.foto))

foto_perfil.allow_tags = True

def __str__(self):
    return self.usuario.username