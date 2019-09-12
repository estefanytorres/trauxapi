from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *


#######################################################################################################################
#                                                 Authentication                                                      #
#######################################################################################################################


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff', 'first_name', 'last_name')


#######################################################################################################################
#                                                     Tool box                                                        #
#######################################################################################################################


# class MessageSetSerializer(serializers.HyperlinkedModelSerializer):
#
#     class Meta:
#         model = MessageSet
#         fields = ('url', 'message_set', 'title', 'description')
#
#
# class MessageCatalogSerializer(serializers.HyperlinkedModelSerializer):
#
#     class Meta:
#         model = MessageCatalog
#         fields = ('url', 'message_set', 'message_nbr', 'description', 'message')


#######################################################################################################################
#                                                    Website                                                          #
#######################################################################################################################


class WebConsultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WebConsult
        fields = '__all__'


#######################################################################################################################
#                                                    Accounts                                                         #
#######################################################################################################################


# class ClientSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Client
#         fields = '__all__'
#
#
# class ModuleSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Module
#         fields = '__all__'
#
#
# class LicenseSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = License
#         fields = '__all__'


# https://stackoverflow.com/questions/53404738/how-to-send-email-with-django-rest-framwork
# https://www.django-rest-framework.org/tutorial/1-serialization/
# https://github.com/encode/rest-framework-tutorial/blob/master/snippets/serializers.py
# https://wsvincent.com/django-contact-form/
# https://scotch.io/courses/build-your-first-angular-website/create-a-contact-page-and-contact-form
