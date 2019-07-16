from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, WebConsultSerializer
from .models import WebConsult
from django.core.mail import EmailMessage
from django.conf import settings


#######################################################################################################################
#                                                   Function catalog                                                  #
#######################################################################################################################
def send_email(title, content, send_from, send_to):
    if settings.ENV != 'PRD':
        content = '##########################################################################################\n\n' \
                  'env: ' + settings.ENV + '\n\n' + \
                  'subject: ' + title + '\n\n' + \
                  'send_from: ' + send_from + '\n\n' + \
                  'send_to: ' + ', '.join(send_to) + '\n\n' + \
                  '##########################################################################################\n\n\n\n' \
                  + content
        title = '[' + settings.ENV + '] ' + title
        send_from = settings.EMAIL_DEFAULT_SENDER
        send_to = [settings.EMAIL_TEST_RECIPIENT]

    email = EmailMessage(
        title,
        content,
        send_from,
        send_to
    )
    email.send()


#######################################################################################################################
#                                                   REST ViewSets                                                     #
#######################################################################################################################
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class WebConsultViewSet(viewsets.ModelViewSet):
    queryset = WebConsult.objects.all()
    serializer_class = WebConsultSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super(WebConsultViewSet, self).create(request, *args, **kwargs)
        serializer = WebConsultSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['name'] == 'D':
                send_email(
                    'Descarga de DEMO desde la web',
                    'Nombres: %s \n\nEmpresa: %s \n\nCorreo: %s \n\nTelefono: %s \n\n' %
                    (serializer.validated_data['name'], serializer.validated_data['company'],
                     serializer.validated_data['email'], serializer.validated_data['phone']),
                    ['info@trauxerp.com']
                )
                send_email(
                    'Tu trauxerp version DEMO!',
                    'Hola %s! \n\n Gracias por empezar tu camino hacia un'
                    ['info@trauxerp.com']
                )
            else:
                send_email(
                    'Solicitud de contacto desde la web',
                    'Nombres: %s \n\nEmpresa: %s \n\nCorreo: %s \n\nTelefono: %s \n\n'
                    '------------------------- Mensaje -------------------------\n\n%s'
                    % (serializer.validated_data['name'], serializer.validated_data['company'],
                       serializer.validated_data['email'], serializer.validated_data['phone'],
                       serializer.validated_data['describe']),
                    serializer.validated_data['email'],
                    ['info@trauxerp.com']
                )
        return response
