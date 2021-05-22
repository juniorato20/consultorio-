from django.contrib import admin
from .models import  *

class TratamientoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion','precio')
    search_fields = ['nombre']

class PacienteAdmin(admin.ModelAdmin):
    list_display = ('cedula','nombre','apellido','direccion','fecha','sexo','correo','celular')
    search_fields = ['nombre', 'apellido']

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('cedula','nombre','apellido','especialidad','sexo','direccion','correo','celular')
    search_fields = ['nombre','apellido']

class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente','doctor','tratamiento','fecha','hora')
    search_fields = ['fecha']
 
class PerfilAdmin(admin.ModelAdmin):
    list_diplay =('cedula','usuario','celular','direccion','foto_perfil')
    search_fields = ['cedula','usuario']
    
admin.site.register(Tratamiento,TratamientoAdmin)    
admin.site.register(Paciente,PacienteAdmin)
admin.site.register(Doctor,DoctorAdmin)
admin.site.register(Cita,CitaAdmin)
admin.site.register(Perfil,PerfilAdmin)
