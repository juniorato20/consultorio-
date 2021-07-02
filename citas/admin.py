from django.contrib import admin
from citas.models import  *



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
    list_display = ('paciente','doctor','tratamiento','fecha','hora','estado')
    search_fields = ['fecha']
    
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('id','paciente','observacion','fecha')
    search_fields = ['id']
    

    
admin.site.register(Tratamiento,TratamientoAdmin)    
admin.site.register(Paciente,PacienteAdmin)
admin.site.register(Doctor,DoctorAdmin)
admin.site.register(Cita,CitaAdmin)
admin.site.register(Reporte,ReporteAdmin)



