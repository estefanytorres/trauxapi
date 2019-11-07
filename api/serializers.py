from django.contrib.auth.models import User
from rest_framework import serializers
from .models import (
    File,
    FileTransaction,
    WebConsult,
    Client,
    License
)


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


class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = ('pk', 'number', 'type', 'allowed_users', 'start_date', 'end_date')
        depth = 1


class ClientSerializer(serializers.ModelSerializer):
    license_set = LicenseSerializer(many=True)

    class Meta:
        model = Client
        fields = ('pk', 'name', 'license_set')


class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = "__all__"


class FileTransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FileTransaction
        fields = "__all__"


# https://stackoverflow.com/questions/53404738/how-to-send-email-with-django-rest-framwork
# https://www.django-rest-framework.org/tutorial/1-serialization/
# https://github.com/encode/rest-framework-tutorial/blob/master/snippets/serializers.py
# https://wsvincent.com/django-contact-form/
# https://scotch.io/courses/build-your-first-angular-website/create-a-contact-page-and-contact-form
