"""CONSULTORIO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.messages import views
from django.urls import path,include
from citas.views import *
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import handler404, handler500



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name="vista_login"),
    path('login/', login_view, name="vista_login"),
    path('inicio/', inicio_view, name="vista_inicio"),
    path('logout/', logout_view, name="vista_logout"), 

    path('registro/', registro, name="registro"),

    path('reset/password/',ResetPasswordView.as_view(),name="reset_password"),
    path('change/password/<str:token>/', ChangePasswordView.as_view(), name='change_password'),

    path('',include('citas.urls')),   
#     #=============== URL CON VISTAS BASADAS EN CLASES Y FUNCIONES==============#
    path('lista_paciente/', login_required(ListadoPaciente.as_view()), name ='listar_paciente'),
    path('crear_paciente/', login_required(CrearPaciente.as_view()), name = 'crear_paciente'),
    path('editar_paciente/<int:pk>/', login_required(ActualizarPaciente.as_view()), name = 'editar_paciente'),
    path('eliminar_paciente/<id>/', eliminar_paciente, name = 'eliminar_paciente'),


    path('lista_cita/',login_required(ListadoCita.as_view()), name ='listar_cita'),
    path('crear_cita/',login_required(CrearCita.as_view()), name = 'crear_cita'),
    path('editar_cita/<int:pk>/',login_required(ActualizarCita.as_view()), name = 'editar_cita'),
    path('eliminar_cita/<id>/',eliminar_cita, name = 'eliminar_cita'),
    
    
    path('lista_doctor/',login_required(ListadoDoctor.as_view()), name ='listar_doctor'),
    path('crear_doctor/',login_required(CrearDoctor.as_view()), name = 'crear_doctor'),
    path('editar_doctor/<int:pk>/',login_required(ActualizarDoctor.as_view()), name = 'editar_doctor'),
    path('eliminar_doctor/<id>/',eliminar_doctor, name = 'eliminar_doctor'),
    
    
    path('lista_tratamiento/',login_required(ListadoTratamiento.as_view()), name ='listar_tratamiento'),
    path('crear_tratamiento/',login_required(CrearTratamiento.as_view()), name = 'crear_tratamiento'),
    path('editar_tratamiento/<int:pk>/',login_required(ActualizarTratamiento.as_view()), name = 'editar_tratamiento'),
    path('eliminar_tratamiento/<id>/',eliminar_tratamiento , name = 'eliminar_tratamiento'),
    
    
    path('lista_reporte/',login_required(ListadoReporte.as_view()), name ='listar_reporte'),
    path('crear_reporte/',login_required(CrearReporte.as_view()), name = 'crear_reporte'),
    path('editar_reporte/<int:pk>/',login_required(ActualizarReporte.as_view()), name = 'editar_reporte'),
    path('eliminar_reporte/<id>/',eliminar_reporte, name = 'eliminar_reporte'),
 ] 
handler404 = Error404View.as_view()
handler500 = Error505View.as_error_view()

admin.site.site_header = 'CONSULTORIO ODONTOLOGICO '
