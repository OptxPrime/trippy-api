from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view


@api_view(['POST'])
def register_agency(request):
    return JsonResponse(request.data)
