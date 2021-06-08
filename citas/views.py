from django.db.models import query
from django.http.response import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, request
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import *
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import *
from django.contrib import messages
from citas.forms import * 
from citas.models import *

def login_view(request):
    mensaje = None
    if request.user.is_authenticated:
        return HttpResponseRedirect('listar_paciente')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                usuario = authenticate(username=username,password=password)
                if usuario is not None:
                    if usuario.is_active:
                        login(request,usuario)
                        messages.success(request,"BIENVENIDO AL CONSULTORIO ODONTOLOGICO")
                        return HttpResponseRedirect('/lista_paciente/')
                    else: 
                        mensaje = "Usuario inactivo"     
                else:
                    mensaje = "Usuario o contraseña invalido"
            else:
                form = LoginForm()
        ctx = {'mensaje': mensaje}
        return render(request, 'login/login.html', ctx)

def logout_view(request):
    logout(request)
    messages.success(request, 'TE HAS DESCONECTADO CON EXISTO')
    return HttpResponseRedirect('/login/')

@login_required(login_url= '/login/')
def inicio_view(request):
    citas = Paciente.objects.all()
    ctx = {'citas': citas}
    return render(request,'inicio/vista_principal.html',ctx)

##------------METODO REGISTRAR USUARIO------------
def registrar_view(request):
    info = "inicializar"
    if request.method == 'POST':
        form = PerfilForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save()
            # message = "Image uploaded succesfully!"
            # print(user +"Se guardo el usuario")
            perfil = Perfil()
            perfil.usuario = user
            perfil.celular = form.cleaned_data['celular']
            perfil.direccion = form.cleaned_data['direccion']
            perfil.cedula= form.cleaned_data['cedula']
            perfil.correo= form.cleaned_data['correo']
            perfil.foto= form.cleaned_data['foto']

            perfil.save()
            print(perfil+"Se guardo el perfil")
            info = "Guardado Satisfactoriamente"
            ctx = {'info':info}
            return render(request,'login/resgistro_exitoso.html',ctx)
        else:
            print(form)
    else:
        form = PerfilForm()
        form.fields['username'].help_text = None
        form.fields['password1'].help_text = None
        form.fields['password2'].help_text = None
    ctx ={'form':form, 'info': info}
    return render(request, 'login/registro_usuario.html',ctx)

# #========================== VISTAS BASADOS EN CLASES PACIENTE =======================#   
class CrearPaciente(SuccessMessageMixin,CreateView):
    model = Paciente
    template_name='paciente/crear_paciente.html'
    form_class = PacienteForm
    success_url = reverse_lazy('listar_paciente')
    success_message = "%(nombre)s %(apellido)s se ha creado correctamente"

class ListadoPaciente(ListView): 
    model = Paciente
    template_name= 'paciente/listar_paciente.html'
    form_class = PacienteForm
    queryset = Paciente.objects.all()
    paginate_by = 3
    context_object_name = 'pacientes'

    def get_queryset(self):
        query = self.request.GET.get('q')
        print(query)
        pacientes=None
        if query != None:
            pacientes = Paciente.objects.filter(nombre__icontains=query)
        elif query == None:
            pacientes =Paciente.objects.all()
        else:
            pacientes =Paciente.objects.none()

        return pacientes

class ActualizarPaciente(SuccessMessageMixin,UpdateView):
    model = Paciente
    template_name = 'paciente/editar_paciente.html'
    form_class = PacienteForm
    success_url = reverse_lazy('listar_paciente')
    success_message = "%(nombre)s %(apellido)s se ha actualizado correctamente"

class EliminarPaciente(SuccessMessageMixin,DeleteView):
    model = Paciente
    template_name = 'paciente/paciente_confirm_delete.html'
    success_url = reverse_lazy('listar_paciente')
    success_message = "%(nombre)s %(apellido)s se ha elimado correctamente"
        
#========================== VISTAS BASADOS EN CLASES CITA =======================#
class CrearCita(SuccessMessageMixin,CreateView):
    model = Cita
    template_name='cita/crear_cita.html'
    form_class = CitaForm
    success_url = reverse_lazy('listar_cita')
    success_message = "Cita creada correctamente"

class ListadoCita(ListView):
    model = Cita
    template_name= 'cita/listar_cita.html'
    context_object_name = 'citas'

    def get_queryset(self):
        queryset = self.model.objects.filter(estado = True)
        return queryset
   
