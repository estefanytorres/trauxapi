from django.db import models
from django.contrib.auth.models import User

#######################################################################################################################
#                                                     Tool box                                                        #
#######################################################################################################################


class MessageSet(models.Model):

    message_set = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    def __repr__(self):
        return '<MessageSet %i>' % self.message_set

    def __str__(self):
        return '[%i] %s' % (self.message_set, self.description)

    class Meta:
        ordering = ['message_set']


class MessageCatalog(models.Model):

    message_set = models.ForeignKey(MessageSet, on_delete=models.PROTECT)
    message_nbr = models.IntegerField()
    description = models.CharField(max_length=150)
    message = models.TextField(blank=True)

    def __repr__(self):
        return '<MessageCatalog [%i, %i]>' % (self.message_set.message_set, self.message_nbr)

    def __str__(self):
        return '[%i, %i] %s' % (self.message_set.message_set, self.message_nbr, self.description)

    class Meta:
        unique_together = (('message_set', 'message_nbr'),)
        ordering = ['message_set', 'message_nbr']


class File(models.Model):

    TYPE_CHOICES = [('XML', 'XML'), ('TXT', 'TXT'), ('CSV', 'CSV')]

    file = models.FileField(blank=False, null=False)
    type = models.CharField(max_length=5, choices=TYPE_CHOICES)

    def __str__(self):
        return self.file.name


class FileTransaction(models.Model):

    TYPE_CHOICES = [('XMLTOCSV', 'XML a CSV'), ('XMLTOTEXT', 'XML a texto plano')]

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    files_in = models.ManyToManyField(File, related_name='files_in')
    files_out = models.ManyToManyField(File, related_name='files_out', blank=True)
    date = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return '<FileTransaction [%s, %s]>' % (self.user.username, self.date)

    def __str__(self):
        return '[%s] %s' % (self.user.username, self.date)

    class Meta:
        ordering = ['-date']


#######################################################################################################################
#                                                    Website                                                          #
#######################################################################################################################


class WebConsult(models.Model):
    TYPE_CHOICES = [('D', 'DEMO'), ('C', 'Contact')]

    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    name = models.CharField(max_length=60)
    company = models.CharField(max_length=60, blank=True)
    email = models.CharField(max_length=60)
    phone = models.CharField(max_length=60, blank=True)
    describe = models.TextField(blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'web_consult'
        ordering = ['-create_date']


#######################################################################################################################
#                                                    Accounts                                                         #
#######################################################################################################################


class Client(models.Model):
    COUNTRY_CHOICES = [('CO', 'Colombia'), ('VE', 'Venezuela')]

    users = models.ManyToManyField(User, blank=True)
    name = models.CharField(max_length=150)
    nid = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    phone = models.CharField(max_length=60, blank=True)
    contact = models.CharField(max_length=60, blank=True)
    address1 = models.CharField(max_length=150)
    address2 = models.CharField(max_length=150, blank=True)
    address3 = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)
    active = models.BooleanField(default=True)

    def __repr__(self):
        return '<Client (%i) %s>' % (self.id, self.name)

    def __str__(self):
        return '[%i] %s' % (self.id, self.name)

    class Meta:
        ordering = ['id']


class Module(models.Model):
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=150)

    def __repr__(self):
        return '<Module %s>' % self.code

    def __str__(self):
        return self.code

    class Meta:
        ordering = ['id']


class License(models.Model):
    TYPE_CHOICES = [('ERP', 'Traux ERP'), ('FAC', 'Facturación electrónica')]

    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    number = models.CharField(max_length=12, unique=True)
    allowed_users = models.IntegerField(default=0, blank=True)
    active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=150, default=None, null=True, blank=True)
    activation_date = models.DateTimeField(default=None, null=True, blank=True)
    modules = models.ManyToManyField(Module, blank=True)
    start_date = models.DateField(default=None, null=True, blank=True)
    end_date = models.DateField(default=None, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return '<License %s>' % self.number

    def __str__(self):
        return self.number

    class Meta:
        ordering = ['id']


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activation_license = models.ForeignKey(License, null=True, default=None, on_delete=models.PROTECT)

    def __repr__(self):
        return '<User profile %s>' % self.self.user.username

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['user_id']



