from itertools import chain
import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.core import serializers

from datetime import datetime

from rest_framework.decorators import api_view

from .models import Traveler, Agency, SoloTrip, GroupTour
from .functions import check_if_registered_email, check_if_registered_username, generate_random_password, get_agency_trips


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
        agency.save()
        try:
            send_mail(
                'Dzale Trips - password change',
                f'Your new password is ${new_password}.',
                'dzalewebshop@gmail.com',
                ['dzakatarik@gmail.com'],
                fail_silently=False,
            )
        except:
            return HttpResponse('Mail not sent (internal error)', status=500)
        else:
            return HttpResponse('OK', status=200)


@api_view(['GET'])
def get_user_by_token(request):
    token = json.loads(request.headers['Authorization'].split(' ')[1])
    user_type = token.split('#')[0]
    user_id = token.split('#')[1]

    if user_type == 'agency':
        try:
            agency = get_object_or_404(Agency, pk=user_id)
        except (KeyError, Agency.DoesNotExist):
            return HttpResponse('Unauthorized', status=401)
        else:
            return JsonResponse(agency.to_json(), safe=False)
    else:
        try:
            traveler = get_object_or_404(Traveler, pk=user_id)
        except (KeyError, Traveler.DoesNotExist):
            return HttpResponse('Unauthorized', status=401)
        else:
            return JsonResponse(traveler.to_json(), safe=False)


@api_view(['POST'])
def update_profile(request):
    token = json.loads(request.headers['Authorization'].split(' ')[1])
    user_type = token.split('#')[0]
    user_id = token.split('#')[1]

    updated_info = request.data

    if user_type == 'agency':
        js_date = updated_info['establishment_date']
        updated_info['establishment_date'] = datetime.strptime(js_date, '%Y-%m-%d')
        try:
            agency = get_object_or_404(Agency, pk=user_id)
        except (KeyError, Agency.DoesNotExist):
            return HttpResponse('Unauthorized', status=404)
        else:
            agency.name = updated_info['name']
            agency.agency_id = updated_info['agency_id']
            agency.password = updated_info['password']
            agency.establishment_date = updated_info['establishment_date']
            agency.save()
            return HttpResponse('Ok', status=200)
    else:
        try:
            traveler = get_object_or_404(Traveler, pk=user_id)
        except (KeyError, Traveler.DoesNotExist):
            return HttpResponse('Unauthorized', status=401)
        else:
            return HttpResponse('Ok', status=200)


@api_view(['POST'])
def add_solo_trip(request):
    try:
        token = json.loads(request.headers['Authorization'].split(' ')[1])
        user_type = token.split('#')[0]
        user_id = token.split('#')[1]
    except Exception:
        return HttpResponse("Invalid token", status=401)
    else:
        if user_type != 'traveler':
            return HttpResponse("Only travelers can add solo trips!", 401)
        try:
            traveler = get_object_or_404(Traveler, pk=user_id)
        except (KeyError, Traveler.DoesNotExist):
            return HttpResponse('Unauthorized', status=401)
        else:
            dt_obj = datetime.strptime(request.data['datetime'], '%Y-%m-%dT%H:%M')
            transport = ','.join(request.data['transport'])
            try:
                solo_trip = SoloTrip(
                    title=request.data['title'],
                    description=request.data['description'],
                    agency=Agency.objects.get(pk=request.data['agency']),
                    traveler=Traveler.objects.get(pk=traveler.id),
                    datetime=dt_obj,
                    transport=transport,
                    location_name=request.data['location'],
                    lat=request.data['lat'],
                    lng=request.data['lng'],
                    max_price=request.data['max_price'],
                )
                solo_trip.save()
            except Exception as e:
                return HttpResponse('%s' % type(e), status=500)
            else:
                return HttpResponse('Added solo trip', status=201)


@api_view(['POST'])
def add_group_tour(request):
    try:
        token = json.loads(request.headers['Authorization'].split(' ')[1])
        user_type = token.split('#')[0]
        user_id = token.split('#')[1]
    except Exception:
        return HttpResponse("Invalid token", status=401)
    else:
        if user_type != 'agency':
            return HttpResponse("Only agencies can add group tours!", 401)
        try:
            agency = get_object_or_404(Agency, pk=user_id)
        except (KeyError, Traveler.DoesNotExist):
            return HttpResponse('Unauthorized', status=401)
        else:
            dt_obj = datetime.strptime(request.data['datetime'], '%Y-%m-%dT%H:%M')
            transport = ','.join(request.data['transport'])
            try:
                group_tour = GroupTour(
                    title=request.data['title'],
                    description=request.data['description'],
                    agency=agency,
                    datetime=dt_obj,
                    transport=transport,
                    location_name=request.data['location'],
                    lat=request.data['lat'],
                    lng=request.data['lng'],
                    min_travelers=request.data['min_travelers'],
                    max_travelers=request.data['max_travelers'],
                    picture_url=request.data['picture_url']
                )
                group_tour.save()
            except Exception as e:
                return HttpResponse('%s' % type(e), status=500)
            else:
                return HttpResponse('Added group tour', status=201)


# TO DO: insert is_registered and current_travelers field to all trips because of check in/check out
@api_view(['GET'])
def get_future_trips(request):
    try:
        token = json.loads(request.headers['Authorization'].split(' ')[1])
        user_type = token.split('#')[0]
        user_id = token.split('#')[1]
    except Exception:
        return HttpResponse("Invalid token", status=401)
    else:
        if user_type == 'agency':
            serialized_trips = get_agency_trips(user_id, 'future')
            return JsonResponse(serialized_trips, safe=False)
        else:
            try:
                traveler = get_object_or_404(Traveler, pk=user_id)
            except (KeyError, Traveler.DoesNotExist):
                return HttpResponse('Unauthorized', status=401)
            else:
                solo_trips = SoloTrip.objects.filter(traveler=traveler).filter(datetime__gte=datetime.now()).distinct()
                group_tours = GroupTour.objects.filter(datetime__gte=datetime.now()).distinct()
                trips = list(chain(solo_trips, group_tours))
                serialized_trips = serializers.serialize('json', trips)

                return JsonResponse(serialized_trips, safe=False)


# TO DO: insert is_registered and current_travelers field to all trips because of check in/check out
# TO DO: filter group tours of traveler to include only those he attended
@api_view(['GET'])
def get_my_trips(request):
    try:
        token = json.loads(request.headers['Authorization'].split(' ')[1])
        user_type = token.split('#')[0]
        user_id = token.split('#')[1]
    except Exception:
        return HttpResponse("Invalid token", status=401)
    else:
        if user_type == 'agency':
            serialized_trips = get_agency_trips(user_id, 'past')
            return JsonResponse(serialized_trips, safe=False)
        else:
            try:
                traveler = get_object_or_404(Traveler, pk=user_id)
            except (KeyError, Traveler.DoesNotExist):
                return HttpResponse('Unauthorized', status=401)
            else:
                solo_trips = SoloTrip.objects.filter(traveler=traveler).filter(datetime__lte=datetime.now()).filter(status='accepted')
                group_tours = GroupTour.objects.filter(datetime__lte=datetime.now()) # to do: filter by attendance of current traveler
                trips = list(chain(solo_trips, group_tours))
                serialized_trips = serializers.serialize('json', trips)

                return JsonResponse(serialized_trips, safe=False)
