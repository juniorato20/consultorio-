from django.contrib import admin
from .models import  *

class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre','apellido','direccion','sexo','correo','celular')
    search_fields = ['nombre', 'apellido']

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('nombre','apellido','especialidad','sexo','direccion','celular')
    search_fields = ['nombre','apellido']

class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente','doctor','fecha','hora','descripcion')
    search_fields = ['fecha']
   
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('paciente','fecha','descripcion')
    search_fields = ['paciente']
 
class PerfilAdmin(admin.ModelAdmin):
    list_diplay =('cedula','usuario','celular','direccion','foto_perfil')
    search_fields = ['cedula','usuario']
    
admin.site.register(Paciente,PacienteAdmin)
admin.site.register(Doctor,DoctorAdmin)
admin.site.register(Cita,CitaAdmin)
admin.site.register(Reporte,ReporteAdmin)
admin.site.register(Perfil,PerfilAdmin)
