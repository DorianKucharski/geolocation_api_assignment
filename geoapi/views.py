from django.http import JsonResponse
from rest_framework.decorators import api_view
from geoapi.serializers import GeolocationSerializer
from .models import Geolocation
from rest_framework import status
import requests
from urllib.parse import urlparse
import validators
import json

from django.db.models import Q


def make_request(ip_or_domain):
    api_key = "955b1cee6fb88efe199fb801d6388506"
    url = f'http://api.ipstack.com/{ip_or_domain}?access_key={api_key}'
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("Cannot get access to IP Stack")
    return r.json()


def create_object_from_response(response):
    keys = Geolocation.__doc__.replace("Geolocation(", "").replace(")", "").split(", ")
    keys.remove("id")
    keys.remove("domain")
    filtered_response = {your_key: response[your_key] for your_key in keys}
    return Geolocation(**filtered_response)


@api_view(['GET', 'DELETE', 'POST'])
def params_way(request, param):
    if not any([validators.ipv4(param), validators.ipv6(param), validators.url(param), validators.domain(param)]):
        return JsonResponse({'message': 'Not valid value'}, status=status.HTTP_404_NOT_FOUND)

    if validators.url(param):
        param = urlparse(param).netloc

    geolocation = Geolocation.objects.filter(Q(ip=param) | Q(domain=param))

    if request.method == 'GET':
        if not geolocation:
            return JsonResponse({'message': 'The geolocation does not exist'}, status=status.HTTP_204_NO_CONTENT)
        serializer = GeolocationSerializer(geolocation[0])
        return JsonResponse(serializer.data)

    elif request.method == 'DELETE':
        if not geolocation:
            return JsonResponse({'message': 'The geolocation does not exist'}, status=status.HTTP_204_NO_CONTENT)
        geolocation[0].delete()
        return JsonResponse({'message': 'geolocation was deleted successfully!'}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        try:
            new_data = make_request(param)
            new_geolocation = create_object_from_response(new_data)
            if validators.domain(param):
                new_geolocation.domain = param
            serializer = GeolocationSerializer(new_geolocation)
            json_response = serializer.data
            if geolocation:
                geolocation = new_geolocation
                json_response["status"] = "geo updated"
            else:
                new_geolocation.save()
            return JsonResponse(json_response)
        except Exception as e:
            return JsonResponse({'message': 'Error: ' + str(e)})


@api_view(['GET', 'DELETE', 'POST'])
def json_way(request):
    if not request.body:
        objects = Geolocation.objects.all()
        response = {'Geolocations': [GeolocationSerializer(o).data for o in objects]}
        return JsonResponse(response)
    else:
        data = json.loads(request.body)

        if data.get("url") and data.get("ip"):
            return JsonResponse({'message': 'Use ony "url" or "ip" key '}, status=status.HTTP_404_NOT_FOUND)

        if data.get("url"):
            if not (validators.url(data.get("url")) or validators.domain(data.get("url"))):
                return JsonResponse({'message': 'Not valid url or domain'}, status=status.HTTP_404_NOT_FOUND)
            if validators.url(data.get("url")):
                data["url"] = urlparse(data.get("url")).netloc
        if data.get("ip"):
            if not (validators.ipv4(data.get("ip")) or validators.ipv6(data.get("ip"))):
                return JsonResponse({'message': 'Not valid ip'}, status=status.HTTP_404_NOT_FOUND)


        geolocation = Geolocation.objects.filter(Q(ip=data.get("ip")) | Q(domain=data.get("url")))

        if request.method == 'GET':
            if not geolocation:
                return JsonResponse({'message': 'The geolocation does not exist'}, status=status.HTTP_204_NO_CONTENT)
            serializer = GeolocationSerializer(geolocation[0])
            return JsonResponse(serializer.data)

        elif request.method == 'DELETE':
            if not geolocation:
                return JsonResponse({'message': 'The geolocation does not exist'}, status=status.HTTP_204_NO_CONTENT)
            geolocation[0].delete()
            return JsonResponse({'message': 'The geolocation was deleted successfully!'},
                                status=status.HTTP_200_OK)

        elif request.method == 'POST':
            try:
                new_data = make_request(data.get("ip") if data.get("ip") else data.get("url"))
                new_geolocation = create_object_from_response(new_data)
                if data.get("url"):
                    new_geolocation.domain = data.get("url")
                serializer = GeolocationSerializer(new_geolocation)
                json_response = serializer.data
                if geolocation:
                    geolocation = new_geolocation
                    json_response["status"] = "geo updated"
                else:
                    new_geolocation.save()
                return JsonResponse(json_response)
            except Exception as e:
                return JsonResponse({'message': 'Error: ' + str(e)})