class ActualizarCita(SuccessMessageMixin,UpdateView):
    model = Cita
    template_name = 'cita/editar_cita.html'
    form_class = CitaForm
    success_url = reverse_lazy('listar_cita')
    success_message = "Cita actualizada correctamente"
 
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
    success_message = "%(nombre)s %(apellido)s se ha creado correctamente"

class ListadoDoctor(ListView):
    model = Doctor
    template_name = 'doctor/listar_doctor.html'
    form_class = DoctorForm
    queryset = Doctor.objects.all()
    paginate_by = 3
    context_object_name = 'doctores'  

    def get_queryset(self):
        query = self.request.GET.get('q')
        print(query)
        doctores=None
        if query != None:
            doctores = Doctor.objects.filter(nombre__icontains=query)
        elif query == None:
            doctores=Doctor.objects.all()
        else:
            doctores=Doctor.objects.none()

        return doctores 

class ActualizarDoctor(SuccessMessageMixin,UpdateView):
    model = Doctor
    template_name = 'doctor/editar_doctor.html'
    form_class = DoctorForm
    success_url = reverse_lazy('listar_doctor')
    success_message = "%(nombre)s %(apellido)s se actualizo correctamente"
   
class EliminarDoctor(SuccessMessageMixin,DeleteView):
    model = Doctor
    template_name = 'doctor/doctor_confirm_delete.html'
    success_url = reverse_lazy('listar_doctor')
    success_message = "%(nombre)s %(apellido)sElimado Correctamente"

#========================== VISTAS BASADOS EN CLASES TRATAMIENTO=======================#
class CrearTratamiento(SuccessMessageMixin,CreateView):
    model = Tratamiento
    template_name = 'tratamiento/crear_tratamiento.html'
    form_class = TratamientoForm
    success_url = reverse_lazy('listar_tratamiento')
    success_message = "%(nombre)s  se ha creado correctamente"

class ListadoTratamiento(ListView):
    template_name = 'tratamiento/listar_tratamiento.html'
    queryset = Tratamiento.objects.all()
    paginate_by = 3
    context_object_name = 'tratamientos'  

    def get_queryset(self):
        query = self.request.GET.get('q')
        print(query)
        tratamientos=None
        if query != None:
            tratamientos = Tratamiento.objects.filter(nombre__icontains=query)
        elif query == None:
            tratamientos=Tratamiento.objects.all()
        else:
            tratamientos=Tratamiento.objects.none()

        return tratamientos 

class ActualizarTratamiento(SuccessMessageMixin,UpdateView):
    model = Tratamiento
    template_name = 'tratamiento/editar_tratamiento.html'
    form_class = TratamientoForm
    success_url = reverse_lazy('listar_tratamiento')
    success_message = "%(nombre)s  se actualizo correctamente"
   
class EliminarTratamiento(SuccessMessageMixin,DeleteView):
    model = Tratamiento
    template_name = 'tratamiento/tratamiento_confirm_delete.html'
    success_url = reverse_lazy('listar_tratamiento')
    success_message = "%(nombre)s Elimado Correctamente"

class CrearReporte(SuccessMessageMixin,CreateView):
    model = Reporte
    template_name = 'reporte/crear_reporte.html'
    form_class = ReporteForm
    success_url = reverse_lazy('listar_reporte')
    success_message = "  se ha creado correctamente"

class ListadoReporte(ListView):
    template_name = 'reporte/listar_reporte.html'
    queryset = Reporte.objects.all()
    paginate_by = 3
    context_object_name = 'reportes'  

    def get_queryset(self):
        query = self.request.GET.get('q')
        print(query)
        reportes=None
        if query != None:
            reportes = Reporte.objects.filter(paciente__icontains=query)
        elif query == None:
            reportes=Reporte.objects.all()
        else:
            reportes=Reporte.objects.none()

        return reportes

class ActualizarReporte(SuccessMessageMixin,UpdateView):
    model = Reporte
    template_name = 'reporte/editar_reporte.html'
    form_class = ReporteForm
    success_url = reverse_lazy('listar_reporte')
    success_message = " se actualizo correctamente"

class EliminarReporte(SuccessMessageMixin,DeleteView):
    model = Reporte
    template_name = 'reporte/reporte_confirm_delete.html'
    success_url = reverse_lazy('listar_reporte')
    success_message = "Elimado Correctamente"
    









