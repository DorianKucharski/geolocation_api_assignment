from django.conf.urls import url
from geoapi import views
from django.urls import path, include

urlpatterns = [
    url(r'^/2/(.*?)$', views.params_way),
    path('', views.json_way)
    ]
