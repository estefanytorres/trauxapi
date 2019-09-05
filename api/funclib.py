from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import MessageSet, MessageCatalog

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


def get_message(message_set_id, message_nbr):
    try:
        message_set = MessageSet.objects.get(message_set=message_set_id)
        message = MessageCatalog.objects.get(message_set=message_set, message_nbr=message_nbr).message
    except (MessageSet.DoesNotExist, MessageCatalog.DoesNotExist):
        message = ''
    return message
