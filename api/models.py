from django.db import models


# Online contact consults from webpage
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