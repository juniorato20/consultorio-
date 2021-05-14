from django.contrib import admin
from .models import  *
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class PacienteResource(resources.ModelResource):
    class Meta:
       model = Paciente

class PacienteAdmin(ImportExportModelAdmin):
    list_display = ('nombre','apellido','direccion','sexo','correo','fecha_nacimiento','celular','estado')
    search_fields = ['nombre', 'apellido']
    resources_class = PacienteResource


class DoctorResource(resources.ModelResource):
    class Meta:
       model = Doctor

class DoctorAdmin(ImportExportModelAdmin):
    list_display = ('nombre','apellido','especialidad','sexo','direccion','celular')
    search_fields = ['nombre','apellido']
    resources_class = DoctorResource

class CitaResource(resources.ModelResource):
    class Meta:
       model = Cita

class CitaAdmin(ImportExportModelAdmin):
    list_display = ('paciente','doctor','fecha','hora','descripcion','estado')
    search_fields = ['fecha']
    resources_class = CitaResource

class ReporteResource(resources.ModelResource):
    class Meta:
        model = Reporte

class ReporteAdmin(ImportExportModelAdmin):
    list_display = ('paciente','fecha','descripcion','estado')
    search_fields = ['paciente']
    resources_class = ReporteResource

class PerfilAdmin(admin.ModelAdmin):
    list_diplay =('cedula','usuario','celular','direccion','foto_perfil')
    search_fields = ['cedula','usuario']
    
admin.site.register(Paciente,PacienteAdmin)
admin.site.register(Doctor,DoctorAdmin)
admin.site.register(Cita,CitaAdmin)
admin.site.register(Reporte,ReporteAdmin)
admin.site.register(Perfil,PerfilAdmin)
