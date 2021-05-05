from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import *
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import * 
from .models import *


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
    return HttpResponseRedirect('/login/')

@login_required(login_url= '/login/')
def inicio_view(request):
    citas = Paciente.objects.all()
    ctx = {'citas': citas}
    return render(request,'inicio/vista_principal.html',ctx)

def registrar_view(request):
    info = "inicializar"
    if request.method == 'POST':
        form = PerfilForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save()
            perfil = Perfil()
            perfil.usuario = user
            perfil.celular = form.cleaned_data['celular']
            perfil.direccion = form.cleaned_data['direccion']
            perfil.cedula= form.cleaned_data['cedula']
            perfil.foto = form.cleaned_data['foto']
            perfil.save()
            info = "Guardado Satisfactoriamente"
            ctx = {'info':info}
            return render(request, 'login/resgistro_exitoso.html',ctx)
    else:
        form = PerfilForm()
        form.fields['username'].help_text = None
        form.fields['password1'].help_text = None
        form.fields['password2'].help_text = None
    ctx ={'form':form, 'info': info}
    return render(request, 'login/registro_usuario.html',ctx)

#========================== VISTAS BASADOS EN CLASES PACIENTE =======================#   
class CrearPaciente(SuccessMessageMixin,CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name='paciente/crear_paciente.html'
    success_url = reverse_lazy('listar_paciente')
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return  "Se ha Creado Correctamente"

class ListadoPaciente(ListView):
    template_name= 'paciente/listar_paciente.html'
    queryset = Paciente.objects.all().order_by('-id')
    paginate_by = 5
    context_object_name = 'pacientes'
    
class ActualizarPaciente(SuccessMessageMixin,UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'paciente/editar_paciente.html'
    success_url = reverse_lazy('listar_paciente')
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return  "Se ha Actualizado Correctamente"

class EliminarPaciente(DeleteView):
    model = Paciente
    template_name = 'paciente/paciente_confirm_delete.html'
    def post(self, request, pk, *args, **kwargs):
        object = Paciente.objects.get(id=pk)
        object.estado = False
        object.save()
        return redirect('listar_paciente')

#========================== VISTAS BASADOS EN CLASES CITA =======================#
class CrearCita(SuccessMessageMixin,CreateView):
    model = Cita
    form_class = CitaForm
    template_name = 'cita/crear_cita.html'
    success_url = reverse_lazy('listar_cita')
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return  "Se ha Creado Correctamente"

class ListadoCita(ListView):
    model = Cita 
    template_name= 'cita/listar_cita.html'
    queryset = Cita.objects.filter(estado=True)
    context_object_name = 'citas'

class ActualizarCita(SuccessMessageMixin,UpdateView):
    model = Cita
    form_class = CitaForm
    template_name = 'cita/editar_cita.html'
    success_url = reverse_lazy('listar_cita')
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return  "Se ha Actualizado Correctamente"

class EliminarCita(DeleteView):
    model = Cita
    template_name = 'cita/cita_confirm_delete.html'
    def post(self, request, pk, *args, **kwargs):
        object = Cita.objects.get(id=pk)
        object.estado = False
        object.save()
        return redirect('listar_cita')

#========================== VISTAS BASADOS EN CLASES DOCTOR =======================#
class CrearDoctor(SuccessMessageMixin,CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'doctor/crear_doctor.html'
    success_url = reverse_lazy('listar_doctor')
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return  "Se ha Creado Correctamente"

class ListadoDoctor(ListView):
    template_name = 'doctor/listar_doctor.html'
    queryset = Doctor.objects.all().order_by('-id')
    paginate_by = 5
    context_object_name = 'doctores'

class ActualizarDoctor(SuccessMessageMixin,UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'doctor/editar_doctor.html'
    success_url = reverse_lazy('listar_doctor')
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return  "Se ha Actualizado Correctamente"

class EliminarDoctor(SuccessMessageMixin,DeleteView):
    model = Doctor
    template_name = 'doctor/doctor_confirm_delete.html'
    success_url = reverse_lazy('listar_doctor')
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return  "Se ha Elininado Correctamente"
    
#========================== VISTAS BASADOS EN CLASES REPORTE =======================#
class CrearReporte(SuccessMessageMixin,CreateView):
    model = Reporte
    form_class = ReporteForm
    template_name = 'reporte/crear_reporte.html'
    success_url = reverse_lazy('listar_reporte')
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return  "Se ha Creado Correctamente"

class ListadoReporte(ListView):
    template_name= 'reporte/listar_reporte.html'
    queryset = Reporte.objects.all().order_by('-id')
    paginate_by = 1
    context_object_name = 'reportes'

class ActualizarReporte(SuccessMessageMixin,UpdateView):
    model = Reporte
    form_class = ReporteForm
    template_name = 'reporte/editar_reporte.html'
    success_url = reverse_lazy('listar_reporte')
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return  "Se ha Actualizado Correctamente"

class EliminarReporte(SuccessMessageMixin, DeleteView):
    model = Reporte
    success_url = reverse_lazy('listar_reporte')
    template_name = 'reporte/reporte_confirm_delete.html'
    success_message = 'Reporte %(nombre)s Eliminar'
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return  "Se ha Elininado Correctamente"
