from django.urls import path

from . import views

urlpatterns = [
    path('register/agency', views.register_agency, name='register_agency'),
]