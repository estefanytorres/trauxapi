# Django
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMultiAlternatives
from django.utils import six
# Rest Framework
from rest_framework.response import Response
# Local
from .models import MessageSet, MessageCatalog
# Installed packages
from html2text import html2text


def send_email(sender, recipient, subject, body):
    if settings.ENV != 'PRD':
        subject = '[' + settings.ENV + '] ' + subject
        body = '<p><b>environment:</b> {}<br><b>send_from:</b> {}<br><b>send_to:</b> {}<br></p><hr>'.format(
            settings.ENV,
            sender,
            ', '.join(recipient)
        ) + body
        sender = settings.EMAIL_DEFAULT_SENDER
        recipient = [settings.EMAIL_TEST_RECIPIENT]

    email = EmailMultiAlternatives(subject, html2text(body), sender, recipient)
    email.attach_alternative(body, "text/html")
    email.send()


def encode_email_address(email):
    email_parts = email.split('@')
    user = email_parts[0]
    domain = email_parts[1]
    length = len(user)
    if length <= 2:
        user = user[0] + '*'
    elif length <= 5:
        user = user[:1] + '*'*(length - 2) + user[-1:]
    else:
        user = user[:2] + '*'*(length-4) + user[-2:]
    return user + '@' + domain


def get_message(message_set_id, message_nbr):
    try:
        message_set = MessageSet.objects.get(message_set=message_set_id)
        message = MessageCatalog.objects.get(message_set=message_set, message_nbr=message_nbr).message
    except (MessageSet.DoesNotExist, MessageCatalog.DoesNotExist):
        message = ''
    return message


def get_response(status, code, data=None):
    message = get_message(status, code)
    if status < 300:
        return Response({'status': status, 'code': code, 'message': message, 'data': data}, status)
    else:
        if data:
            return Response({'status': status, 'code': code, 'message': message, 'exception': data.__str__()}, status)
        else:
            return Response({'status': status, 'code': code, 'message': message}, status)


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
