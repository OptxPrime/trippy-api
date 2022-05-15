from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404

import json
from datetime import datetime

from rest_framework.decorators import api_view

from .models import Traveler, Agency


# important: handling data from post requests in django
# https://stackoverflow.com/questions/16213324/django-tastypie-request-post-is-empty
# https://stackoverflow.com/questions/29780060/trying-to-parse-request-body-from-post-in-django

@api_view(['POST'])
def register_agency(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    values = body['values']

    # https://stackoverflow.com/questions/30819423/convert-string-date-into-date-format-in-python
    js_date = values['establishment_date']
    python_date = datetime.strptime(js_date, '%Y-%m-%d')

    agency = Agency(
        name=values['agency_name'],
        agency_id=values['agency_id'],
        establishment_date=python_date,
        email=values['email'],
        password=values['password']
    )
    agency.save()
    return HttpResponse('OK', status=200)

@api_view(['POST'])
def register_traveler(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    values = body['values']

    traveler = Traveler(
        first_name=values['first_name'],
        last_name=values['last_name'],
        username=values['username'],
        email=values['email'],
        password=values['password']
    )
    traveler.save()
    return HttpResponse('OK', status=200)


@api_view(['POST'])
def login_agency(request):
    try:
        agency = get_object_or_404(Agency, email=request.data['email'])
    except (KeyError, Agency.DoesNotExist):
        return HttpResponse('Unauthorized', status=401)
    else:
        if agency.password == request.data['password']:
            return JsonResponse(agency.id, safe=False)
        else:
            return HttpResponse('Unauthorized', status=401)


@api_view(['POST'])
def login_traveler(request):
    try:
        traveler = get_object_or_404(Traveler, email=request.data['email'])
    except (KeyError, Traveler.DoesNotExist):
        return HttpResponse('Unauthorized', status=401)
    else:
        if traveler.password == request.data['password']:
            return JsonResponse(traveler.id, safe=False)
        else:
            return HttpResponse('Unauthorized', status=401)

