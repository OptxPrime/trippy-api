from django.db import models


class Traveler(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    username = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    password = models.CharField(max_length=512)


class Agency(models.Model):
    name = models.CharField(max_length=32)
    agency_id = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    password = models.CharField(max_length=512)
    establishment_date = models.DateTimeField('date of establishment')


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
# class SoloTrip(models.Model):
#     agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
#     city = models.ForeignKey(City, on_delete=models.CASCADE)
#     date = models.DateTimeField('trip date')
#     # transport = models.CharField(choices=TransportType.choices, default=TransportType.PLANE)
#     max_price = models.PositiveIntegerField()
#     # accepted = models.BooleanField(default=False)
#     status = models.CharField(choices=TripStatus.choices, default=TripStatus.on_hold)
#
#
# class GroupTour(models.Model):
#     agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
#     city = models.ForeignKey(City, on_delete=models.CASCADE)
#     date = models.DateTimeField('trip date')
#     # transport = models.CharField(choices=TransportType.choices, default=TransportType.PLANE)
#     min_passengers = models.PositiveIntegerField()
#     max_passengers = models.PositiveIntegerField()
