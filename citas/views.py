from django.db.models import query
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
from .forms import * 
from .models import *



# class Login(FormView):
#     form_class = FormularioLogin
#     template_name = 'login/login.html'
#     success_url = reverse_lazy('lista_paciente')

#     @method_decorator(csrf_protect)
#     @method_decorator(never_cache)
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated():
#             return HttpResponseRedirect(self.get_success_url())
#         else:
#             return super(Login,self).dispatch(request, *args, **kwargs)

#     def form_valid(self,form):
#         login(self.request,form.get_user())
#         return super(Login,self).form_valid(form)

# class LogoutUsuario(RedirectView):
#     pattern_name = "login" 

#     def get(self,request, *args, **kwargs):
#         logout(request)
#         return super(login, self).get(request, *args, **kwargs)    

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('')
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

class EliminarPaciente(DeleteView):
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
    form_class = PacienteForm
    queryset = Cita.objects.all()
    paginate_by = 3
    context_object_name = 'citas'

    def get_queryset(self):
        query = self.request.GET.get('q')
        print(query)
        citas=None
        if query != None:
            citas = Cita.objects.filter(fecha__icontains=query)
        elif query == None:
            citas=Cita.objects.all()
        else:
            citas=Cita.objects.none()

        return citas

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
    template_name = 'doctor/listar_doctor.html'
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

    # def delete(self, request, *args, **kwargs):
    #     obj = self.get_object()
    #     messages.success(self.request, self.success_message % obj.__dict__)
    #     return super(EliminarDoctor, self).delete(request, *args, **kwargs)

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

    def get_queryset(self):
        query = self.request.GET.get('q')
        print(query)
        reportes=None
        if query != None:
            reportes = Reporte.objects.filter(fecha__icontains=query)
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
    success_message = "Modificado Correctamente"

class EliminarReporte(SuccessMessageMixin,DeleteView):
    model = Reporte
    template_name = 'reporte/reporte_confirm_delete.html'
    success_url = reverse_lazy('listar_reporte')
    success_message = "Elimado Correctamente"