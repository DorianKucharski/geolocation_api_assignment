# Generated by Django 3.2.3 on 2021-09-08 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geoapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='geolocation',
            name='domain',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]