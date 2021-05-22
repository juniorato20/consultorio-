from django import forms
from django.forms import fields, widgets
from citas.models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

# class FormularioLogin(AuthenticationForm):
#     def __init__(self, *args, **kwargs):
#         super(FormularioLogin, self).__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs['class'] = 'form-control'
#         self.fields['username'].widget.attrs['placeholder'] = 'nombre de usuario'
#         self.fields['password'].widget.attrs['class'] = 'form-control'
#         self.fields['password'].widget.attrs['placeholder'] = 'contraseña'
        
        
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = User
        fields = ['username', 'password']


class PerfilForm(UserCreationForm):
    celular = forms.CharField(widget=forms.TextInput())
    direccion = forms.CharField(widget=forms.TextInput())
    cedula = forms.CharField(widget=forms.TextInput())
    foto = forms.ImageField()


class ResetPasswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese un username',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def clean(self):
        cleaned = super().clean()
        if not User.objects.filter(username=cleaned['username']).exists():
            # self._errors['error'] = self._errors.get('error', self.error_class())
            # self._errors['error'].append('El usuario no existe')
            raise forms.ValidationError('El usuario no existe')
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
            # self._errors['error'] = self._errors.get('error', self.error_class())
            # self._errors['error'].append('El usuario no existe')
            raise forms.ValidationError('Las contraseñas deben ser iguales')
        return cleaned


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['cedula','nombre', 'apellido', 'direccion', 'fecha','sexo', 'correo','celular']
        labels = {
           
           'cedula' : 'Cedula',
            'nombre': 'Nombre',
            'apellido':'Apellido',
            'direccion': 'Direccion',
            'fecha' : 'Fecha Nacimento',
            'sexo': 'Sexo',
            'correo': 'Correo',
            'celular': 'Ingrese su celular',
        }
        widgets = {
            'celula' : forms.NumberInput(attrs={'class':'form-control', 'placeholder':'1900754632'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Juan Diego', }),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Torres Reyes', }),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zumbi '}),
            'fecha' : forms.DateInput(attrs={'type': 'date'}, format="%Y-%m-%d"),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@gmail.com', }),
            
            'celular': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0989765432', 'maxlength': '9999999999'})
                   }


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['cedula','nombre', 'apellido', 'especialidad',
                  'sexo', 'direccion', 'celular']
        labels = {
            'cedula' : 'Cedula',        
            'nombre': 'Ingrese su nombre',
            'apellido': 'Ingrese su apellido',
            'especialidad': 'Ingrese su especialidad',
            'sexo': 'Sexo',
            'direccion': 'Ingrese su direccion',
            'celular': 'Ingrese su celular'
        }
        widgets = {
            'cedula' : forms.NumberInput(attrs={ 'class':'form-control', 'placeholder':'1900876534'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Julia Maria', }),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cabrera Cordero'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Yantzaza'}),
            'celular': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0987908790', 'maxlength': '9999999999'})
                   }


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['paciente','doctor', 'fecha', 'hora', 'tratamiento']
        labels = {
            'fecha': 'Ingrese fecha',
            'hora': 'Ingrese hora',
        
        }
        widgets = {
            'fecha' : forms.DateInput(attrs={'type': 'date'}, format="%Y-%m-%d"),
            
                   }
    
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



