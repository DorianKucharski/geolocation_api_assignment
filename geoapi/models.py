from django.db import models


class Geolocation(models.Model):
    ip = models.CharField(max_length=100)
    domain = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=4)
    longitude = models.DecimalField(max_digits=8, decimal_places=4)
    continent_name = models.CharField(max_length=100)
    country_name = models.CharField(max_length=100)
    region_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip




