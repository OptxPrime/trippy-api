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
]
