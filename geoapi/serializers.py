from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Geolocation


class GeolocationSerializer(serializers.Serializer):
    ip = serializers.CharField(max_length=40)
    domain = serializers.CharField(max_length=80)
    latitude = serializers.DecimalField(max_digits=8, decimal_places=4)
    longitude = serializers.DecimalField(max_digits=8, decimal_places=4)
    continent_name = serializers.CharField(max_length=15)
    country_name = serializers.CharField(max_length=30)
    region_name = serializers.CharField(max_length=80)
    city = serializers.CharField(max_length=80)
    zip = serializers.CharField(max_length=10)

    def update(self, instance, validated_data):
        instance.ip = validated_data.get('ip')
        instance.domain = validated_data.get('domain')
        instance.latitude = validated_data.get('latitude')
        instance.longitude = validated_data.get('longitude')
        instance.continent_name = validated_data.get('continent_name')
        instance.country_name = validated_data.get('country_name')
        instance.region_name = validated_data.get('region_name')
        instance.city = validated_data.get('city')
        instance.zip = validated_data.get('zip')
        instance.save()
        return instance

    def create(self, validated_data):
        return Geolocation.objects.create(validated_data)
