from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.core import serializers

from datetime import datetime
from itertools import chain
import string
import random

from putovanja_app.models import Traveler, Agency, SoloTrip, GroupTour, TourRegistrations


def check_if_registered_email(user_type, email):
    if user_type == 'traveler':
        try:
            Traveler.objects.get(email=email)
        except Traveler.DoesNotExist:
            return False
        else:
            return True
    else:
        try:
            Agency.objects.get(email=email)
        except Agency.DoesNotExist:
            return False
        else:
            return True


def check_if_registered_username(username):
    try:
        Traveler.objects.get(username=username)
    except Traveler.DoesNotExist:
        return False
    else:
        return True


# characters to generate password from
characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")


# function below taken from https://geekflare.com/password-generator-python-code/
def generate_random_password():
    length = 8

    # shuffling the characters
    random.shuffle(characters)

    # picking random characters from the list
    password = []
    for i in range(length):
        password.append(random.choice(characters))

    # shuffling the resultant password
    random.shuffle(password)

    # converting the list to string
    # printing the list
    return "".join(password)


def get_agency_trips(agency_id, when):
    try:
        agency = get_object_or_404(Agency, pk=agency_id)
    except (KeyError, Agency.DoesNotExist):
        return HttpResponse('Unauthorized', status=401)
    else:
        solo_trips = SoloTrip.objects.filter(agency=agency)
        group_tours = GroupTour.objects.filter(agency=agency)
        if when == 'past':
            solo_trips = solo_trips.filter(datetime__lte=datetime.now()).filter(status='accepted')
            group_tours = group_tours.filter(datetime__lte=datetime.now())
        elif when == 'future':
            solo_trips = solo_trips.filter(datetime__gte=datetime.now())
            group_tours = group_tours.filter(datetime__gte=datetime.now())

        # https://stackoverflow.com/questions/431628/how-can-i-combine-two-or-more-querysets-in-a-django-view
        trips = list(chain(solo_trips, group_tours))
        # https://stackoverflow.com/questions/757022/how-do-you-serialize-a-model-instance-in-django
        serialized_trips = serializers.serialize('json', trips)
        return serialized_trips


# returns QuerySet containing ids of group tours for which specified traveler registered
# https://stackoverflow.com/questions/22124549/django-models-get-list-of-id
def get_traveler_registrations(traveler_id):
    return TourRegistrations.objects.filter(traveler=traveler_id).values_list('tour_id', flat=True)


def get_tour_registrations(tour_id):
    return TourRegistrations.objects.filter(tour_id=tour_id).count()

def draw_pdf_section(pdf, x, label, content ):
    pdf.setFont('Helvetica-Bold', 14)
    pdf.drawString(20, x, label)
    pdf.setFont('Helvetica', 12)
    pdf.drawString(20, x-20, content)
