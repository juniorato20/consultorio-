from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from CONSULTORIO.wsgi import *
import smtplib
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from  CONSULTORIO.settings import base

def send_email():
    try:
        mailServer = smtplib.SMTP(base.EMAIL_HOST, base.EMAIL_PORT)
        print(mailServer.ehlo())
        mailServer.starttls()
        print(mailServer.ehlo())
        mailServer.login(base.EMAIL_HOST_USER, base.EMAIL_HOST_PASSWORD)
        print('Conectado......')

        email_to = 'dmundotorres@gmail.com'
        # Construimos el mensaje simple
        mensaje =  MIMEText('Consultorio odontologico')
        mensaje['From'] = base.EMAIL_HOST_USER
        mensaje['To'] = email_to
        mensaje['Subject'] = "Tienes un correo"

        mailServer.sendmail(base.EMAIL_HOST_USER,
                            email_to,
                            mensaje.as_string())

        print('Correo enviado correctamente')
    except Exception as e:
        print(e)

send_email()