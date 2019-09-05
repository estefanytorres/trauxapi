from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .funclib import *
from .serializers import *
from .models import *


#######################################################################################################################
#                                                 Authentication                                                      #
#######################################################################################################################


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(username=self.request.user)


#######################################################################################################################
#                                                     Tool box                                                        #
#######################################################################################################################


class MessageSetViewSet(viewsets.ModelViewSet):
    queryset = MessageSet.objects.all()
    serializer_class = MessageSetSerializer
    permission_classes = [AllowAny]


class MessageCatalogViewSet(viewsets.ModelViewSet):
    queryset = MessageCatalog.objects.all()
    serializer_class = MessageCatalogSerializer
    permission_classes = [AllowAny]


#######################################################################################################################
#                                                    Website                                                          #
#######################################################################################################################


class WebConsultViewSet(viewsets.ModelViewSet):
    queryset = WebConsult.objects.all()
    serializer_class = WebConsultSerializer
    http_method_names = ['post']
    permission_classes = [AllowAny]

    link_download_demo = settings.CORS_ORIGIN_WHITELIST[0] + '/assets/downloads/Setup-TrauxERP.exe'
    link_traux_logo = settings.CORS_ORIGIN_WHITELIST[0] + '/assets/logo.png'

    def create(self, request, *args, **kwargs):
        response = super(WebConsultViewSet, self).create(request, *args, **kwargs)
        serializer = WebConsultSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['type'] == 'D':
                send_email(
                    'noreply@trauxerp.com',
                    ['info@trauxerp.com'],
                    get_message(1000, 3),
                    get_message(1000, 4).format(
                        serializer.validated_data['name'],
                        serializer.validated_data['company'],
                        serializer.validated_data['email'],
                        serializer.validated_data['phone']
                    )
                )
                send_email(
                    'info@trauxerp.com',
                    [serializer.validated_data['email']],
                    get_message(1000, 5),
                    get_message(1000, 6).format(
                        serializer.validated_data['name'],
                        self.link_download_demo,
                        self.link_traux_logo
                    )
                )
            elif serializer.validated_data['type'] == 'C':
                send_email(
                    serializer.validated_data['email'],
                    ['info@trauxerp.com'],
                    get_message(1000, 1),
                    get_message(1000, 2).format(
                        serializer.validated_data['name'],
                        serializer.validated_data['company'],
                        serializer.validated_data['email'],
                        serializer.validated_data['phone'],
                        serializer.validated_data['describe']
                    )
                )
        return response

