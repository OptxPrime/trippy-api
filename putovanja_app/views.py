from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

import json
from datetime import datetime

from rest_framework.decorators import api_view

from .models import Traveler, Agency
from .functions import check_if_registered_email, check_if_registered_username, generate_random_password


# important: handling data from post requests in django
# https://stackoverflow.com/questions/16213324/django-tastypie-request-post-is-empty
# https://stackoverflow.com/questions/29780060/trying-to-parse-request-body-from-post-in-django

@api_view(['POST'])
def register_agency(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    values = body['values']

    if check_if_registered_email('agency', values['email']) or check_if_registered_email('traveler', values['email']):
        return HttpResponse('Email already registered', status=409)

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

    if check_if_registered_email('traveler', values['email']) or check_if_registered_email('agency', values['email']):
        return HttpResponse('Email already registered', status=409)

    if check_if_registered_username(values['username']):
        return HttpResponse('Username already taken', status=409)

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


@api_view(['POST'])
def reset_password(request):
    try:
        agency = Agency.objects.get(email=request.data['email'])
    except Agency.DoesNotExist:
        try:
            traveler = Traveler.objects.get(email=request.data['email'])
        except Traveler.DoesNotExist:
            return HttpResponse('No account with given email', status=404)
        else:
            new_password = generate_random_password()
            traveler.password = new_password
            traveler.save()
            try:
                send_mail(
                    'Dzale Trips - password change',
                    f'Your new password is ${new_password}.',
                    'dzalewebshop@gmail.com',
                    [f'${traveler.email}'],
                    fail_silently=False,
                )
            except:
                return HttpResponse('Mail not sent (internal error)', status=500)
            else:
                return HttpResponse('OK', status=200)
    else:
        new_password = generate_random_password()
        agency.password = new_password
        print(agency.establishment_date)
        agency.save()
        try:
            send_mail(
                'Dzale Trips - password change',
                f'Your new password is ${new_password}.',
                'dzalewebshop@gmail.com',
                ['dzakatarik@gmail.com'],
                # [f'${agency.email}'],
                fail_silently=False,
            )
        except:
            return HttpResponse('Mail not sent (internal error)', status=500)
        else:
            return HttpResponse('OK', status=200)
