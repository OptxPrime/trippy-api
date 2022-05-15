from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

import string
import random

from putovanja_app.models import Traveler, Agency


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


## characters to generate password from
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

