from django.shortcuts import get_object_or_404, render
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from django.contrib.auth import authenticate, login, logout
from  CONSULTORIO.settings import base
from django.db.models import query
from django.http import response
from django.http.response import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, request
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.template.loader import render_to_string
from django.views.generic import *
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from django.contrib import messages
from citas.forms import * 
from citas.models import *

def login_view(request):
    mensaje = None
    if request.user.is_authenticated:
        return HttpResponseRedirect('inicio')
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
                        messages.success(request,"Bienvenido al consultorio odontologico")
                        return HttpResponseRedirect('/inicio/')
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
    messages.success(request, 'Saliste existosamente')
    return redirect('/login/')

def inicio_view(request):
    citas = Paciente.objects.all()
    ctx = {'citas': citas}
    return render(request,'login/vista_principal.html',ctx)

##------------METODO REGISTRAR USUARIO------------
class  MixinFormInvalid:
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errers, status=400)
        else:
            return response

class ResetPasswordView(FormView):
    form_class = ResetPasswordForm
    template_name = 'registration/resetpwd.html'
    success_url = reverse_lazy()

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def send_email_reset_pwd(self, user):
        data = {}
        try:
            URL = base.DOMAIN if not base.DEBUG else self.request.META['HTTP_HOST']
            user.token = uuid.uuid4()
            user.save()

            mailServer = smtplib.SMTP(base.EMAIL_HOST, base.EMAIL_PORT)
            mailServer.starttls()
            mailServer.login(base.EMAIL_HOST_USER, base.EMAIL_HOST_PASSWORD)

            email_to = user.email
            mensaje = MIMEMultipart()
            mensaje['From'] = base.EMAIL_HOST_USER
            mensaje['To'] = email_to
            mensaje['Subject'] = 'Reseteo de contraseña'

            content = render_to_string('login/send_email.html', {
                'user': user,
                'link_resetpwd': 'http://{}/login/change/password/{}/'.format(URL, str(user.token)),
                'link_home': 'http://{}'.format(URL)
            })
            mensaje.attach(MIMEText(content, 'html'))

            mailServer.sendmail(base.EMAIL_HOST_USER,
                                email_to,
                                mensaje.as_string())
        except Exception as e:
            data['error'] = str(e)
        return data

   
    def post(self,request, *args, **kwargs):
        data = {}
        try:
            form = ResetPasswordForm(request.POST)   
            if  form.is_valid():
                user = form.get_user()
                data = self.send_email_reset_pwd(user)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, self=False)
        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reseteo de contraseña'
        return context

class ChangePasswordView(FormView):
    form_class = ChangePasswordForm
    template_name = 'registration/changepwd.html'
    success_url = reverse_lazy()

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        token = self.kwargs['token']
        if User.objects.filter(token=token).exists():
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect('/')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                user = User.objects.get(token=self.kwargs['token'])
                user.set_password(request.POST['password'])
                user.token = uuid.uuid4()
                user.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reseteo de Contraseña'
        context['login_url'] = settings.LOGIN_URL
        return context

def registro(request):
    data = {
        'form' : CustomUserCreationForm()
    }
    if request.method == 'POST':
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            usuario = authenticate(username=username,password=password)
            login(request, usuario)
            messages.success(request, "Te has registrado correctamente")
            return redirect('/inicio/')
        data["form"] = form

    return render(request, 'login/registrar.html', data)

# #========================== VISTAS BASADOS EN CLASES Y FUNCIONES =======================#   
class CrearPaciente(SuccessMessageMixin, MixinFormInvalid, CreateView):
    model = Paciente
    template_name='paciente/crear_paciente.html'
    form_class = PacienteForm
    success_url = reverse_lazy('listar_paciente')
    success_message = "creado correctamente!"

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
            pacientes = Paciente.objects.filter(Q(cedula__icontains=query)| Q(nombre__contains=query)
            | Q(apellido__contains=query)| Q(correo__contains=query)|Q(fecha__contains=query))
        elif query == None:
            pacientes =Paciente.objects.all()
        else:
            pacientes =Paciente.objects.none()
        return pacientes

class ActualizarPaciente(SuccessMessageMixin, MixinFormInvalid, UpdateView):
    model = Paciente
    template_name = 'paciente/editar_paciente.html'
    form_class = PacienteForm
    success_url = reverse_lazy('listar_paciente')
    success_message = 'actualizado correctamente!'

def eliminar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    paciente.delete()
    messages.success(request, "eliminado correctamente!")
    return redirect(to="listar_paciente")
        
#========================== VISTAS BASADOS EN CLASES  Y FUNCIONES =======================#
class CrearCita(SuccessMessageMixin,CreateView):
    model = Cita
    template_name='cita/crear_cita.html'
    form_class = CitaForm
    success_url = reverse_lazy('listar_cita')
    success_message = "Creada correctamente!"

