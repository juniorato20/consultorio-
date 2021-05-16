from django.db.models import query
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, request
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import *
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import * 
from .models import *

# def busqueda(self):
#     q = request.GET.get('q','')
#     query = (Q(nombre_icontains=q)| Q(apellido_icontains=q))
#     pacientes = Paciente.objects.filter(query)
#     return render(request, 'paciente/paciente_busqueda.html', {'pacientes': pacientes}) 

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/lista_paciente/')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                usuario = authenticate(username=username,password=password)
                if usuario is not None and usuario.is_active:
                    login(request,usuario)
                    messages.success(request,"BIENVENIDO AL CONSULTORIO ODONTOLOGICO")
                    return HttpResponseRedirect('/lista_paciente/')
        form = LoginForm()
        ctx = {'form': form}
        return render(request, 'login/login.html', ctx)

def logout_view(request):
    logout(request)
    messages.success(request, 'Te has desconectado con exito.')
    return HttpResponseRedirect('/login/')

@login_required(login_url= '/login/')
def inicio_view(request):
    citas = Paciente.objects.all()
    ctx = {'citas': citas}
    return render(request,'inicio/vista_principal.html',ctx)

#========================== VISTAS BASADOS EN CLASES PACIENTE =======================#   
class CrearPaciente(SuccessMessageMixin,CreateView):
    model = Paciente
    template_name='paciente/crear_paciente.html'
    form_class = PacienteForm
    success_url = reverse_lazy('listar_paciente')
    success_message = "%(nombre)s creado correctamente"

class ListadoPaciente(ListView): 
    model = Paciente
    form_class = PacienteForm
    template_name= 'paciente/listar_paciente.html'
    queryset = Paciente.objects.all()
    paginate_by = 3
    context_object_name = 'pacientes'

    # def get_queryset(self):
    #     query = self.request.GET.get('q')
    #     if query:
    #         object_list = self.model.objects.filter(nombre__icontains=query)
    #     else:
    #         object_list = self.model.objects.none()
    #     return object_list

class ActualizarPaciente(SuccessMessageMixin,UpdateView):
    model = Paciente
    template_name = 'paciente/editar_paciente.html'
    form_class = PacienteForm
    success_url = reverse_lazy('listar_paciente')
    success_message = "Modificado Correctamente"

class EliminarPaciente(DeleteView):
    model = Paciente
    template_name = 'paciente/paciente_confirm_delete.html'
    success_url = reverse_lazy('listar_paciente')
    success_message = "Elimado Correctamente"
        
#========================== VISTAS BASADOS EN CLASES CITA =======================#
class CrearCita(SuccessMessageMixin,CreateView):
    model = Cita
    template_name='cita/crear_cita.html'
    form_class = CitaForm
    success_url = reverse_lazy('listar_cita')
    success_message = "%(paciente)s creado correctamente"

class ListadoCita(ListView):
    template_name= 'cita/listar_cita.html'
    queryset = Cita.objects.all()
    paginate_by = 3
    context_object_name = 'citas'

class ActualizarCita(SuccessMessageMixin,UpdateView):
    model = Cita
    template_name = 'cita/editar_cita.html'
    form_class = CitaForm
    success_url = reverse_lazy('listar_cita')
    success_message = "Modificado Correctamente"
 
class EliminarCita(DeleteView):
    model = Cita
    template_name = 'cita/cita_confirm_delete.html'
    success_url = reverse_lazy('listar_cita')
    success_message = "Elimado Correctamente"
    
#========================== VISTAS BASADOS EN CLASES DOCTOR =======================#
class CrearDoctor(SuccessMessageMixin,CreateView):
    model = Doctor
    template_name = 'doctor/crear_doctor.html'
    form_class = DoctorForm
    success_url = reverse_lazy('listar_doctor')
    success_message = "%(nombre)s creado correctamente"

class ListadoDoctor(ListView):
    template_name = 'doctor/listar_doctor.html'
    queryset = Doctor.objects.all()
    paginate_by = 3
    context_object_name = 'doctores'   

class ActualizarDoctor(SuccessMessageMixin,UpdateView):
    model = Doctor
    template_name = 'doctor/editar_doctor.html'
    form_class = DoctorForm
    success_url = reverse_lazy('listar_doctor')
    success_message = "Modificado Correctamente"
   
class EliminarDoctor(DeleteView):
    model = Doctor
    template_name = 'doctor/doctor_confirm_delete.html'
    success_url = reverse_lazy('listar_doctor')
    success_message = "Elimado Correctamente"

#========================== VISTAS BASADOS EN CLASES REPORTE =======================#
class CrearReporte(SuccessMessageMixin,CreateView):
    model = Reporte
    template_name = 'reporte/crear_reporte.html'
    form_class = ReporteForm
    success_url = reverse_lazy('listar_reporte')
    success_message = "%(paciente)s creado correctamente"

class ListadoReporte(ListView):
    template_name= 'reporte/listar_reporte.html'
    queryset = Reporte.objects.all()
    paginate_by = 3
    context_object_name = 'reportes'

class ActualizarReporte(SuccessMessageMixin,UpdateView):
    model = Reporte
    template_name = 'reporte/editar_reporte.html'
    form_class = ReporteForm
    success_url = reverse_lazy('listar_reporte')
    success_message = "Modificado Correctamente"

class EliminarReporte(DeleteView):
    model = Reporte
    template_name = 'reporte/reporte_confirm_delete.html'
    success_url = reverse_lazy('listar_reporte')
    success_message = "Elimado Correctamente"
