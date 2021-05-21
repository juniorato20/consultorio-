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
from django.contrib import admin
from django.urls import path,include
from citas.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
#=============== URL CON VISTAS BASADAS EN CLASES LOGIN  ==============#
    # path('login/', Login.as_view(), name='login'),
    # path('logout/', LogoutUsuario.as_view(), name='logout'),

    path('', login_view, name="vista_login"),
    path('login/', login_view, name="vista_login"),
    path('inicio/', inicio_view, name="vista_inicio"),
    path('logout/', logout_view, name="vista_logout"),  
    path('',include('citas.urls')),
    
    #=============== URL CON VISTAS BASADAS EN CLASES PACIENTE  ==============#
    path('lista_paciente/', login_required(ListadoPaciente.as_view()), name ='listar_paciente'),
    path('crear_paciente/', login_required(CrearPaciente.as_view()), name = 'crear_paciente'),
    path('editar_paciente/<int:pk>/', login_required(ActualizarPaciente.as_view()), name = 'editar_paciente'),
    path('eliminar_paciente/<int:pk>/', login_required(EliminarPaciente.as_view()), name = 'eliminar_paciente'),

    # #=============== URL CON VISTAS BASADAS EN CLASES CITAS  ==============#
    path('lista_cita/',login_required(ListadoCita.as_view()), name ='listar_cita'),
    path('crear_cita/',login_required(CrearCita.as_view()), name = 'crear_cita'),
    path('editar_cita/<int:pk>/',login_required(ActualizarCita.as_view()), name = 'editar_cita'),
    path('eliminar_cita/<int:pk>/',login_required(EliminarCita.as_view()), name = 'eliminar_cita'),

     # #=============== URL CON VISTAS BASADAS EN CLASES CITAS  ==============#
    path('lista_reporte/',login_required(ListadoReporte.as_view()), name ='listar_reporte'),
    path('crear_reporte/',login_required(CrearReporte.as_view()), name = 'crear_reporte'),
    path('editar_reporte/<int:pk>/',login_required(ActualizarReporte.as_view()), name = 'editar_reporte'),
    path('eliminar_reporte/<int:pk>/',login_required(EliminarReporte.as_view()), name = 'eliminar_reporte'),

     # #=============== URL CON VISTAS BASADAS EN CLASES CITAS  ==============#
    path('lista_doctor/',login_required(ListadoDoctor.as_view()), name ='listar_doctor'),
    path('crear_doctor/',login_required(CrearDoctor.as_view()), name = 'crear_doctor'),
    path('editar_doctor/<int:pk>/',login_required(ActualizarDoctor.as_view()), name = 'editar_doctor'),
    path('eliminar_doctor/<int:pk>/',login_required(EliminarDoctor.as_view()), name = 'eliminar_doctor'),
]
# admin.site.site_header = 'CONSULTORIO ODONTOLOGICO '
