# Generated by Django 2.2.3 on 2019-09-26 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20190925_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='license',
            name='type',
            field=models.CharField(choices=[('ERP', 'Traux ERP'), ('FAC', 'Facturación electrónica')], default='ERP', max_length=3),
            preserve_default=False,
        ),
    ]
