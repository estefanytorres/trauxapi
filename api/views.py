from django.conf import settings
from django.db import IntegrityError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from .funclib import (
    send_email,
    get_message,
    TokenGenerator,
    encode_email_address,
    get_response
)
from .serializers import *
from .models import *


#######################################################################################################################
#                                                 Authentication                                                      #
#######################################################################################################################


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
            account_activation_token = TokenGenerator()
            url = settings.CORS_ORIGIN_WHITELIST[1] + "/login/?action=activate&uid={}&token={}".format(
                urlsafe_base64_encode(force_bytes(user.pk)),
                account_activation_token.make_token(user)
            )
            send_email(
                'noreply@trauxerp.com',
                [activation_license.client.email],
                get_message(1000, 7),
                get_message(1000, 8).format(user.first_name, url, url)
            )

        except License.DoesNotExist as e:
            return get_response(400, 1, e)
        except IntegrityError as e:
            return get_response(400, 2, e)
        except UserProfile.DoesNotExist as e:
            return get_response(500, 1, e)
        except IndexError as e:
            return get_response(500, 2, e)
        except Exception as e:
            return get_response(500, 0, e)

        return get_response(201, 1 if user.email == activation_license.client.email else 2,
                            {"email": encode_email_address(activation_license.client.email)})

    @action(detail=False, methods=['POST'])
    def activate(self, request, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(request.data['uid']))
            user = User.objects.get(pk=uid)
            account_activation_token = TokenGenerator()
            if user.is_active:
                return get_response(200, 11)
            if not account_activation_token.check_token(user, request.data['token']):
                return get_response(400, 10)
            user.is_active = True
            user.save()
            user_profile = UserProfile.objects.get(user=user)
            client = user_profile.activation_license.client
            client.users.add(user)
            send_email(
                'noreply@trauxerp.com',
                [user.email],
                get_message(1000, 9),
                get_message(1000, 10).format(user.first_name, user.username)
            )
            return get_response(200, 10)
        except User.DoesNotExist:
            return get_response(400, 11)
        except KeyError as e:
            return get_response(400, 12, e)
        except UserProfile.DoesNotExist:
            return get_response(500, 11)
        except IndexError as e:
            return get_response(500, 12, e)
        except Exception as e:
            return get_response(500, 10, e)

    @action(detail=False, methods=['POST'])
    def email_reset_password(self, request, **kwargs):
        try:
            user = User.objects.get(username=request.data['username'])
            token_generator = PasswordResetTokenGenerator()
            url = settings.CORS_ORIGIN_WHITELIST[1] + "/forgotpassword/?action=reset&uid={}&token={}".format(
                urlsafe_base64_encode(force_bytes(user.pk)),
                token_generator.make_token(user)
            )
            send_email(
                'noreply@trauxerp.com',
                [user.email],
                get_message(1000, 11),
                get_message(1000, 12).format(user.first_name, url, url)
            )
            return get_response(200, 20)
        except IndexError as e:
            return get_response(400, 20, e)
        except User.DoesNotExist:
            return get_response(400, 21)
        except Exception as e:
            return get_response(500, 20, e)

    @action(detail=False, methods=['POST'])
    def reset_password(self, request, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(request.data['uid']))
            user = User.objects.get(pk=uid)
            token_generator = PasswordResetTokenGenerator()
            if not user.is_active:
                return get_response(400, 30)
            if not token_generator.check_token(user, request.data['token']):
                return get_response(400, 31)
            user.set_password(request.data['password'])
            user.save()
            return get_response(200, 30, {'username': user.username})
        except User.DoesNotExist:
            return get_response(400, 32)
        except KeyError as e:
            return get_response(400, 33, e)
        except Exception as e:
            return get_response(500, 10, e)


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
