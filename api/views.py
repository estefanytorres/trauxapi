from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.db import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .funclib import (
    send_email,
    get_message,
    TokenGenerator,
    encode_email_address
)
from .serializers import *
from .models import *


#######################################################################################################################
#                                                 Authentication                                                      #
#######################################################################################################################


def send_activation_email(user):
    try:
        user_profile = UserProfile.objects.get(user=user)
        account_activation_token = TokenGenerator()
        url = settings.CORS_ORIGIN_WHITELIST[1] + "/login/?action=activate&uid={}&token={}".format(
            urlsafe_base64_encode(force_bytes(user.pk)),
            account_activation_token.make_token(user)
        )
        send_email(
            'noreply@trauxerp.com',
            [user_profile.activation_license.client.email],
            get_message(1000, 7),
            get_message(1000, 8).format(user.first_name, url, url)
        )
        return True
    except UserProfile.DoesNotExist as e:
        return False
    except IndexError:
        return False


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.filter(username=self.request.user)

    @action(detail=False, methods=['POST'])
    def register(self, request, **kwargs):
        try:
            activation_license = License.objects.get(number=request.data['license'])
            user = User.objects.create_user(request.data['email'], request.data['email'], request.data['password'])
            user.first_name = request.data['first_name']
            user.last_name = request.data['last_name']
            user.is_active = False
            user.save()
            user_profile = UserProfile.objects.create(
                user=user,
                activation_license=activation_license
            )
            user_profile.save()
            send_activation_email(user)

        except License.DoesNotExist as e:
            return Response({"code": 4001,  "message": e.__str__()}, 400)
        except IntegrityError as e:
            return Response({"code": 4002,  "message": e.__str__()}, 400)
        except IndexError as e:
            return Response({"code": 5001, "message": e.__str__()}, 500)
        except Exception as e:
            return Response({"code": 5002, "message": e.__str__()}, 500)

        return Response(
            {
                "code": (2001 if user.email == activation_license.client.email else 2002),
                "message": "User registered, activation code sent to license registered email",
                "email": encode_email_address(activation_license.client.email)
            }, 201)

    @action(detail=False, methods=['POST'])
    def activate(self, request, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(request.data['uid']))
            user = User.objects.get(pk=uid)
            account_activation_token = TokenGenerator()
            if user.is_active:
                return Response({"code": 2004, "message": 'User is already active'}, 200)
            if account_activation_token.check_token(user, request.data['token']):
                user.is_active = True
                user.save()
                user_profile = UserProfile.objects.get(user=user)
                client = user_profile.activation_license.client
                client.users.add(user)

                try:
                    send_email(
                        'noreply@trauxerp.com',
                        [user.email],
                        get_message(1000, 9),
                        get_message(1000, 10).format(user.first_name, user.username)
                    )
                except IndexError:
                    pass

                return Response({"code": 2003, "message": 'Account activated'}, 200)
            else:
                return Response({"code": 4006, "message": 'Invalid token'}, 400)
        except KeyError:
            return Response({"code": 4003, "message": 'Invalid parameters, required fields: [uid, token]'}, 400)
        except User.DoesNotExist as e:
            return Response({"code": 4004, "message": e.__str__()}, 400)
        except UserProfile.DoesNotExist as e:
            return Response({"code": 4005, "message": e.__str__()}, 400)
        except Exception as e:
            return Response({"code": 5003, "message": e.__str__()}, 500)

    @action(detail=False, methods=['POST'])
    def send_reset_password_link(self, request, **kwargs):
        try:
            activation_license = License.objects.get(number=request.data['license'])
            user = User.objects.get(pk=uid)
            user_profile = UserProfile.objects.create(
                user=user,
                activation_license=activation_license
            )
            user_profile.save()
            send_activation_email(user)

        except License.DoesNotExist as e:
            return Response({"code": 4006,  "message": e.__str__()}, 400)
        except IntegrityError as e:
            return Response({"code": 4007,  "message": e.__str__()}, 400)
        except IndexError as e:
            return Response({"code": 5001, "message": e.__str__()}, 500)
        except Exception as e:
            return Response({"code": 5002, "message": e.__str__()}, 500)

        return Response(
            {
                "code": (2001 if user.email == activation_license.client.email else 2002),
                "message": "User registered, activation code sent to license registered email",
                "email": encode_email_address(activation_license.client.email)
            }, 201)


#######################################################################################################################
#                                                     Tool box                                                        #
#######################################################################################################################


# class MessageSetViewSet(viewsets.ModelViewSet):
#     queryset = MessageSet.objects.all()
#     serializer_class = MessageSetSerializer
#     permission_classes = [AllowAny]
#
#
# class MessageCatalogViewSet(viewsets.ModelViewSet):
#     queryset = MessageCatalog.objects.all()
#     serializer_class = MessageCatalogSerializer
#     permission_classes = [AllowAny]


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


#######################################################################################################################
#                                                    Accounts                                                         #
#######################################################################################################################


# class ClientViewSet(viewsets.ModelViewSet):
#     queryset = Client.objects.all()
#     serializer_class = ClientSerializer
#     permission_classes = [AllowAny]
#
#
# class ModuleViewSet(viewsets.ModelViewSet):
#     queryset = Module.objects.all()
#     serializer_class = ModuleSerializer
#     permission_classes = [AllowAny]
#
#
# class LicenseViewSet(viewsets.ModelViewSet):
#     queryset = License.objects.all()
#     serializer_class = LicenseSerializer
#     permission_classes = [AllowAny]
