from django.urls import path

from . import views

urlpatterns = [
    path('register/agency', views.register_agency, name='register agency'),
    path('register/traveler', views.register_traveler, name='register traveler'),
    path('login/agency', views.login_agency, name='login agency'),
    path('login/traveler', views.login_traveler, name='login traveler'),
    path('reset-password', views.reset_password, name='reset password'),
    path('get_user', views.get_user_by_token, name='get current user'),
    path('update-profile', views.update_profile, name='update profile'),
    path('add-solo-trip', views.add_solo_trip, name='add solo trip'),
    path('add-group-tour', views.add_group_tour, name='add group tour'),
    path('get-future-trips', views.get_future_trips, name='get future trips'),
    path('get-my-trips', views.get_my_trips, name='get my trips'),
    path('change-trip-status', views.change_trip_status, name='change trip status'),
    path('delete-trip', views.delete_trip),
    path('get-traveler-registrations', views.get_traveler_registrations, name='get traveler registrations'),
    path('tour-registration', views.tour_registration, name='tour registration'),
]
