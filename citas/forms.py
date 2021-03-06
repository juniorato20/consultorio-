from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from django.forms import fields, widgets
from citas.models import *
from django.contrib.auth import authenticate
from django.contrib.auth.forms import  UserCreationForm, AuthenticationForm
from django.contrib.auth.models import  User
from django.forms import ValidationError
        
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = User
        fields = ['username', 'password']
        
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','last_name','email','password1','password2']
        labels = {
            'username' : 'Nombre',
            'last_name':'Apellido',
            'email' : 'Correo',
            'password1' : 'Contraseña',
            'password2' : 'Confirmar contraseña',
        }
        widgets = {
            'username' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': '' }),
            'last_name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': '' }),
            'email' : forms.EmailInput(attrs={'class' : 'form-control', 'placeholder': ''}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':''}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ''}),
        }
       
class ResetPasswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese un username',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def clean(self):
        cleaned = super().clean()
        if not User.objects.filter(username=cleaned['username']).exists():
            self._errors['error'] = self._errors.get('error', self.error_class())
            self._errors['error'].append('El usuario no existe')
           # raise forms.ValidationError('El usuario no existe')
        return cleaned

    def get_user(self):
        username = self.cleaned_data.get('username')
        return User.objects.get(username=username)

class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese un password',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    confirmPassword = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repita el password',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def clean(self):
        cleaned = super().clean()
        password = cleaned['password']
        confirmPassword = cleaned['confirmPassword']
        if password != confirmPassword:
            self._errors['error'] = self._errors.get('error', self.error_class())
            self._errors['error'].append('El usuario no existe')
            #raise forms.ValidationError('Las contraseñas deben ser iguales')
        return cleaned

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['cedula','nombre', 'apellido', 'direccion', 'fecha','sexo','observacion', 'correo','celular']
        labels = {
           'cedula' : 'Cedula de Identidad',
            'nombre': 'Nombres Completos',
            'apellido':'Apellidos Completos',
            'direccion': 'Direccion',
            'fecha' : 'Fecha Nacimento',
            'sexo': 'Sexo', 
            'observacion': 'Observacion',
            'correo': 'Correo',
            'celular': 'Celular',
        }
        widgets = {
            'cedula' : forms.NumberInput(attrs={'class':'form-control', 'placeholder':''}),
            'nombre': forms.TextInput(attrs={ 'class' : 'form-control', 'placeholder': '', }),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '', }),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}),
            'fecha' :  forms.DateInput(attrs={'type': 'date','class': 'form-control'}, format="%Y-%m-%d"),
            'sexo' :  forms.Select(attrs={'class': 'form-control'}),
            'observacion' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder':''}) ,
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '', }),
            'celular': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ''})
            }

    def clean(self):
        try:
            sc = Paciente.objects.get(
                cedula= self.cleaned_data['cedula'].upper()
                )
            if not self.instance.pk:
                print('Regristro ya existe')
                raise forms.ValidationError("Ya existe paciente con este numero de cedula ")
            elif self.instance.pk!= sc.pk:
                print('Cambio no permitido')
                raise forms.ValidationError("Cambio no permitido")
        except Paciente.DoesNotExist: 
            pass
        return self.cleaned_data
        
    
    # def clean_email(self, *args, **kwargs):
    #     email = self.cleaned_data.get("email")
    #     if not email.endwith("edu"):
    #         raise forms.ValidationError("")
    #     return email

#    """  def clean_num(self):
#         numeros = self.cleaned_data
#         cedula = numeros.get('cedula')
#         if len(cedula) < 10 or len(cedula) >10:
#             raise forms.ValidationError('Debe ser de 10 Digitos') """

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['cedula','nombre', 'apellido', 'especialidad','sexo', 'direccion','correo','celular']
        labels = {
            'cedula' : 'Cedula de Identidad',        
            'nombre': 'Nombres Completos',
            'apellido': 'Apellidos Completos ',
            'especialidad': 'Especialidad',
            'sexo': 'Sexo',
            'direccion': 'Direccion',
            'correo' : 'Correo ',
            'celular': 'Celular'
        }
        widgets = {
            'cedula' : forms.NumberInput(attrs={ 'class':'form-control', 'placeholder':''}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'especialidad' :  forms.Select(attrs={'class': 'form-control'}),
            'sexo' :  forms.Select(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'correo' : forms.EmailInput(attrs={'class' : 'form-control', 'placeholder': ''}),
            'celular': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '', 'maxlength': '9999999999'})
                   }
            
    def clean_cedula(self):
        try:
            sc = Doctor.objects.get(
                cedula= self.cleaned_data['cedula'].upper()
                )
            if not self.instance.pk:
                raise forms.ValidationError("La cedula ya esta en uso")
            elif self.instance.pk!= sc.pk:
                raise forms.ValidationError("Cambio no permitido")
        except Doctor.DoesNotExist: 
            pass
        return self.cleaned_data
    
    def clean_(self):
        try:
            sc = Doctor.objects.get(
                correo= self.cleaned_data['correo'].upper()
                )
            if not self.instance.pk:
                raise forms.ValidationError("El correo ya esta en uso ")
            elif self.instance.pk!= sc.pk:
                raise forms.ValidationError("Cambio no permitido")
        except Doctor.DoesNotExist: 
            pass
        return self.cleaned_data

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['paciente','doctor', 'fecha', 'hora', 'tratamiento']
        labels = {
            'fecha': 'Ingrese fecha',
            'hora': 'Ingrese hora',
        }
        widgets = {
            'paciente' :  forms.Select(attrs={'class': 'form-control'}),
            'doctor' :  forms.Select(attrs={'class': 'form-control'}),
            'fecha' : forms.DateInput(attrs={'type': 'date','class': 'form-control'}, format="%Y-%m-%d"),
            'hora' :  forms.Select(attrs={'class': 'form-control'}),
            'tratamiento' :  forms.Select(attrs={'class': 'form-control'}),
                }
    
    def clean(self):
        fecha = self.cleaned_data.get('fecha')
        if Cita.objects.filter(fecha=fecha).exists():
            raise forms.ValidationError("Campo ocupado ")
  
class TratamientoForm(forms.ModelForm):
    class Meta:
        model = Tratamiento
        fields = ['nombre', 'descripcion', 'precio']
        labels = {
            'nombre' : 'Nombre',
            'descripcion': 'Descripcion',
            'precio' : 'Precio'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '', }),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'precio': forms.NumberInput(attrs={'class':'form-control'}),
            }
    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"]
        existe = Tratamiento.objects.filter(nombre__iexact=nombre).exists()
        if existe:
            raise ValidationError("Este nombre ya existe")
        return nombre