class ListadoCita(ListView):
    model = Cita
    template_name= 'cita/listar_cita.html'
    form_class = CitaForm
    queryset = Doctor.objects.all()
    paginate_by = 6
    context_object_name = 'citas'

    def get_queryset(self):
        query = self.request.GET.get('q')
        #print(query)
        citas=None
        if query != None:
            citas = Cita.objects.filter(Q(paciente__nombre__icontains=query)| Q(doctor__nombre__contains=query)
            | Q(paciente__apellido__contains=query)| Q(doctor__nombre__contains=query)| Q(tratamiento__nombre__contains=query))
        elif query == None:
            citas =Cita.objects.all()
        else:
            citas =Cita.objects.none()
        return citas
   
class ActualizarCita(SuccessMessageMixin,UpdateView):
    model = Cita
    template_name = 'cita/editar_cita.html'
    form_class = CitaForm
    success_url = reverse_lazy('listar_cita')
    success_message = "Actualizado!"
     
def eliminar_cita(request, id):
    cita = get_object_or_404(Cita, id=id)
    cita.delete()
    messages.success(request, "Eliminado correctamente!")
    return redirect(to="listar_cita")

#========================== VISTAS BASADOS EN CLASES Y FUNCIONES =======================#
class CrearDoctor(SuccessMessageMixin, MixinFormInvalid, CreateView):
    model = Doctor
    template_name = 'doctor/crear_doctor.html'
    form_class = DoctorForm
    success_url = reverse_lazy('listar_doctor')
    success_message = "Creada correctamente!"

class ListadoDoctor(ListView):
    model = Doctor
    template_name = 'doctor/listar_doctor.html'
    form_class = DoctorForm
    queryset = Doctor.objects.all()
    paginate_by = 3
    context_object_name = 'doctores'  

    def get_queryset(self):
        query = self.request.GET.get('q')
        # print(query)
        doctores=None

        if query != None:
            doctores = Doctor.objects.filter(Q(cedula__icontains=query)  | Q(nombre__contains=query) 
            | Q(apellido__contains=query) | Q(correo__contains=query))
        elif query == None:
            doctores=Doctor.objects.all()
        else:
            doctores=Doctor.objects.none()

        return doctores 

class ActualizarDoctor(SuccessMessageMixin, MixinFormInvalid, UpdateView):
    model = Doctor
    template_name = 'doctor/editar_doctor.html'
    form_class = DoctorForm
    success_url = reverse_lazy('listar_doctor')
    success_message = "Actualizado correctamente!"

def eliminar_doctor(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    doctor.delete()
    messages.success(request, "Eliminado correctamente!")
    return redirect(to="listar_doctor")
#========================== VISTAS BASADOS EN CLASES y FUNCIONES =======================#
class CrearTratamiento(SuccessMessageMixin,MixinFormInvalid,CreateView):
    model = Tratamiento
    template_name = 'tratamiento/crear_tratamiento.html'
    form_class = TratamientoForm
    success_url = reverse_lazy('listar_tratamiento')
    success_message = "creada correctamente!"

class ListadoTratamiento(ListView):
    template_name = 'tratamiento/listar_tratamiento.html'
    queryset = Tratamiento.objects.all()
    paginate_by = 5
    context_object_name = 'tratamientos'  

    def get_queryset(self):
        query = self.request.GET.get('q')
        print(query)
        tratamientos=None
        if query != None:
            tratamientos = Tratamiento.objects.filter(Q(nombre__icontains=query) | Q(descripcion__contains=query))
        elif query == None:
            tratamientos=Tratamiento.objects.all()
        else:
            tratamientos=Tratamiento.objects.none()

        return tratamientos 

class ActualizarTratamiento(SuccessMessageMixin,MixinFormInvalid,UpdateView):
    model = Tratamiento
    template_name = 'tratamiento/editar_tratamiento.html'
    form_class = TratamientoForm
    success_url = reverse_lazy('listar_tratamiento')
    success_message = "actualizado correctamente !"
   
def eliminar_tratamiento(request, id):
    tratamiento = get_object_or_404(Tratamiento, id=id)
    tratamiento.delete()
    messages.success(request, "eliminado correctamente!")
    return redirect(to="listar_tratamiento")
        
class CrearReporte(SuccessMessageMixin,CreateView):
    model = Reporte
    template_name = 'reporte/crear_reporte.html'
    form_class = ReporteForm
    success_url = reverse_lazy('listar_reporte')
    success_message = " creada correctamente!"

class ListadoReporte(ListView):
    template_name = 'reporte/listar_reporte.html'
    queryset = Reporte.objects.all()
    paginate_by = 5
    context_object_name = 'reportes'  

    def get_queryset(self):
        query = self.request.GET.get('q')
        print(query)
        reportes=None
        if query != None:
            reportes = Reporte.objects.filter(Q(paciente__nombre__icontains=query) | Q(observacion__contains=query))
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
    success_message = " actualizado correctamente!"

def eliminar_reporte(request, id):
    reporte = get_object_or_404(Reporte, id=id)
    reporte.delete()
    messages.success(request, "eliminado correctamente!")
    return redirect(to="listar_reporte")
        
class Error404View(TemplateView):
    template_name = "login/error_404.html"

class Error505View(TemplateView):
    template_name = "login/error_500.html"

    @classmethod
    def as_error_view(cls):

        v = cls.as_view()
        def view(request):
            r = v(request)
            r.render()
        return view
