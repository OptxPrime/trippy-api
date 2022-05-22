import jsonpickle
import copy
from django.db import models


class Traveler(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    username = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    password = models.CharField(max_length=512)

    # https://stackoverflow.com/questions/18246024/easy-way-to-exclude-django-state-attribute-from-jsonpickle-encode
    def to_json(self):
        clone = copy.deepcopy(self)
        return jsonpickle.encode(clone, unpicklable=False, indent=4)


class Agency(models.Model):
    name = models.CharField(max_length=32)
    agency_id = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    password = models.CharField(max_length=512)
    establishment_date = models.DateTimeField('date of establishment')

    def to_json(self):
        clone = copy.deepcopy(self)
        return jsonpickle.encode(clone, unpicklable=False, indent=4)


# class City(models.Model):
#     name = models.CharField(max_length=32)
#     country = models.CharField(max_length=32)
#     is_capital = models.BooleanField(default=False)
#
#
# class TransportType(models.TextChoices):
#     PLANE = 'AVION'
#     SHIP = 'BROD'
#     BUS = 'AUTOBUS'
#     VAN = 'KOMBI'
#
#
# class TripStatus(models.TextChoices):
#     accepted = 'accepted'
#     rejected = 'rejected'
#     on_hold = 'on_hold'
#
#
class SoloTrip(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    traveler = models.ForeignKey(Traveler, on_delete=models.CASCADE)
    datetime = models.DateTimeField('trip datetime')
    transport = models.CharField(max_length=64)
    location_name = models.CharField(max_length=128)
    lat = models.DecimalField(decimal_places=7, max_digits=10)
    lng = models.DecimalField(decimal_places=7, max_digits=10)
    max_price = models.PositiveIntegerField()
    status = models.CharField(max_length=16, default='in review')

    def to_json(self):
        clone = copy.deepcopy(self)
        return jsonpickle.encode(clone, unpicklable=False, indent=4)


class GroupTour(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    location_name = models.CharField(max_length=128)
    lat = models.DecimalField(decimal_places=7, max_digits=10)
    lng = models.DecimalField(decimal_places=7, max_digits=10)
    datetime = models.DateTimeField('tour datetime')
    transport = models.CharField(max_length=64)
    min_travelers = models.PositiveIntegerField()
    max_travelers = models.PositiveIntegerField()
    picture_url = models.URLField(max_length=200)

    def to_json(self):
        clone = copy.deepcopy(self)
        return jsonpickle.encode(clone, unpicklable=False, indent=4)
