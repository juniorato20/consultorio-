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
        print('Conectado..')

        email_to = 'jhunniorguerrero@gmail.com'
        # Construimos el mensaje simple
        mensaje =  MIMEMultipart()
        mensaje['From'] = base.EMAIL_HOST_USER
        mensaje['To'] = email_to
        mensaje['Subject'] = "Tienes un correo"

        content = render_to_string('send_email.html', {'user': User.objects.get(pk=1)})
        mensaje.attach(MIMEText(content, 'html'))

        mailServer.sendmail(base.EMAIL_HOST_USER,
                            email_to,
                            mensaje.as_string())

        print('Correo enviado correctamente')
    except Exception as e:
        print(e)


send_email()