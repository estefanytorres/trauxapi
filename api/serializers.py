from django.contrib.auth.models import User
from rest_framework import serializers
from .models import WebConsult


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class WebConsultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WebConsult
        fields = '__all__'
            # ('url', 'id', 'name', 'company', 'email', 'phone', 'describe', 'create_date', 'update_date')

# https://stackoverflow.com/questions/53404738/how-to-send-email-with-django-rest-framwork
# https://www.django-rest-framework.org/tutorial/1-serialization/
# https://github.com/encode/rest-framework-tutorial/blob/master/snippets/serializers.py
# https://wsvincent.com/django-contact-form/
# https://scotch.io/courses/build-your-first-angular-website/create-a-contact-page-and-contact-form
