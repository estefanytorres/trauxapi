from django.db import models

#######################################################################################################################
#                                                     Tool box                                                        #
#######################################################################################################################


class MessageSet(models.Model):

    message_set = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'message_set'
        ordering = ['message_set']


class MessageCatalog(models.Model):

    message_set = models.ForeignKey(MessageSet, on_delete=models.PROTECT)
    message_nbr = models.IntegerField()
    description = models.CharField(max_length=150)
    message = models.TextField(blank=True)

    class Meta:
        unique_together = (('message_set', 'message_nbr'),)
        db_table = 'message_catalog'
        ordering = ['message_set', 'message_nbr']


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



