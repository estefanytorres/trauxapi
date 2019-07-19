from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, WebConsultSerializer
from .models import WebConsult
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.http import JsonResponse


#######################################################################################################################
#                                                   Function catalog                                                  #
#######################################################################################################################
def send_email(title, content, html_content, send_from, send_to):
    if settings.ENV != 'PRD':
        content = '##########################################################################################\n\n' \
                  'environment: ' + settings.ENV + '\n\n' + \
                  'send_from: ' + send_from + '\n\n' + \
                  'send_to: ' + ', '.join(send_to) + '\n\n' + \
                  '##########################################################################################\n\n\n\n' \
                  + content
        html_content = 'environment: %s<br>send_from: %s<br>send_to: %s<br><hr>' % \
                       (settings.ENV, send_from, ', '.join(send_to)) + html_content
        title = '[' + settings.ENV + '] ' + title
        send_from = settings.EMAIL_DEFAULT_SENDER
        send_to = [settings.EMAIL_TEST_RECIPIENT]

    email = EmailMultiAlternatives(title, content, send_from, send_to)
    email.attach_alternative(html_content, "text/html")
    email.send()



#######################################################################################################################
#                                                   REST ViewSets                                                     #
#######################################################################################################################
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class WebConsultViewSet(viewsets.ModelViewSet):
    queryset = WebConsult.objects.all()
    serializer_class = WebConsultSerializer
    http_method_names = ['post']
    permission_classes = [AllowAny]

    link_youtube_instructions = 'https://youtu.be/IW10vAp9Lbw'
    link_download_demo = settings.CORS_ORIGIN_WHITELIST[0] + '/assets/downloads/Setup-TrauxERP.exe'
    link_traux_logo = settings.CORS_ORIGIN_WHITELIST[0] + '/assets/logo.png'

    def create(self, request, *args, **kwargs):
        response = super(WebConsultViewSet, self).create(request, *args, **kwargs)
        serializer = WebConsultSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['type'] == 'D':
                send_email(
                    'Descarga de traux versión DEMO desde la web',
                    'Nombres: %s \n\nEmpresa: %s \n\nCorreo: %s \n\nTelefono: %s \n\n' %
                    (serializer.validated_data['name'], serializer.validated_data['company'],
                     serializer.validated_data['email'], serializer.validated_data['phone']),
                    '<p>Nombres: %s<br>Empresa: %s<br>Correo: %s<br>Telefono: %s</p>' %
                    (serializer.validated_data['name'], serializer.validated_data['company'],
                     serializer.validated_data['email'], serializer.validated_data['phone']),
                    'noreply@trauxerp.com',
                    ['info@trauxerp.com']
                )
                send_email(
                    'Tu trauxerp version DEMO!',
                    'Hola %s! \n\n \n\n ' % (serializer.validated_data['name']) +
                    'Te felicito por iniciar tu camino hacia organizar y mejorar los procesos de negocio de tu '
                    'empresa, de parte de todo el equipo traux te damos las gracias por considerarnos como opción, '
                    'sabemos que hay muchos sistemas en el mercado y que quieres estar seguro que aquel que eligas '
                    'este en sintonía con tus objetivos. Es por eso que nosotros ofrecemos tres meses de prueba con '
                    'nuestro sistema, solo queremos ayudarte a decidir si traux es la opción correcta para tí.'
                    '\n\n \n\n'
                    'Para descargarlo solo tienes que seguir las instrucciones que tenemos para ti en nuestro canal de '
                    '<a href="%s">youtube</a> usando el siguiente link \n\n \n\n %s \n\n \n\n'
                    'Si llegas a tener cualquier duda por favor comunícate con nosotros respondiento a este '
                    'correo que con gusto te ayudaremos! \n\n \n\n'
                    'De nuevo muchas gracias,\n\n \n\n'
                    'El equipo traux\n\n \n\n' % (self.link_youtube_instructions, self.link_download_demo),
                    '<h2>Hola %s!</h2>' % (serializer.validated_data['name']) +
                    '<p>Te felicito por iniciar tu camino hacia organizar y mejorar los procesos de negocio de tu '
                    'empresa, de parte de todo el equipo traux te damos las gracias por considerarnos como opción, '
                    'sabemos que hay muchos sistemas en el mercado y que quieres estar seguro que aquel que eligas '
                    'este en sintonía con tus objetivos. Es por eso que nosotros ofrecemos tres meses de prueba con '
                    'nuestro sistema, solo queremos ayudarte a decidir si traux es la opción correcta para tí.</p>'
                    '<p>Para descargarlo solo tienes que seguir las instrucciones que tenemos para ti en nuestro canal '
                    'de <a href="%s">youtube</a> desde el siguiente link:</p><p><a href="%s">DESCARGA AQUÍ</a></p>'
                    '<p>Si llegas a tener cualquier duda por favor comunícate con nosotros respondiento a este '
                    'correo que con gusto te ayudaremos!</p>'
                    '<p>De nuevo muchas gracias,<br>'
                    'El equipo traux</p>' % (self.link_youtube_instructions, self.link_download_demo) +
                    '<img src="%s">' % self.link_traux_logo,
                    'info@trauxerp.com',
                    [serializer.validated_data['email']]
                )
            else:
                send_email(
                    'Solicitud de contacto desde la web',
                    'Nombres: %s \n\nEmpresa: %s \n\nCorreo: %s \n\nTelefono: %s \n\n'
                    '------------------------- Mensaje -------------------------\n\n%s'
                    % (serializer.validated_data['name'], serializer.validated_data['company'],
                       serializer.validated_data['email'], serializer.validated_data['phone'],
                       serializer.validated_data['describe']),
                    '<p>Nombres: %s<br>Empresa: %s<br>Correo: %s<br>Telefono: %s</p>'
                    '<p>------------------------- Mensaje -------------------------</p><p>%s</p>'
                    % (serializer.validated_data['name'], serializer.validated_data['company'],
                       serializer.validated_data['email'], serializer.validated_data['phone'],
                       serializer.validated_data['describe']),
                    serializer.validated_data['email'],
                    ['info@trauxerp.com']
                )
        return response
