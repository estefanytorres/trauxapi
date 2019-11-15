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
import xml.etree.ElementTree as ET
import pandas as pd


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


class InvoiceLine:

    def __init__(self):
        self.code = None
        self.description = None
        self.depot = 'Principal'
        self.verified = 0
        self.quantity = 0
        self.unit = 'Und.'
        self.price = 0.0
        self.tax = 0.0


class Invoice:

    def __init__(self, xml_text):

        self.xml = xml_text
        self.client = None
        self.clientID = None
        self.clientCode = None
        self.document = 'FV'
        self.prefix = ''
        self.number = None
        self.date = None
        self.expiry_date = None
        self.collector = 0
        self.payment_form = 'Credito'
        self.cost_center = 'OPERACIONAL'
        self.null = 0
        self.discount = 0
        self.factor = 0
        self.mov_factor = 0
        self.cost_tax = 0
        self.pers1 = ''
        self.lines = []

        cac = '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}'
        cbc = '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}'
        root = ET.fromstring(self.xml)
        document = ET.fromstring(
            root.find(cac + 'Attachment').find(cac + 'ExternalReference').find(cbc + 'Description').text)
        self.client = document.find(cac + 'AccountingCustomerParty').find(cac + 'Party').find(
            cac + 'PartyTaxScheme').find(cbc + 'RegistrationName').text
        self.clientID = document.find(cac + 'AccountingCustomerParty').find(cac + 'Party').find(
            cac + 'PartyTaxScheme').find(cbc + 'CompanyID').text
        self.number = document.find(cbc + 'ID').text
        self.date = document.find(cbc + 'IssueDate').text
        self.expiry_date = document.find(cbc + 'DueDate').text
        for node in document.findall(cac + 'InvoiceLine'):
            line = InvoiceLine()
            line.code = node.find(cac + 'Item').find(cac + 'SellersItemIdentification').find(cbc + 'ID').text
            line.description = node.find(cac + 'Item').find(cbc + 'Description').text
            line.quantity = node.find(cbc + 'InvoicedQuantity').text
            line.price = node.find(cbc + 'LineExtensionAmount').text
            line.tax = node.find(cac + 'TaxTotal').find(cac + 'TaxSubtotal').find(cac + 'TaxCategory').find(
                cbc + 'Percent').text
            line.tax = float(line.tax)/100
            self.lines.append(line)


def xml_transform(xml_collection):

    header = ['Empresa', 'Documento', 'Prefijo', 'Num.Documento', 'Fecha', 'IdTerceroExterno', 'Tercero Interno',
              'Recaudador', 'Nota', 'Verificado', 'Forma de Pago', 'Codigo Descripcion', 'Bodega', 'Cantidad',
              'Unidad de Medida', 'Valor Unitario', 'Iva', 'Vencimiento', 'Centro de Costo', 'Tercero', 'Anulado',
              'Descuento', 'Factor', 'Factormov', 'IvaalCosto', 'Personalizado1']
    content = []
    for xml in xml_collection:
        invoice = Invoice(xml)
        for line in invoice.lines:
            content.append([invoice.client, invoice.document, invoice.prefix, invoice.number, invoice.date,
                            invoice.clientID, invoice.clientID, invoice.collector, line.description, line.verified,
                            invoice.payment_form, line.code, line.depot, line.quantity, line.unit, line.price, line.tax,
                            invoice.expiry_date, invoice.cost_center, invoice.clientID, invoice.null, invoice.discount,
                            invoice.factor, invoice.mov_factor, invoice.cost_tax, invoice.pers1])

    return pd.DataFrame(content, columns=header).to_csv(index=False)


